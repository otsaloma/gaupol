# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Opening files and creating new projects."""


from gettext import gettext as _
import os
import urllib
import urlparse

import gtk

from gaupol.base.error           import FileFormatError
from gaupol.base.util            import enclib, listlib
from gaupol.gtk                  import cons
from gaupol.gtk.delegate         import Delegate, UIMAction
from gaupol.gtk.dialog.file      import OpenFileDialog, OpenVideoDialog
from gaupol.gtk.dialog.message   import ErrorDialog, WarningDialog
from gaupol.gtk.dialog.projsplit import ProjectSplitDialog
from gaupol.gtk.error            import Default
from gaupol.gtk.icons            import *
from gaupol.gtk.page             import Page
from gaupol.gtk.util             import conf, gtklib

try:
    import chardet
    _CHARDET_AVAILABLE = True
except ImportError:
    print 'Universal Encoding Detector not found.'
    print 'Encoding auto-detection not possible.'
    _CHARDET_AVAILABLE = False


class AppendFileAction(UIMAction):

    """Appending subtitles from a file to current project."""

    action_item = (
        'append_file',
        None,
        _('_Append File...'),
        None,
        _('Append subtitles from file to the current project'),
        'on_append_file_activate'
    )

    paths = ['/ui/menubar/tools/append_file']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return page is not None


class NewProjectAction(UIMAction):

    """Creating a new project."""

    action_item = (
        'new_project',
        gtk.STOCK_NEW,
        _('_New'),
        '<control>N',
        _('Create a new project'),
        'on_new_project_activate'
    )

    paths = ['/ui/menubar/file/new']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return True


class OpenMainFileAction(UIMAction):

    """Opening main files."""

    action_item = (
        'open_main_file',
        gtk.STOCK_OPEN,
        _('_Open...'),
        '<control>O',
        _('Open main files'),
        'on_open_main_file_activate'
    )

    paths = ['/ui/menubar/file/open']
    widgets = ['_open_button']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return True


class OpenTranslationFileAction(UIMAction):

    """Opening translation files."""

    action_item = (
        'open_translation_file',
        gtk.STOCK_OPEN,
        _('O_pen Translation...'),
        '',
        _('Open a translation file'),
        'on_open_translation_file_activate'
    )

    paths = ['/ui/menubar/file/open_translation']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        if page.project.main_file is None:
            return False
        return True


class SelectVideoFileAction(UIMAction):

    """Selecting a video file."""

    action_item = (
        'select_video_file',
        None,
        _('Se_lect Video...'),
        None,
        _('Select a video file'),
        'on_select_video_file_activate'
    )

    paths = ['/ui/menubar/file/select_video']
    widgets = ['_video_button']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        if page.project.main_file is None:
            return False
        return True


class SplitProjectAction(UIMAction):

    """Splitting a project in two."""

    action_item = (
        'split_project',
        None,
        _('_Split Project...'),
        None,
        _('Split the current project in two'),
        'on_split_project_activate'
    )

    paths = ['/ui/menubar/tools/split_project']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return page is not None


class _BigFileWarningDialog(WarningDialog):

    """Dialog to warn when opening a big file."""

    def __init__(self, parent, basename, size):

        WarningDialog.__init__(
            self, parent,
            _('Open abnormally large file "%s"?') % basename,
            _('Size of the file is %.1f MB, which is abnormally large for a '
              'text-based subtitle file. Please, check that you are not '
              'trying to open a binary file.') % size
        )
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO)
        self.add_button(gtk.STOCK_OPEN, gtk.RESPONSE_YES)
        self.set_default_response(gtk.RESPONSE_NO)


class _FormatErrorDialog(ErrorDialog):

    """Dialog to inform that filetype is not supported."""

    def __init__(self, parent, basename):

        ErrorDialog.__init__(
            self, parent,
            _('Failed to recognize format of file "%s"') % basename,
            _('Please check that the file you are trying to open is a '
              'subtitle file of a format supported by Gaupol.')
        )


class _IOErrorDialog(ErrorDialog):

    """Dialog to inform that IOError occured while opening file."""

    def __init__(self, parent, basename, message):

        ErrorDialog.__init__(
            self, parent,
            _('Failed to open file "%s"') % basename,
            _('%s.') % message
        )


