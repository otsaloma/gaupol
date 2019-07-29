# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Previewing subtitles with a video player."""

import aeidon
import gaupol
import shutil
import tempfile

from aeidon.i18n   import _
from gi.repository import GLib
from gi.repository import Gtk


class PreviewAgent(aeidon.Delegate):

    """Previewing subtitles with a video player."""

    def _check_process_state(self, page, process, fout, command):
        """Check if `process` has terminated or not."""
        if process.poll() is None: return True
        self._handle_output(process, fout, command)
        return False # to not check again.

    def _handle_output(self, process, fout, command):
        """Handle output of finished `process`."""
        fout.close()
        with open(fout.name, "r", errors="replace") as f:
            output = f.read().splitlines()
        output = "\n".join(output[:100])
        print("\nPREVIEW: {}\n{}".format(command, output))
        aeidon.temp.remove(fout.name)
        if process.returncode == 0: return
        dialog = gaupol.PreviewErrorDialog(self.window, output)
        gaupol.util.flash_dialog(dialog)

    @aeidon.deco.export
    def _on_preview_activate(self, *args):
        """Preview from selected position with a video player."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        row = rows[0] if rows else 0
        position = page.project.subtitles[row].start
        col = page.view.get_focus()[1]
        if col == page.view.columns.TRAN_TEXT:
            doc = aeidon.documents.TRAN
        else: # Any other column previews the main file.
            doc = aeidon.documents.MAIN
        self.preview(page, position, doc)

    @aeidon.deco.export
    def preview(self, page, position, doc, temp=False):
        """Preview from `position` with a video player."""
        if (not gaupol.conf.preview.use_custom_command and
            not shutil.which(gaupol.conf.preview.player.executable)):
            return self._show_player_not_found_error_dialog()
        command = gaupol.util.get_preview_command()
        offset = gaupol.conf.preview.offset
        encoding = "utf_8" if gaupol.conf.preview.force_utf_8 else None
        try:
            process, command, fout = page.project.preview(
                position, doc, command, offset, encoding, temp)
        except aeidon.ProcessError as error:
            return self._show_process_error_dialog(str(error))
        except (IOError, OSError) as error:
            return self._show_io_error_dialog(str(error))
        except UnicodeError:
            return self._show_encoding_error_dialog()
        # GLib.child_watch_add does not appear to work on Windows,
        # so let's watch the process by polling it at regular intervals.
        GLib.timeout_add(1000,
                         self._check_process_state,
                         page, process, fout, command)

    @aeidon.deco.export
    def preview_changes(self, page, row, doc, method, args=None, kwargs=None):
        """Preview changes caused by `method` with a video player."""
        subtitles = [x.copy() for x in page.project.subtitles]
        framerate = page.project.framerate
        blocked = page.project.block_all()
        method(register=None, *(args or ()), **(kwargs or {}))
        position = page.project.subtitles[row].start
        page.project.unblock_all(blocked)
        self.preview(page, position, doc, temp=True)
        page.project.set_framerate(framerate, register=None)
        page.project.subtitles = subtitles

    def _show_encoding_error_dialog(self):
        """Show an error dialog after failing to encode file."""
        title = _('Failed to encode subtitle file to temporary directory "{}"').format(tempfile.gettempdir())
        message = _("Subtitle data could not be encoded to a temporary file for preview with the current character encoding. Please first save the subtitle file with a different character encoding.")
        dialog = gaupol.ErrorDialog(self.window, title, message)
        dialog.add_button(_("_OK"), Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _show_io_error_dialog(self, message):
        """Show an error dialog after failing to write file."""
        title = _('Failed to save subtitle file to temporary directory "{}"').format(tempfile.gettempdir())
        dialog = gaupol.ErrorDialog(self.window, title, message)
        dialog.add_button(_("_OK"), Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _show_player_not_found_error_dialog(self):
        """Show an error dialog if video player not found."""
        title = _("Video player not found")
        message = _("Please install one of the supported video players: mpv (recommended), MPlayer or VLC. See the preferences dialog to choose the video player or to customize the command.")
        dialog = gaupol.ErrorDialog(self.window, title, message)
        dialog.add_button(_("_OK"), Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _show_process_error_dialog(self, message):
        """Show an error dialog after failing to launch video player."""
        title = _("Failed to launch video player")
        dialog = gaupol.ErrorDialog(self.window, title, message)
        dialog.add_button(_("_OK"), Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)
