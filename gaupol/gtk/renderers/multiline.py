# Copyright (C) 2005-2008 Osmo Salomaa
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

import gaupol.gtk
import gobject
import gtk

__all__ = ("MultilineCellRenderer",)


class _CellTextView(gtk.TextView, gtk.CellEditable):

    """Text view suitable for cell renderer use."""

    __gtype_name__ = "CellTextView"

    def __init__(self, text_buffer=None):
        """Initialize a _CellTextView object."""

        gtk.TextView.__init__(self, text_buffer)
        gaupol.gtk.util.prepare_text_view(self)

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
        """Return the text."""

        text_buffer = self.get_buffer()
        bounds = text_buffer.get_bounds()
        return text_buffer.get_text(*bounds)

    def set_text(self, text):
        """Set the text."""

        self.get_buffer().set_text(text)


class MultilineCellRenderer(gtk.CellRendererText):

    """Cell renderer for multiline text data.

    If conf.editor.show_lengths_cell is True, line lengths are shown as
    superscripts at the end of each line. The original text without those
    superscripts is stored in instance variable '_text'.
    """

    __gtype_name__ = "MultilineCellRenderer"

    def __init__(self):
        """Initialize a MultilineCellRenderer object."""

        gtk.CellRendererText.__init__(self)
        self._in_editor_menu = False
        self._show_lengths = gaupol.gtk.conf.editor.show_lengths_cell
        self._text = ""

        gaupol.gtk.conf.connect(self, "editor", "show_lengths_cell")
        gaupol.util.connect(self, self, "notify::text")

    def _on_conf_editor_notify_show_lengths_cell(self, *args):
        """Synch the '_show_lengths' attribute with conf."""

        self._show_lengths = gaupol.gtk.conf.editor.show_lengths_cell

    def _on_editor_focus_out_event(self, editor, *args):
        """End editing."""

        if self._in_editor_menu: return
        editor.remove_widget()
        self.emit("editing-canceled")

    def _on_editor_key_press_event(self, editor, event):
        """End editing if Enter pressed."""

        if event.state & (gtk.gdk.SHIFT_MASK | gtk.gdk.CONTROL_MASK): return
        if event.keyval in (gtk.keysyms.Return, gtk.keysyms.KP_Enter):
            editor.remove_widget()
            self.emit("edited", editor.get_data("path"), editor.get_text())
        elif event.keyval == gtk.keysyms.Escape:
            editor.remove_widget()
            self.emit("editing-canceled")

    def _on_editor_populate_popup(self, editor, menu):
        """Disable the ending of editing on focus-out-event."""

        self._in_editor_menu = True
        def on_menu_unmap(menu, self):
            self._in_editor_menu = False
        menu.connect("unmap", on_menu_unmap, self)

    def _on_notify_text(self, *args):
        """Set markup by adding line lengths to text."""

        self._text = text = unicode(self.props.text)
        if not (text and self._show_lengths): return
        lengths = gaupol.gtk.ruler.get_lengths(text)
        text = gobject.markup_escape_text(text)
        lines = text.split("\n")
        for i in (x for x in range(len(lines)) if lines[x]):
            lines[i] += " <small><sup>%d</sup></small>" % lengths[i]
        self.props.markup = "\n".join(lines)

    def do_start_editing(self, event, widget, path, bg_area, cell_area, flags):
        """Initialize and return the editor widget."""

        editor = _CellTextView()
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
        """Show line lengths if show_lengths is True."""

        self._show_lengths = show_lengths
        gaupol.gtk.conf.disconnect(self, "editor", "show_lengths_cell")
