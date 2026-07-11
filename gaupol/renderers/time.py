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

"""Cell renderer for time data in format ``[-]HH:MM:SS.SSS``."""

import gaupol

from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gtk

class TimeCellRenderer(Gtk.CellRendererText):

    """Cell renderer for time data in format ``[-]HH:MM:SS.SSS``."""

    __gtype_name__ = "TimeCellRenderer"

    def __init__(self):
        """Initialize a :class:`TimeCellRenderer` instance."""
        GObject.GObject.__init__(self)

    def do_start_editing(self, event, widget, path, bg_area, cell_area, flags):
        """Initialize and return a :class:`gaupol.TimeEntry` widget."""
        editor = gaupol.TimeEntry()
        gaupol.style.use_font(editor, "custom")
        # Match the renderer's yalign=0 when the cell
        # is taller than one line of text.
        editor.set_valign(Gtk.Align.START)
        editor.set_has_frame(False)
        editor.set_alignment(self.props.xalign)
        editor.set_text(self.props.text)
        editor.select_region(0, -1)
        editor.gaupol_path = path
        controller = Gtk.EventControllerFocus()
        controller.connect("leave", self._on_editor_focus_leave, editor)
        editor.add_controller(controller)
        controller = Gtk.EventControllerKey()
        controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        controller.connect("key-pressed", self._on_editor_key_pressed, editor)
        editor.add_controller(controller)
        return editor

    def _on_editor_focus_leave(self, controller, editor):
        """End editing."""
        # The leave event is delivered in the middle of the focus
        # change and removing the focused editor there sends GTK's
        # focus handling into an infinite loop. Defer to idle and
        # skip if editing already ended (editor unparented).
        def end_editing():
            if editor.get_parent() is None: return
            editor.remove_widget()
            self.emit("editing-canceled")
        gaupol.util.idle_add(end_editing)

    def _on_editor_key_pressed(self, controller, keyval, keycode, state, editor):
        """End editing if ``Enter`` or ``Escape`` pressed."""
        if (state &
            (Gdk.ModifierType.SHIFT_MASK |
             Gdk.ModifierType.CONTROL_MASK)): return False
        if keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            editor.remove_widget()
            self.emit("edited", editor.gaupol_path, editor.get_text())
            return True
        if keyval == Gdk.KEY_Escape:
            editor.remove_widget()
            self.emit("editing-canceled")
            return True
        return False
