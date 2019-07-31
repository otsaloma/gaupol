# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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
import platform
import sys
import traceback

from aeidon.i18n   import _
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Pango

__all__ = ("DebugDialog",)


class DebugDialog(Gtk.MessageDialog):

    """Dialog for displaying a traceback in case of an unhandled exception."""

    def __init__(self):
        """Initialize a :class:`DebugDialog` instance."""
        GObject.GObject.__init__(self,
                                 message_type=Gtk.MessageType.ERROR,
                                 text=_("Something went wrong"),
                                 secondary_text=_("You have probably discovered a bug. Please report it by providing the below information and a description of what you were doing."))

        self._text_view = Gtk.TextView()
        self._init_dialog()
        self._init_text_view()

    def _init_dialog(self):
        """Initialize the dialog."""
        self.add_button(_("_Report Bug"), Gtk.ResponseType.HELP)
        self.add_button(_("_Quit"), Gtk.ResponseType.NO)
        self.add_button(_("_Close"), Gtk.ResponseType.CLOSE)
        self.set_default_response(Gtk.ResponseType.CLOSE)
        self.set_modal(True)
        aeidon.util.connect(self, self, "response")

    def _init_text_view(self):
        """Initialize the text view."""
        self._text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self._text_view.set_editable(False)
        self._text_view.set_cursor_visible(False)
        self._text_view.set_accepts_tab(False)
        self._text_view.set_left_margin(6)
        self._text_view.set_right_margin(6)
        with aeidon.util.silent(AttributeError):
            # Top and bottom margins available since GTK 3.18.
            self._text_view.set_top_margin(6)
            self._text_view.set_bottom_margin(6)
        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag("monospace", family="monospace")
        text_buffer.create_tag("bold", weight=Pango.Weight.BOLD)
        text_buffer.create_tag("large", scale=1.1)
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(*((Gtk.PolicyType.AUTOMATIC,)*2))
        scroller.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        scroller.add(self._text_view)
        box = self.get_message_area()
        gaupol.util.pack_start_expand(box, scroller)
        box.show_all()

    def _insert_environment(self):
        """Insert information about user's platform and environment."""
        locale = aeidon.locales.get_system_code()
        encoding = aeidon.encodings.get_locale_code()
        self._insert_text("Platform: {}\n".format(platform.platform(True)))
        self._insert_text("Locale: {}.{}\n\n".format(locale, encoding))

    def _insert_dependencies(self):
        """Insert version numbers of selected dependencies."""
        dotjoin = lambda x: ".".join(map(str, x))
        chardet_version = aeidon.util.get_chardet_version()
        gspell_version = gaupol.util.get_gspell_version()
        gst_version = gaupol.util.get_gst_version()
        gtk_version = dotjoin((
            Gtk.get_major_version(),
            Gtk.get_minor_version(),
            Gtk.get_micro_version(),
        ))
        pygobject_version = dotjoin(GObject.pygobject_version)
        python_version = dotjoin(sys.version_info[:3])
        self._insert_text("aeidon: {}\n".format(aeidon.__version__))
        self._insert_text("chardet: {}\n".format(chardet_version))
        self._insert_text("gaupol: {}\n".format(gaupol.__version__))
        self._insert_text("gspell: {}\n".format(gspell_version))
        self._insert_text("gstreamer: {}\n".format(gst_version))
        self._insert_text("gtk+: {}\n".format(gtk_version))
        self._insert_text("pygobject: {}\n".format(pygobject_version))
        self._insert_text("python: {}\n".format(python_version))

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
        # Copyright (C) 2005 by Async Open Source and Sicem S.L.,
        # available under the GNU LGPL version 2 or later.
        for i in range(limit):
            if tb is None: break
            path = tb.tb_frame.f_code.co_filename
            name = tb.tb_frame.f_code.co_name
            line = linecache.getline(path, tb.tb_lineno).strip()
            self._insert_text("File: {}\n".format(path))
            self._insert_text("Line: {}\n".format(tb.tb_lineno))
            self._insert_text("In: {}\n\n".format(name))
            self._insert_text("    {}\n\n".format(line))
            tb = tb.tb_next
        exception = traceback.format_exception_only(exctype, value)[0]
        exception, space, message = exception.partition(" ")
        self._insert_text(exception, "bold")
        self._insert_text("{}{}\n".format(space, message))

    def _on_response(self, dialog, response):
        """Do not send response if reporting bug."""
        if response != Gtk.ResponseType.HELP: return
        gaupol.util.show_uri(gaupol.BUG_REPORT_URL)
        self.stop_emission("response")

    def set_text(self, exctype, value, tb):
        """Set text from `tb` to the text view."""
        self._insert_title("Traceback")
        self._insert_traceback(exctype, value, tb)
        self._insert_title("Environment")
        self._insert_environment()
        self._insert_title("Versions")
        self._insert_dependencies()
        gaupol.util.scale_to_content(self._text_view,
                                     min_nchar=60,
                                     max_nchar=100,
                                     min_nlines=10,
                                     max_nlines=25,
                                     font="monospace")
