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


"""List widget to display subtitle data.

Module variables:

    _ACTIVE_ATTR: pango.AttrList of the active column header label
    _NORMAL_ATTR: pango.AttrList of a normal column header label
"""


import gobject
import gtk
import pango

from gaupol.gtk import conf, cons, util
from gaupol.gtk.cellrend import *
from gaupol.gtk.index import *


_ACTIVE_ATTR = pango.AttrList()
_ACTIVE_ATTR.insert(pango.AttrWeight(pango.WEIGHT_BOLD, 0, -1))
_NORMAL_ATTR = pango.AttrList()
_NORMAL_ATTR.insert(pango.AttrWeight(pango.WEIGHT_NORMAL, 0, -1))


class View(gtk.TreeView):

    """List widget to display subtitle data.

    Instance variables:

        _active_col: Index of the active column
    """

    def __init__(self, edit_mode):

        gtk.TreeView.__init__(self)

        self._active_col = None

        self._init_props(edit_mode)
        self._init_signal_handlers()

    def _get_renderer(self, col, edit_mode):
        """Initialize and return a new cell renderer."""

        font = ("" if conf.editor.use_default_font else conf.editor.font)
        if col == NO:
            renderer = gtk.CellRendererText()
            renderer.props.editable = False
            renderer.props.xalign = 1
        elif col in (SHOW, HIDE, DURN):
            if edit_mode == cons.MODE.TIME:
                renderer = TimeCellRenderer()
            elif edit_mode == cons.MODE.FRAME:
                renderer = gtk.CellRendererSpin()
                adjustment = gtk.Adjustment(0, 0, 99999999, 1, 10)
                renderer.props.adjustment = adjustment
                renderer.props.xalign = 1
            renderer.props.editable = True
        elif col in (MTXT, TTXT):
            renderer = MultilineCellRenderer()
            renderer.props.editable = True
        renderer.props.font = font
        return renderer

    def _init_columns(self, edit_mode):
        """Initialize the tree view columns."""

        for i in range(6):

            name = cons.COLUMN.display_names[i]
            renderer = self._get_renderer(i, edit_mode)
            column = gtk.TreeViewColumn(name, renderer , text=i)
            self.append_column(column)
            column.set_clickable(True)
            column.set_resizable(True)
            column.set_visible(i in conf.editor.visible_cols)
            column.set_expand(i in (4, 5))

            # Set the header label wide enough.
            label = gtk.Label(column.get_title())
            label.props.xalign = 0
            column.set_widget(label)
            label.show()
            label.set_attributes(_ACTIVE_ATTR)
            width = label.size_request()[0]
            if i in (SHOW, HIDE, DURN) and edit_mode == cons.MODE.FRAME:
                spin = gtk.SpinButton()
                digits = (0 if i == DURN else 5)
                spin.set_digits(digits)
                width = max(width, spin.size_request()[0])
            label.set_size_request(width, -1)
            label.set_attributes(_NORMAL_ATTR)

        # Set the data in the number column automatically.
        def set_number(column, renderer, store, itr):
            renderer.props.text = store.get_path(itr)[0] + 1
        column = self.get_column(NO)
        renderer = column.get_cell_renderers()[0]
        column.set_cell_data_func(renderer, set_number)

    def _init_props(self, edit_mode):
        """Initialize properties."""

        self.set_headers_visible(True)
        self.set_rules_hint(True)
        selection = self.get_selection()
        selection.set_mode(gtk.SELECTION_MULTIPLE)
        self.set_enable_search(True)
        self.set_search_column(NO)

        columns = [gobject.TYPE_INT]
        if edit_mode == cons.MODE.TIME:
            columns += [gobject.TYPE_STRING] * 3
        elif edit_mode == cons.MODE.FRAME:
            columns += [gobject.TYPE_INT] * 3
        columns += [gobject.TYPE_STRING] * 2
        store = gtk.ListStore(*columns)
        self.set_model(store)
        self._init_columns(edit_mode)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, self, "cursor-changed")
        util.connect(self, self, "key-press-event")

        conf.connect(self, "editor", "font")
        conf.connect(self, "editor", "length_unit")
        conf.connect(self, "editor", "show_lengths_cell")
        conf.connect(self, "editor", "use_default_font")

    @util.silent(AssertionError)
    def _on_conf_editor_notify_font(self, *args):
        """Apply the new font."""

        assert not conf.editor.use_default_font
        for column in self.get_columns():
            renderer = column.get_cell_renderers()[0]
            renderer.props.font = conf.editor.font
        self.columns_autosize()

    @util.silent(AssertionError)
    def _on_conf_editor_notify_length_unit(self, *args):
        """Repaint the cells."""

        assert conf.editor.show_lengths_cell
        self.columns_autosize()

    def _on_conf_editor_notify_show_lengths_cell(self, *args):
        """Repaint the cells."""

        self.columns_autosize()

    def _on_conf_editor_notify_use_default_font(self, *args):
        """Apply the new font."""

        font = ("" if conf.editor.use_default_font else conf.editor.font)
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

    def get_focus(self):
        """Get the row and column of the current focus."""

        row, col = self.get_cursor()
        if row is not None:
            row = row[0]
        if col is not None:
            col = self.get_columns().index(col)
        return row, col

    def get_selected_rows(self):
        """Get a list of the selected rows."""

        rows = self.get_selection().get_selected_rows()[1]
        return [x[0] for x in rows]

    def scroll_to_row(self, row):
        """Scroll to row."""

        self.scroll_to_cell(row, None, True, 0.5, 0)

    def select_rows(self, rows):
        """Select rows, clearing previous selection."""

        # Select by ranges to avoid sending too many 'changed' signals.
        selection = self.get_selection()
        selection.unselect_all()
        for lst in util.get_ranges(rows):
            selection.select_range(lst[0], lst[-1])

    def set_focus(self, row, col=None):
        """Set the focus to row, col.

        row can be -1 for the last row.
        """
        if row == -1:
            row = len(self.get_model()) - 1
        if col is not None:
            col = self.get_column(col)
        self.set_cursor(row, col)

    @util.silent(AssertionError)
    def update_headers(self):
        """Update the attributes of the column header labels."""

        col = self.get_focus()[1]
        assert col != self._active_col
        if self._active_col is not None:
            label = self.get_column(self._active_col).get_widget()
            label.set_attributes(_NORMAL_ATTR)
        if col is not None:
            label = self.get_column(col).get_widget()
            label.set_attributes(_ACTIVE_ATTR)
        self._active_col = col
