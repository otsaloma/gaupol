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

"""Widget to display subtitle data in the form of a list."""

import aeidon
import gaupol
import re

from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("View",)


class View(Gtk.TreeView):

    """
    Widget to display subtitle data in the form of a list.

    :ivar columns: Enumeration for columns currently shown

       The values of the enumeration items correspond to the column indices and
       are updated when columns are added, removed or reordered. Note that
       these indices are not necessarily the same as the column indices in the
       underlying :class:`Gtk.ListStore` data model.
    """

    def __init__(self, edit_mode):
        """Initialize a :class:`View` instance."""
        GObject.GObject.__init__(self)
        self._active_col_name = ""
        self._calc = aeidon.Calculator()
        self.columns = aeidon.Enumeration()
        self._selection_changed_handlers = {}
        self._init_signal_handlers()
        self._init_props(edit_mode)

    def connect_selection_changed(self, callback):
        """
        Connect to the "changed" signal of selection.

        Using this instead of the tree selection's own ``connect`` method
        allows signal handlers to be blocked while in the process of selecting
        multiple rows, which should be significantly faster if actually doing
        something in the signal handler.

        Return signal handler ID.
        """
        selection = self.get_selection()
        handler_id = selection.connect("changed", callback)
        self._selection_changed_handlers[handler_id] = callback
        return handler_id

    def disconnect_selection_changed(self, callback):
        """Disconnect from the "changed" signal of selection."""
        selection = self.get_selection()
        for handler_id in list(self._selection_changed_handlers):
            if self._selection_changed_handlers[handler_id] is callback:
                selection.handler_disconnect(handler_id)
                self._selection_changed_handlers.pop(handler_id)

    def get_focus(self):
        """Return the row and column of the current focus."""
        path, col = self.get_cursor()
        row = gaupol.util.tree_path_to_row(path)
        if col is not None:
            col = self.get_columns().index(col)
        return row, col

    def get_header_label(self, field=None, title=None):
        """Return a column header label from `text`."""
        title = title or field.label
        label = Gtk.Label(label=title)
        # Avoid column resizing by "preallocating"
        # sufficient width for usual expected data.
        if field == gaupol.fields.NUMBER:
            size_label = Gtk.Label(label="8888")
            size_label.show()
            width = size_label.get_preferred_width()[1]
            label.set_size_request(width, -1)
        if field == gaupol.fields.DURATION:
            size_label = Gtk.Label(label="88.888")
            size_label.show()
            width = size_label.get_preferred_width()[1]
            label.set_size_request(width, -1)
        label.set_halign(Gtk.Align.START)
        label.show()
        return label

    def _get_renderer(self, field, edit_mode):
        """Initialize and return a new cell renderer for `field`."""
        font = gaupol.util.get_font()
        if field == gaupol.fields.NUMBER:
            renderer = gaupol.IntegerCellRenderer()
            renderer.props.editable = False
            renderer.props.xalign = 1
        elif field.is_position:
            if edit_mode == aeidon.modes.TIME:
                if field == gaupol.fields.DURATION:
                    renderer = gaupol.FloatCellRenderer()
                else: renderer = gaupol.TimeCellRenderer()
            elif edit_mode == aeidon.modes.FRAME:
                renderer = gaupol.IntegerCellRenderer()
            renderer.props.editable = True
            renderer.props.xalign = 1
        elif field.is_text:
            renderer = gaupol.MultilineCellRenderer()
            renderer.props.editable = True
            renderer.props.xalign = 0
        renderer.props.font = font
        renderer.props.yalign = 0
        renderer.props.xpad = 4
        renderer.props.ypad = 4
        return renderer

    def get_selected_rows(self):
        """Return a sequence of selected rows."""
        paths = self.get_selection().get_selected_rows()[1]
        return tuple(gaupol.util.tree_path_to_row(x) for x in paths)

    def _init_cell_data_functions(self):
        """Initialize functions to automatically update cell data."""
        # Set the data in the number column automatically.
        def set_number(column, renderer, store, itr, data):
            path = store.get_path(itr)
            row = gaupol.util.tree_path_to_row(path)
            renderer.props.text = str(row + 1)
        column = self.get_column(self.columns.NUMBER)
        renderer = column.get_cells()[0]
        column.set_cell_data_func(renderer, set_number, None)
        if gaupol.conf.editor.use_zebra_stripes:
            column = self.get_column(self.columns.MAIN_TEXT)
            renderer = column.get_cells()[0]
            callback = self._on_renderer_set_background
            column.set_cell_data_func(renderer, callback, None)

    def _init_columns(self, edit_mode):
        """Initialize the tree view columns."""
        visible_fields = gaupol.conf.editor.visible_fields
        for field in gaupol.conf.editor.field_order:
            renderer = self._get_renderer(field, edit_mode)
            column = Gtk.TreeViewColumn(field.label, renderer, text=field)
            column.gaupol_id = field.name.lower()
            self.append_column(column)
            column.set_clickable(True)
            column.set_resizable(True)
            column.set_reorderable(True)
            column.set_expand(field.is_text)
            column.set_visible(field in visible_fields)
            label = self.get_header_label(field)
            label.set_tooltip_text(field.tooltip)
            column.set_widget(label)

    def _init_props(self, edit_mode):
        """Initialize properties."""
        if edit_mode == aeidon.modes.TIME:
            columns = (int, str, str, float, str, str)
        if edit_mode == aeidon.modes.FRAME:
            columns = (int, int, int, int, str, str)
        store = Gtk.ListStore(*columns)
        self.set_model(store)
        self._init_columns(edit_mode)
        self._init_cell_data_functions()
        self.set_name("gaupol-view")
        self.set_headers_visible(True)
        self.set_rubber_banding(True)
        selection = self.get_selection()
        selection.set_mode(Gtk.SelectionMode.MULTIPLE)
        self._init_search()

    def _init_search(self):
        """Initialize the interactive search properties."""
        self.set_enable_search(True)
        self.set_search_column(self.columns.NUMBER)
        self.set_search_equal_func(self._search_equals, None)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""
        aeidon.util.connect(self, self, "columns-changed")
        aeidon.util.connect(self, self, "cursor-changed")
        aeidon.util.connect(self, self, "key-press-event")
        gaupol.conf.connect_notify("editor", "custom_font", self)
        gaupol.conf.connect_notify("editor", "length_unit", self)
        gaupol.conf.connect_notify("editor", "show_lengths_cell", self)
        gaupol.conf.connect_notify("editor", "use_custom_font", self)

    def is_position_column(self, col):
        """Return ``True`` if `col` is a position column."""
        return col in (self.columns.START,
                       self.columns.END,
                       self.columns.DURATION)

    def is_text_column(self, col):
        """Return True if `col` is a text column."""
        return col in (self.columns.MAIN_TEXT,
                       self.columns.TRAN_TEXT)

    def _on_conf_editor_notify_custom_font(self, *args):
        """Apply the new font to all columns."""
        font = gaupol.util.get_font()
        for column in self.get_columns():
            renderer = column.get_cells()[0]
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
            renderer = column.get_cells()[0]
            if hasattr(renderer.props, "font"):
                renderer.props.font = font
        self.columns_autosize()

    def _on_columns_changed(self, *args):
        """Reset the columns enumeration to match new column layout."""
        count_changed = (len(self.columns) != len(self.get_columns()))
        self._reset_columns()
        field_order = []
        for column in self.get_columns():
            attribute = column.gaupol_id.upper()
            item = aeidon.EnumerationItem()
            setattr(self.columns, attribute, item)
            if hasattr(gaupol.fields, attribute):
                field = getattr(gaupol.fields, attribute)
                field_order.append(field)
        if not count_changed:
            gaupol.conf.editor.field_order = field_order

    def _on_cursor_changed(self, *args):
        """Update the column header labels to reflect changed focus."""
        self.update_headers()

    def _on_key_press_event(self, widget, event):
        """Handle various special-case key combinations."""
        # Disable Ctrl+PageUp/PageDown to allow them to be
        # used solely for navigation between notebook tabs.
        if event.get_state() & Gdk.ModifierType.CONTROL_MASK:
            if event.keyval in (Gdk.KEY_Page_Up, Gdk.KEY_Page_Down):
                return widget.stop_emission("key-press-event")
        # Use interactive search for a subtitle number or time
        # only if valid string keys have been pressed.
        self.set_enable_search(event.string.isdigit() or
                               event.string == ":" or
                               event.string == ".")

    def _on_renderer_set_background(self, column, renderer, store, itr, data):
        """Set zerba-striped backgrounds for all columns."""
        path = self.get_model().get_path(itr)
        row = gaupol.util.tree_path_to_row(path)
        color = (gaupol.util.get_zebra_color(self)
                 if row % 2 == 0 else None)

        for column in self.get_columns():
            for renderer in column.get_cells():
                renderer.props.cell_background_rgba = color

    def _reset_columns(self):
        """Recreate the columns enumeration and set all items to ``None``."""
        self.columns = aeidon.Enumeration()
        self.columns.NUMBER = None
        self.columns.START = None
        self.columns.END = None
        self.columns.DURATION = None
        self.columns.MAIN_TEXT = None
        self.columns.TRAN_TEXT = None

    def scroll_to_row(self, row):
        """Scroll view until `row` is visible."""
        self.scroll_to_cell(path=row,
                            column=None,
                            use_align=False,
                            row_align=0.5,
                            col_align=0)

    def _search_equals(self, store, column, key, itr, data):
        """Return ``False`` if `key` matches either subtitle number or time."""
        path = store.get_path(itr)
        row = gaupol.util.tree_path_to_row(path)
        if key.count(":") == 0:
            # Search for subtitle number.
            try:
                return row != (int(key) - 1)
            except ValueError:
                return False
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
            try:
                seconds = float(match.group(2) or "00.000")
            except ValueError:
                return False
        if key.count(":") == 2:
            # Search for time of form '[HH]:MM:[SS.SSS]'
            match = re.search(r"^(\d{,2}):(\d{1,2}):([\d.]+)?$", key)
            if match is None: return False
            hours = int(match.group(1) or "00")
            minutes = int(match.group(2))
            try:
                seconds = float(match.group(3) or "00.000")
            except ValueError:
                return False
        time_key = "{:02d}:{:02d}:{:06.3f}".format(hours, minutes, seconds)
        if not self._calc.is_valid_time(time_key): return False
        time_iter = store[row][col]
        if not ":" in time_iter: return False
        try:
            time_next = store[row+1][col]
        except IndexError:
            time_next = "99:59:59.999"
        return not (self._calc.time_to_seconds(time_iter) <=
                    self._calc.time_to_seconds(time_key) <
                    self._calc.time_to_seconds(time_next))

    def select_rows(self, rows):
        """Select `rows`, clearing previous selection."""
        # Avoid sending more than one 'changed' signal.
        selection = self.get_selection()
        for handler_id in self._selection_changed_handlers:
            selection.handler_block(handler_id)
        selection.unselect_all()
        for lst in aeidon.util.get_ranges(rows):
            start = gaupol.util.tree_row_to_path(lst[0])
            end = gaupol.util.tree_row_to_path(lst[-1])
            selection.select_range(start, end)
        for handler_id in self._selection_changed_handlers:
            selection.handler_unblock(handler_id)
        selection.emit("changed")

    def set_focus(self, row, col=None):
        """Set the focus to `row` (-1 for last), `col`."""
        if row == -1:
            row = len(self.get_model()) - 1
        if col is not None:
            col = self.get_column(col)
        path = gaupol.util.tree_row_to_path(row)
        self.set_cursor(path, col, start_editing=False)
        if col is not None:
            self.update_headers()

    def update_headers(self):
        """Update the attributes of all column header labels."""
        fcol = self.get_focus()[1]
        acol = getattr(self.columns, self._active_col_name, None)
        if fcol == acol: return
        self._active_col_name = ""
        if acol is not None:
            label = self.get_column(acol).get_widget()
            text = GLib.markup_escape_text(label.get_text())
            label.set_markup("{}".format(text))
        if fcol is not None:
            label = self.get_column(fcol).get_widget()
            text = GLib.markup_escape_text(label.get_text())
            label.set_markup("<i>{}</i>".format(text))
            self._active_col_name = self.columns[fcol].name
