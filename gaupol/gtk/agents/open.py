# Copyright (C) 2005-2009 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Opening files and creating new projects."""

from __future__ import division

import functools
import gaupol.gtk
import gtk
import os
_ = gaupol.i18n._


class OpenAgent(gaupol.Delegate):

    """Opening files and creating new projects."""

    # pylint: disable-msg=E1101,E0203,W0201

    __metaclass__ = gaupol.Contractual

    def _append_subtitles(self, current, temp):
        """Append subtitles in temporary page to current.

        Return a sequence of indices appended.
        """
        indices = range(len(current.project.subtitles),
            len(current.project.subtitles) + len(temp.project.subtitles))
        current.project.block("action-done")
        current.project.insert_subtitles(indices, temp.project.subtitles)
        current.project.set_action_description(
            gaupol.registers.DO, _("Appending file"))
        current.project.unblock("action-done")
        return tuple(indices)

    def _check_file_exists(self, path):
        """Check if file to be opened actually exists.

        Raise Default if  opening subtitle should be stopped.
        """
        gaupol.gtk.util.raise_default(not os.path.isfile(path))

    def _check_file_is_not_open(self, path, check_open):
        """Check if file is already open and further opening need stop.

        Raise Default if  opening subtitle should be stopped.
        """
        if not check_open: return
        self._ensure_file_not_open(path)

    def _check_file_size(self, path):
        """Check if filesize is too large for a text-based subtitle file.

        Raise Default if  opening subtitle should be stopped.
        """
        basename = os.path.basename(path)
        megabyte_size = os.stat(path)[6] / 1048576
        if megabyte_size <= 1: return
        self._show_size_warning_dialog(basename, megabyte_size)

    def _check_sort_count(self, path, sort_count):
        """Check if file should be opened after subtitled were moved.

        Raise Default if  opening subtitle should be stopped.
        """
        if sort_count <= 0: return
        basename = os.path.basename(path)
        self._show_sort_warning_dialog(basename, sort_count)

    def _ensure_file_not_open(self, path):
        """Check if file is already open and select that page if it is.

        Raise Default if file is already open and further opening need stop.
        """
        for page in self.pages:
            files = [page.project.main_file, page.project.tran_file]
            paths = [x.path for x in filter(None, files)]
            if not path in paths: continue
            self.set_current_page(page)
            basename = os.path.basename(path)
            message = _('File "%s" is already open')
            self.flash_message(message % basename)
            raise gaupol.gtk.Default

    def _get_encodings_require(self, first=None):
        if not first in (None, "auto"):
            assert gaupol.encodings.is_valid_code(first)

    def _get_encodings_ensure(self, value, first=None):
        assert value
        for encoding in (x for x in value if x != "auto"):
            assert gaupol.encodings.is_valid_code(encoding)
        if first is not None:
            assert value[0] == first

    def _get_encodings(self, first=None):
        """Return a sequence of encodings to try when opening files."""

        encodings = [first]
        if gaupol.gtk.conf.encoding.try_locale:
            encoding = gaupol.encodings.get_locale_code()
            encodings.append(encoding)
        encodings += gaupol.gtk.conf.encoding.fallbacks
        try_auto = gaupol.gtk.conf.encoding.try_auto
        if try_auto and gaupol.util.chardet_available():
            encodings.append("auto")
        while None in encodings:
            encodings.remove(None)
        encodings = encodings or ["utf_8"]
        return tuple(gaupol.util.get_unique(encodings))

    def _open_file(self, path, encodings, doc, check_open=True):
        """Open file and return parental page if successful.

        Raise Default if cancelled or file cannot be opened.
        """
        self._pre_open_check(path, check_open)
        basename = os.path.basename(path)
        if doc == gaupol.documents.MAIN:
            page = gaupol.gtk.Page()
            open_method = page.project.open_main
        elif doc == gaupol.documents.TRAN:
            page = self.get_current_page()
            open_method = functools.partial(
                page.project.open_translation,
                align_method=gaupol.gtk.conf.file.align_method)
        for encoding in encodings:
            args = (open_method, path, encoding)
            sort_count = self._try_open_file(*args)
            if sort_count is not None:
                file = page.project.get_file(doc)
                self._post_open_check(file, sort_count)
                return page
        self._show_encoding_error_dialog(basename)
        raise gaupol.gtk.Default

    def _post_open_check(self, file, sort_count):
        """Check file to see if it can be nicely opened.

        Raise Default if file is not fit for opening.
        """
        self._check_sort_count(file.path, sort_count)

    def _pre_open_check(self, path, check_open):
        """Check file to see if it can be nicely opened.

        Raise Default if file is not fit for opening.
        """
        self._check_file_exists(path)
        self._check_file_is_not_open(path, check_open)
        self._check_file_size(path)

    def _select_files(self, title, doc):
        """Select files and return paths and encoding.

        Raise Default if opening subtitle files cancelled.
        """
        gaupol.gtk.util.set_cursor_busy(self.window)
        dialog = gaupol.gtk.OpenDialog(self.window, title, doc)
        page = self.get_current_page()
        if (page is not None) and (page.project.main_file is not None):
            directory = os.path.dirname(page.project.main_file.path)
            dialog.set_current_folder(directory)
        gaupol.gtk.util.set_cursor_normal(self.window)
        response = self.run_dialog(dialog)
        paths = dialog.get_filenames()
        encoding = dialog.get_encoding()
        dialog.destroy()
        gaupol.gtk.util.raise_default(response != gtk.RESPONSE_OK)
        gaupol.gtk.util.iterate_main()
        return paths, encoding

    def _show_encoding_error_dialog(self, basename):
        """Show an error dialog after failing to decode file."""

        title = _('Failed to decode file "%s" with all '
            'attempted codecs') % basename
        message = _("Please try to open the file with a "
            "different character encoding.")
        dialog = gaupol.gtk.ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _show_format_error_dialog(self, basename):
        """Show an error dialog after failing to recognize file format."""

        title = _('Failed to recognize format of file "%s"') % basename
        message = _("Please check that the file you are trying to open is a "
            "subtitle file of a format supported by Gaupol.")
        dialog = gaupol.gtk.ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _show_io_error_dialog(self, basename, message):
        """Show an error dialog after failing to read file."""

        title = _('Failed to open file "%s"') % basename
        message = _("%s.") % message
        dialog = gaupol.gtk.ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _show_parse_error_dialog(self, basename, format):
        """Show an error dialog after failing to parse file."""

        title = _('Failed to parse file "%s"') % basename
        message = _("Please check, e.g. with a text editor, that the file you "
            "are trying open is a valid %s file. If you think it is, file a "
            "bug report and attach the file.") % format.label
        dialog = gaupol.gtk.ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _show_size_warning_dialog(self, basename, size):
        """Show a warning dialog when trying to open a big file.

        Raise Default if subtitle file opening cancelled.
        """
        title = _('Open abnormally large file "%s"?') % basename
        message = _("Size of the file is %.1f MB, which is abnormally large "
            "for a text-based subtitle file. Please, check that you are not "
            "trying to open a binary file.") % size
        dialog = gaupol.gtk.WarningDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO)
        dialog.add_button(gtk.STOCK_OPEN, gtk.RESPONSE_YES)
        dialog.set_default_response(gtk.RESPONSE_NO)
        response = self.flash_dialog(dialog)
        gaupol.gtk.util.raise_default(response != gtk.RESPONSE_YES)

    def _show_sort_warning_dialog(self, basename, count):
        """Show a warning dialog when subtitles have been sorted.

        Raise Default if subtitle file opening cancelled.
        """
        title = _('Open unsorted file "%s"?') % basename
        message = _("The order of %d subtitles needs to be changed. "
            "If %d sounds like a lot, the file may be erroneously composed.")
        message = message % (count, count)
        dialog = gaupol.gtk.WarningDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO)
        dialog.add_button(gtk.STOCK_OPEN, gtk.RESPONSE_YES)
        dialog.set_default_response(gtk.RESPONSE_YES)
        response = self.flash_dialog(dialog)
        gaupol.gtk.util.raise_default(response != gtk.RESPONSE_YES)

    def _show_translation_warning_dialog(self, page):
        """Show a warning dialog if opening a new translation file.

        Raise Default if translation opening cancelled.
        """
        title = _('Save changes to translation document "%s" before '
            'opening a new one?') % page.get_translation_basename()
        message = _("If you don't save, changes will be permanently lost.")
        dialog = gaupol.gtk.WarningDialog(self.window, title, message)
        dialog.add_button(_("Open _Without Saving"), gtk.RESPONSE_NO)
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dialog.add_button(gtk.STOCK_SAVE, gtk.RESPONSE_YES)
        dialog.set_default_response(gtk.RESPONSE_YES)
        response = self.flash_dialog(dialog)
        if response == gtk.RESPONSE_YES:
            return self.save_translation_document(page)
        gaupol.gtk.util.raise_default(response != gtk.RESPONSE_NO)

    @gaupol.deco.silent(UnicodeError)
    def _try_open_file(self, open_method, path, encoding):
        """Try to open file and return sort count.

        Raise Default if reading or parsing file fails.
        Return None if decoding file fails.
        """
        gaupol.gtk.util.set_cursor_busy(self.window)
        basename = os.path.basename(path)
        if encoding == "auto":
            encoding = gaupol.encodings.detect(path)
            if encoding is None: return
        try: return open_method(path, encoding)
        except gaupol.FormatError:
            gaupol.gtk.util.set_cursor_normal(self.window)
            self._show_format_error_dialog(basename)
        except IOError, (no, message):
            gaupol.gtk.util.set_cursor_normal(self.window)
            self._show_io_error_dialog(basename, message)
        except gaupol.ParseError:
            gaupol.gtk.util.set_cursor_normal(self.window)
            bom_encoding = gaupol.encodings.detect_bom(path)
            encoding = bom_encoding or encoding
            determiner = gaupol.FormatDeterminer()
            silent = gaupol.deco.silent(Exception)
            format = silent(determiner.determine)(path, encoding)
            self._show_parse_error_dialog(basename, format)
        finally:
            gaupol.gtk.util.set_cursor_normal(self.window)
        raise gaupol.gtk.Default

    def add_new_page(self, page):
        """Add a new page to the application."""

        self.pages.append(page)
        callback = self.on_page_close_request
        page.connect("close-request", callback)
        callback = self.on_project_action_done
        page.project.connect("action-done", callback)
        callback = self.on_project_action_redone
        page.project.connect("action-redone", callback)
        callback = self.on_project_action_undone
        page.project.connect("action-undone", callback)
        callback = self.on_page_tab_widget_button_press_event
        page.tab_widget.connect("button-press-event", callback, page)
        self.connect_to_view_signals(page.view)
        page.project.clipboard.set_texts(self.clipboard.get_texts())

        scroller = gtk.ScrolledWindow()
        scroller.set_policy(*((gtk.POLICY_AUTOMATIC,) * 2))
        scroller.add(page.view)
        self.notebook.append_page(scroller, page.tab_widget)
        self.notebook.set_tab_reorderable(scroller, True)
        self.notebook.show_all()
        self.set_current_page(page)
        self.emit("page-added", page)

    def add_to_recent_files(self, path, format, doc):
        """Add path to recent files managed by the recent manager."""

        uri = gaupol.util.path_to_uri(path)
        if doc == gaupol.documents.MAIN:
            group = "gaupol-main"
        elif doc == gaupol.documents.TRAN:
            group = "gaupol-translation"
        metadata = {"mime_type": format.mime_type,
                    "app_name": "gaupol",
                    "app_exec": "gaupol %F",
                    "groups": (group,),}
        self.recent_manager.add_full(uri, metadata)

    def append_file(self, path, encoding=None):
        """Append subtitles from file to the current project.

        Raise Default if cancelled or something goes wrong.
        """
        encodings = self._get_encodings(encoding)
        doc = gaupol.documents.MAIN
        temp = self._open_file(path, encodings, doc, False)
        gaupol.gtk.util.set_cursor_busy(self.window)
        current = self.get_current_page()
        shift = current.project.subtitles[-1].end
        temp.project.shift_positions(None, shift)
        rows = self._append_subtitles(current, temp)
        amount = len(rows)
        current.view.set_focus(rows[0], None)
        current.view.select_rows(rows)
        current.view.scroll_to_row(rows[0])
        basename = temp.get_main_basename()
        message = _('Appended %(amount)d subtitles from "%(basename)s"')
        self.flash_message(message % locals())
        gaupol.gtk.util.set_cursor_normal(self.window)

    def connect_to_view_signals(self, view):
        """Connect to signals emitted by view."""

        selection = view.get_selection()
        selection.connect("changed", self.on_view_selection_changed)
        view.connect_after("move-cursor", self.on_view_move_cursor)
        view.connect("button-press-event", self.on_view_button_press_event)
        for column in view.get_columns():
            renderer = column.get_cell_renderers()[0]
            callback = self.on_view_renderer_edited
            renderer.connect("edited", callback, column)
            callback = self.on_view_renderer_editing_started
            renderer.connect("editing-started", callback, column)
            callback = self.on_view_renderer_editing_canceled
            renderer.connect("editing-canceled", callback, column)
            button = column.get_widget().get_ancestor(gtk.Button)
            callback = self.on_view_header_button_press_event
            button.connect("button-press-event", callback)

    @gaupol.deco.silent(gaupol.gtk.Default)
    def on_append_file_activate(self, *args):
        """Append subtitles from file to the current project."""

        gaupol.gtk.util.set_cursor_busy(self.window)
        dialog = gaupol.gtk.AppendDialog(self.window)
        gaupol.gtk.util.set_cursor_normal(self.window)
        response = self.run_dialog(dialog)
        paths = dialog.get_filenames()
        encoding = dialog.get_encoding()
        dialog.destroy()
        if response != gtk.RESPONSE_OK: return
        if not paths: return
        gaupol.gtk.util.iterate_main()
        self.append_file(paths[0], encoding)

    def on_new_project_activate(self, *args):
        """Create a new project and add a page for it in the application."""

        page = gaupol.gtk.Page(self.counter.next())
        page.project.insert_blank_subtitles((0,), register=None)
        self.add_new_page(page)

    def on_notebook_drag_data_received(
        self, notebook, context, x, y, selection_data, info, time):
        """Open main files from dragged URIs."""

        uris = selection_data.get_uris()
        paths = [gaupol.util.uri_to_path(x) for x in uris]
        self.open_main_files(paths)

    @gaupol.deco.silent(gaupol.gtk.Default)
    def on_open_main_files_activate(self, *args):
        """Open main files."""

        doc = gaupol.documents.MAIN
        paths, encoding = self._select_files(_("Open"), doc)
        self.open_main_files(paths, encoding)

    @gaupol.deco.silent(gaupol.gtk.Default)
    def on_open_translation_file_activate(self, *args):
        """Open a translation file."""

        page = self.get_current_page()
        if page.project.tran_changed:
            self._show_translation_warning_dialog(page)
        doc = gaupol.documents.TRAN
        paths, encoding = self._select_files(_("Open Translation"), doc)
        self.open_translation_file(paths[0], encoding)

    def on_recent_main_menu_item_activated(self, chooser):
        """Open a recent main file."""

        uri = chooser.get_current_uri()
        path = gaupol.util.uri_to_path(uri)
        self.open_main_file(path)

    def on_recent_translation_menu_item_activated(self, chooser):
        """Open a recent translation file."""

        uri = chooser.get_current_uri()
        path = gaupol.util.uri_to_path(uri)
        align_method = gaupol.align_methods.POSITION
        self.open_translation_file(path, None, align_method)

    def on_select_video_file_activate(self, *args):
        """Select a video file."""

        gaupol.gtk.util.set_cursor_busy(self.window)
        page = self.get_current_page()
        path = page.project.video_path
        dialog = gaupol.gtk.VideoDialog(self.window)
        if page.project.video_path is not None:
            dialog.set_filename(page.project.video_path)
        elif page.project.main_file is not None:
            directory = os.path.dirname(page.project.main_file.path)
            dialog.set_current_folder(directory)
        gaupol.gtk.util.set_cursor_normal(self.window)
        response = self.run_dialog(dialog)
        path = dialog.get_filename()
        dialog.destroy()
        if response != gtk.RESPONSE_OK: return
        page.project.video_path = path
        self.update_gui()

    def on_split_project_activate(self, *args):
        """Split the current project in two."""

        self.flash_dialog(gaupol.gtk.SplitDialog(self.window, self))

    def on_video_button_clicked(self, *args):
        """Select a video file."""

        self.get_action("select_video_file").activate()

    def on_video_button_drag_data_received(
        self, notebook, context, x, y, selection_data, info, time):
        """Set the video file from dragged URI."""

        page = self.get_current_page()
        uri = selection_data.get_uris()[0]
        path = gaupol.util.uri_to_path(uri)
        if not os.path.isfile(path): return
        page.project.video_path = path
        self.update_gui()

    @gaupol.deco.silent(gaupol.gtk.Default)
    def open_main_file(self, path, encoding=None):
        """Open main file."""

        encodings = self._get_encodings(encoding)
        page = self._open_file(path, encodings, gaupol.documents.MAIN)
        gaupol.gtk.util.set_cursor_busy(self.window)
        self.add_new_page(page)
        format = page.project.main_file.format
        self.add_to_recent_files(path, format, gaupol.documents.MAIN)
        basename = page.get_main_basename()
        self.flash_message(_('Opened main file "%s"') % basename)
        gaupol.gtk.util.iterate_main()
        gaupol.gtk.util.set_cursor_normal(self.window)

    def open_main_files(self, paths, encoding=None):
        """Open main files."""

        for path in sorted(paths):
            self.open_main_file(path, encoding)

    @gaupol.deco.silent(gaupol.gtk.Default)
    def open_translation_file(self, path, encoding=None, align_method=None):
        """Open translation file."""

        if align_method is not None:
            gaupol.gtk.conf.file.align_method = align_method
        encodings = self._get_encodings(encoding)
        page = self._open_file(path, encodings, gaupol.documents.TRAN)
        gaupol.gtk.util.set_cursor_busy(self.window)
        col = page.view.columns.TRAN_TEXT
        if not page.view.get_column(col).get_visible():
            self.get_column_action(gaupol.gtk.fields.TRAN_TEXT).activate()
        format = page.project.tran_file.format
        self.add_to_recent_files(path, format, gaupol.documents.TRAN)
        basename = page.get_translation_basename()
        self.flash_message(_('Opened translation file "%s"') % basename)
        gaupol.gtk.util.set_cursor_normal(self.window)
