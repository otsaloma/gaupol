# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010-2012 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Dialog for displaying a traceback in case of an unhandled exception."""

import aeidon
import gaupol
import linecache
import os
import platform
import string
import sys
import traceback
_ = aeidon.i18n._

from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Pango

__all__ = ("DebugDialog",)


class DebugDialog(gaupol.BuilderDialog):

    """Dialog for displaying a traceback in case of an unhandled exception."""

    _widgets = ("message_label", "text_view")

    def __init__(self):
        """Initialize a :class:`DebugDialog` instance."""
        gaupol.BuilderDialog.__init__(self, "debug-dialog.ui")
        self._init_text_tags()
        self._init_signal_handlers()
        self._dialog.set_default_response(Gtk.ResponseType.CLOSE)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""
        aeidon.util.connect(self, self, "response")
        aeidon.util.connect(self, "_text_view", "motion-notify-event")

    def _init_text_tags(self):
        """Initialize tags for the text buffer."""
        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag("bold", weight=Pango.Weight.BOLD)
        text_buffer.create_tag("large", scale=1.2)
        text_buffer.create_tag("monospace", family="monospace")

    def _insert_environment(self):
        """Insert environment information."""
        locale = aeidon.locales.get_system_code()
        encoding = aeidon.encodings.get_locale_code()
        ins = self._insert_text
        ins("Platform: {}\n".format(platform.platform(True)))
        ins("Locale: {}.{}\n\n".format(locale, encoding))

    def _insert_library_versions(self):
        """Insert version numbers of libraries."""
        dotjoin = lambda seq: ".".join(map(str, seq))
        python_version = dotjoin(sys.version_info[:3])
        gtk_version = dotjoin((Gtk.get_major_version(),
                               Gtk.get_minor_version(),
                               Gtk.get_micro_version()))

        pygobject_version = dotjoin(GObject.pygobject_version)
        gst_version = gaupol.util.get_gst_version()
        ins = self._insert_text
        ins("Python: {}\n".format(python_version))
        ins("GTK+: {}\n".format(gtk_version))
        ins("PyGObject: {}\n".format(pygobject_version))
        ins("GStreamer: {}\n\n".format(gst_version))

    def _insert_link(self, path, lineno, *tags):
        """Insert `path` as a link into the text view."""
        text_buffer = self._text_view.get_buffer()
        tag = text_buffer.create_tag(None, foreground="blue")
        tag.props.underline = Pango.Underline.SINGLE
        tag.connect("event", self._on_text_view_link_tag_event)
        path = os.path.abspath(path)
        tag.gaupol_path = path
        tag.gaupol_lineno = lineno
        if path.startswith(os.getcwd()):
            path = path.replace(os.getcwd(), "")
            while path.startswith(os.sep):
                path = path.replace(os.sep, "", 1)
        itr = text_buffer.get_end_iter()
        tag_table = text_buffer.get_tag_table()
        tags = list(map(tag_table.lookup, tags + ("monospace",)))
        text_buffer.insert_with_tags(itr, path, tag, *tags)

    def _insert_python_package_versions(self):
        """Insert version numbers of Python packages."""
        ins = self._insert_text
        ins("aeidon: {}\n".format(aeidon.__version__))
        ins("gaupol: {}\n".format(gaupol.__version__))
        ins("enchant: {}\n".format(aeidon.util.get_enchant_version()))
        ins("chardet: {}\n".format(aeidon.util.get_chardet_version()))

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
        # This function has been originally adapted from Gazpacho
        # Copyright (C) 2005 by Async Open Source and Sicem S.L.
        for i in range(limit):
            if tb is None: break
            lineno = tb.tb_lineno
            filename = tb.tb_frame.f_code.co_filename
            name = tb.tb_frame.f_code.co_name
            line = linecache.getline(filename, lineno)
            line = line.strip()
            self._insert_text("File: ")
            self._insert_link(filename, lineno)
            self._insert_text("\n")
            self._insert_text("Line: {}\n".format(str(lineno)))
            self._insert_text("In: {}\n\n".format(name))
            if line.strip():
                indent = "    "
                self._insert_text("{}{}\n\n".format(indent, line))
            tb = tb.tb_next
        exception = traceback.format_exception_only(exctype, value)[0]
        exception, space, message = exception.partition(" ")
        self._insert_text(exception, "bold")
        self._insert_text("{}{}\n".format(space, message))

    def _on_editor_exit(self, pid, return_value, command):
        """Print an error message if editor process failed."""
        if return_value == 0: return
        print(("Command {} failed with return value {}"
               .format(repr(command), repr(return_value))),
              file=sys.stderr)

    def _on_response(self, dialog, response):
        """Do not send response if reporting bug."""
        if response != Gtk.ResponseType.YES: return
        gaupol.util.show_uri(gaupol.BUG_REPORT_URL)
        self.stop_emission("response")

    def _on_text_view_link_tag_event(self, tag, text_view, event, itr):
        """Open linked file in editor."""
        if event.type != Gdk.EventType.BUTTON_RELEASE: return
        text_buffer = self._text_view.get_buffer()
        if text_buffer.get_selection_bounds(): return
        self._open_link(tag)

    def _on_text_view_motion_notify_event(self, text_view, event):
        """Change mouse pointer when hovering over a link."""
        x = int(event.x)
        y = int(event.y)
        window = Gtk.TextWindowType.WIDGET
        x, y = text_view.window_to_buffer_coords(window, x, y)
        window = text_view.get_window(Gtk.TextWindowType.TEXT)
        for tag in text_view.get_iter_at_location(x, y).get_tags():
            if hasattr(tag, "gaupol_path"):
                window.set_cursor(Gdk.Cursor(cursor_type=Gdk.CursorType.HAND2))
                return True
        window.set_cursor(Gdk.Cursor(cursor_type=Gdk.CursorType.XTERM))
        return False

    def _open_link(self, tag):
        """Open linked file in editor."""
        path = aeidon.util.shell_quote(tag.gaupol_path)
        command = string.Template(gaupol.conf.debug.text_editor)
        command = command.safe_substitute(LINENO=tag.gaupol_lineno,
                                          FILE=path)

        process = aeidon.util.start_process(command)
        GLib.child_watch_add(process.pid, self._on_editor_exit, command)
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
                                     min_nchar=40,
                                     max_nchar=100,
                                     min_nlines=5,
                                     max_nlines=30,
                                     font="monospace")
