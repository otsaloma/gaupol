# Copyright (C) 2005-2008,2010-2011 Osmo Salomaa
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

# This file has been originally adapted from Gazpacho with copyright notice
# Copyright (C) 2005 by Async Open Source and Sicem S.L.

import aeidon
import gaupol
import glib
import gtk
import linecache
import os
import pango
import platform
import string
import sys
import traceback
_ = aeidon.i18n._

__all__ = ("DebugDialog",)


class DebugDialog(gaupol.BuilderDialog):

    """Dialog for displaying a traceback in case of an unhandled exception."""

    _widgets = ("message_label", "text_view")

    def __init__(self):
        """Initialize a :class:`DebugDialog` object."""
        gaupol.BuilderDialog.__init__(self, "debug-dialog.ui")
        self._init_text_tags()
        self._init_signal_handlers()
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""
        aeidon.util.connect(self, self, "response")
        aeidon.util.connect(self, "_text_view", "motion-notify-event")

    def _init_text_tags(self):
        """Initialize tags for the text buffer."""
        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag("bold", weight=pango.WEIGHT_BOLD)
        text_buffer.create_tag("large", scale=pango.SCALE_LARGE)
        text_buffer.create_tag("monospace", family="monospace")

    def _insert_environment(self):
        """Insert environment information."""
        map(self._insert_text,
            ("Platform: %s\n" % platform.platform(True),
             "Locale: %s\n" % aeidon.locales.get_system_code(),
             "\n"))

    def _insert_library_versions(self):
        """Insert version numbers of libraries."""
        map(self._insert_text,
            ("Python: %d.%d.%d\n" % sys.version_info[:3],
             "GTK+: %d.%d.%d\n" % gtk.gtk_version,
             "GStreamer: %s\n" % gaupol.util.get_gst_version(),
             "\n"))

    def _insert_link(self, path, lineno, *tags):
        """Insert `path` as a link into the text view."""
        text_buffer = self._text_view.get_buffer()
        tag = text_buffer.create_tag(None, foreground="blue")
        tag.props.underline = pango.UNDERLINE_SINGLE
        tag.connect("event", self._on_text_view_link_tag_event)
        path = os.path.abspath(path)
        tag.set_data("path", path)
        tag.set_data("lineno", lineno)
        if path.startswith(os.getcwd()):
            path = path.replace(os.getcwd(), "")
        while path.startswith(os.sep):
            path = path.replace(os.sep, "", 1)
        itr = text_buffer.get_end_iter()
        tag_table = text_buffer.get_tag_table()
        tags = map(tag_table.lookup, tags + ("monospace",))
        text_buffer.insert_with_tags(itr, path, tag, *tags)

    def _insert_python_package_versions(self):
        """Insert version numbers of Python packages."""
        map(self._insert_text,
            ("aeidon: %s\n" % aeidon.__version__,
             "gaupol: %s\n" % gaupol.__version__,
             "gtk: %d.%d.%d\n" % gtk.pygtk_version,
             "gst: %s\n" % gaupol.util.get_pygst_version(),
             "enchant: %s\n" % aeidon.util.get_enchant_version(),
             "chardet: %s\n" % aeidon.util.get_chardet_version(),
             ))

    def _insert_text(self, text, *tags):
        """Insert `text` with `tags` to the text view."""
        text_buffer = self._text_view.get_buffer()
        itr = text_buffer.get_end_iter()
        tags = tags + ("monospace",)
        text_buffer.insert_with_tags_by_name(itr, text, *tags)

    def _insert_title(self, text):
        """Insert `text` as a title to the text view."""
        self._insert_text(text, "large", "bold")
        self._insert_text("\n\n")

    def _insert_traceback(self, exctype, value, tb, limit=100):
        """Insert up to `limit` stack trace entries from `tb`."""
        for i in range(limit):
            if tb is None: break
            frame = tb.tb_frame
            code = frame.f_code
            line = linecache.getline(code.co_filename,
                                     tb.tb_lineno).strip()

            self._insert_text("File: ")
            self._insert_link(code.co_filename, tb.tb_lineno)
            self._insert_text("\n")
            self._insert_text("Line: %s\n" % str(tb.tb_lineno))
            self._insert_text("In: %s\n\n" % code.co_name)
            if line.strip():
                indent = "\302\240" * 4
                self._insert_text("%s%s\n\n" % (indent, line))
            tb = tb.tb_next
        exception = traceback.format_exception_only(exctype, value)[0]
        exception, space, message = exception.partition(" ")
        self._insert_text(exception, "bold")
        self._insert_text("%s%s\n" % (space, message))

    def _on_editor_exit(self, pid, return_value, command):
        """Print an error message if editor process failed."""
        if return_value == 0: return
        print ("Command '%s' failed with return value %d"
               % (command, return_value))

    def _on_response(self, dialog, response):
        """Do not send response if reporting bug."""
        if response != gtk.RESPONSE_YES: return
        gaupol.util.show_uri(gaupol.BUG_REPORT_URL)
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
        path = aeidon.util.shell_quote(tag.get_data("path"))
        command = string.Template(gaupol.conf.debug.text_editor)
        command = command.safe_substitute(LINENO=tag.get_data("lineno"),
                                          FILE=path)

        process = aeidon.util.start_process(command)
        glib.child_watch_add(process.pid, self._on_editor_exit, command)
        tag.props.foreground = "purple"

    def set_text(self, exctype, value, tb):
        """Set text from `tb` to the text view."""
        self._insert_title("Traceback")
        self._insert_traceback(exctype, value, tb)
        self._insert_title("Environment")
        self._insert_environment()
        self._insert_title("Libraries")
        self._insert_library_versions()
        self._insert_title("Python Packages")
        self._insert_python_package_versions()
        gaupol.util.scale_to_content(self._text_view,
                                     min_nchar=72,
                                     min_nlines=10,
                                     max_nchar=100,
                                     max_nlines=30,
                                     font="monospace")
