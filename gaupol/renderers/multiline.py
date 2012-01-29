# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

"""Cell renderer for multiline text data."""

import aeidon
import gaupol
# import glib
from gi.repository import Gtk

__all__ = ("MultilineCellRenderer",)


class CellTextView(Gtk.TextView, Gtk.CellEditable):

    # XXX:
    # Warning: Object class CellTextView doesn't implement property
    # 'editing-canceled' from interface 'GtkCellEditable'

    """A :class:`Gtk.TextView` suitable for cell renderer use."""

    __gtype_name__ = "CellTextView"

    def __init__(self, text_buffer=None):
        """Initialize a :class:`CellTextView` object."""
        GObject.GObject.__init__(self, text_buffer)
        gaupol.util.prepare_text_view(self)

    def do_editing_done(self, *args):
        """End editing."""
        self.remove_widget()

    def do_remove_widget(self, *args):
        """Remove widget."""
        pass

    def do_start_editing(self, *args):
        """Start editing."""
        pass

    def get_text(self):
        """Return text."""
        text_buffer = self.get_buffer()
        bounds = text_buffer.get_bounds()
        return text_buffer.get_text(*bounds)

    def set_text(self, text):
        """Set text."""
        self.get_buffer().set_text(text)


class MultilineCellRenderer(Gtk.CellRendererText):

    """
    Cell renderer for multiline text data.

    If :attr:`gaupol.conf.editor.show_lengths_cell` is ``True``, line lengths
    are shown as superscripts at the end of each line.
    """

    __gtype_name__ = "MultilineCellRenderer"

    def __init__(self):
        """Initialize a MultilineCellRenderer object."""
        GObject.GObject.__init__(self)
        self._in_editor_menu = False
        self._show_lengths = gaupol.conf.editor.show_lengths_cell
        self._text = ""
        gaupol.conf.connect_notify("editor", "show_lengths_cell", self)
        aeidon.util.connect(self, self, "notify::text")

    def _on_conf_editor_notify_show_lengths_cell(self, *args):
        """Hide or show line lengths if ``conf`` changed."""
        self._show_lengths = gaupol.conf.editor.show_lengths_cell

    def _on_editor_focus_out_event(self, editor, *args):
        """End editing."""
        if self._in_editor_menu: return
        editor.remove_widget()
        self.emit("editing-canceled")

    def _on_editor_key_press_event(self, editor, event):
        """End editing if ``Enter`` or ``Escape`` pressed."""
        if event.get_state() & (Gdk.EventMask.SHIFT_MASK | Gdk.EventMask.CONTROL_MASK): return
        if event.keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            editor.remove_widget()
            self.emit("edited", editor.get_data("path"), editor.get_text())
        if event.keyval == Gdk.KEY_Escape:
            editor.remove_widget()
            self.emit("editing-canceled")

    def _on_editor_populate_popup(self, editor, menu):
        """Disable "focus-out-event" ending editing."""
        self._in_editor_menu = True
        def on_menu_unmap(menu, self):
            self._in_editor_menu = False
        menu.connect("unmap", on_menu_unmap, self)

    def _on_notify_text(self, *args):
        """Set markup by adding line lengths to text."""
        self._text = text = self.props.text
        if not (text and self._show_lengths): return
        lengths = gaupol.ruler.get_lengths(text)
        text = glib.markup_escape_text(text)
        lines = text.split("\n")
        for i, line in [x for x in enumerate(lines) if x[1]]:
            lines[i] += " <sup>{:d}</sup>".format(lengths[i])
        self.props.markup = "\n".join(lines)

    def do_start_editing(self, event, widget, path, bg_area, cell_area, flags):
        """Initialize and return a :class:`CellTextView` widget."""
        editor = CellTextView()
        editor.modify_font(self.props.font_desc)
        editor.set_text(self._text)
        editor.set_size_request(cell_area.width, cell_area.height)
        editor.set_border_width(min(self.props.xpad, self.props.ypad))
        editor.set_data("path", path)
        editor.connect("focus-out-event", self._on_editor_focus_out_event)
        editor.connect("key-press-event", self._on_editor_key_press_event)
        editor.connect("populate-popup", self._on_editor_populate_popup)
        editor.show()
        return editor

    def set_show_lengths(self, show_lengths):
        """Show or hide line lengths overriding ``conf``."""
        self._show_lengths = show_lengths
        gaupol.conf.disconnect_notify("editor", "show_lengths_cell", self)
