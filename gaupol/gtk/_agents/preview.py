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


"""Previewing subtitles with a video player."""


from __future__ import with_statement

import copy
import gobject
import gtk
import os
import tempfile
from gettext import gettext as _

from gaupol.base import Delegate
from gaupol.gtk import conf, util
from gaupol.gtk.dialogs import ErrorDialog, PreviewErrorDialog
from gaupol.gtk.index import *


class PreviewAgent(Delegate):

    """Previewing subtitles with a video player."""

    # pylint: disable-msg=E0203,W0201

    def _clean(self, output_path, temp_path):
        """Remove output and temporary files if they exist."""

        remove = util.silent(OSError, TypeError)(os.remove)
        remove(output_path)
        remove(temp_path)

    def _post_process(self, pid, return_value, data):
        """Process output of finished preview."""

        output_path, temp_path = data
        with open(output_path, "r") as fobj:
            output = fobj.read()
        self._clean(output_path, temp_path)
        self.output_window.set_output(output)
        if return_value != 0:
            dialog = PreviewErrorDialog(self.window, output)
            self.flash_dialog(dialog)

    def _show_encoding_error_dialog(self):
        """Show an error dialog after failing to encode file."""

        title = _('Failed to encode subtitle file to '
            'temporary directory "%s"') % tempfile.gettempdir()
        message = _("Subtitle data could not be encoded to a temporary "
            "file for preview with the current character encoding. Please "
            "first save the subtitle file with a different character "
            "encoding.")
        dialog = ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _show_io_error_dialog(self, message):
        """Show an error dialog after failing to write file."""

        title = _('Failed to save subtitle file to '
            'temporary directory "%s"') % tempfile.gettempdir()
        message = _("%s.") % message
        dialog = ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def on_preview_activate(self, *args):
        """Preview from selected position with a video player."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        row = (rows[0] if rows else 0)
        time = page.project.times[row][0]
        col = page.view.get_focus()[1]
        col = (TTXT if col == TTXT else MTXT)
        doc = page.text_column_to_document(col)
        self.preview(page, time, doc)

    def preview(self, page, time, doc, path=None):
        """Preview from time with a video player."""

        command = conf.preview.video_player.command
        if not conf.preview.use_predefined:
            command = conf.preview.custom_command
        offset = conf.preview.offset

        try:
            output = page.project.preview(time, doc, command, offset, path)
            process, command, output_path, temp_path = output
        except IOError, (no, message):
            self._clean(output_path, temp_path)
            return self._show_io_error_dialog(message)
        except UnicodeError:
            self._clean(output_path, temp_path)
            return self._show_encoding_error_dialog()

        data = (output_path, temp_path)
        if process.poll() is not None:
            # If the process was terminated by the time we got here,
            # it needs to be processed manually.
            return self._post_process(process.pid, process.returncode, data)
        gobject.child_watch_add(process.pid, self._post_process, data)

    def preview_changes(self, page, row, doc, method, args=None, kwargs=None):
        """Preview changes caused by method with a video player."""

        times = copy.deepcopy(page.project.times)
        frames = copy.deepcopy(page.project.frames)
        main_texts = copy.deepcopy(page.project.main_texts)
        tran_texts = copy.deepcopy(page.project.tran_texts)

        blocked = page.project.block_all()
        args = (args if args is not None else [])
        kwargs = (kwargs if kwargs is not None else {})
        kwargs["register"] = None
        method(*args, **kwargs)
        path = page.project.get_temp_file_path(doc)
        time = page.project.times[row][0]
        page.project.unblock_all(blocked)

        page.project.times = times
        page.project.frames = frames
        page.project.main_texts = main_texts
        page.project.tran_texts = tran_texts
        self.preview(page, time, doc, path)
