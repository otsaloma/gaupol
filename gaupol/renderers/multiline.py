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

"""Cell renderer for multiline text data."""

import aeidon
import gaupol

from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("MultilineCellRenderer",)


class CellTextView(Gtk.TextView, Gtk.CellEditable):

    """A :class:`Gtk.TextView` suitable for cell renderer use."""

    __gproperties__ = {
        "editing-canceled": (bool,
                             "Editing canceled",
                             "Editing canceled",
                             False,
                             GObject.PARAM_READWRITE),

    }
    __gtype_name__ = "CellTextView"

    def __init__(self, text_buffer=None):
        """Initialize a :class:`CellTextView` instance."""
        GObject.GObject.__init__(self)
        gaupol.util.prepare_text_view(self)

    def do_editing_done(self, *args):
        """End editing."""
        pass

    def do_remove_widget(self, *args):
        """Remove widget."""
        pass

    def do_start_editing(self, *args):
        """Start editing."""
        # Don't let anyone else handle button-press-events
        # that happen within the text view.
        self.connect_after("button-press-event", lambda *args: True)

    def get_text(self):
        """Return text."""
        text_buffer = self.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end, False)

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
        """Initialize a :class:`MultilineCellRenderer` instance."""
        GObject.GObject.__init__(self)
        self._in_editor_menu = False
        self._show_lengths = gaupol.conf.editor.show_lengths_cell
        self._text = ""
        gaupol.conf.connect_notify("editor", "show_lengths_cell", self)
        aeidon.util.connect(self, self, "notify::text")

    def do_start_editing(self, event, widget, path, bg_area, cell_area, flags):
        """Initialize and return a :class:`CellTextView` widget."""
        editor = CellTextView()
        gaupol.style.use_font(editor, "custom")
        editor.set_text(self._text)
        editor.set_size_request(cell_area.width, cell_area.height)
        editor.set_left_margin(self.props.xpad)
        editor.set_right_margin(self.props.xpad)
        with aeidon.util.silent(AttributeError):
            # Top and bottom margins available since GTK+ 3.18.
            editor.set_top_margin(self.props.ypad)
            editor.set_bottom_margin(self.props.ypad)
        editor.gaupol_path = path
        editor.connect("focus-out-event", self._on_editor_focus_out_event)
        editor.connect("key-press-event", self._on_editor_key_press_event)
        editor.connect("populate-popup",  self._on_editor_populate_popup)
        editor.show()
        return editor

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
        if (event.get_state() &
            (Gdk.ModifierType.SHIFT_MASK |
             Gdk.ModifierType.CONTROL_MASK)): return
        if event.keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            editor.editing_done()
            editor.remove_widget()
            self.emit("edited", editor.gaupol_path, editor.get_text())
            return True
        if event.keyval == Gdk.KEY_Escape:
            editor.editing_done()
            editor.remove_widget()
            self.emit("editing-canceled")
            return True

    def _on_editor_populate_popup(self, editor, menu):
        """Disable "focus-out-event" ending editing."""
        self._in_editor_menu = True
        def on_menu_unmap(menu, self):
            self._in_editor_menu = False
        menu.connect("unmap", on_menu_unmap, self)

    def _on_notify_text(self, *args):
        """Set markup by adding line lengths to text."""
        # Since GTK+ 3.6, the notify::text signal seems to get
        # emitted insanely often even if text hasn't changed at
        # all. Let's try to keep this callback as fast as possible.
        self._text = self.props.text
        self.props.markup = self._text_to_markup(self.props.text,
                                                 self._show_lengths,
                                                 gaupol.conf.editor.length_unit)

    def set_show_lengths(self, show_lengths):
        """Show or hide line lengths, overriding ``conf``."""
        self._show_lengths = show_lengths
        gaupol.conf.disconnect_notify("editor", "show_lengths_cell", self)

    @aeidon.deco.memoize(1000)
    def _text_to_markup(self, text, show_lengths, length_unit):
        """Return `text` rendered as markup for display."""
        # We don't actually use the length_unit argument,
        # but do need it accounted for in memoized values.
        if not text: return ""
        if not show_lengths:
            return GLib.markup_escape_text(text)
        lengths = gaupol.ruler.get_lengths(text)
        text = GLib.markup_escape_text(text)
        lines = text.split("\n")
        return "\n".join(("{} <small>[{:d}]</small>"
                          .format(lines[i], lengths[i])
                          if lines[i] else lines[i]
                          for i in range(len(lines))))
