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

"""Widget to display subtitle data in the form of a list."""

import gaupol.gtk
import gtk
import pango
_ = gaupol.i18n._

__all__ = ("View",)


class View(gtk.TreeView):

    """Widget to display subtitle data in the form of a list.

    Instance variable 'columns' is an enumeration of the columns as shown
    currently in the view. The values of the enumeration items correspond to
    the column indices and are updated when columns are added, removed or
    reordered. Note that these indices are not necessarily the same as the
    column indices in the underlying list store data model.
    """

    __metaclass__ = gaupol.gtk.ContractualGObject

    def __init__(self, edit_mode):

        gtk.TreeView.__init__(self)
        self._active_attr = None
        self._active_col_name = ""
        self._normal_attr = None
        self.columns = gaupol.Enumeration()

        self._init_column_attributes()
        self._init_signal_handlers()
        self._init_props(edit_mode)

    def _get_header_label(self, field, edit_mode):
        """Return a column header label that's wide enough."""

        label = gtk.Label(field.label)
        label.props.xalign = 0
        label.show()
        label.set_attributes(self._active_attr)
        width = label.size_request()[0]
        label.set_size_request(width, -1)
        label.set_attributes(self._normal_attr)
        return label

    def _get_renderer(self, field, edit_mode):
        """Initialize and return a new cell renderer."""

        font = gaupol.gtk.util.get_font()
        if field == gaupol.gtk.fields.NUMBER:
            renderer = gtk.CellRendererText()
            renderer.props.xalign = 1
        elif field.is_position:
            if edit_mode == gaupol.modes.TIME:
                renderer = gaupol.gtk.TimeCellRenderer()
            elif edit_mode == gaupol.modes.FRAME:
                renderer = gtk.CellRendererText()
            renderer.props.xalign = 1
        elif field.is_text:
            renderer = gaupol.gtk.MultilineCellRenderer()
            renderer.props.yalign = 0
        renderer.props.editable = (field != gaupol.gtk.fields.NUMBER)
        renderer.props.font = font
        return renderer

    def _init_cell_data_functions(self):
        """Initialize functions to automatically update cell data."""

        # Set the data in the number column automatically.
        def set_number(column, renderer, store, itr):
            renderer.props.text = store.get_path(itr)[0] + 1
        column = self.get_column(self.columns.NUMBER)
        renderer = column.get_cell_renderers()[0]
        column.set_cell_data_func(renderer, set_number)

    def _init_column_attributes(self):
        """Initialize the column header pango attribute lists."""

        self._active_attr = pango.AttrList()
        attr = pango.AttrWeight(pango.WEIGHT_BOLD, 0, -1)
        self._active_attr.insert(attr)
        self._normal_attr = pango.AttrList()
        attr = pango.AttrWeight(pango.WEIGHT_NORMAL, 0, -1)
        self._normal_attr.insert(attr)

    def _init_columns(self, edit_mode):
        """Initialize the tree view columns."""

        visible_fields = gaupol.gtk.conf.editor.visible_fields
        for field in gaupol.gtk.conf.editor.field_order:
            renderer = self._get_renderer(field, edit_mode)
            column = gtk.TreeViewColumn(field.label, renderer, text=field)
            column.set_data("identifier", field.name.lower())
            self.append_column(column)
            column.set_clickable(True)
            column.set_resizable(True)
            column.set_reorderable(True)
            column.set_expand(field.is_text)
            column.set_visible(field in visible_fields)
            label = self._get_header_label(field, edit_mode)
            column.set_widget(label)

    def _init_props(self, edit_mode):
        """Initialize properties."""

        if edit_mode == gaupol.modes.TIME:
            columns = (int, str, str, str, str, str)
        elif edit_mode == gaupol.modes.FRAME:
            columns = (int, int, int, int, str, str)
        store = gtk.ListStore(*columns)
        self.set_model(store)
        self._init_columns(edit_mode)
        self._init_cell_data_functions()
        self.set_headers_visible(True)
        self.set_rules_hint(True)
        self.set_rubber_banding(True)
        selection = self.get_selection()
        selection.set_mode(gtk.SELECTION_MULTIPLE)
        self._init_search()

    def _init_search(self):
        """Initialize the interactive search properties."""

        self.set_enable_search(True)
        self.set_search_column(self.columns.NUMBER)
        def equals_subtitle_number(store, column, key, itr):
            # Return False if key matches subtitle number.
            return store.get_path(itr)[0] != (int(key) - 1)
        self.set_search_equal_func(equals_subtitle_number)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, self, "columns-changed")
        gaupol.util.connect(self, self, "cursor-changed")
        gaupol.util.connect(self, self, "key-press-event")

        gaupol.gtk.conf.connect(self, "editor", "custom_font")
        gaupol.gtk.conf.connect(self, "editor", "length_unit")
        gaupol.gtk.conf.connect(self, "editor", "show_lengths_cell")
        gaupol.gtk.conf.connect(self, "editor", "use_custom_font")

    def _on_conf_editor_notify_custom_font(self, *args):
        """Apply the new font to all columns."""

        if not gaupol.gtk.conf.editor.use_custom_font: return
        for column in self.get_columns():
            renderer = column.get_cell_renderers()[0]
            renderer.props.font = gaupol.gtk.conf.editor.custom_font
        self.columns_autosize()

    def _on_conf_editor_notify_length_unit(self, *args):
        """Repaint the cells to update line length display."""

        if gaupol.gtk.conf.editor.show_lengths_cell:
            self.columns_autosize()

    def _on_conf_editor_notify_show_lengths_cell(self, *args):
        """Repaint the cells to update line length display."""

        self.columns_autosize()

    def _on_conf_editor_notify_use_custom_font(self, *args):
        """Apply the new font to all columns."""

        font = gaupol.gtk.util.get_font()
        for column in self.get_columns():
            renderer = column.get_cell_renderers()[0]
            renderer.props.font = font
        self.columns_autosize()

    def _on_columns_changed(self, *args):
        """Reset the columns enumeration to match new column layout."""

        count_changed = len(self.columns) != len(self.get_columns())
        self._reset_columns()
        field_order = []
        for column in self.get_columns():
            identifier = column.get_data("identifier")
            attribute = identifier.upper()
            item = gaupol.EnumerationItem()
            setattr(self.columns, attribute, item)
            if hasattr(gaupol.gtk.fields, attribute):
                field = getattr(gaupol.gtk.fields, attribute)
                field_order.append(field)
        if not count_changed:
            gaupol.gtk.conf.editor.field_order = field_order

    def _on_cursor_changed(self, *args):
        """Update the column header labels to refelect changed focus."""

        self.update_headers()

    def _on_key_press_event(self, widget, event):
        """Handle various special-case key combinations."""

        # Disable Ctrl+PageUp/PageDown to allow them to be
        # used solely for navigation between notebook tabs.
        if event.state & gtk.gdk.CONTROL_MASK:
            if event.keyval in (gtk.keysyms.Page_Up, gtk.keysyms.Page_Down):
                return widget.stop_emission("key-press-event")

        # Use interactive search for a subtitle number
        # only if numeric keys have been pressed.
        self.set_enable_search(event.string.isdigit())

    def _reset_columns(self):
        """Recreate the columns enumeration and set all items to None."""

        # Set default cell enumeration items to None without magic to silence
        # false Pylint positives about referencing a missing attribute.
        self.columns = gaupol.Enumeration()
        self.columns.NUMBER = None
        self.columns.START = None
        self.columns.END = None
        self.columns.DURATION = None
        self.columns.MAIN_TEXT = None
        self.columns.TRAN_TEXT = None

    def get_focus_ensure(self, value):
        store = self.get_model()
        if value[0] is not None:
            assert 0 <= value[0] < len(store)
        if value[1] is not None:
            assert value[1] in self.columns

    def get_focus(self):
        """Return the row and column of the current focus."""

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
        """Return a sequence of the selected rows."""

        rows = self.get_selection().get_selected_rows()[1]
        return tuple(x[0] for x in rows)

    def is_position_column(self, col):
        """Return True if column is a position column."""

        columns = self.columns
        return col in (columns.START, columns.END, columns.DURATION)

    def is_text_column(self, col):
        """Return True if column is a text column."""

        columns = self.columns
        return col in (columns.MAIN_TEXT, columns.TRAN_TEXT)

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
        for lst in gaupol.util.get_ranges(rows):
            selection.select_range(lst[0], lst[-1])

    def set_focus_require(self, row, col=None):
        store = self.get_model()
        assert -1 <= row < len(store)
        if col is not None:
            assert col in self.columns

    def set_focus(self, row, col=None):
        """Set the focus to row (-1 for last), col."""

        if row == -1:
            row = len(self.get_model()) - 1
        if col is not None:
            col = self.get_column(col)
        self.set_cursor(row, col)

    def update_headers(self):
        """Update the attributes of the column header labels."""

        fcol = self.get_focus()[1]
        acol = getattr(self.columns, self._active_col_name, None)
        if fcol == acol: return
        self._active_col_name = ""
        if acol is not None:
            label = self.get_column(acol).get_widget()
            label.set_attributes(self._normal_attr)
        if fcol is not None:
            label = self.get_column(fcol).get_widget()
            label.set_attributes(self._active_attr)
            self._active_col_name = self.columns[fcol].name
