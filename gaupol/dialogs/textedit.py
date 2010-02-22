# Copyright (C) 2005-2007,2010 Osmo Salomaa
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

"""Dialog for editing text of a single subtitle."""

import gaupol
import gtk


class TextEditDialog(gtk.Dialog):

    """Dialog for editing text of a single subtitle."""

    def __init__(self, parent, text=""):
        """Initialize a :class:`TextEditDialog` object."""
        gtk.Dialog.__init__(self)
        self._text_view = None
        self._init_dialog(parent)
        self._init_text_view()
        self.set_text(text)

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.set_default_response(gtk.RESPONSE_OK)
        self.set_has_separator(False)
        self.set_transient_for(parent)
        self.set_border_width(6)
        self.set_modal(True)

    def _init_text_view(self):
        """Initialize the text view."""
        self._text_view = gtk.TextView()
        gaupol.util.prepare_text_view(self._text_view)
        self._text_view.set_wrap_mode(gtk.WRAP_NONE)
        self._text_view.set_accepts_tab(False)
        self._text_view.set_left_margin(6)
        self._text_view.set_right_margin(6)
        gaupol.util.set_size_request(self._text_view, 35, 70, 5)
        scroller = gtk.ScrolledWindow()
        scroller.set_border_width(6)
        scroller.set_policy(*((gtk.POLICY_AUTOMATIC,) * 2))
        scroller.set_shadow_type(gtk.SHADOW_IN)
        scroller.add(self._text_view)
        vbox = self.get_child()
        vbox.add(scroller)
        vbox.show_all()

    def get_text(self):
        """Return text in the text view."""
        text_buffer = self._text_view.get_buffer()
        bounds = text_buffer.get_bounds()
        return text_buffer.get_text(*bounds)

    def set_text(self, text):
        """Set `text` to the text view."""
        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(text)
