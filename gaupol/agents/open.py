# -*- coding: utf-8 -*-

# Copyright (C) 2005-2010,2012 Osmo Salomaa
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

"""Opening subtitle files and creating new projects."""

import aeidon
import gaupol
import os
_ = aeidon.i18n._

from gi.repository import Gtk
from gi.repository import GObject


class OpenAgent(aeidon.Delegate):

    """Opening subtitle files and creating new projects."""

    def _append_subtitles(self, page, subtitles):
        """
        Append `subtitles` to `page`.

        Return sequence of new indices in `page`.
        """
        project = page.project
        n = len(project.subtitles)
        indices = list(range(n, n + len(subtitles)))
        project.block("action-done")
        project.insert_subtitles(indices, subtitles)
        project.set_action_description(aeidon.registers.DO,
                                       _("Appending file"))

        project.unblock("action-done")
        return tuple(indices)

    def _check_file_exists(self, path):
        """Raise :exc:`gaupol.Default` if no file at `path`."""
        gaupol.util.raise_default(not os.path.isfile(path))

    def _check_file_not_open(self, path):
        """Raise :exc:`gaupol.Default` if file at `path` already open."""
        for page in self.pages:
            files = (page.project.main_file, page.project.tran_file)
            paths = [x.path for x in [y for y in files if y]]
            if not path in paths: continue
            self.set_current_page(page)
            message = _('File "{}" is already open')
            self.flash_message(message.format(os.path.basename(path)))
            raise gaupol.Default

    def _check_file_size(self, path):
        """Raise :exc:`gaupol.Default` if size of file at `path` too large."""
        size_mb = os.stat(path)[6] / 1048576
        if size_mb <= 1: return
        basename = os.path.basename(path)
        self._show_size_warning_dialog(basename, size_mb)

    def _check_sort_count(self, path, sort_count):
        """Raise :exc:`gaupol.Default` if `sort_count` too large."""
        if sort_count <= 0: return
        basename = os.path.basename(path)
        self._show_sort_warning_dialog(basename, sort_count)

    def _get_encodings(self, first=None):
        """Return a sequence of encodings to try when opening files."""
        encodings = [first]
        if gaupol.conf.encoding.try_locale:
            encoding = aeidon.encodings.get_locale_code()
            encodings.append(encoding)
        encodings += gaupol.conf.encoding.fallback
        try_auto = gaupol.conf.encoding.try_auto
        if try_auto and aeidon.util.chardet_available():
            encodings.append("auto")
        while None in encodings:
            encodings.remove(None)
        encodings = encodings or ["utf_8"]
        return tuple(aeidon.util.get_unique(encodings))

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def _on_append_file_activate(self, *args):
        """Append subtitles from file to the current project."""
        gaupol.util.set_cursor_busy(self.window)
        dialog = gaupol.AppendDialog(self.window)
        gaupol.util.set_cursor_normal(self.window)
        response = gaupol.util.run_dialog(dialog)
        paths = dialog.get_filenames()
        encoding = dialog.get_encoding()
        dialog.destroy()
        if response != Gtk.ResponseType.OK: return
        if not paths: return
        gaupol.util.iterate_main()
        self.append_file(paths[0], encoding)

    @aeidon.deco.export
    def _on_new_project_activate(self, *args):
        """Create a new project."""
        if gaupol.fields.TRAN_TEXT in gaupol.conf.editor.visible_fields:
            gaupol.conf.editor.visible_fields.remove(gaupol.fields.TRAN_TEXT)
        page = gaupol.Page(next(self.counter))
        page.project.insert_subtitles((0,), register=None)
        self.add_page(page)

    @aeidon.deco.export
    def _on_notebook_drag_data_received(self, notebook, context, x, y,
                                        selection_data, info, time):

        """Open main files from dragged URIs."""
        uris = selection_data.get_uris()
        paths = list(map(aeidon.util.uri_to_path, uris))
        self.open_main(paths)

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def _on_open_main_files_activate(self, *args):
        """Open main files."""
        doc = aeidon.documents.MAIN
        paths, encoding = self._select_files(_("Open"), doc)
        self.open_main(paths, encoding)

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def _on_open_main_files_recent_activate(self, *args):
        """Open main files."""
        doc = aeidon.documents.MAIN
        paths, encoding = self._select_files(_("Open"), doc)
        self.open_main(paths, encoding)

    @aeidon.deco.export
    def _on_open_main_files_recent_item_activated(self, chooser):
        """Open a recent main file."""
        uri = chooser.get_current_uri()
        path = aeidon.util.uri_to_path(uri)
        self.open_main(path)

    @aeidon.deco.export
    def _on_open_recent_main_file_item_activated(self, chooser):
        """Open a recent main file."""
        uri = chooser.get_current_uri()
        path = aeidon.util.uri_to_path(uri)
        self.open_main(path)

    @aeidon.deco.export
    def _on_open_recent_translation_file_item_activated(self, chooser):
        """Open a recent translation file."""
        uri = chooser.get_current_uri()
        path = aeidon.util.uri_to_path(uri)
        align_method = aeidon.align_methods.POSITION
        self.open_translation(path,
                              encoding=None,
                              align_method=align_method)

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def _on_open_translation_file_activate(self, *args):
        """Open a translation file."""
        page = self.get_current_page()
        if page.project.tran_changed:
            self._show_translation_warning_dialog(page)
        doc = aeidon.documents.TRAN
        paths, encoding = self._select_files(_("Open Translation"), doc)
        self.open_translation(paths[0], encoding)

    @aeidon.deco.export
    def _on_select_video_file_activate(self, *args):
        """Select a video file."""
        gaupol.util.set_cursor_busy(self.window)
        page = self.get_current_page()
        path = page.project.video_path
        dialog = gaupol.VideoDialog(self.window,
                                    title=_("Select Video"),
                                    button_label=_("_Select"))

        if page.project.main_file is not None:
            directory = os.path.dirname(page.project.main_file.path)
            dialog.set_current_folder(directory)
        if page.project.video_path is not None:
            dialog.set_filename(page.project.video_path)
        gaupol.util.set_cursor_normal(self.window)
        response = gaupol.util.run_dialog(dialog)
        path = dialog.get_filename()
        dialog.destroy()
        if response != Gtk.ResponseType.OK: return
        page.project.video_path = path
        self.update_gui()

    @aeidon.deco.export
    def _on_split_project_activate(self, *args):
        """Split the current project in two."""
        gaupol.util.flash_dialog(gaupol.SplitDialog(self.window, self))

    def _open_file(self, path, encodings, doc, check_open=True):
        """
        Open file at `path` and return corresponding page if successful.

        Raise :exc:`gaupol.Default` if cancelled or file cannot be opened.
        """
        self._check_file_exists(path)
        if check_open:
            self._check_file_not_open(path)
        self._check_file_size(path)
        basename = os.path.basename(path)
        page = (gaupol.Page if doc == aeidon.documents.MAIN
                else self.get_current_page)()

        for encoding in encodings:
            try:
                sort_count = self._try_open_file(page,
                                                 doc,
                                                 path,
                                                 encoding)

            except UnicodeError:
                continue
            self._check_sort_count(path, sort_count)
            return page
        # Report if all codecs failed to decode file.
        self._show_encoding_error_dialog(basename)
        raise gaupol.Default

    def _select_files(self, title, doc):
        """
        Show a :class:`gaupol.OpenDialog` to select files.

        Raise :exc:`gaupol.Default` if cancelled.
        """
        gaupol.util.set_cursor_busy(self.window)
        dialog = gaupol.OpenDialog(self.window, title, doc)
        page = self.get_current_page()
        if (page is not None) and (page.project.main_file is not None):
            directory = os.path.dirname(page.project.main_file.path)
            dialog.set_current_folder(directory)
        gaupol.util.set_cursor_normal(self.window)
        response = gaupol.util.run_dialog(dialog)
        paths = dialog.get_filenames()
        encoding = dialog.get_encoding()
        dialog.destroy()
        gaupol.util.raise_default(response != Gtk.ResponseType.OK)
        gaupol.util.iterate_main()
        return paths, encoding

    def _show_encoding_error_dialog(self, basename):
        """Show an error dialog after failing to decode file."""
        title = _('Failed to decode file "{}" with all '
            'attempted codecs').format(basename)
        message = _("Please try to open the file with a "
            "different character encoding.")
        dialog = gaupol.ErrorDialog(self.window, title, message)
        dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _show_format_error_dialog(self, basename):
        """Show an error dialog after failing to recognize file format."""
        title = _('Failed to recognize format of file "{}"').format(basename)
        message = _("Please check that the file you are trying to open is a "
            "subtitle file of a format supported by Gaupol.")
        dialog = gaupol.ErrorDialog(self.window, title, message)
        dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _show_io_error_dialog(self, basename, message):
        """Show an error dialog after failing to read file."""
        title = _('Failed to open file "{}"').format(basename)
        dialog = gaupol.ErrorDialog(self.window, title, message)
        dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _show_parse_error_dialog(self, basename, format):
        """Show an error dialog after failing to parse file."""
        title = _('Failed to parse file "{}"').format(basename)
        message = _("Please check that the file you are trying "
            "to open is a valid {} file.").format(format.label)
        dialog = gaupol.ErrorDialog(self.window, title, message)
        dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _show_size_warning_dialog(self, basename, size):
        """
        Show a warning dialog when trying to open a large file.

        Raise :exc:`gaupol.Default` if opening cancelled.
        """
        title = _('Open abnormally large file "{}"?').format(basename)
        message = _("Size of the file is {:.1f} MB, which is abnormally large "
            "for a text-based subtitle file. Please, check that you are not "
            "trying to open a binary file.").format(size)
        dialog = gaupol.WarningDialog(self.window, title, message)
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.NO)
        dialog.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.YES)
        dialog.set_default_response(Gtk.ResponseType.NO)
        response = gaupol.util.flash_dialog(dialog)
        gaupol.util.raise_default(response != Gtk.ResponseType.YES)

    def _show_sort_warning_dialog(self, basename, count):
        """
        Show a warning dialog when subtitles have been sorted.

        Raise :exc:`gaupol.Default` if opening cancelled.
        """
        title = _('Open unsorted file "{}"?').format(basename)
        message = _("The order of {:d} subtitles needs to be changed. "
            "If {:d} sounds like a lot, the file may be erroneously composed.")
        message = message.format(count, count)
        dialog = gaupol.WarningDialog(self.window, title, message)
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.NO)
        dialog.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.YES)
        dialog.set_default_response(Gtk.ResponseType.YES)
        response = gaupol.util.flash_dialog(dialog)
        gaupol.util.raise_default(response != Gtk.ResponseType.YES)

    def _show_translation_warning_dialog(self, page):
        """
        Show a warning dialog if opening a new translation file.

        Raise :exc:`gaupol.Default` if opening cancelled.
        """
        title = _('Save changes to translation document "{}" before '
            'opening a new one?').format(page.get_translation_basename())
        message = _("If you don't save, changes will be permanently lost.")
        dialog = gaupol.WarningDialog(self.window, title, message)
        dialog.add_button(_("Open _Without Saving"), Gtk.ResponseType.NO)
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_SAVE, Gtk.ResponseType.YES)
        dialog.set_default_response(Gtk.ResponseType.YES)
        response = gaupol.util.flash_dialog(dialog)
        if response == Gtk.ResponseType.YES:
            return self.save_translation(page)
        gaupol.util.raise_default(response != Gtk.ResponseType.NO)

    def _try_open_file(self, page, doc, path, encoding, **kwargs):
        """
        Try to open file at `path` and return subtitle sort count.

        Raise :exc:`gaupol.Default` if reading or parsing fails.
        Raise :exc:`UnicodeError`if decoding fails.
        """
        gaupol.util.set_cursor_busy(self.window)
        basename = os.path.basename(path)
        if encoding == "auto":
            encoding = aeidon.encodings.detect(path)
            if encoding is None: raise UnicodeError
        if doc == aeidon.documents.TRAN:
            kwargs["align_method"] = gaupol.conf.file.align_method
        try:
            return page.project.open(doc, path, encoding, **kwargs)
        except aeidon.FormatError:
            gaupol.util.set_cursor_normal(self.window)
            self._show_format_error_dialog(basename)
        except IOError as error:
            gaupol.util.set_cursor_normal(self.window)
            self._show_io_error_dialog(basename, str(error))
        except aeidon.ParseError:
            gaupol.util.set_cursor_normal(self.window)
            bom_encoding = aeidon.encodings.detect_bom(path)
            encoding = bom_encoding or encoding
            silent = aeidon.deco.silent(Exception)
            format = silent(aeidon.util.detect_format)(path, encoding)
            self._show_parse_error_dialog(basename, format)
        finally:
            gaupol.util.set_cursor_normal(self.window)
        raise gaupol.Default

    @aeidon.deco.export
    def add_page(self, page):
        """Add `page` to the application."""
        self.pages.append(page)
        page.connect("close-request", self._on_page_close_request)
        page.project.connect("action-done", self._on_project_action_done)
        page.project.connect("action-redone", self._on_project_action_redone)
        page.project.connect("action-undone", self._on_project_action_undone)
        callback = self._on_tab_widget_button_press_event
        page.tab_widget.connect("button-press-event", callback, page)
        self.connect_view_signals(page.view)
        page.project.clipboard.set_texts(self.clipboard.get_texts())
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(*((Gtk.PolicyType.AUTOMATIC,) * 2))
        scroller.add(page.view)
        self.notebook.append_page(scroller, page.tab_widget)
        self.notebook.set_tab_reorderable(scroller, True)
        self.notebook.show_all()
        self.set_current_page(page)
        self.emit("page-added", page)

    @aeidon.deco.export
    def add_to_recent_files(self, path, format, doc):
        """Add `path` to recent files managed by the recent manager."""
        uri = aeidon.util.path_to_uri(path)
        if GObject.pygobject_version >= (3, 7, 4):
            # Trying to set strings to struct fields
            # fails with earlier versions of PyGObject.
            # https://bugzilla.gnome.org/show_bug.cgi?id=678401
            recent_data = Gtk.RecentData()
            recent_data.mime_type = format.mime_type
            recent_data.app_name = "gaupol"
            recent_data.app_exec = "gaupol %F"
            # XXX: We still cannot set string lists (gchar**).
            # https://bugzilla.gnome.org/show_bug.cgi?id=695970
            # group = ("gaupol-translation"
            #          if doc == aeidon.documents.TRAN
            #          else "gaupol-main")

            # recent_data.groups = (group,)
            self.recent_manager.add_full(uri, recent_data)
        else:
            self.recent_manager.add_item(uri)

    @aeidon.deco.export
    def append_file(self, path, encoding=None):
        """
        Append subtitles from file at `path` to the current project.

        Raise :exc:`gaupol.Default` if cancelled or something goes wrong.
        """
        encodings = self._get_encodings(encoding)
        doc = aeidon.documents.MAIN
        temp = self._open_file(path, encodings, doc, check_open=False)
        gaupol.util.set_cursor_busy(self.window)
        current = self.get_current_page()
        offset = current.project.subtitles[-1].end
        temp.project.shift_positions(None, offset)
        rows = self._append_subtitles(current, temp.project.subtitles)
        amount = len(rows)
        current.view.set_focus(rows[0], None)
        current.view.select_rows(rows)
        current.view.scroll_to_row(rows[0])
        basename = temp.get_main_basename()
        message = _('Appended {amount:d} subtitles from "{basename}"')
        self.flash_message(message.format(**locals()))
        gaupol.util.set_cursor_normal(self.window)

    @aeidon.deco.export
    def connect_view_signals(self, view):
        """Connect to signals emitted by `view`."""
        view.connect_selection_changed(self._on_view_selection_changed)
        view.connect_after("move-cursor", self._on_view_move_cursor)
        view.connect("button-press-event", self._on_view_button_press_event)
        for column in view.get_columns():
            renderer = column.get_cells()[0]
            callback = self._on_view_renderer_edited
            renderer.connect("edited", callback, column)
            callback = self._on_view_renderer_editing_started
            renderer.connect("editing-started", callback, column)
            callback = self._on_view_renderer_editing_canceled
            renderer.connect("editing-canceled", callback, column)
            button = column.get_widget().get_ancestor(Gtk.Button)
            callback = self._on_view_header_button_press_event
            button.connect("button-press-event", callback)

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def open_main(self, path, encoding=None):
        """
        Open file at `path` as a main file.

        `path` can be a sequence of paths to open multiple files.
        Use ``None`` for `encoding` to try the default sequence.
        """
        if gaupol.fields.TRAN_TEXT in gaupol.conf.editor.visible_fields:
            gaupol.conf.editor.visible_fields.remove(gaupol.fields.TRAN_TEXT)
        if isinstance(path, (list, set, tuple)):
            return [self.open_main(x, encoding) for x in sorted(path)]
        encodings = self._get_encodings(encoding)
        page = self._open_file(path, encodings, aeidon.documents.MAIN)
        gaupol.util.set_cursor_busy(self.window)
        self.add_page(page)
        format = page.project.main_file.format
        self.add_to_recent_files(path, format, aeidon.documents.MAIN)
        gaupol.util.iterate_main()
        gaupol.util.set_cursor_normal(self.window)

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def open_translation(self, path, encoding=None, align_method=None):
        """
        Open file at `path` as a translation file.

        Use ``None`` for `encoding` to try the default sequence.
        Use ``None`` for `align_method` to use whatever happens to be as
        :attr:`gaupol.conf.file.align_method`.
        """
        if align_method is not None:
            gaupol.conf.file.align_method = align_method
        encodings = self._get_encodings(encoding)
        page = self._open_file(path, encodings, aeidon.documents.TRAN)
        gaupol.util.set_cursor_busy(self.window)
        col = page.view.columns.TRAN_TEXT
        if not page.view.get_column(col).get_visible():
            self.get_column_action(gaupol.fields.TRAN_TEXT).activate()
        format = page.project.tran_file.format
        self.add_to_recent_files(path, format, aeidon.documents.TRAN)
        gaupol.util.set_cursor_normal(self.window)
