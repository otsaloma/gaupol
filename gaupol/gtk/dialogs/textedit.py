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


"""Dialog for editing the text of a single subtitle."""


import gaupol.gtk
import gtk


class TextEditDialog(gtk.Dialog):

    """Dialog for editing the text of a single subtitle."""

    def __init__(self, parent, text=""):

        gtk.Dialog.__init__(self)
        self._text_view = None

        self._init_dialog(parent)
        self._init_text_view()
        self._init_sizes()
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
        gaupol.gtk.util.prepare_text_view(self._text_view)
        self._text_view.set_wrap_mode(gtk.WRAP_NONE)
        self._text_view.set_accepts_tab(False)
        self._text_view.set_left_margin(6)
        self._text_view.set_right_margin(6)

        scroller = gtk.ScrolledWindow()
        scroller.set_border_width(6)
        scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroller.set_shadow_type(gtk.SHADOW_IN)
        scroller.add(self._text_view)
        vbox = self.get_child()
        vbox.add(scroller)
        vbox.show_all()

    def _init_sizes(self):
        """Initialize widget sizes."""

        label = gtk.Label("\n".join(["M" * 40] * 5))
        if not gaupol.gtk.conf.editor.use_default_font:
            font = gaupol.gtk.conf.editor.font
            gaupol.gtk.util.set_label_font(label, font)
        width, height = label.size_request()
        self._text_view.set_size_request(width + 4, height + 7)

    def get_text(self):
        """Get the text in the text view."""

        text_buffer = self._text_view.get_buffer()
        bounds = text_buffer.get_bounds()
        return text_buffer.get_text(*bounds)

    def set_text(self, text):
        """Set text to the text view."""

        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(text)
