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


"""Dialog for displaying a traceback in case of an unhandled exception."""

# This file has been adapted from Gazpacho with copyright notice
# Copyright (C) 2005 by Async Open Source and Sicem S.L.


import linecache
import os
import platform
import sys
import traceback
from gettext import gettext as _

import gobject
import gtk
import pango

from gaupol import urls, __version__
from gaupol.gtk import conf, util
from .glade import GladeDialog
from .message import ErrorDialog


class DebugDialog(GladeDialog):

    """Dialog for displaying a traceback in case of an unhandled exception.

    Instance variables:

        _code_lines: List of lines of code displayed
        _text_view:  gtk.TextView displaying the traceback
    """

    def __init__(self):

        GladeDialog.__init__(self, "debug-dialog")

        self._code_lines = []
        self._text_view  = self._glade_xml.get_widget("text_view")

        self._init_text_tags()
        self._init_signal_handlers()
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, self, "response")
        util.connect(self, "_text_view", "motion-notify-event")

    def _init_text_tags(self):
        """Initialize tags for the text buffer."""

        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag("bold", weight=pango.WEIGHT_BOLD)
        text_buffer.create_tag("large", scale=pango.SCALE_LARGE)
        text_buffer.create_tag("margin_12", left_margin=12)
        text_buffer.create_tag("margin_24", left_margin=24)
        text_buffer.create_tag("monospace", family="monospace")

    def _insert_link(self, path, lineno, *tags):
        """Insert path into the text view."""

        text_buffer = self._text_view.get_buffer()
        tag = text_buffer.create_tag(None, foreground="blue")
        tag.props.underline = pango.UNDERLINE_SINGLE
        tag.connect("event", self._on_text_view_link_tag_event)
        path = os.path.abspath(path)
        if path.startswith(os.getcwd()):
            path = path.replace(os.getcwd(), "")[len(os.sep):]
        tag.set_data("path", os.path.abspath(path))
        tag.set_data("lineno", lineno)
        end_iter = text_buffer.get_end_iter()
        tag_table = text_buffer.get_tag_table()
        tags = tuple(tag_table.lookup(x) for x in tags)
        text_buffer.insert_with_tags(end_iter, path, tag, *tags)

    def _insert_text(self, text, *tags):
        """Insert text with tags to the text view."""

        text_buffer = self._text_view.get_buffer()
        end_iter = text_buffer.get_end_iter()
        text_buffer.insert_with_tags_by_name(end_iter, text, *tags)

    def _on_response(self, dialog, response):
        """Do not send response if reporting bug."""

        if response == gtk.RESPONSE_YES:
            util.browse_url(urls.BUG_REPORT)
            self.stop_emission("response")

    def _on_text_view_link_tag_event(self, tag, text_view, event, itr):
        """Open linked file in editor."""

        if event.type == gtk.gdk.BUTTON_RELEASE and event.button == 1:
            text_buffer = self._text_view.get_buffer()
            if not text_buffer.get_selection_bounds():
                self._open_link(tag)

    def _on_text_view_motion_notify_event(self, text_view, event):
        """Change mouse pointer when hovering over a link."""

        window = gtk.TEXT_WINDOW_WIDGET
        x = int(event.x)
        y = int(event.y)
        x, y = text_view.window_to_buffer_coords(window, x, y)
        window = text_view.get_window(gtk.TEXT_WINDOW_TEXT)
        for tag in text_view.get_iter_at_location(x, y).get_tags():
            if tag.get_data("path") is not None:
                window.set_cursor(util.HAND_CURSOR)
                text_view.window.get_pointer()
                return
        window.set_cursor(util.INSERT_CURSOR)
        text_view.window.get_pointer()

    def _open_link(self, tag):
        """Open linked file in editor."""

        def on_editor_exit(pid, return_value):
            if return_value != 0:
                self._show_editor_error_dialog()
        path = util.shell_quote_path(tag.get_data("path"))
        process = util.start_process("%s %s +%d" % (
            conf.debug.editor, path, tag.get_data("lineno")))
        gobject.child_watch_add(process.pid, on_editor_exit)
        tag.props.foreground = "purple"

    def _print_platform(self):
        """Print platform information."""

        def insert_text(text, *tags):
            self._insert_text(text, "margin_12", *tags)
        insert_text("System: ", "bold")
        insert_text(platform.system())
        insert_text("\n")
        insert_text("Desktop environment: ", "bold")
        insert_text(util.get_desktop_environment() or "?")
        insert_text("\n")

    def _print_traceback(self, exctype, value, tb, limit=None):
        """Print up to limit stack trace entries from traceback."""

        def insert_text(text, *tags):
            self._insert_text(text, "margin_12", *tags)

        i = 0
        while tb is not None and (limit is None or i < limit):
            frame = tb.tb_frame
            lineno = tb.tb_lineno
            code = frame.f_code
            filename = code.co_filename
            name = code.co_name
            insert_text("File: ", "bold")
            self._insert_link(filename, lineno)
            insert_text("\n")
            insert_text("Line: ", "bold")
            insert_text(str(lineno))
            insert_text("\n")
            insert_text("In: ", "bold")
            insert_text(name)
            insert_text("\n")
            line = linecache.getline(filename, lineno).strip()
            if line:
                self._code_lines.append(line)
                insert_text("\n%s\n\n" % line, "monospace", "margin_24")
            tb = tb.tb_next
            i += 1

        exception = traceback.format_exception_only(exctype, value)[0]
        message = ""
        if exception.count(" "):
            exception, message = exception.split(" ", 1)
        insert_text(exception + " ", "bold")
        insert_text(message)
        insert_text("\n")

    def _print_versions(self):
        """Print version information."""

        def insert_text(text, *tags):
            self._insert_text(text, "margin_12", *tags)
        insert_text("Gaupol: ", "bold")
        insert_text(__version__)
        insert_text("\n")
        insert_text("Python: ", "bold")
        insert_text("%d.%d.%d" % sys.version_info[:3])
        insert_text("\n")
        insert_text("GTK: ", "bold")
        insert_text("%d.%d.%d" % gtk.gtk_version)
        insert_text("\n")
        insert_text("PyGTK: ", "bold")
        insert_text("%d.%d.%d" % gtk.pygtk_version)
        insert_text("\n")
        insert_text("PyEnchant: ", "bold")
        insert_text(util.get_enchant_version() or "N/A")
        insert_text("\n")
        insert_text("Universal Encoding Detector: ", "bold")
        insert_text(util.get_chardet_version() or "N/A")
        insert_text("\n")

    def _resize(self):
        """Resize dialog based on the text view's content."""

        # Get required width and height to display text.
        text_buffer = self._text_view.get_buffer()
        bounds = text_buffer.get_bounds()
        text = text_buffer.get_text(*bounds)
        label = gtk.Label(text)
        text_width, height = label.size_request()

        # Get required width to display code.
        attrs = pango.AttrList()
        attrs.insert(pango.AttrFamily("monospace", 0, -1))
        label.set_attributes(attrs)
        label.set_text("\n".join(self._code_lines))
        code_width = label.size_request()[0]

        # Set dialog size.
        width = max(text_width, code_width) + 150 + util.EXTRA
        height = height + 160 + util.EXTRA
        util.resize_message_dialog(self, width, height)

    def _show_editor_error_dialog(self):
        """Show an error dialog after failing to open editor."""

        title = _('Failed to open editor "%s"') % conf.debug.editor
        message = _('To change the editor, edit option "editor" under ' \
            'section "debug" in configuration file "%s".') % conf.CONFIG_FILE
        dialog = ErrorDialog(self._dialog, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def set_text(self, exctype, value, tb):
        """Set text to the text view."""

        self._insert_text("Traceback", "large", "bold")
        self._insert_text("\n\n")
        self._print_traceback(exctype, value, tb, 100)
        self._insert_text("Platform", "large", "bold")
        self._insert_text("\n\n")
        self._print_platform()
        self._insert_text("\n")
        self._insert_text("Versions", "large", "bold")
        self._insert_text("\n\n")
        self._print_versions()

        self._resize()


def show(exctype, value, tb):
    """Show exception traceback in dialog.

    This function is usable as sys.excepthook.
    """
    traceback.print_exception(exctype, value, tb)
    if not isinstance(value, Exception):
        return
    try:
        dialog = DebugDialog()
        dialog.set_text(exctype, value, tb)
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_NO:
            try:
                gtk.main_quit()
            except RuntimeError:
                raise SystemExit(1)
    except Exception:
        traceback.print_exc()
