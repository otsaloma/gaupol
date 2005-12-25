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


"""Debug dialog."""

# This file has been adpated from Gazpacho's debugwindow.py by Lorenzo Gil
# Sanchez and Johan Dahlin.


try:
    from psyco.classes import *
except ImportError:
    pass

import linecache
import os
import sys
import traceback

import gtk
import pango

from gaupol.base.util          import wwwlib
from gaupol.gtk.delegates.help import BUG_REPORT_URL
from gaupol.gtk.util           import gui


class DebugDialog(object):

    """Debug dialog."""

    def __init__(self):

        glade_xml = gui.get_glade_xml('debug-dialog.glade')
        self._dialog = glade_xml.get_widget('dialog')
        self._text_view = glade_xml.get_widget('text_view')
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

        # Create text tags for text view.
        tag = self._text_view.get_buffer().create_tag
        tag('header', weight=pango.WEIGHT_BOLD, scale=pango.SCALE_LARGE)
        tag('title' , weight=pango.WEIGHT_BOLD, left_margin=12)
        tag('text'  , left_margin=12)
        tag('code'  , family='monospace', left_margin=24)

        self._pwd = os.getcwd()

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def _insert_text(self, text, *tags):
        """Insert text to text view."""

        text_buffer = self._text_view.get_buffer()
        end_iter = text_buffer.get_end_iter()
        text_buffer.insert_with_tags_by_name(end_iter, text, *tags)

    def _print_file(self, filename, lineno, name):
        """Print a single file traceback text view."""

        if filename.startswith(self._pwd):
            filename = filename.replace(self._pwd, '')[1:]

        self._insert_text('File: '   , 'title')
        self._insert_text(filename   , 'text' )
        self._insert_text('\n'       , 'text' )
        self._insert_text('Line: '   , 'title')
        self._insert_text(str(lineno), 'text' )
        self._insert_text('\n'       , 'text' )
        self._insert_text('In: '     , 'title')
        self._insert_text(name       , 'text' )
        self._insert_text('\n'       , 'text' )

    def _print_system_information(self):
        """Print system information."""

        # Operating system
        self._insert_text('Operating system: ', 'title')
        self._insert_text(sys.platform, 'text')
        self._insert_text('\n', 'text')

        # Desktop environment
        self._insert_text('Desktop environment: ', 'title')
        if os.getenv('GNOME_DESKTOP_SESSION_ID') is not None:
            self._insert_text('GNOME', 'text')
        else:
            self._insert_text('Not GNOME', 'text')
        self._insert_text('\n', 'text')

        # Python
        self._insert_text('Python version: ', 'title')
        self._insert_text(sys.version, 'text')
        self._insert_text('\n', 'text')

        # PyGTK
        self._insert_text('PyGTK version: ', 'title')
        self._insert_text('%d.%d.%d' % gtk.pygtk_version, 'text')
        self._insert_text('\n', 'text')

        # PyEnchant
        self._insert_text('PyEnchant version: ', 'title')
        try:
            import enchant
            self._insert_text(enchant.__version__, 'text')
        except (ImportError, enchant.Error):
            self._insert_text('Not found', 'text')
        self._insert_text('\n', 'text')

    def _print_traceback(self, tb, limit=None):
        """Print up to limit stack trace entries from the traceback "tb"."""

        if limit is None:
            if hasattr(sys, 'tracebacklimit'):
                limit = sys.tracebacklimit
        n = 0
        while tb is not None and (limit is None or n < limit):

            frame    = tb.tb_frame
            lineno   = tb.tb_lineno
            code     = frame.f_code
            filename = code.co_filename
            name     = code.co_name

            self._print_file(filename, lineno, name)
            line = linecache.getline(filename, lineno)
            line = line.lstrip()
            if line:
                self._insert_text('\n', 'code')
                self._insert_text(line, 'code')
                self._insert_text('\n', 'code')

            tb = tb.tb_next
            n += 1

    def run(self):
        """Show and run the dialog."""

        self._dialog.show()
        return self._dialog.run()

    def set_text(self, exctype, value, tb):
        """Set text to traceback text view."""

        # Traceback entries
        self._insert_text('Traceback', 'header')
        self._insert_text('\n\n', 'header')
        self._print_traceback(tb)

        # Exception
        exception = traceback.format_exception_only(exctype, value)[0]
        self._insert_text(exception, 'title')
        self._insert_text('\n', 'title')

        # System information
        self._insert_text('System Information', 'header')
        self._insert_text('\n\n', 'header')
        self._print_system_information()

        # Get required width and height to display text.
        text_buffer = self._text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        text = text_buffer.get_text(start, end, True)
        label = gtk.Label(text)
        width, height = label.size_request()

        width  = min(500, width  + 48)
        height = min(400, height + 48)
        self._text_view.set_size_request(width, height)


def show(exctype, value, tb):
    """Show exception in dialog."""

    # Output to terminal as well.
    traceback.print_tb(tb)

    if exctype is KeyboardInterrupt:
        return

    dialog = DebugDialog()
    dialog.set_text(exctype, value, tb)

    # Leave the dialog open if user clicked to report the bug.
    while True:
        response = dialog.run()
        if response == gtk.RESPONSE_YES:
            wwwlib.open_url(BUG_REPORT_URL)
        else:
            break

    dialog.destroy()