class _SortWarningDialog(WarningDialog):

    """Dialog to warn that subtitles were resorted."""

    def __init__(self, parent, count):

        WarningDialog.__init__(
            self, parent,
            _('%d subtitles will be moved') % count,
            _('The file you are trying to open is not in sorted order and may '
              'thus be faulty. If you open the file, all subtitles will be '
              'arranged in sorted order.')
        )
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO)
        self.add_button(gtk.STOCK_OPEN, gtk.RESPONSE_YES)
        self.set_default_response(gtk.RESPONSE_YES)


class _SSAWarningDialog(WarningDialog):

    """Dialog to warn when opening an SSA or ASS file."""

    def __init__(self, parent):

        WarningDialog.__init__(
            self, parent,
            _('Open only partially supported file?'),
            _('Sub Station Alpha and Advanced Sub Station Alpha formats are '
              'not fully supported. Only the header and fields "Start", "End" '
              'and "Text" of the dialogue are read. Saving the file will '
              'cause you to lose all other data.')
        )
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO)
        self.add_button(gtk.STOCK_OPEN, gtk.RESPONSE_YES)
        self.set_default_response(gtk.RESPONSE_NO)


class _TranslateWarningDialog(WarningDialog):

    """Dialog to warn when opening a translation file."""

    def __init__(self, parent, basename):

        WarningDialog.__init__(
            self, parent,
            _('Save changes to translation document "%s" before opening a new '
              'one?') % basename,
            _('If you don\'t save, changes will be permanently lost.')
        )
        self.add_button(_('Open _Without Saving'), gtk.RESPONSE_NO)
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_SAVE, gtk.RESPONSE_YES)
        self.set_default_response(gtk.RESPONSE_YES)


class _UnicodeErrorDialog(ErrorDialog):

    """Dialog to inform that UnicodeError occured while opening file."""

    def __init__(self, parent, basename):

        ErrorDialog.__init__(
            self, parent,
            _('Failed to decode file "%s" with all attempted codecs') \
            % basename,
            _('Please try to open the file with a different character '
              'encoding.')
        )


