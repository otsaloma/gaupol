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

"""Dialog for editing text of a single subtitle."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import GObject
from gi.repository import Gtk


class TextEditDialog(Gtk.Dialog):

    """Dialog for editing text of a single subtitle."""

    def __init__(self, parent, text=""):
        """Initialize a :class:`TextEditDialog` instance."""
        GObject.GObject.__init__(self, use_header_bar=True)
        self._text_view = Gtk.TextView()
        self._init_dialog(parent)
        self._init_text_view()
        self.set_text(text)

    def get_text(self):
        """Return text in the text view."""
        text_buffer = self._text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end, False)

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("_OK"), Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_title(_("Edit Text"))

    def _init_text_view(self):
        """Initialize the text view."""
        gaupol.util.prepare_text_view(self._text_view)
        self._text_view.set_wrap_mode(Gtk.WrapMode.NONE)
        self._text_view.set_accepts_tab(False)
        self._text_view.set_left_margin(6)
        self._text_view.set_right_margin(6)
        with aeidon.util.silent(AttributeError):
            # Top and bottom margins available since GTK 3.18.
            self._text_view.set_top_margin(6)
            self._text_view.set_bottom_margin(6)
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(*((Gtk.PolicyType.AUTOMATIC,)*2))
        scroller.set_shadow_type(Gtk.ShadowType.NONE)
        scroller.add(self._text_view)
        box = self.get_content_area()
        gaupol.util.pack_start_expand(box, scroller)
        gaupol.util.scale_to_size(self._text_view,
                                  nchar=55,
                                  nlines=7,
                                  font="custom")

        box.show_all()

    def set_text(self, text):
        """Set `text` to the text view."""
        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(text)
