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


"""Cell renderer for multiline text data."""


import gobject
import gtk

from gaupol.gtk import conf, lengthlib, util


class _CellTextView(gtk.TextView, gtk.CellEditable):

    """Text view suitable for cell renderer use."""

    __gtype_name__ = "CellTextView"

    def __init__(self, text_buffer=None):

        # pylint: disable-msg=W0231
        gtk.TextView.__init__(self, text_buffer)
        util.prepare_text_view(self)

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
        """Get the text."""

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

        gtk.CellRendererText.__init__(self)
        self._show_lengths = conf.editor.show_lengths_cell
        self._text = ""
        conf.connect(self, "editor", "show_lengths_cell")
        util.connect(self, self, "notify::text")

    def _on_conf_editor_notify_show_lengths_cell(self, *args):
        """Synch the '_show_lengths' attribute with conf."""

        self._show_lengths = conf.editor.show_lengths_cell

    def _on_editor_focus_out_event(self, editor, *args):
        """End editing."""

        editor.remove_widget()
        self.emit("editing-canceled")

    @util.asserted_return
    def _on_editor_key_press_event(self, editor, event):
        """End editing if Enter pressed."""

        assert not event.state & (gtk.gdk.SHIFT_MASK | gtk.gdk.CONTROL_MASK)
        if event.keyval in (gtk.keysyms.Return, gtk.keysyms.KP_Enter):
            editor.remove_widget()
            self.emit("edited", editor.get_data("path"), editor.get_text())
        elif event.keyval == gtk.keysyms.Escape:
            editor.remove_widget()
            self.emit("editing-canceled")

    @util.asserted_return
    def _on_notify_text(self, *args):
        """Set markup by adding line lengths to text."""

        self._text = text = self.props.text
        assert text and self._show_lengths
        lengths = lengthlib.get_lengths(text)
        text = gobject.markup_escape_text(text)
        lines = text.split("\n")
        for i in (x for x in range(len(lines)) if lines[x]):
            lines[i] += " <small><sup>%d</sup></small>" % lengths[i]
        self.props.markup = "\n".join(lines)

    def do_start_editing(self, event, widget, path, bg_area, cell_area, flags):
        """Initialize and return the editor widget."""

        editor = _CellTextView()
        editor.set_text(self._text)
        editor.set_size_request(cell_area.width, cell_area.height)
        editor.set_border_width(min(self.props.xpad, self.props.ypad))
        editor.set_data("path", path)
        editor.connect("focus-out-event", self._on_editor_focus_out_event)
        editor.connect("key-press-event", self._on_editor_key_press_event)
        editor.show()
        return editor
