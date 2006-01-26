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
import tempfile
import threading

import gobject
import gtk
import pango

from gaupol.base.error          import ExternalError
from gaupol.constants           import Document, VideoPlayer
from gaupol.gtk.colconstants    import *
from gaupol.gtk.delegates       import Delegate, UIMAction
from gaupol.gtk.dialogs.message import ErrorDialog
from gaupol.gtk.util            import config, gtklib


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


class CommandErrorDialog(object):

    """Dialog to inform that preview command failed."""

    def __init__(self, parent, output):

        glade_xml = gtklib.get_glade_xml('previewerror-dialog.glade')
        output_label = glade_xml.get_widget('output_label')
        self._dialog = glade_xml.get_widget('dialog')
        text_view  = glade_xml.get_widget('text_view')

        # Set mnemonics.
        output_label.set_mnemonic_widget(text_view)

        # Set output.
        text_buffer = text_view.get_buffer()
        text_buffer.create_tag('code', family='monospace')
        end_iter = text_buffer.get_end_iter()
        text_buffer.insert_with_tags_by_name(end_iter, output, 'code')

        # Set dialog size.
        label = gtk.Label()
        attrs = pango.AttrList()
        attrs.insert(pango.AttrFamily('monospace', 0, -1))
        label.set_attributes(attrs)
        label.set_text(output)
        width, height = label.size_request()
        width  = width  + 112 + gtklib.EXTRA
        height = height + 148 + gtklib.EXTRA
        gtklib.resize_message_dialog(self._dialog, width, height)

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def run(self):
        """Show and run the dialog."""

        self._dialog.show()
        return self._dialog.run()


class IOErrorDialog(ErrorDialog):

    """Dialog to inform that IOError occured while saving file."""

    def __init__(self, parent, message):

        title   = _('Failed to save subtitle file to temporary directory '
                    '"%s"') % tempfile.gettempdir()
        message = _('Because the subtitle document you\'re trying to preview '
                    'is changed, it needs to be saved to a temporary file '
                    'before previewing. Attempt to write that temporary file '
                    'returned error: %s.') % message

        ErrorDialog.__init__(self, parent, title, message)


class UnicodeErrorDialog(ErrorDialog):

    """Dialog to inform that UnicodeError occured while saving file."""

    def __init__(self, parent):

        title   = _('Failed to encode subtitle file to temporary directory '
                    '"%s"') % tempfile.gettempdir()
        message = _('Because the subtitle document you\'re trying to preview '
                    'is changed, it needs to be saved to a temporary file '
                    'before previewing. The temporary file is saved in the '
                    'same character encoding as the actual subtitle file. '
                    'Please save the actual subtitle file with a different '
                    'character encoding.')

        ErrorDialog.__init__(self, parent, title, message)


class PreviewDelegate(Delegate):

    """Previewing subtitles with video player."""

    def on_preview_activated(self, *args):
        """Preview subtitles with video player."""

        page     = self.get_current_page()
        row      = page.view.get_selected_rows()[0]
        col      = page.view.get_focus()[1]
        document = max(0, col - 4)

        args = page, row, document
        thread = threading.Thread(target=self._preview, args=args)
        thread.start()

    def _preview(self, page, row, document):
        """Preview subtitles with video player."""

        if config.preview.use_custom:
            command = config.preview.custom_command
        else:
            video_player = config.preview.video_player
            command = VideoPlayer.commands[video_player]

        offset = config.preview.offset

        try:
            page.project.preview(row, document, command, offset)
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

        dialog = CommandErrorDialog(self.window, page.project.output)
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
