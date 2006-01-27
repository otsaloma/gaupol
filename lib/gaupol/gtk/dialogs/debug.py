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
# Sanchez and Johan Dahlin. URLs in text view has been adapted from Porthole's
# summary.py by Fredrik Arnerup, Daniel G. Taylor, Brian Dolbec and
# Wm. F. Wheeler.


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _
import linecache
import os
import sys
import traceback

import gtk
import pango

from gaupol.base.util           import wwwlib
from gaupol.gtk.delegates.help  import BUG_REPORT_URL
from gaupol.gtk.dialogs.message import ErrorDialog
from gaupol.gtk.util            import config, gtklib


normal_cursor = gtk.gdk.Cursor(gtk.gdk.XTERM)
hand_cursor   = gtk.gdk.Cursor(gtk.gdk.HAND2)


class OpenEditorErrorDialog(ErrorDialog):

    """Dialog to inform that editor was not successfully opened."""

    def __init__(self, parent, editor):

        title   = _('Failed to open editor "%s"') % editor
        message = _('Currently only "gvim" and "emacs" editors are supported. '
                    'If you don\'t like this, file a bug report. To change '
                    'the editor, edit file "%s" under section "general".') \
                    % config.CONFIG_PATH

        ErrorDialog.__init__(self, parent, title, message)


class DebugDialog(object):

    """Debug dialog."""

    def __init__(self):

        glade_xml = gtklib.get_glade_xml('debug-dialog.glade')
        self._dialog    = glade_xml.get_widget('dialog')
        self._text_view = glade_xml.get_widget('text_view')

        # Text tags for URLs. Names of the tags are integers corresponding to
        # indexes in self._files.
        self._url_tags = []

        # Tuples of filepaths and line numbers
        self._files = []

        # Lines of code displayed.
        self._code_lines = []

        # Current working directory
        self._pwd = os.getcwd()

        self._init_signals()
        self._init_text_tags()
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _init_signals(self):
        """Initialize signals."""

        # Follow the mouse pointer.
        method = self._on_text_view_motion_notify_event
        self._text_view.connect('motion-notify-event', method)

    def _init_text_tags(self):
        """Initialize text tags."""

        BOLD  = pango.WEIGHT_BOLD
        LARGE = pango.SCALE_LARGE

        text_buffer = self._text_view.get_buffer()
        create_tag  = text_buffer.create_tag

        create_tag('header', weight=BOLD, scale=LARGE)
        create_tag('title', weight=BOLD, left_margin=12)
        create_tag('text', left_margin=12)
        create_tag('code', family='monospace', left_margin=24)

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def _insert_text(self, text, *tags):
        """Insert text to text view."""

        text_buffer = self._text_view.get_buffer()
        end_iter = text_buffer.get_end_iter()
        text_buffer.insert_with_tags_by_name(end_iter, text, *tags)

    def _insert_url(self, url, lineno):
        """Insert url into text view."""

        # Create a new tag for URL.
        text_buffer = self._text_view.get_buffer()
        name = str(len(self._files))
        tag = text_buffer.create_tag(name, foreground='blue')
        tag.connect('event', self._on_url_event)

        # Append URL to lists of tags and files.
        self._url_tags.append(tag)
        self._files.append((url, lineno))

        # Shorten URL for display.
        text = url
        if url.startswith(self._pwd):
            text = url.replace(self._pwd, '')[1:]
        self._insert_text(text, name)

    def _on_text_view_motion_notify_event(self, widget, event):
        """Set GUI properties when mouse moves over URL."""

        window_type = gtk.TEXT_WINDOW_TEXT

        # Get a list of text tags at mouse position.
        x, y = self._text_view.get_pointer()
        x, y = self._text_view.window_to_buffer_coords(window_type, x, y)
        tags = self._text_view.get_iter_at_location(x, y).get_tags()

        # Underline current URL.
        for tag in self._url_tags:
            if tag in tags:
                tag.props.underline = pango.UNDERLINE_SINGLE
            else:
                tag.props.underline = pango.UNDERLINE_NONE

        # Show hand cursor over URL.
        window = self._text_view.get_window(window_type)
        for tag in tags:
            if tag in self._url_tags:
                window.set_cursor(hand_cursor)
                return

        window.set_cursor(normal_cursor)

    def _on_url_event(self, tag, widget, event, itr):
        """Open URL in editor."""

        if not event.type == gtk.gdk.BUTTON_RELEASE:
            return

        path, lineno = self._files[int(tag.props.name)]

        editor = config.general.editor
        if editor in ('gvim', 'emacs'):
            retval = os.system('%s +%d "%s"' % (editor, lineno, path))
            if retval == 0:
                return

        dialog = OpenEditorErrorDialog(self._dialog, editor)
        dialog.run()
        dialog.destroy()

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
        self._insert_text('%d.%d.%d' % sys.version_info[:3], 'text')
        self._insert_text('\n', 'text')

        # GTK
        self._insert_text('GTK version: ', 'title')
        self._insert_text('%d.%d.%d' % gtk.gtk_version, 'text')
        self._insert_text('\n', 'text')

        # PyGTK
        self._insert_text('PyGTK version: ', 'title')
        self._insert_text('%d.%d.%d' % gtk.pygtk_version, 'text')
        self._insert_text('\n', 'text')

        # Psyco. Hex.
        self._insert_text('Psyco version: ', 'title')
        try:
            import psyco
            self._insert_text('%x' % psyco.__version__, 'text')
        except ImportError:
            self._insert_text('Not found', 'text')
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
        """Print up to limit stack trace entries from the traceback."""

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

            # Insert file information.
            self._insert_text('File: '   , 'title')
            self._insert_url(filename, lineno)
            self._insert_text('\n'       , 'text' )
            self._insert_text('Line: '   , 'title')
            self._insert_text(str(lineno), 'text' )
            self._insert_text('\n'       , 'text' )
            self._insert_text('In: '     , 'title')
            self._insert_text(name       , 'text' )
            self._insert_text('\n'       , 'text' )

            # Insert one line of code.
            line = linecache.getline(filename, lineno)
            line = line.lstrip()
            if line:
                self._code_lines.append(line.strip())
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
        try:
            exception, message = exception.split(' ', 1)
            self._insert_text(exception, 'title')
            self._insert_text(' %s' % message, 'text')
        except ValueError:
            self._insert_text(exception, 'title')
        self._insert_text('\n', 'text')

        # System information
        self._insert_text('System Information', 'header')
        self._insert_text('\n\n', 'header')
        self._print_system_information()

        # Get required width and height to display text.
        text_buffer = self._text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        text = text_buffer.get_text(start, end, True)
        label = gtk.Label(text)
        text_width, height = label.size_request()

        # Get required width to display code.
        attrs = pango.AttrList()
        attrs.insert(pango.AttrFamily('monospace', 0, -1))
        label.set_attributes(attrs)
        label.set_text('\n'.join(self._code_lines))
        code_width = label.size_request()[0]

        # Set dialog size.
        width = max(text_width, code_width) + 150
        height += 160
        gtklib.resize_message_dialog(self._dialog, width, height)


