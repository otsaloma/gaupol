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

"""Cell renderer for time data in format ``[-]HH:MM:SS.SSS``."""

import gaupol

from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("TimeCellRenderer",)


class TimeCellRenderer(Gtk.CellRendererText):

    """Cell renderer for time data in format ``[-]HH:MM:SS.SSS``."""

    __gtype_name__ = "TimeCellRenderer"

    def __init__(self):
        """Initialize a :class:`TimeCellRenderer` instance."""
        GObject.GObject.__init__(self)
        self._in_editor_menu = False

    def do_start_editing(self, event, widget, path, bg_area, cell_area, flags):
        """Initialize and return a :class:`gaupol.TimeEntry` widget."""
        editor = gaupol.TimeEntry()
        gaupol.style.use_font(editor, "custom")
        editor.set_has_frame(False)
        editor.set_alignment(self.props.xalign)
        editor.set_text(self.props.text)
        editor.select_region(0, -1)
        editor.gaupol_path = path
        editor.connect("focus-out-event", self._on_editor_focus_out_event)
        editor.connect("key-press-event", self._on_editor_key_press_event)
        editor.connect("populate-popup",  self._on_editor_populate_popup)
        editor.show()
        return editor

    def _on_editor_focus_out_event(self, editor, *args):
        """End editing."""
        if self._in_editor_menu: return
        editor.remove_widget()
        self.emit("editing-canceled")

    def _on_editor_key_press_event(self, editor, event):
        """End editing if ``Enter`` or ``Escape`` pressed."""
        if (event.get_state() &
            (Gdk.ModifierType.SHIFT_MASK |
             Gdk.ModifierType.CONTROL_MASK)): return
        if event.keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            editor.remove_widget()
            self.emit("edited", editor.gaupol_path, editor.get_text())
            return True
        if event.keyval == Gdk.KEY_Escape:
            editor.remove_widget()
            self.emit("editing-canceled")

    def _on_editor_populate_popup(self, editor, menu):
        """Disable "focus-out-event" ending editing."""
        self._in_editor_menu = True
        def on_menu_unmap(menu, self):
            self._in_editor_menu = False
        menu.connect("unmap", on_menu_unmap, self)
