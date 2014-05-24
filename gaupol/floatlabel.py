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
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Floating label that can be overlaid on another widget."""

import gaupol

from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("FloatingLabel",)


class FloatingLabel(Gtk.Box):

    """Floating label that can be overlaid on another widget."""

    # FloatingLabel is inspired by, but not an implementation of
    # the floating statusbar found in nautilus.
    # https://git.gnome.org/browse/nautilus/tree/src/nautilus-floating-bar.c

    def __init__(self):
        """Initialize a :class:`FloatingLabel` instance."""
        GObject.GObject.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        self._label = Gtk.Label()
        self._event_box = Gtk.EventBox()
        self._handlers = []
        self._hide_id = None
        self.props.halign = Gtk.Align.START
        self.props.valign = Gtk.Align.END
        self._init_widgets()

    def flash_text(self, text, duration=6):
        """Show label with `text` for `duration` seconds."""
        self.set_text(text)
        self._hide_id = gaupol.util.delay_add(duration*1000, self.hide)

    def get_text(self):
        """Return text shown in the label."""
        return self._label.get_text()

    def hide(self, *args):
        """Hide the label."""
        self.props.visible = False
        while self._handlers:
            widget, handler_id = self._handlers.pop()
            if widget.handler_is_connected(handler_id):
                widget.handler_disconnect(handler_id)

    def _init_widgets(self):
        """Initialize widgets contained in the box."""
        self._label.set_name("gaupol-floating-label")
        self._event_box.add(self._label)
        self.pack_start(self._event_box, expand=False, fill=False, padding=0)
        self._event_box.connect("enter-notify-event", self.hide)

    def register_hide_event(self, widget, signal):
        """Register `widget`'s `signal` as cause to hide the label."""
        handler_id = widget.connect(signal, self.hide)
        self._handlers.append((widget, handler_id))

    def set_text(self, text):
        """Show `text` in the label."""
        if self._hide_id is not None:
            GObject.source_remove(self._hide_id)
        if not text: return self.hide()
        self._label.set_text(text)
        self.show()

    def show(self, *args):
        """Show the label."""
        self.props.visible = True
