# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Cell renderer for time data in format HH:MM:SS,SSS."""


import gtk

from gaupol.gtk.entries import TimeEntry


class TimeCellRenderer(gtk.CellRendererText):

    """Cell renderer for time data in format HH:MM:SS.SSS."""

    __gtype_name__ = "TimeCellRenderer"

    def _on_editor_editing_done(self, editor, *args):
        """End editing."""

        self.emit("edited", editor.get_text(), editor.get_data("path"))

    def _on_editor_focus_out_event(self, editor, *args):
        """End editing."""

        editor.emit("editing-done")

    def do_start_editing(self, event, widget, path, bg_area, cell_area, flags):
        """Initialize and return the editor widget."""

        editor = TimeEntry()
        editor.set_has_frame(False)
        editor.set_alignment(self.props.xalign)
        editor.modify_font(self.props.font_desc)
        editor.set_text(self.props.text)
        editor.select_region(0, -1)
        editor.set_data("path", path)
        editor.connect("editing-done", self._on_editor_editing_done)
        editor.connect("focus-out-event", self._on_editor_focus_out_event)
        editor.show()
        return editor
