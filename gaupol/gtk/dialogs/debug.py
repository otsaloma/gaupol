# Copyright (C) 2005-2008 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Dialog for displaying a traceback in case of an unhandled exception."""

# This file has been adapted from Gazpacho with copyright notice
# Copyright (C) 2005 by Async Open Source and Sicem S.L.

import gaupol.gtk
import gobject
import gtk
import linecache
import os
import pango
import platform
import sys
import traceback
_ = gaupol.i18n._

__all__ = ("DebugDialog",)


class DebugDialog(gaupol.gtk.GladeDialog):

    """Dialog for displaying a traceback in case of an unhandled exception."""

    def __init__(self):
        """Initialize a DebugDialog object."""

        gaupol.gtk.GladeDialog.__init__(self, "debug.glade")
        get_widget = self._glade_xml.get_widget
        self._message_label = get_widget("message_label")
        self._text_view = get_widget("text_view")
        self._code_lines = []

        self._init_text_tags()
        self._init_signal_handlers()
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, self, "response")
        gaupol.util.connect(self, "_text_view", "motion-notify-event")

    def _init_text_tags(self):
        """Initialize tags for the text buffer."""

        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag("bold", weight=pango.WEIGHT_BOLD)
        text_buffer.create_tag("large", scale=pango.SCALE_LARGE)
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

    def _on_response(self, dialog, response):
        """Do not send response if reporting bug."""

        if response != gtk.RESPONSE_YES: return
        gaupol.util.browse_url(gaupol.BUG_REPORT_URL)
        self.stop_emission("response")

    def _on_text_view_link_tag_event(self, tag, text_view, event, itr):
        """Open linked file in editor."""

        if event.type != gtk.gdk.BUTTON_RELEASE: return
        if event.button != 1: return
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
                window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
                return text_view.window.get_pointer()
        window.set_cursor(gtk.gdk.Cursor(gtk.gdk.XTERM))
        text_view.window.get_pointer()

    def _open_link(self, tag):
        """Open linked file in editor."""

        def on_editor_exit(pid, return_value, self):
            if return_value == 0: return
            self._show_editor_error_dialog()
        path = gaupol.util.shell_quote(tag.get_data("path"))
        process = gaupol.util.start_process("%s %s +%d" % (
            gaupol.gtk.conf.debug.editor, path, tag.get_data("lineno")))
        gobject.child_watch_add(process.pid, on_editor_exit, self)
        tag.props.foreground = "purple"

    def _print_platform(self):
        """Print platform information."""

        self._insert_text("%s\n\n" % platform.platform(True))

    def _print_traceback(self, exctype, value, tb, limit=100):
        """Print up to limit stack trace entries from traceback."""

        depth = 0
        indent = "    "
        while (tb is not None) and (depth < limit):
            frame = tb.tb_frame
            code = frame.f_code
            self._insert_text("File: ")
            self._insert_link(code.co_filename, tb.tb_lineno)
            self._insert_text("\n")
            self._insert_text("Line: %s\n" % str(tb.tb_lineno))
            self._insert_text("In: %s\n\n" % code.co_name)
            line = linecache.getline(code.co_filename, tb.tb_lineno).strip()
            self._insert_text("%s%s\n\n" % (indent, line), "monospace")
            self._code_lines.append("%s%s" % (indent, line))
            tb = tb.tb_next
            depth += 1

        exception = traceback.format_exception_only(exctype, value)[0]
        exception, space, message = exception.partition(" ")
        self._insert_text(exception, "bold")
        self._insert_text("%s%s\n" % (space, message))

    def _print_versions(self):
        """Print version numbers of dependencies."""

        self._insert_text("Gaupol: %s\n" % gaupol.__version__)
        self._insert_text("Python: %d.%d.%d\n" % sys.version_info[:3])
        self._insert_text("GTK+: %d.%d.%d\n" % gtk.gtk_version)
        self._insert_text("PyGTK: %d.%d.%d\n" % gtk.pygtk_version)
        version = gaupol.util.get_enchant_version() or "N/A"
        self._insert_text("PyEnchant: %s\n" % version)
        version = gaupol.util.get_chardet_version() or "N/A"
        self._insert_text("Universal Encoding Detector: %s\n" % version)

    def _resize(self):
        """Resize dialog based on the text view's content."""

        get_size = gaupol.gtk.util.get_text_view_size
        text_width, height = get_size(self._text_view)
        label = gtk.Label("\n".join(self._code_lines))
        gaupol.gtk.util.set_label_font(label, "monospace")
        code_width = label.size_request()[0]
        width = max(text_width, code_width) + 150 + gaupol.gtk.EXTRA
        height = height + 160 + gaupol.gtk.EXTRA
        gaupol.gtk.util.resize_message_dialog(self, width, height)
        self._message_label.set_size_request(width - 150, -1)

    def _show_editor_error_dialog(self):
        """Show an error dialog after failing to open editor."""

        editor = gaupol.gtk.conf.debug.editor
        title = _('Failed to open editor "%s"') % editor
        config_file = gaupol.gtk.conf.config_file
        message = _(('To change the editor, edit option "editor" under '
            'section "debug" in configuration file "%s".')) % config_file
        dialog = gaupol.gtk.ErrorDialog(self._dialog, title, message)
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


def show(exctype, value, tb):
    """Show exception traceback in dialog."""

    traceback.print_exception(exctype, value, tb)
    if not isinstance(value, Exception): return
    try: # Avoid recursion.
        dialog = DebugDialog()
        dialog.set_text(exctype, value, tb)
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_NO:
            raise SystemExit(1)
    except Exception:
        traceback.print_exc()
