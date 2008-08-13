# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Previewing subtitles with a video player."""

from __future__ import with_statement

import gaupol.gtk
import gobject
import gtk
import tempfile
_ = gaupol.i18n._


class PreviewAgent(gaupol.Delegate):

    """Previewing subtitles with a video player."""

    # pylint: disable-msg=E0203,W0201

    def _check_process_state(self, process, output_path, command):
        """Check if the process has terminated or not."""

        if process.poll() is None: return True
        self._handle_output(process, output_path, command)
        return False # to not check again.

    def _handle_output(self, process, output_path, command):
        """Handle the output of finished preview process."""

        with open(output_path, "r") as fobj:
            output = fobj.read()
        output = command + "\n\n" + output
        gaupol.temp.remove(output_path)
        self.output_window.set_output(output)
        if process.returncode == 0: return
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

    def _show_process_error_dialog(self, message):
        """Show an error dialog after failing to launch video player."""

        title = _("Failed to launch video player")
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
        col = page.view.get_focus()[1]
        if col == page.view.columns.TRAN_TEXT:
            doc = gaupol.documents.TRAN
        else: # Any other column previews the main file.
            doc = gaupol.documents.MAIN
        self.preview(page, time, doc)

    def preview(self, page, time, doc, path=None):
        """Preview from time with a video player."""

        command = gaupol.gtk.conf.preview.video_player.command
        if gaupol.gtk.conf.preview.use_custom:
            command = gaupol.gtk.conf.preview.custom_command
        offset = gaupol.gtk.conf.preview.offset
        preview = page.project.preview
        args = (time, doc, command, offset, path)
        try: process, command, output_path = preview(*args)
        except gaupol.ProcessError, message:
            return self._show_process_error_dialog(message)
        except (IOError, OSError), (no, message):
            return self._show_io_error_dialog(message)
        except UnicodeError:
            return self._show_encoding_error_dialog()
        # 'gobject.child_watch_add' does not appear to work on Windows,
        # so let's watch the process by polling it at regular intervals.
        function = self._check_process_state
        args = (process, output_path, command)
        gobject.timeout_add(1000, function, *args)

    def preview_changes(self, page, row, doc, method, args=None, kwargs=None):
        """Preview changes caused by method with a video player."""

        subtitles = [x.copy() for x in page.project.subtitles]
        framerate = page.project.framerate
        blocked = page.project.block_all()
        method(register=None, *(args or ()), **(kwargs or {}))
        path = page.project.get_temp_file_path(doc)
        time = page.project.subtitles[row].start_time
        page.project.unblock_all(blocked)
        page.project.subtitles = subtitles
        page.project.set_framerate(framerate, register=None)
        self.preview(page, time, doc, path)
