# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Previewing subtitles with video player."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _
import copy
import tempfile
import threading

import gobject
import gtk
import pango

from gaupol.base.error               import ExternalError
from gaupol.constants                import Document, VideoPlayer
from gaupol.gtk.colconstants         import *
from gaupol.gtk.delegates            import Delegate, UIMAction
from gaupol.gtk.dialogs.message      import ErrorDialog
from gaupol.gtk.dialogs.previewerror import PreviewErrorDialog
from gaupol.gtk.util                 import config, gtklib


class PreviewAction(UIMAction):

    """Previewing subtitles with video player."""

    uim_action_item = (
        'preview',
        gtk.STOCK_MEDIA_PLAY,
        _('_Preview'),
        'F6',
        _('Preview from selected position with a video player'),
        'on_preview_activated'
    )

    uim_paths = [
        '/ui/menubar/tools/preview',
        '/ui/main_toolbar/preview',
        '/ui/view/preview'
    ]

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False
        if page.project.video_path is None:
            return False
        if not page.view.get_selected_rows():
            return False

        focus_col = page.view.get_focus()[1]
        if focus_col == TTXT:
            if page.project.tran_file is None:
                return False
        else:
            if page.project.main_file is None:
                return False

        return True


class IOErrorDialog(ErrorDialog):

    """Dialog to inform that IOError occured while saving file."""

    def __init__(self, parent, message):

        title   = _('Failed to save subtitle file to temporary directory '
                    '"%s"') % tempfile.gettempdir()
        message = _('Attempt to write temporary subtitle file for preview '
                    'returned error: %s.') % message
        ErrorDialog.__init__(self, parent, title, message)


class UnicodeErrorDialog(ErrorDialog):

    """Dialog to inform that UnicodeError occured while saving file."""

    def __init__(self, parent):

        title   = _('Failed to encode subtitle file to temporary directory '
                    '"%s"') % tempfile.gettempdir()
        message = _('Current data cannot be encoded to a temporary subtitle '
                    'file for preview with the current character encoding. '
                    'Please first save the subtitle file with a different '
                    'character encoding.')
        ErrorDialog.__init__(self, parent, title, message)


class PreviewDelegate(Delegate):

    """Previewing subtitles with video player."""

    def on_preview_activated(self, *args):
        """Preview subtitles with video player."""

        page = self.get_current_page()
        row  = page.view.get_selected_rows()[0]
        time = page.project.times[row][0]
        col  = page.view.get_focus()[1]
        document = max(0, col - 4)

        args = page, time, document
        thread = threading.Thread(target=self._run_preview, args=args)
        thread.start()

    def preview_changes(self, page, row, document, method, args=[], kwargs={}):
        """Start threaded preview with video player."""

        # Backup original data.
        times      = copy.deepcopy(page.project.times)
        frames     = copy.deepcopy(page.project.frames)
        main_texts = copy.deepcopy(page.project.main_texts)

        # Change data.
        kwargs['register'] = None
        method(*args, **kwargs)
        path = page.project.get_temp_file_path(document)
        time = page.project.times[row][0]

        # Restore original data.
        page.project.times      = times
        page.project.frames     = frames
        page.project.main_texts = main_texts

        # Preview temporary file with changed data.
        args = page, time, document, path
        thread = threading.Thread(target=self._run_preview, args=args)
        thread.start()

    def _run_preview(self, page, time, document, path=None):
        """Run preview with video player."""

        if config.preview.use_custom:
            command = config.preview.custom_command
        else:
            video_player = config.preview.video_player
            command = VideoPlayer.commands[video_player]
        offset = config.preview.offset

        try:
            page.project.preview_time(time, document, command, offset, path)
        except ExternalError:
            self._show_command_error_dialog(page)
        except IOError, (no, message):
            self._show_io_error_dialog(message)
        except UnicodeError:
            self._show_unicode_error_dialog()

        self._show_output(page)

    @gtklib.idlemethod
    def _show_command_error_dialog(self, page):
        """Show CommandErrorDialog."""

        dialog = PreviewErrorDialog(self.window, page.project.output)
        dialog.run()
        dialog.destroy()

    @gtklib.idlemethod
    def _show_io_error_dialog(self, message):
        """Show IOErrorDialog."""

        dialog = IOErrorDialog(self.window, message)
        dialog.run()
        dialog.destroy()

    @gtklib.idlemethod
    def _show_output(self, page):
        """Show output in output window."""

        self.output_window.set_output(page.project.output)

    @gtklib.idlemethod
    def _show_unicode_error_dialog(self):
        """Show UnicodeErrorDialog."""

        dialog = UnicodeErrorDialog(self.window)
        dialog.run()
        dialog.destroy()


if __name__ == '__main__':

    from gaupol.gtk.application import Application
    from gaupol.test            import Test

    class TestPreviewDelegate(Test):

        def __init__(self):

            Test.__init__(self)
            self.application = Application()
            self.application.open_main_files([self.get_subrip_path()])
            self.delegate = PreviewDelegate(self.application)

        def destroy(self):

            self.application.window.destroy()

        def test_dialogs(self):

            page = self.application.get_current_page()
            page.project.output = 'test'

            self.delegate._show_command_error_dialog(page)
            self.delegate._show_io_error_dialog('test')
            self.delegate._show_output(page)
            self.delegate._show_unicode_error_dialog()

    TestPreviewDelegate().run()

