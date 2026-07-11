# -*- coding: utf-8 -*-

# Copyright (C) 2013 Osmo Salomaa
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

"""Toast notification that can be overlaid on another widget."""

import gaupol

from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("Toast",)

class Toast(Gtk.Box):

    """Toast notification that can be overlaid on another widget."""

    def __init__(self):
        """Initialize a :class:`Toast` instance."""
        GObject.GObject.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self._hide_id = None
        self._label = Gtk.Label()
        self.add_css_class("gaupol-toast")
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.END)
        self._init_widgets()

    def flash_text(self, text, duration=3):
        """Show toast with `text` for `duration` seconds."""
        if not text:
            return self._hide()
        self.set_text(text)
        self._hide_id = gaupol.util.delay_add(duration * 1000, self._hide)

    def get_text(self):
        """Return text shown in the toast."""
        return self._label.get_text()

    def _hide(self, *args):
        """Hide the toast."""
        self.set_visible(False)
        self._hide_id = None

    def _init_widgets(self):
        """Initialize widgets contained in the toast."""
        gaupol.util.pack_start(self, self._label)
        button = Gtk.Button.new_from_icon_name("window-close-symbolic")
        button.add_css_class("flat")
        button.add_css_class("circular")
        button.connect("clicked", self._hide)
        gaupol.util.pack_start(self, button)

    def set_text(self, text):
        """Show `text` in the toast."""
        if not text:
            return self._hide()
        if self._hide_id is not None:
            GLib.source_remove(self._hide_id)
        self._label.set_text(text)
        self.set_visible(True)