def show(exctype, value, tb):
    """Show exception in dialog."""

    # Output to terminal as well.
    traceback.print_exception(exctype, value, tb)

    if exctype is KeyboardInterrupt:
        return

    # Wrap all of this debug-dialoging in a try-except wrapper to avoid
    # spawning a new debug dialog if this raises an exception.
    try:
        dialog = DebugDialog()
        dialog.set_text(exctype, value, tb)

        # Leave the dialog open if user clicked to report the bug.
        while True:
            response = dialog.run()
            if response == gtk.RESPONSE_YES:
                wwwlib.open_url(BUG_REPORT_URL)
            elif response == gtk.RESPONSE_NO:
                dialog.destroy()
                try:
                    gtk.main_quit()
                except RuntimeError:
                    raise SystemExit(1)
                return
            else:
                break

        dialog.destroy()

    except Exception:
        traceback.print_exc()


if __name__ == '__main__':

    from gaupol.test import Test

    class TestOpenEditorErrorDialog(Test):

        def test_init(self):

            OpenEditorErrorDialog(gtk.Window(), 'foo')

    class TestDebugDialog(Test):

        def test_all(self):

            dialog = DebugDialog()
            try:
                raise IOError('testing')
            except IOError:
                dialog.set_text(*sys.exc_info())
            dialog.run()
            dialog.destroy()

    TestOpenEditorErrorDialog().run()
    TestDebugDialog().run()
