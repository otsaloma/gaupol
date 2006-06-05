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


"""Debug dialog."""


# This file has been adpated from Gazpacho's debugwindow.py by Lorenzo Gil
# Sanchez and Johan Dahlin. URLs in text view has been adapted from Porthole's
# summary.py by Fredrik Arnerup, Daniel G. Taylor, Brian Dolbec and
# Wm. F. Wheeler.


from gettext import gettext as _
import linecache
import os
import sys
import traceback

import gtk
import pango

from gaupol.base.util          import wwwlib
from gaupol.gtk.delegate.help  import BUG_REPORT_URL
from gaupol.gtk.dialog.message import ErrorDialog
from gaupol.gtk.util           import config, gtklib


CURSOR_NORMAL = gtk.gdk.Cursor(gtk.gdk.XTERM)
CURSOR_HAND   = gtk.gdk.Cursor(gtk.gdk.HAND2)


class EditorErrorDialog(ErrorDialog):

    """Dialog to inform that editor was not successfully opened."""

    def __init__(self, parent, editor):

        title   = _('Failed to open editor "%s"') % editor
        message = _('To change the editor, edit configuration file "%s" under '
                    'section "debug".') % config.CONFIG_FILE
        ErrorDialog.__init__(self, parent, title, message)


class DebugDialog(object):

    """Debug dialog."""

    def __init__(self):

        glade_xml = gtklib.get_glade_xml('debug-dialog')
        self._dialog    = glade_xml.get_widget('dialog')
        self._text_view = glade_xml.get_widget('text_view')

        self._url_tags   = []
        self._files      = []
        self._code_lines = []

        self._init_signals()
        self._init_text_tags()
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _init_signals(self):
        """Initialize signals."""

        self._text_view.connect(
            'motion-notify-event', self._on_text_view_motion_notify_event)

    def _init_text_tags(self):
        """Initialize text tags."""

        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag(
            'header',
            weight=pango.WEIGHT_BOLD,
            scale=pango.SCALE_LARGE
        )
        text_buffer.create_tag(
            'title',
            weight=pango.WEIGHT_BOLD,
            left_margin=12
        )
        text_buffer.create_tag(
            'text',
            left_margin=12
        )
        text_buffer.create_tag(
            'code',
            family='monospace',
            left_margin=24
        )

    def destroy(self):
        """Destroy dialog."""

        self._dialog.destroy()

    def _insert_text(self, text, *tags):
        """Insert text with tags to text view."""

        text_buffer = self._text_view.get_buffer()
        end_iter = text_buffer.get_end_iter()
        text_buffer.insert_with_tags_by_name(end_iter, text, *tags)

    def _insert_url(self, url, lineno):
        """Insert url into text view."""

        text_buffer = self._text_view.get_buffer()
        name = str(len(self._files))
        tag = text_buffer.create_tag(name, foreground='blue')
        tag.connect('event', self._on_url_event)
        self._url_tags.append(tag)
        self._files.append((url, lineno))

        if url.startswith(os.getcwd()):
            url = url.replace(os.getcwd(), '')[len(os.sep):]
        self._insert_text(url, name)

    def _on_text_view_motion_notify_event(self, widget, event):
        """Change mouse pointer when hovering over an URL."""

        window_type = gtk.TEXT_WINDOW_TEXT
        x, y = self._text_view.get_pointer()
        x, y = self._text_view.window_to_buffer_coords(window_type, x, y)
        tags = self._text_view.get_iter_at_location(x, y).get_tags()

        for url_tag in self._url_tags:
            if url_tag in tags:
                url_tag.props.underline = pango.UNDERLINE_SINGLE
            else:
                url_tag.props.underline = pango.UNDERLINE_NONE

        window = self._text_view.get_window(window_type)
        for tag in tags:
            if tag in self._url_tags:
                window.set_cursor(CURSOR_HAND)
                return
        window.set_cursor(CURSOR_NORMAL)

    def _on_url_event(self, tag, widget, event, iter_):
        """Open URL in editor."""

        if not event.type == gtk.gdk.BUTTON_RELEASE:
            return

        editor = config.Debug.editor
        path, lineno = self._files[int(tag.props.name)]
        return_value = os.system('%s +%d "%s"' % (editor, lineno, path))
        if return_value != 0:
            dialog = EditorErrorDialog(self._dialog, editor)
            dialog.run()
            dialog.destroy()

    def _print_platform(self):
        """Print platform information."""

        self._insert_text('Operating system: ', 'title')
        self._insert_text(sys.platform + '\n', 'text')
        self._insert_text('Desktop environment: ', 'title')
        if os.getenv('GNOME_DESKTOP_SESSION_ID') is not None:
            self._insert_text('GNOME\n', 'text')
        elif os.getenv('KDE_FULL_SESSION') is not None:
            self._insert_text('KDE\n', 'text')
        else:
            self._insert_text('?\n', 'text')

    def _print_versions(self):
        """Print version information."""

        self._insert_text('Python: ', 'title')
        self._insert_text('%d.%d.%d\n' % sys.version_info[:3], 'text')
        self._insert_text('GTK: ', 'title')
        self._insert_text('%d.%d.%d\n' % gtk.gtk_version, 'text')
        self._insert_text('PyGTK: ', 'title')
        self._insert_text('%d.%d.%d\n' % gtk.pygtk_version, 'text')
        self._insert_text('PyEnchant: ', 'title')
        try:
            import enchant
            self._insert_text(enchant.__version__ + '\n', 'text')
        except ImportError:
            self._insert_text('-\n', 'text')
        except enchant.Error:
            self._insert_text('-\n', 'text')

    def _print_traceback(self, tb, limit=None):
        """Print up to limit stack trace entries from traceback."""

        n = 0
        while tb is not None and (limit is None or n < limit):

            frame    = tb.tb_frame
            lineno   = tb.tb_lineno
            code     = frame.f_code
            filename = code.co_filename
            name     = code.co_name

            self._insert_text('File: ', 'title')
            self._insert_url(filename, lineno)
            self._insert_text('\n', 'text')
            self._insert_text('Line: ', 'title')
            self._insert_text(str(lineno) + '\n', 'text')
            self._insert_text('In: ', 'title')
            self._insert_text(name + '\n', 'text')

            line = linecache.getline(code.co_filename, tb.tb_lineno).strip()
            if line:
                self._code_lines.append(line)
                self._insert_text('\n%s\n\n' % line, 'code')

            tb = tb.tb_next
            n += 1

    def run(self):
        """Show and run dialog."""

        self._dialog.show()
        return self._dialog.run()

    def set_text(self, exctype, value, tb):
        """Set text to text view."""

        self._insert_text('Traceback', 'header')
        self._insert_text('\n\n', 'text')
        self._print_traceback(tb)
        exception = traceback.format_exception_only(exctype, value)[0]
        try:
            exception, message = exception.split(' ', 1)
            self._insert_text(exception, 'title')
            self._insert_text(' %s\n' % message, 'text')
        except ValueError:
            self._insert_text(exception + '\n', 'title')

        self._insert_text('Platform', 'header')
        self._insert_text('\n\n', 'text')
        self._print_platform()
        self._insert_text('\n', 'text')
        self._insert_text('Versions', 'header')
        self._insert_text('\n\n', 'text')
        self._print_versions()

        # Get required width and height to display text.
        text_buffer = self._text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        text = text_buffer.get_text(start, end)
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

    # Always print to stdout and stderr.
    traceback.print_exception(exctype, value, tb)
    if exctype is KeyboardInterrupt:
        return

    # Avoid spawning a new dialog if this one raises an exception.
    try:
        dialog = DebugDialog()
        dialog.set_text(exctype, value, tb)
        while True:
            response = dialog.run()
            if response == gtk.RESPONSE_YES:
                wwwlib.browse_url(BUG_REPORT_URL)
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
