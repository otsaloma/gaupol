# Copyright (C) 2005-2010 Osmo Salomaa
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

import aeidon
import gaupol
import gtk
import pango
import re
_ = aeidon.i18n._

__all__ = ("View",)


class View(gtk.TreeView):

    """Widget to display subtitle data in the form of a list.

    :ivar columns: Enumeration for columns currently shown

       The values of the enumeration items correspond to the column indices and
       are updated when columns are added, removed or reordered. Note that
       these indices are not necessarily the same as the column indices in the
       underlying :class:`gtk.ListStore` data model.
    """

    __metaclass__ = gaupol.ContractualGObject

    def __init__(self, edit_mode):
        """Initialize a :class:`View` object."""
        gtk.TreeView.__init__(self)
        self._active_attr = None
        self._active_col_name = ""
        self._calc = aeidon.Calculator()
        self._normal_attr = None
        self.columns = aeidon.Enumeration()
        self._init_column_attributes()
        self._init_signal_handlers()
        self._init_props(edit_mode)

    def _get_renderer(self, field, edit_mode):
        """Initialize and return a new cell renderer for `field`."""
        font = gaupol.util.get_font()
        if field == gaupol.fields.NUMBER:
            renderer = gtk.CellRendererText()
            renderer.props.xalign = 1
        elif field.is_position:
            if edit_mode == aeidon.modes.TIME:
                if field == gaupol.fields.DURATION:
                    renderer = gaupol.FloatCellRenderer()
                else: renderer = gaupol.TimeCellRenderer()
            elif edit_mode == aeidon.modes.FRAME:
                renderer = gtk.CellRendererText()
            renderer.props.xalign = 1
        elif field.is_text:
            renderer = gaupol.MultilineCellRenderer()
            renderer.props.yalign = 0
        renderer.props.editable = (field != gaupol.fields.NUMBER)
        renderer.props.font = font
        renderer.props.xpad = 4
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
        """Initialize the column header :class:`pango.AttrList`."""
        self._active_attr = pango.AttrList()
        attr = pango.AttrWeight(pango.WEIGHT_BOLD, 0, -1)
        self._active_attr.insert(attr)
        self._normal_attr = pango.AttrList()
        attr = pango.AttrWeight(pango.WEIGHT_NORMAL, 0, -1)
        self._normal_attr.insert(attr)

    def _init_columns(self, edit_mode):
        """Initialize the tree view columns."""
        visible_fields = gaupol.conf.editor.visible_fields
        for field in gaupol.conf.editor.field_order:
            renderer = self._get_renderer(field, edit_mode)
            column = gtk.TreeViewColumn(field.label, renderer, text=field)
            column.set_data("identifier", field.name.lower())
            self.append_column(column)
            column.set_clickable(True)
            column.set_resizable(True)
            column.set_reorderable(True)
            column.set_expand(field.is_text)
            column.set_visible(field in visible_fields)
            label = self.get_header_label(field.label)
            label.set_tooltip_text(field.tooltip)
            column.set_widget(label)

    def _init_props(self, edit_mode):
        """Initialize properties."""
        if edit_mode == aeidon.modes.TIME:
            columns = (int, str, str, float, str, str)
        if edit_mode == aeidon.modes.FRAME:
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
        self.set_search_equal_func(self._search_equals)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""
        aeidon.util.connect(self, self, "columns-changed")
        aeidon.util.connect(self, self, "cursor-changed")
        aeidon.util.connect(self, self, "key-press-event")
        gaupol.conf.connect_notify("editor", "custom_font", self)
        gaupol.conf.connect_notify("editor", "length_unit", self)
        gaupol.conf.connect_notify("editor", "show_lengths_cell", self)
        gaupol.conf.connect_notify("editor", "use_custom_font", self)

    def _on_conf_editor_notify_custom_font(self, *args):
        """Apply the new font to all columns."""
        font = gaupol.util.get_font()
        for column in self.get_columns():
            renderer = column.get_cell_renderers()[0]
            if hasattr(renderer.props, "font"):
                renderer.props.font = font
        self.columns_autosize()

    def _on_conf_editor_notify_length_unit(self, *args):
        """Repaint the cells to update line length display."""
        if gaupol.conf.editor.show_lengths_cell:
            self.columns_autosize()

    def _on_conf_editor_notify_show_lengths_cell(self, *args):
        """Repaint the cells to update line length display."""
        self.columns_autosize()

    def _on_conf_editor_notify_use_custom_font(self, *args):
        """Apply the new font to all columns."""
        font = gaupol.util.get_font()
        for column in self.get_columns():
            renderer = column.get_cell_renderers()[0]
            if hasattr(renderer.props, "font"):
                renderer.props.font = font
        self.columns_autosize()

    def _on_columns_changed(self, *args):
        """Reset the columns enumeration to match new column layout."""
        count_changed = (len(self.columns) != len(self.get_columns()))
        self._reset_columns()
        field_order = []
        for column in self.get_columns():
            identifier = column.get_data("identifier")
            attribute = identifier.upper()
            item = aeidon.EnumerationItem()
            setattr(self.columns, attribute, item)
            if hasattr(gaupol.fields, attribute):
                field = getattr(gaupol.fields, attribute)
                field_order.append(field)
        if not count_changed:
            gaupol.conf.editor.field_order = field_order

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
        # Use interactive search for a subtitle number or time
        # only if valid string keys have been pressed.
        self.set_enable_search(event.string.isdigit() or
                               event.string == ":" or
                               event.string == ".")

    def _reset_columns(self):
        """Recreate the columns enumeration and set all items to ``None``."""
        # Set default cell enumeration items to None without magic to silence
        # false pylint positives about referencing a missing attribute.
        self.columns = aeidon.Enumeration()
        self.columns.NUMBER = None
        self.columns.START = None
        self.columns.END = None
        self.columns.DURATION = None
        self.columns.MAIN_TEXT = None
        self.columns.TRAN_TEXT = None

    def _search_equals(self, store, column, key, itr):
        """Return ``False`` if `key` matches either subtitle number or time."""
        row = int(store.get_path(itr)[0])
        if key.count(":") == 0:
            # Search for subtitle number.
            try: return row != (int(key) - 1)
            except ValueError: return False
        col = gaupol.conf.editor.field_order.index(gaupol.fields.START)
        hours = minutes = seconds = 0
        if key.count(":") == 1 and key.startswith(":"):
            # Search for time of form ':MM'
            match = re.search(r"^:(\d{1,2})$", key)
            if match is None: return False
            minutes = int(match.group(1))
        if key.count(":") == 1 and not key.startswith(":"):
            # Search for time of form 'MM:[SS.SSS]'
            match = re.search(r"^(\d{1,2}):([\d.]+)?$", key)
            if match is None: return False
            minutes = int(match.group(1))
            try: seconds = float(match.group(2) or "00.000")
            except ValueError: return False
        if key.count(":") == 2:
            # Search for time of form '[HH]:MM:[SS.SSS]'
            match = re.search(r"^(\d{,2}):(\d{1,2}):([\d.]+)?$", key)
            if match is None: return False
            hours = int(match.group(1) or "00")
            minutes = int(match.group(2))
            try: seconds = float(match.group(3) or "00.000")
            except ValueError: return False
        time_key = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
        if not self._calc.is_valid_time(time_key): return False
        time_iter = store[row][col]
        if not ":" in time_iter: return False
        try: time_next = store[row + 1][col]
        except IndexError: time_next = "99:59:59.999"
        return not (self._calc.time_to_seconds(time_iter)
                    <= self._calc.time_to_seconds(time_key)
                    < self._calc.time_to_seconds(time_next))

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

    def get_header_label(self, text):
        """Return a column header label that's wide enough."""
        label = gtk.Label(text)
        label.props.xalign = 0
        label.show()
        label.set_attributes(self._active_attr)
        width = label.size_request()[0]
        label.set_size_request(width, -1)
        label.set_attributes(self._normal_attr)
        return label

    def get_selected_rows_ensure(self, value):
        store = self.get_model()
        for row in value:
            assert 0 <= row < len(store)

    def get_selected_rows(self):
        """Return a sequence of the selected rows."""
        rows = self.get_selection().get_selected_rows()[1]
        return tuple(x[0] for x in rows)

    def is_position_column(self, col):
        """Return ``True`` if `col` is a position column."""
        return col in (self.columns.START,
                       self.columns.END,
                       self.columns.DURATION)

    def is_text_column(self, col):
        """Return True if `col` is a text column."""
        return col in (self.columns.MAIN_TEXT,
                       self.columns.TRAN_TEXT)

    def scroll_to_row_require(self, row):
        store = self.get_model()
        assert 0 <= row < len(store)

    def scroll_to_row(self, row):
        """Scroll view until `row` is visible."""
        self.scroll_to_cell(row, None, True, 0.5, 0)

    def select_rows_require(self, rows):
        store = self.get_model()
        for row in rows:
            assert 0 <= row < len(store)

    def select_rows(self, rows):
        """Select `rows`, clearing previous selection."""
        # Select by ranges to avoid sending too many 'changed' signals.
        selection = self.get_selection()
        selection.unselect_all()
        for lst in aeidon.util.get_ranges(rows):
            selection.select_range(lst[0], lst[-1])

    def set_focus_require(self, row, col=None):
        store = self.get_model()
        assert -1 <= row < len(store)
        if col is not None:
            assert col in self.columns

    def set_focus(self, row, col=None):
        """Set the focus to `row` (-1 for last), `col`."""
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
