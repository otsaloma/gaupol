# Copyright (C) 2005-2007 Osmo Salomaa
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


from __future__ import division

import functools
import gtk
import os
from gettext import gettext as _

from gaupol import enclib
from gaupol.base import Delegate
from gaupol.gtk import conf, const, util
from gaupol.gtk.dialogs import AppendDialog, OpenDialog, VideoDialog
from gaupol.gtk.dialogs import ErrorDialog, WarningDialog
from gaupol.gtk.dialogs import SplitDialog
from gaupol.gtk.errors import Default, FormatError
from gaupol.gtk.index import *
from gaupol.gtk.page import Page


class OpenAgent(Delegate):

    """Opening files and creating new projects."""

    # pylint: disable-msg=E0203,W0201

    def _append_subtitles(self, current, temp):
        """Append subtitles in temporary page to current.

        Return a list of rows appended.
        """
        rows = range(len(current.project.times),
            len(current.project.times) + len(temp.project.times))
        current.project.block("action-done")
        current.project.insert_subtitles(rows,
            temp.project.times,
            temp.project.frames,
            temp.project.main_texts,
            temp.project.tran_texts)
        current.project.set_action_description(
            const.REGISTER.DO, _("Appending file"))
        current.project.unblock("action-done")
        return rows

    def _get_encodings(self, first=None):
        """Get a list of encodings to try."""

        encodings = [first]
        if conf.encoding.try_locale:
            encodings.append(enclib.get_locale_python_name())
        encodings += conf.encoding.fallbacks
        if conf.encoding.try_auto and util.chardet_available():
            encodings.append("auto")
        while None in encodings:
            encodings.remove(None)
        if not encodings:
            encodings.append("utf_8")
        return util.get_unique(encodings)

    def _get_file_open(self, path):
        """Switch page and return True if file is already open."""

        paths = []
        indexes = []
        for i, page in enumerate(self.pages):
            files = (page.project.main_file, page.project.tran_file)
            for file in (x for x in files if x is not None):
                paths.append(file.path)
                indexes.append(i)
        if path in paths:
            index = indexes[paths.index(path)]
            self.notebook.set_current_page(index)
            basename = os.path.basename(path)
            self.push_message(_('File "%s" is already open') % basename)
            return True
        return False

    def _open_file(self, path, encodings, doc, check_open=True):
        """Open file and return page.

        Raise Default if something goes wrong.
        """
        self._pre_open_check(path, check_open)
        basename = os.path.basename(path)

        if doc == const.DOCUMENT.MAIN:
            page = Page()
            open_method = page.project.open_main
        elif doc == const.DOCUMENT.TRAN:
            page = self.get_current_page()
            open_method = page.project.open_translation
            open_method = functools.partial(
                open_method, smart=conf.file.smart_tran)

        for encoding in encodings:
            sort_count = self._try_open_file(open_method, path, encoding)
            if sort_count is not None:
                file = page.project.get_file(doc)
                self._post_open_check(file, sort_count)
                return page
        self._show_encoding_error_dialog(basename)
        raise Default

    def _post_open_check(self, file, sort_count):
        """Check file after opening.

        Raise Default if something goes wrong.
        """
        if file.format in (const.FORMAT.SSA, const.FORMAT.ASS):
            if conf.file.warn_ssa:
                self._show_ssa_warning_dialog()
        if sort_count > 0:
            basename = os.path.basename(file.path)
            self._show_sort_warning_dialog(basename, sort_count)

    def _pre_append_shift(self, current, temp):
        """Shift subtitles in current page before appending ones in temp."""

        mode = temp.project.get_mode()
        if mode == const.MODE.TIME:
            count = current.project.times[-1][1]
            count = current.project.calc.time_to_seconds(count)
            method = temp.project.shift_seconds
        elif mode == const.MODE.FRAME:
            count = current.project.frames[-1][1]
            method = temp.project.shift_frames
        method([], count, register=None)

    def _pre_open_check(self, path, check_open):
        """Check file before opening.

        Raise Default if something goes wrong.
        """
        if not os.path.isfile(path):
            raise Default
        if check_open and self._get_file_open(path):
            raise Default
        basename = os.path.basename(path)
        size = os.stat(path)[6] / 1048576
        if size > 1:
            self._show_size_warning_dialog(basename, size)

    @util.gc_collected
    def _select_files(self, title, doc):
        """Select and return files and encoding."""

        paths = []
        encoding = None
        util.set_cursor_busy(self.window)
        dialog = OpenDialog(doc, title, self.window)
        page = self.get_current_page()
        if page is not None and page.project.main_file is not None:
            directory = os.path.dirname(page.project.main_file.path)
            dialog.set_current_folder(directory)
        util.set_cursor_normal(self.window)
        response = self.run_dialog(dialog)
        if response == gtk.RESPONSE_OK:
            paths = dialog.get_filenames()
            encoding = dialog.get_encoding()
        dialog.destroy()
        while gtk.events_pending():
            gtk.main_iteration()
        return paths, encoding

    def _show_encoding_error_dialog(self, basename):
        """Show an error dialog after failing to decode file."""

        title = _('Failed to decode file "%s" with all attempted codecs') \
            % basename
        message = _("Please try to open the file with a different character "
            "encoding.")
        dialog = ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _show_format_error_dialog(self, basename):
        """Show an error dialog after failing to recognize file format."""

        title = _('Failed to recognize format of file "%s"') % basename
        message = _("Please check that the file you are trying to open is a "
            "subtitle file of a format supported by Gaupol.")
        dialog = ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _show_io_error_dialog(self, basename, message):
        """Show an error dialog after failing to read file."""

        title = _('Failed to open file "%s"') % basename
        message = _("%s.") % message
        dialog = ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _show_size_warning_dialog(self, basename, size):
        """Show a warning dialog when trying to open a big file.

        Raise Default to abort.
        """
        title = _('Open abnormally large file "%s"?') % basename
        message = _("Size of the file is %.1f MB, which is abnormally large "
            "for a text-based subtitle file. Please, check that you are not "
            "trying to open a binary file.") % size
        dialog = WarningDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO)
        dialog.add_button(gtk.STOCK_OPEN, gtk.RESPONSE_YES)
        dialog.set_default_response(gtk.RESPONSE_NO)
        response = self.flash_dialog(dialog)
        if response != gtk.RESPONSE_YES:
            raise Default

    def _show_sort_warning_dialog(self, basename, count):
        """Show a warning dialog when subtitles have to be sorted.

        Raise Default to abort.
        """
        title = _('Open unsorted file "%s"?') % basename
        message = _("To open the file, %d subtitles need to be moved to reach "
            "sorted order.") % count
        dialog = WarningDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO)
        dialog.add_button(gtk.STOCK_OPEN, gtk.RESPONSE_YES)
        dialog.set_default_response(gtk.RESPONSE_YES)
        response = self.flash_dialog(dialog)
        if response != gtk.RESPONSE_YES:
            raise Default

    def _show_ssa_warning_dialog(self):
        """Show a warning dialog if opening a SSA or an ASS file.

        Raise Default to abort.
        """
        title = _("Open only partially supported file?")
        message = _('Sub Station Alpha and Advanced Sub Station Alpha formats '
            'are not fully supported. Only the header and fields "Start", '
            '"End" and "Text" of the dialogue are read. Saving the file will '
            'cause you to lose all other data.')
        dialog = WarningDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO)
        dialog.add_button(gtk.STOCK_OPEN, gtk.RESPONSE_YES)
        dialog.set_default_response(gtk.RESPONSE_YES)
        response = self.flash_dialog(dialog)
        if response != gtk.RESPONSE_YES:
            raise Default

    def _show_translation_warning_dialog(self, page):
        """Show a warning dialog if opening a new translation file.

        Raise Default to abort.
        """
        title = _('Save changes to translation document "%s" before opening a '
            'new one?') % page.get_translation_basename()
        message = _("If you don't save, changes will be permanently lost.")
        dialog = WarningDialog(self.window, title, message)
        dialog.add_button(_("Open _Without Saving"), gtk.RESPONSE_NO)
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dialog.add_button(gtk.STOCK_SAVE, gtk.RESPONSE_YES)
        dialog.set_default_response(gtk.RESPONSE_YES)
        response = self.flash_dialog(dialog)
        if response == gtk.RESPONSE_YES:
            return self.save_translation(page)
        if response != gtk.RESPONSE_NO:
            raise Default

    def _try_open_file(self, method, path, encoding):
        """Try to open file and return sort count.

        Raise Default if reading file fails.
        Return None if decoding file fails.
        """
        util.set_cursor_busy(self.window)
        try:
            if encoding == "auto":
                encoding = enclib.detect(path)
            return method(path, encoding)
        except FormatError:
            util.set_cursor_normal(self.window)
            basename = os.path.basename(path)
            self._show_format_error_dialog(basename)
            raise Default
        except IOError, (no, message):
            util.set_cursor_normal(self.window)
            basename = os.path.basename(path)
            self._show_io_error_dialog(basename, message)
            raise Default
        except (UnicodeError, ValueError):
            return None
        finally:
            util.set_cursor_normal(self.window)

    def add_new_page(self, page):
        """Add a new page."""

        self.pages.append(page)
        page.connect("close-request", self.on_page_close_request)
        page.project.connect("action-done", self.on_project_action_done)
        page.project.connect("action-redone", self.on_project_action_redone)
        page.project.connect("action-undone", self.on_project_action_undone)
        method = self.on_page_tab_widget_button_press_event
        page.tab_widget.connect("button-press-event", method)
        self.connect_to_view_signals(page.view)
        page.project.clipboard.data = self.clipboard.data[:]

        scroller = gtk.ScrolledWindow()
        scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroller.add(page.view)
        self.notebook.append_page(scroller, page.tab_widget)
        self.notebook.set_tab_reorderable(scroller, True)
        self.notebook.show_all()
        self.notebook.set_current_page(self.pages.index(page))
        self.emit("page-added", page)

    def add_to_recent_files(self, path, doc):
        """Add path to recent files."""

        group = ("gaupol-main", "gaupol-translation")[doc]
        self.recent_manager.add_full(
            util.path_to_uri(path), {
                "mime_type": "text/plain",
                "app_name": "gaupol",
                "app_exec": "gaupol %F",
                "groups": [group],})

    def connect_to_view_signals(self, view):
        """Connect to signals emitted by view."""

        selection = view.get_selection()
        selection.connect("changed", self.on_view_selection_changed)
        view.connect_after("move-cursor", self.on_view_move_cursor)
        view.connect("button-press-event", self.on_view_button_press_event)

        for i, column in enumerate(view.get_columns()):
            renderer = column.get_cell_renderers()[0]
            method = self.on_view_renderer_edited
            renderer.connect("edited", method, i)
            method = self.on_view_renderer_editing_started
            renderer.connect("editing-started", method, i)
            method = self.on_view_renderer_editing_canceled
            renderer.connect("editing-canceled", method)
            button = util.get_parent(column.get_widget(), gtk.Button)
            method = self.on_view_header_button_press_event
            button.connect("button-press-event", method)

    @util.gc_collected
    @util.silent(Default)
    def on_append_file_activate(self, *args):
        """Append subtitles from file to the current project."""

        util.set_cursor_busy(self.window)
        dialog = AppendDialog(self.window)
        util.set_cursor_normal(self.window)
        response = self.run_dialog(dialog)
        if response != gtk.RESPONSE_OK:
            return dialog.destroy()
        path = dialog.get_filenames()[0]
        encoding = dialog.get_encoding()
        dialog.destroy()
        while gtk.events_pending():
            gtk.main_iteration()

        encodings = self._get_encodings(encoding)
        temp = self._open_file(path, encodings, const.DOCUMENT.MAIN, False)
        util.set_cursor_busy(self.window)
        current = self.get_current_page()
        self._pre_append_shift(current, temp)
        rows = self._append_subtitles(current, temp)
        current.view.set_focus(rows[0], None)
        current.view.select_rows(rows)
        current.view.scroll_to_row(rows[0])
        basename = temp.get_main_basename()
        fields = {"amount": len(rows), "filename": basename}
        self.push_message(
            _('Appended %(amount)d subtitles from "%(filename)s"') % fields)
        util.set_cursor_normal(self.window)

    def on_new_project_activate(self, *args):
        """Create a new project."""

        util.set_cursor_busy(self.window)
        self.counter += 1
        page = Page(self.counter)
        page.project.insert_blank_subtitles([0], register=None)
        self.add_new_page(page)
        util.set_cursor_normal(self.window)

    def on_notebook_drag_data_received(
        self, notebook, context, x, y, selection_data, info, time):
        """Open dragged files."""

        uris = selection_data.get_uris()
        paths = [util.uri_to_path(x) for x in uris]
        self.open_main_files(paths)

    def on_open_button_clicked(self, *args):
        """Open main files."""

        self.on_open_main_file_activate()

    def on_open_main_file_activate(self, *args):
        """Open main files."""

        paths, encoding = self._select_files(_("Open"), const.DOCUMENT.MAIN)
        if paths and encoding:
            self.open_main_files(paths, encoding)

    def on_open_translation_file_activate(self, *args):
        """Open a translation file."""

        page = self.get_current_page()
        if page.project.tran_active and page.project.tran_changed:
            self._show_translation_warning_dialog(page)

        paths, encoding = self._select_files(
            _("Open Translation"), const.DOCUMENT.TRAN)
        if paths and encoding:
            self.open_translation_file(paths[0], encoding)

    def on_recent_main_menu_item_activated(self, chooser):
        """Open a recent main file."""

        path = util.uri_to_path(chooser.get_current_uri())
        self.open_main_files([path])

    def on_recent_translation_menu_item_activated(self, chooser):
        """Open a recent translation file."""

        path = util.uri_to_path(chooser.get_current_uri())
        self.open_translation_file(path)

    @util.gc_collected
    def on_select_video_file_activate(self, *args):
        """Select a video file."""

        util.set_cursor_busy(self.window)
        page = self.get_current_page()
        path = page.project.video_path
        dialog = VideoDialog(self.window)
        if path is not None:
            dialog.set_filename(path)
        elif page.project.main_file is not None:
            directory = os.path.dirname(page.project.main_file.path)
            dialog.set_current_folder(directory)
        util.set_cursor_normal(self.window)
        response = self.run_dialog(dialog)
        if response == gtk.RESPONSE_OK:
            page.project.video_path = dialog.get_filename()
            self.update_gui()
        dialog.destroy()

    def on_split_project_activate(self, *args):
        """Split the current project in two."""

        dialog = SplitDialog(self)
        self.flash_dialog(dialog)

    def on_video_button_clicked(self, *args):
        """Select a video file."""

        self.on_select_video_file_activate()

    def on_video_button_drag_data_received(
        self, notebook, context, x, y, selection_data, info, time):
        """Set the video file."""

        page = self.get_current_page()
        uri = selection_data.get_uris()[0]
        path = util.uri_to_path(uri)
        if os.path.isfile(path):
            page.project.video_path = path
            self.update_gui()

    def open_main_files(self, paths, encoding=None):
        """Open main files."""

        encodings = self._get_encodings(encoding)
        for path in sorted(paths):
            try:
                page = self._open_file(path, encodings, const.DOCUMENT.MAIN)
            except Default:
                continue
            util.set_cursor_busy(self.window)
            self.add_new_page(page)
            self.add_to_recent_files(path, const.DOCUMENT.MAIN)
            basename = page.get_main_basename()
            self.push_message(_('Opened main file "%s"') % basename)
            while gtk.events_pending():
                gtk.main_iteration()
            util.set_cursor_normal(self.window)

    @util.silent(Default)
    def open_translation_file(self, path, encoding=None):
        """Open translation file."""

        encodings = self._get_encodings(encoding)
        page = self._open_file(path, encodings, const.DOCUMENT.TRAN)
        util.set_cursor_busy(self.window)
        if not page.view.get_column(TTXT).get_visible():
            self.uim.get_action(TTXT.uim_path).activate()
        self.add_to_recent_files(path, const.DOCUMENT.TRAN)
        basename = page.get_translation_basename()
        self.push_message(_('Opened translation file "%s"') % basename)
        util.set_cursor_normal(self.window)
