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


"""List widget to display subtitle data."""


import gaupol.gtk
import gobject
import gtk
import pango

__all__ = ["View"]


class View(gtk.TreeView):

    """List widget to display subtitle data.

    The index of the active column is saved as instance variable '_active_col'.
    The active column header is styled with pango.AttrList according to class
    variable '_active_attr', other column headers as '_normal_attr'.
    """

    __metaclass__ = gaupol.gtk.ContractualGObject
    _active_attr = pango.AttrList()
    _active_attr.insert(pango.AttrWeight(pango.WEIGHT_BOLD, 0, -1))
    _normal_attr = pango.AttrList()
    _normal_attr.insert(pango.AttrWeight(pango.WEIGHT_NORMAL, 0, -1))

    def __init__(self, edit_mode):

        gtk.TreeView.__init__(self)
        self._active_col = None
        self._init_props(edit_mode)
        self._init_signal_handlers()

    def _get_header_label(self, col, edit_mode):
        """Get a column header label that's wide enough."""

        label = gtk.Label(col.label)
        label.props.xalign = 0
        label.show()
        label.set_attributes(self._active_attr)
        width = label.size_request()[0]
        COLUMN = gaupol.gtk.COLUMN
        cols = (COLUMN.START, COLUMN.END, COLUMN.DURATION)
        if (col in cols) and (edit_mode == gaupol.gtk.MODE.FRAME):
            spin = gtk.SpinButton()
            digits = (0 if col == COLUMN.DURATION else 5)
            spin.set_digits(digits)
            width = max(width, spin.size_request()[0])
        label.set_size_request(width, -1)
        label.set_attributes(self._normal_attr)
        return label

    def _get_renderer(self, col, edit_mode):
        """Initialize and return a new cell renderer."""

        font = gaupol.gtk.util.get_font()
        COLUMN = gaupol.gtk.COLUMN
        position_cols = (COLUMN.START, COLUMN.END, COLUMN.DURATION)
        text_cols = (COLUMN.MAIN_TEXT, COLUMN.TRAN_TEXT)
        if col == COLUMN.NUMBER:
            renderer = gtk.CellRendererText()
            renderer.props.xalign = 1
        elif col in position_cols:
            if edit_mode == gaupol.gtk.MODE.TIME:
                renderer = gaupol.gtk.TimeCellRenderer()
            elif edit_mode == gaupol.gtk.MODE.FRAME:
                renderer = gtk.CellRendererSpin()
                adjustment = gtk.Adjustment(0, 0, 99999999, 1, 10)
                renderer.props.adjustment = adjustment
            renderer.props.xalign = 1
        elif col in text_cols:
            renderer = gaupol.gtk.MultilineCellRenderer()
        renderer.props.editable = (col != COLUMN.NUMBER)
        renderer.props.font = font
        return renderer

    def _init_columns(self, edit_mode):
        """Initialize the tree view columns."""

        text_cols = (gaupol.gtk.COLUMN.MAIN_TEXT, gaupol.gtk.COLUMN.TRAN_TEXT)
        for col in gaupol.gtk.COLUMN.members:
            renderer = self._get_renderer(col, edit_mode)
            column = gtk.TreeViewColumn(col.label, renderer , text=col)
            self.append_column(column)
            column.set_clickable(True)
            column.set_resizable(True)
            column.set_visible(col in gaupol.gtk.conf.editor.visible_cols)
            column.set_expand(col in text_cols)
            label = self._get_header_label(col, edit_mode)
            column.set_widget(label)

        # Set the data in the number column automatically.
        def set_number(column, renderer, store, itr):
            renderer.props.text = store.get_path(itr)[0] + 1
        column = self.get_column(gaupol.gtk.COLUMN.NUMBER)
        renderer = column.get_cell_renderers()[0]
        column.set_cell_data_func(renderer, set_number)

    def _init_props(self, edit_mode):
        """Initialize properties."""

        self.set_headers_visible(True)
        self.set_rules_hint(True)
        selection = self.get_selection()
        selection.set_mode(gtk.SELECTION_MULTIPLE)
        self.set_enable_search(True)
        self.set_search_column(gaupol.gtk.COLUMN.NUMBER)

        columns = [gobject.TYPE_INT]
        if edit_mode == gaupol.gtk.MODE.TIME:
            columns += [gobject.TYPE_STRING] * 3
        elif edit_mode == gaupol.gtk.MODE.FRAME:
            columns += [gobject.TYPE_INT] * 3
        columns += [gobject.TYPE_STRING] * 2
        store = gtk.ListStore(*columns)
        self.set_model(store)
        self._init_columns(edit_mode)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.gtk.util.connect(self, self, "cursor-changed")
        gaupol.gtk.util.connect(self, self, "key-press-event")
        gaupol.gtk.conf.connect(self, "editor", "font")
        gaupol.gtk.conf.connect(self, "editor", "length_unit")
        gaupol.gtk.conf.connect(self, "editor", "show_lengths_cell")
        gaupol.gtk.conf.connect(self, "editor", "use_default_font")

    @gaupol.gtk.util.asserted_return
    def _on_conf_editor_notify_font(self, *args):
        """Apply the new font."""

        assert not gaupol.gtk.conf.editor.use_default_font
        for column in self.get_columns():
            renderer = column.get_cell_renderers()[0]
            renderer.props.font = gaupol.gtk.conf.editor.font
        self.columns_autosize()

    @gaupol.gtk.util.asserted_return
    def _on_conf_editor_notify_length_unit(self, *args):
        """Repaint the cells."""

        assert gaupol.gtk.conf.editor.show_lengths_cell
        self.columns_autosize()

    def _on_conf_editor_notify_show_lengths_cell(self, *args):
        """Repaint the cells."""

        self.columns_autosize()

    def _on_conf_editor_notify_use_default_font(self, *args):
        """Apply the new font."""

        font = gaupol.gtk.util.get_font()
        for column in self.get_columns():
            renderer = column.get_cell_renderers()[0]
            renderer.props.font = font
        self.columns_autosize()

    def _on_cursor_changed(self, *args):
        """Update the column header labels."""

        self.update_headers()

    def _on_key_press_event(self, widget, event):
        """Enable or disable the interactive search."""

        self.set_enable_search(event.string.isdigit())

    def get_focus_ensure(self, value):
        store = self.get_model()
        if value[0] is not None:
            assert 0 <= value[0] < len(store)
        if value[1] is not None:
            assert value[1] in gaupol.gtk.COLUMN.members

    def get_focus(self):
        """Get the row and column of the current focus."""

        row, col = self.get_cursor()
        if row is not None:
            row = row[0]
        if col is not None:
            col = self.get_columns().index(col)
        return row, col

    def get_selected_rows_ensure(self, value):
        store = self.get_model()
        for row in value:
            assert 0 <= row < len(store)

    def get_selected_rows(self):
        """Get a list of the selected rows."""

        rows = self.get_selection().get_selected_rows()[1]
        return [x[0] for x in rows]

    def scroll_to_row_require(self, row):
        store = self.get_model()
        assert 0 <= row < len(store)

    def scroll_to_row(self, row):
        """Scroll view until row is visible."""

        self.scroll_to_cell(row, None, True, 0.5, 0)

    def select_rows_require(self, rows):
        store = self.get_model()
        for row in rows:
            assert 0 <= row < len(store)

    def select_rows(self, rows):
        """Select rows, clearing previous selection."""

        # Select by ranges to avoid sending too many 'changed' signals.
        selection = self.get_selection()
        selection.unselect_all()
        for lst in gaupol.gtk.util.get_ranges(rows):
            selection.select_range(lst[0], lst[-1])

    def set_focus_require(self, row, col=None):
        store = self.get_model()
        assert -1 <= row < len(store)
        if col is not None:
            assert col in gaupol.gtk.COLUMN.members

    def set_focus(self, row, col=None):
        """Set the focus to row, col."""

        if row == -1:
            row = len(self.get_model()) - 1
        if col is not None:
            col = self.get_column(col)
        self.set_cursor(row, col)

    @gaupol.gtk.util.asserted_return
    def update_headers(self):
        """Update the attributes of the column header labels."""

        col = self.get_focus()[1]
        assert col != self._active_col
        if self._active_col is not None:
            label = self.get_column(self._active_col).get_widget()
            label.set_attributes(self._normal_attr)
        if col is not None:
            label = self.get_column(col).get_widget()
            label.set_attributes(self._active_attr)
        self._active_col = col
