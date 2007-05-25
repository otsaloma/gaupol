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


import gobject
import gtk
import linecache
import os
import pango
import platform
import sys
import traceback

from gaupol import urls, __version__
from gaupol.gtk import conf, util
from gaupol.i18n import _
from .glade import GladeDialog
from .message import ErrorDialog


class DebugDialog(GladeDialog):

    """Dialog for displaying a traceback in case of an unhandled exception.

    Instance variables:
     * _code_lines: List of lines of code displayed in the traceback
    """

    def __init__(self):

        GladeDialog.__init__(self, "debug-dialog")
        self._text_view = self._glade_xml.get_widget("text_view")
        self._code_lines = []

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
        text_buffer.create_tag("indent", left_margin=24)
        text_buffer.create_tag("monospace", family="monospace")

    def _insert_link(self, path, lineno, *tags):
        """Insert path into the text view."""

        text_buffer = self._text_view.get_buffer()
        tag = text_buffer.create_tag(None, foreground="blue")
        tag.props.underline = pango.UNDERLINE_SINGLE
        tag.connect("event", self._on_text_view_link_tag_event)
        path = os.path.abspath(path)
        tag.set_data("path", path)
        tag.set_data("lineno", lineno)
        if path.startswith(os.getcwd()):
            path = path.replace(os.getcwd(), "")
        if path.startswith(os.sep):
            path = path.replace(os.sep, "", 1)
        itr = text_buffer.get_end_iter()
        tag_table = text_buffer.get_tag_table()
        tags = tuple(tag_table.lookup(x) for x in tags)
        text_buffer.insert_with_tags(itr, path, tag, *tags)

    def _insert_text(self, text, *tags):
        """Insert text with tags to the text view."""

        text_buffer = self._text_view.get_buffer()
        itr = text_buffer.get_end_iter()
        text_buffer.insert_with_tags_by_name(itr, text, *tags)

    @util.asserted_return
    def _on_response(self, dialog, response):
        """Do not send response if reporting bug."""

        assert response == gtk.RESPONSE_YES
        util.browse_url(urls.BUG_REPORT)
        self.stop_emission("response")

    @util.asserted_return
    def _on_text_view_link_tag_event(self, tag, text_view, event, itr):
        """Open linked file in editor."""

        assert event.type == gtk.gdk.BUTTON_RELEASE
        assert event.button == 1
        text_buffer = self._text_view.get_buffer()
        assert not text_buffer.get_selection_bounds()
        self._open_link(tag)

    def _on_text_view_motion_notify_event(self, text_view, event):
        """Change mouse pointer when hovering over a link."""

        x = int(event.x)
        y = int(event.y)
        window = gtk.TEXT_WINDOW_WIDGET
        x, y = text_view.window_to_buffer_coords(window, x, y)
        window = text_view.get_window(gtk.TEXT_WINDOW_TEXT)
        for tag in text_view.get_iter_at_location(x, y).get_tags():
            if tag.get_data("path") is not None:
                window.set_cursor(util.HAND_CURSOR)
                return text_view.window.get_pointer()
        window.set_cursor(util.INSERT_CURSOR)
        text_view.window.get_pointer()

    def _open_link(self, tag):
        """Open linked file in editor."""

        @util.asserted_return
        def on_editor_exit(pid, return_value):
            assert return_value != 0
            self._show_editor_error_dialog()
        path = util.shell_quote(tag.get_data("path"))
        process = util.start_process("%s %s +%d" % (
            conf.debug.editor, path, tag.get_data("lineno")))
        gobject.child_watch_add(process.pid, on_editor_exit)
        tag.props.foreground = "purple"

    def _print_platform(self):
        """Print platform information."""

        self._insert_text("System: %s\n" % platform.system())
        desktop = util.get_desktop_environment() or "???"
        self._insert_text("Desktop environment: %s\n\n" % desktop)

    def _print_traceback(self, exctype, value, tb, limit=100):
        """Print up to limit stack trace entries from traceback."""

        depth = 0
        while (tb is not None) and (depth < limit):
            frame = tb.tb_frame
            code = frame.f_code
            self._insert_text("File: ")
            self._insert_link(code.co_filename, tb.tb_lineno)
            self._insert_text("\n")
            self._insert_text("Line: %s\n" % str(tb.tb_lineno))
            self._insert_text("In: %s\n\n" % code.co_name)
            line = linecache.getline(code.co_filename, tb.tb_lineno).strip()
            self._insert_text(line + "\n\n", "monospace", "indent")
            self._code_lines.append(line)
            tb = tb.tb_next
            depth += 1

        exception = traceback.format_exception_only(exctype, value)[0]
        exception, space, message = exception.partition(" ")
        self._insert_text(exception, "bold")
        self._insert_text("%s%s\n" % (space, message))

    def _print_versions(self):
        """Print version numbers of dependencies."""

        self._insert_text("Gaupol: %s\n" % __version__)
        self._insert_text("Python: %d.%d.%d\n" % sys.version_info[:3])
        self._insert_text("GTK: %d.%d.%d\n" % gtk.gtk_version)
        self._insert_text("PyGTK: %d.%d.%d\n" % gtk.pygtk_version)
        version = util.get_enchant_version() or "N/A"
        self._insert_text("PyEnchant: %s\n" % version)
        version = util.get_chardet_version() or "N/A"
        self._insert_text("Universal Encoding Detector: %s\n" % version)

    def _resize(self):
        """Resize dialog based on the text view's content."""

        text_width, height = util.get_text_view_size(self._text_view)
        label = gtk.Label("\n".join(self._code_lines))
        util.set_label_font(label, "monospace")
        code_width = label.size_request()[0]
        width = max(text_width, code_width) + 150 + util.EXTRA
        height = height + 160 + util.EXTRA
        util.resize_message_dialog(self, width, height)

    def _show_editor_error_dialog(self):
        """Show an error dialog after failing to open editor."""

        title = _('Failed to open editor "%s"') % conf.debug.editor
        message = _('To change the editor, edit option "editor" under ' \
            'section "debug" in configuration file "%s".') % conf.config_file
        dialog = ErrorDialog(self._dialog, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def set_text(self, exctype, value, tb):
        """Set text to the text view."""

        self._insert_text("Traceback", "large", "bold")
        self._insert_text("\n\n")
        self._print_traceback(exctype, value, tb)
        self._insert_text("Platform", "large", "bold")
        self._insert_text("\n\n")
        self._print_platform()
        self._insert_text("Versions", "large", "bold")
        self._insert_text("\n\n")
        self._print_versions()
        self._resize()


@util.asserted_return
def show(exctype, value, tb):
    """Show exception traceback in dialog."""

    traceback.print_exception(exctype, value, tb)
    assert isinstance(value, Exception)
    try:
        dialog = DebugDialog()
        dialog.set_text(exctype, value, tb)
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_NO:
            raise SystemExit(1)
    except Exception:
        traceback.print_exc()