class FileOpenDelegate(Delegate):

    """Opening files and creating new projects."""

    def _add_new_project(self, page):
        """Add new project."""

        self.pages.append(page)
        self._connect_page_signals(page)
        self.connect_view_signals(page)
        try:
            self.add_to_recent_files(page.project.main_file.path)
        except AttributeError:
            pass
        page.project.clipboard.data = self._clipboard.data

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.add(page.view)
        self._notebook.append_page_menu(
            scrolled_window, page.init_tab_widget(), page.tab_menu_label)
        self._notebook.show_all()
        self._notebook.set_current_page(self.pages.index(page))
        page.reload_all()

    def _check_file_open(self, path):
        """
        Check if file is already open.

        If the file is already open, select that page in the notebook.
        Return True if file is open, otherwise False.
        """
        for i, page in enumerate(self.pages):
            for file_ in (page.project.main_file, page.project.tran_file):
                if file_ is None:
                    continue
                if file_.path != path:
                    continue
                self._notebook.set_current_page(i)
                self.set_status_message(
                    _('File "%s" is already open') % os.path.basename(path))
                return True
        return False

    def _connect_page_signals(self, page):
        """Connect page signals."""

        page.project.connect('action_done', self.on_project_action_done)
        page.project.connect('action_redone', self.on_project_action_redone)
        page.project.connect('action_undone', self.on_project_action_undone)
        page.connect('closed', self.on_page_closed)

    def _get_encodings(self, first=None):
        """Get list of encodings to try."""

        encodings = []
        if first is not None:
            encodings.append(first)
        if conf.encoding.try_locale:
            try:
                encodings.append(enclib.get_locale_encoding()[0])
            except ValueError:
                pass
        encodings += conf.encoding.fallbacks[:]
        if conf.encoding.try_auto and _CHARDET_AVAILABLE:
            encodings.append('auto')
        if not encodings:
            encodings.append('utf_8')

        return listlib.unique(encodings)

    def _open_file(self, doc, path, encodings, check_open=True):
        """
        Open file.

        Raise Default if unsuccessful.
        Return page.
        """
        resorts = 0
        self._pre_check(path, check_open)
        basename = os.path.basename(path)
        if path.endswith('.srtx'):
            conf.srtx.directory = os.path.dirname(path)

        for encoding in encodings:
            try:
                if encoding == 'auto':
                    encoding = enclib.detect(path)
                if doc == MAIN:
                    args = path, encoding
                    page = Page(srtx=path.endswith('.srtx'))
                    resorts = page.project.open_main_file(*args)
                    format = page.project.main_file.format
                elif doc == TRAN:
                    args = path, encoding, conf.file.smart_tran
                    page = self.get_current_page()
                    resorts = page.project.open_translation_file(*args)
                    format = page.project.tran_file.format
            except FileFormatError:
                dialog = _FormatErrorDialog(self._window, basename)
                self._run_dialog(dialog)
                raise Default
            except IOError, (no, message):
                dialog = _IOErrorDialog(self._window, basename, message)
                self._run_dialog(dialog)
                raise Default
            except UnicodeError:
                continue
            except ValueError:
                continue
            else:
                self._post_check(format, resorts)
                return page

        dialog = _UnicodeErrorDialog(self._window, basename)
        self._run_dialog(dialog)
        raise Default

    def _post_check(self, format, resorts):
        """
        Check file before opening.

        Raise Default if file is no good.
        """
        if format in (cons.Format.SSA, cons.Format.ASS):
            if conf.file.warn_ssa:
                dialog = _SSAWarningDialog(self._window)
                response = self._run_dialog(dialog)
                if response != gtk.RESPONSE_YES:
                    raise Default

        if resorts > 0:
            dialog = _SortWarningDialog(self._window, resorts)
            response = self._run_dialog(dialog)
            if response != gtk.RESPONSE_YES:
                raise Default

    def _pre_check(self, path, check_open):
        """
        Check file before opening.

        Raise Default if file is no good.
        """
        if not os.path.isfile(path):
            raise Default
        if check_open and self._check_file_open(path):
            raise Default

        basename = os.path.basename(path)
        size = float(os.stat(path)[6]) / 1048576.0
        if size > 1:
            dialog = _BigFileWarningDialog(self._window, basename, size)
            response = self._run_dialog(dialog)
            if response != gtk.RESPONSE_YES:
                raise Default

    def _run_dialog(self, dialog):
        """
        Run message dialog.

        Return response.
        """
        gtklib.set_cursor_normal(self._window)
        response = gtklib.run(dialog)
        gtklib.set_cursor_busy(self._window)
        return response

    def _select_files(self, title, tran, multiple, open_button=None):
        """
        Select files with filechooser.

        Raise Default if cancelled.
        Return paths, encoding.
        """
        dialog = OpenFileDialog(title, tran, self._window)
        dialog.set_select_multiple(multiple)
        if open_button is not None:
            dialog.set_open_button(*open_button)
        gtklib.set_cursor_normal(self._window)
        response = dialog.run()
        gtklib.set_cursor_busy(self._window)
        if response != gtk.RESPONSE_OK:
            gtklib.destroy_gobject(dialog)
            gtklib.set_cursor_normal(self._window)
            raise Default

        paths = dialog.get_filenames()
        encoding = dialog.get_encoding()
        gtklib.destroy_gobject(dialog)
        return paths, encoding

    def add_to_recent_files(self, path):
        """Add path to recent files."""

        try:
            conf.file.recents.remove(path)
        except ValueError:
            pass
        conf.file.recents.insert(0, path)
        self.validate_recent()

    def connect_view_signals(self, page):
        """Connect view signals."""

        view = page.view
        view.connect_after('move-cursor', self.on_view_move_cursor)
        view.connect('button-press-event', self.on_view_button_press_event)
        selection = view.get_selection()
        selection.connect('changed', self.on_view_selection_changed)

        connections = (
            ('edited'          , self.on_view_cell_edited          ),
            ('editing-canceled', self.on_view_cell_editing_canceled),
            ('editing-started' , self.on_view_cell_editing_started ),
        )
        for i, column in enumerate(view.get_columns()):
            for renderer in column.get_cell_renderers():
                for signal, method in connections:
                    renderer.connect(signal, method, i)
            widget = column.get_widget()
            button = gtklib.get_parent_widget(widget, gtk.Button)
            button.connect(
                'button-press-event', self.on_view_header_button_press_event)

    def on_append_file_activate(self, *args):
        """Append subtitles from a file to current project."""

        gtklib.set_cursor_busy(self._window)
        try:
            paths, encoding = self._select_files(
                _('Append File'), False, False, (gtk.STOCK_ADD, _('Append')))
            while gtk.events_pending():
                gtk.main_iteration()
            temp_page = self._open_file(
                MAIN, paths[0], self._get_encodings(encoding), False)
        except Default:
            gtklib.set_cursor_normal(self._window)
            return

        mode = temp_page.project.get_mode()
        if mode == cons.Mode.TIME:
            count = temp_page.project.times[-1][1]
            count = temp_page.project.calc.time_to_seconds(count)
            temp_page.project.shift_seconds(None, count, None)
        elif mode == cons.Mode.FRAME:
            count = temp_page.project.frames[-1][1]
            temp_page.project.shift_frames(None, count, None)

        page = self.get_current_page()
        current_length = len(page.project.times)
        append_length = len(temp_page.project.times)
        rows = range(current_length, current_length + append_length)
        page.project.insert_subtitles(
            rows,
            temp_page.project.times,
            temp_page.project.frames,
            temp_page.project.main_texts,
            temp_page.project.tran_texts
        )

        page.project.set_action_description(
            cons.Action.DO, _('Appending file'))
        page.view.set_focus(current_length, None)
        page.view.select_rows(rows)
        page.view.scroll_to_row(current_length)
        self.set_status_message(
            _('Appended file starting from subtitle %d') \
            % (current_length + 1)
        )
        self.set_sensitivities(page)
        gtklib.destroy_gobject(temp_page)
        gtklib.set_cursor_normal(self._window)

    def on_new_project_activate(self, *args):
        """Start a new project."""

        gtklib.set_cursor_busy(self._window)
        self._counter += 1
        page = Page(self._counter)
        page.project.times = [['00:00:00.000'] * 3]
        page.project.frames = [[0, 0, 0]]
        page.project.main_texts = [u'']
        page.project.tran_texts = [u'']
        self._add_new_project(page)
        gtklib.set_cursor_normal(self._window)
        self.set_status_message(_('Created a new project'))

    def on_notebook_drag_data_received(
        self, notebook, context, x, y, selection_data, info, time):
        """Open drag-dropped files."""

        paths = []
        uris = selection_data.get_uris()
        for uri in uris:
            path = urlparse.urlsplit(urllib.unquote(uri))[2]
            if os.path.isfile(path):
                paths.append(path)

        self.open_main_files(paths)

    def on_open_button_clicked(self, *args):
        """Open main file."""

        self.on_open_main_file_activate()

    def on_open_main_file_activate(self, *args):
        """Open main file."""

        gtklib.set_cursor_busy(self._window)
        try:
            paths, encoding = self._select_files(_('Open'), False, True)
        except Default:
            gtklib.set_cursor_normal(self._window)
            return
        self.open_main_files(paths, encoding)
        gtklib.set_cursor_normal(self._window)

    def on_open_recent_file_activate(self, action):
        """Open recent main file."""

        index = int(action.get_name().split('_')[-1])
        self.open_main_files([conf.file.recents[index]])

    def on_open_translation_file_activate(self, *args):
        """Open translation file."""

        page = self.get_current_page()
        if page.project.tran_active and page.project.tran_changed:
            basename = page.get_translation_basename()
            dialog = _TranslateWarningDialog(self._window, basename)
            response = gtklib.run(dialog)
            if response == gtk.RESPONSE_YES:
                try:
                    self.save_translation(page)
                except Default:
                    return
                self.set_sensitivities()
            elif response != gtk.RESPONSE_NO:
                return

        gtklib.set_cursor_busy(self._window)
        try:
            paths, encoding = self._select_files(
                _('Open Translation'), True, False)
        except Default:
            gtklib.set_cursor_normal(self._window)
            return
        encodings = self._get_encodings(encoding)
        try:
            page = self._open_file(TRAN, paths[0], encodings)
        except Default:
            gtklib.set_cursor_normal(self._window)
            return

        if not page.view.get_column(TTXT).get_visible():
            path = cons.Column.uim_paths[TTXT]
            self._uim.get_action(path).activate()
        self.set_sensitivities()
        page.reload_all()
        self.set_status_message(_('Opened translation file "%s"') \
            % page.get_translation_basename())
        gtklib.set_cursor_normal(self._window)

    def on_select_video_file_activate(self, *args):
        """Select video file."""

        page = self.get_current_page()
        path = page.project.video_path
        gtklib.set_cursor_busy(self._window)
        dialog = OpenVideoDialog(self._window)
        if path is not None:
            dialog.set_filename(path)
        else:
            dirpath = os.path.dirname(page.project.main_file.path)
            dialog.set_current_folder(dirpath)
        gtklib.set_cursor_normal(self._window)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            page.project.video_path = dialog.get_filename()
            self.set_sensitivities(page)
        gtklib.destroy_gobject(dialog)

    def on_split_project_activate(self, *args):
        """Split current project in two."""

        page = self.get_current_page()
        dialog = ProjectSplitDialog(self._window, page)
        response = dialog.run()
        subtitle = dialog.get_subtitle()
        dialog.destroy()
        if response != gtk.RESPONSE_OK:
            return

        gtklib.set_cursor_busy(self._window)
        row = subtitle - 1
        times = page.project.times[row:]
        frames = page.project.frames[row:]
        main_texts = page.project.main_texts[row:]
        tran_texts = page.project.tran_texts[row:]
        page.project.remove_subtitles(range(row, len(page.project.times)))
        page.project.set_action_description(
            cons.Action.DO, _('Splitting project'))
        self.set_sensitivities(page)
        first_page = page

        self._counter += 1
        page = Page(self._counter)
        page.project.times = times
        page.project.frames = frames
        page.project.main_texts = main_texts
        page.project.tran_texts = tran_texts
        mode = page.project.get_mode()
        if mode == cons.Mode.TIME:
            count = first_page.project.times[-1][1]
            count = -1 * page.project.calc.time_to_seconds(count)
            page.project.shift_seconds(None, count, None)
        elif mode == cons.Mode.FRAME:
            count = -1 * first_page.project.frames[-1][1]
            page.project.shift_frames(None, count, None)
        self._add_new_project(page)
        self.set_status_message(_('Split %d subtitles to project "%s"') % (
            len(page.project.times), page.untitle))
        self.set_sensitivities(page)
        gtklib.set_cursor_normal(self._window)

    def on_video_button_clicked(self, *args):
        """Select video file."""

        self.on_select_video_file_activate()

    def on_video_button_drag_data_received(
        self, notebook, context, x, y, selection_data, info, time):
        """Set video  file."""

        page = self.get_current_page()
        uri = selection_data.get_uris()[0]
        path = urlparse.urlsplit(urllib.unquote(uri))[2]
        if os.path.isfile(path):
            page.project.video_path = path
            self.set_sensitivities(page)

    def open_main_files(self, paths, encoding=None):
        """Open main files."""

        paths.sort()
        gtklib.set_cursor_busy(self._window)
        encodings = self._get_encodings(encoding)
        for path in paths:
            try:
                page = self._open_file(MAIN, path, encodings)
            except Default:
                continue
            page.project.guess_video_path()
            self._add_new_project(page)
            conf.file.directory = os.path.dirname(path)
            self.set_status_message(
                _('Opened main file "%s"') % page.get_main_basename())
            while gtk.events_pending():
                gtk.main_iteration()

        gtklib.set_cursor_normal(self._window)

    def validate_recent(self):
        """Remove non-existent and excess recent files."""

        for i in reversed(range(len(conf.file.recents))):
            if not os.path.isfile(conf.file.recents[i]):
                conf.file.recents.pop(i)

        while len(conf.file.recents) > conf.file.max_recent:
            conf.file.recents.pop()
