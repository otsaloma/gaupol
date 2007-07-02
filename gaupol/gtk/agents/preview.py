# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.


"""Previewing subtitles with a video player."""


from __future__ import with_statement

import gaupol.gtk
import gobject
import gtk
import os
import tempfile
_ = gaupol.i18n._


class PreviewAgent(gaupol.Delegate):

    """Previewing subtitles with a video player."""

    # pylint: disable-msg=E0203,W0201

    @gaupol.gtk.util.asserted_return
    def _handle_output(self, pid, return_value, output_path):
        """Handle the output of finished preview process."""

        with open(output_path, "r") as fobj:
            output = fobj.read()
        silent = gaupol.gtk.util.silent(OSError)
        silent(os.remove)(output_path)
        self.output_window.set_output(output)
        assert return_value != 0
        dialog = gaupol.gtk.PreviewErrorDialog(self.window, output)
        self.flash_dialog(dialog)

    def _show_encoding_error_dialog(self):
        """Show an error dialog after failing to encode file."""

        title = _('Failed to encode subtitle file to '
            'temporary directory "%s"') % tempfile.gettempdir()
        message = _("Subtitle data could not be encoded to a temporary file "
            "for preview with the current character encoding. Please first "
            "save the subtitle file with a different character encoding.")
        dialog = gaupol.gtk.ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _show_io_error_dialog(self, message):
        """Show an error dialog after failing to write file."""

        title = _('Failed to save subtitle file to '
            'temporary directory "%s"') % tempfile.gettempdir()
        message = _("%s.") % message
        dialog = gaupol.gtk.ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def on_preview_activate(self, *args):
        """Preview from selected position with a video player."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        row = (rows[0] if rows else 0)
        time = page.project.subtitles[row].start_time
        col = gaupol.gtk.COLUMN.MAIN_TEXT
        if page.view.get_focus()[1] == gaupol.gtk.COLUMN.TRAN_TEXT:
            col = gaupol.gtk.COLUMN.TRAN_TEXT
        doc = gaupol.gtk.util.text_column_to_document(col)
        self.preview(page, time, doc)

    def preview(self, page, time, doc, path=None):
        """Preview from time with a video player."""

        try:
            command = gaupol.gtk.conf.preview.video_player.command
            if gaupol.gtk.conf.preview.use_custom:
                command = gaupol.gtk.conf.preview.custom_command
            offset = gaupol.gtk.conf.preview.offset
            output = page.project.preview(time, doc, command, offset, path)
            process, command, output_path = output
        except IOError, (no, message):
            silent = gaupol.gtk.util.silent(OSError)
            silent(os.remove)(output_path)
            return self._show_io_error_dialog(message)
        except UnicodeError:
            silent = gaupol.gtk.util.silent(OSError)
            silent(os.remove)(output_path)
            return self._show_encoding_error_dialog()
        handler = self._handle_output
        if process.poll() is not None:
            return handler(process.pid, process.returncode, output_path)
        gobject.child_watch_add(process.pid, handler, output_path)

    def preview_changes(self, page, row, doc, method, args=None, kwargs=None):
        """Preview changes caused by method with a video player."""

        subtitles = [x.copy() for x in page.project.subtitles]
        framerate = page.project.framerate
        blocked = page.project.block_all()
        kwargs = kwargs or {}
        kwargs["register"] = None
        method(*(args or ()), **kwargs)
        path = page.project.get_temp_file_path(doc)
        time = page.project.subtitles[row].start_time
        page.project.unblock_all(blocked)
        page.project.subtitles = subtitles
        page.project.set_framerate(framerate, register=None)
        self.preview(page, time, doc, path)
