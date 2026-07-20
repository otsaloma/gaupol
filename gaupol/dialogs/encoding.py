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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Dialogs for selecting character encodings."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import GObject
from gi.repository import Gtk

class EncodingDialog(Gtk.Dialog):

    """Dialog for selecting a character encoding."""

    def __init__(self, parent):
        """Initialize an :class:`EncodingDialog` instance."""
        GObject.GObject.__init__(self, use_header_bar=True)
        self._encoding = None
        self._encoding_list = Gtk.ListBox()
        self._init_dialog(parent)
        self._init_encoding_list()

    def get_encoding(self):
        """Return the selected encoding or ``None``."""
        return self._encoding

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("_OK"), Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_title(_("Character Encodings"))

    def _init_encoding_list(self):
        """Initialize the character encoding list."""
        self._encoding_list.set_selection_mode(Gtk.SelectionMode.NONE)
        self._encoding_list.set_show_separators(True)
        self._encoding_list.add_css_class("rich-list")
        group = None
        for code, name, description in sorted(
                aeidon.encodings.get_valid(), key=lambda x: x[2]):
            box = gaupol.util.new_hbox(spacing=12)
            label = Gtk.Label(label=description)
            label.add_css_class("dim-label")
            box.append(label)
            box.append(Gtk.Label(label=name))
            radio = Gtk.CheckButton(hexpand=True, focusable=True, group=group)
            radio.set_child(box)
            radio.gaupol_code = code
            radio.connect("toggled", self._on_encoding_radio_toggled)
            group = group or radio
            row = Gtk.ListBoxRow(activatable=False, selectable=False)
            row.set_child(self._create_row_child(radio))
            self._encoding_list.append(row)
        frame = Gtk.Frame(child=self._encoding_list)
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        gaupol.util.set_widget_margins(content_box, 18)
        content_box.append(frame)
        scroller = Gtk.ScrolledWindow(
            hscrollbar_policy=Gtk.PolicyType.NEVER,
            propagate_natural_width=True,
            propagate_natural_height=True)
        scroller.set_max_content_height(gaupol.util.lines_to_px(25))
        scroller.set_child(content_box)
        gaupol.util.pack_start_expand(self.get_content_area(), scroller)

    def _create_row_child(self, radio):
        """Return the widget to place in `radio`'s list box row."""
        return radio

    def _on_encoding_radio_toggled(self, radio):
        """Save the selected encoding."""
        if radio.get_active():
            self._encoding = radio.gaupol_code

class MenuEncodingDialog(EncodingDialog):

    """Dialog for selecting character encodings."""

    @aeidon.deco.listify
    def get_visible_encodings(self):
        """Return encodings chosen to be visible."""
        for i in range(1_000_000):
            row = self._encoding_list.get_row_at_index(i)
            if not row: break
            toggle = row.get_child().get_last_child()
            if toggle.get_active():
                yield toggle.gaupol_code

    def _create_row_child(self, radio):
        """Return a row widget with an "In Menu" toggle added."""
        toggle = Gtk.ToggleButton(label=_("In Menu"))
        toggle.set_valign(Gtk.Align.CENTER)
        toggle.set_active(radio.gaupol_code in gaupol.conf.encoding.visible)
        toggle.gaupol_code = radio.gaupol_code
        box = Gtk.Box()
        box.append(radio)
        box.append(toggle)
        return box
