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


"""Previewing subtitles with video player."""


from gettext import gettext as _
import copy
import os
import tempfile

import gobject
import gtk

from gaupol.gtk                   import cons
from gaupol.gtk.icons             import *
from gaupol.gtk.delegate          import Delegate, UIMAction
from gaupol.gtk.dialog.message    import ErrorDialog
from gaupol.gtk.dialog.previewerr import PreviewErrorDialog
from gaupol.gtk.util              import conf, gtklib


class PreviewAction(UIMAction):

    """Previewing subtitles with video player."""

    action_item = (
        'preview',
        gtk.STOCK_MEDIA_PLAY,
        _('_Preview'),
        'F6',
        _('Preview from selected position with a video player'),
        'on_preview_activate'
    )

    paths = [
        '/ui/menubar/tools/preview',
        '/ui/main_toolbar/preview',
        '/ui/view/preview'
    ]

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        if page.project.video_path is None:
            return False
        if not page.view.get_selected_rows():
            return False
        if not conf.preview.use_predefined:
            if not conf.preview.custom_command:
                return False

        if page.view.get_focus()[1] == TTXT:
            if page.project.tran_file is None:
                return False
        else:
            if page.project.main_file is None:
                return False

        return True


class _IOErrorDialog(ErrorDialog):

    """Dialog for informing that IOError occured while saving file."""

    def __init__(self, parent, message):

        ErrorDialog.__init__(
            self, parent,
            _('Failed to save subtitle file to temporary directory "%s"') \
            % tempfile.gettempdir(),
            _('%s.') % message
        )


class _UnicodeErrorDialog(ErrorDialog):

    """Dialog for informing that UnicodeError occured while saving file."""

    def __init__(self, parent):

        ErrorDialog.__init__(
            self, parent,
            _('Failed to encode subtitle file to temporary directory "%s"') \
            % tempfile.gettempdir(),
            _('Current data could not be encoded to a temporary subtitle file '
              'for preview with the current character encoding. Please first '
              'save the subtitle file with a different character encoding.')
        )


class PreviewDelegate(Delegate):

    """Previewing subtitles with video player."""

    def _post_process(self, pid, return_value, data):
        """Process finished preview data."""

        command, output_path, temp_path = data
        fobj = open(output_path, 'r')
        output = fobj.read()
        fobj.close()

        for path in (output_path, temp_path):
            try:
                os.remove(path)
            except (OSError, TypeError):
                pass

        output = '$ ' + command + '\n\n' + output
        self._output_window.set_output(output)
        if return_value != 0:
            gtklib.run(PreviewErrorDialog(self._window, output))

    def _run_preview(self, page, time, doc, path=None):
        """Run preview with video player."""

        if conf.preview.use_predefined:
            command = cons.VideoPlayer.commands[conf.preview.video_player]
        else:
            command = conf.preview.custom_command
        offset = conf.preview.offset

        try:
            output = page.project.preview(time, doc, command, offset, path)
            pid, command, output_path, temp_path = output
        except IOError, (no, message):
            gtklib.run(_IOErrorDialog(self._window, message))
        except UnicodeError:
            gtklib.run(_UnicodeErrorDialog(self._window))
        else:
            data = [command, output_path, temp_path]
            gobject.child_watch_add(pid, self._post_process, data)

    def on_preview_activate(self, *args):
        """Preview subtitles with video player."""

        page = self.get_current_page()
        row  = page.view.get_selected_rows()[0]
        time = page.project.times[row][0]
        col  = page.view.get_focus()[1]
        doc  = 0
        if col is not None:
            doc  = max(0, col - 4)

        self._run_preview(page, time, doc)

    def preview_changes(self, page, row, doc, method, args=[], kwargs={}):
        """Preview changes caused by method with video player."""

        times = copy.deepcopy(page.project.times)
        frames = copy.deepcopy(page.project.frames)
        main_texts = copy.deepcopy(page.project.main_texts)
        tran_texts = copy.deepcopy(page.project.tran_texts)

        kwargs['register'] = None
        method(*args, **kwargs)
        path = page.project.get_temp_file_path(doc)
        time = page.project.times[row][0]

        page.project.times = times
        page.project.frames = frames
        page.project.main_texts = main_texts
        page.project.tran_texts = tran_texts

        self._run_preview(page, time, doc, path)
