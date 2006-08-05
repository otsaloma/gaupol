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


"""List widget to display subtitle data."""


import gobject
import gtk
import pango

from gaupol.gtk                  import cons
from gaupol.gtk.cellrend.classes import *
from gaupol.gtk.icons            import *
from gaupol.gtk.util             import conf, gtklib


_NORMAL_ATTR = pango.AttrList()
_NORMAL_ATTR.insert(pango.AttrWeight(pango.WEIGHT_NORMAL, 0, -1))
_FOCUS_ATTR = pango.AttrList()
_FOCUS_ATTR.insert(pango.AttrWeight(pango.WEIGHT_BOLD, 0, -1))


class View(gtk.TreeView):

    """List widget to display subtitle data."""

    def __init__(self, edit_mode, srtx=False):

        gtk.TreeView.__init__(self)

        self._active_col = None

        self._init_widget(edit_mode, srtx)

    def _init_widget(self, edit_mode, srtx):
        """Initialize tree view."""

        self.set_headers_visible(True)
        self.set_rules_hint(True)
        self.columns_autosize()

        selection = self.get_selection()
        selection.set_mode(gtk.SELECTION_MULTIPLE)
        selection.unselect_all()

        main_renderer = (CellRendererMultiline, CellRendererPixbuf)[srtx]
        if edit_mode == cons.Mode.TIME:
            columns = [gobject.TYPE_INT] + [gobject.TYPE_STRING] * 5
            pos_renderer = CellRendererTime
        elif edit_mode == cons.Mode.FRAME:
            columns = [gobject.TYPE_INT] * 4 + [gobject.TYPE_STRING] * 2
            pos_renderer = CellRendererInteger
        store = gtk.ListStore(*columns)
        self.set_model(store)

        names = cons.Column.display_names
        font = ''
        if not conf.editor.use_default_font:
            font = conf.editor.font

        for i, column in enumerate([
            gtk.TreeViewColumn(names[0], CellRendererInteger()  , text=0),
            gtk.TreeViewColumn(names[1], pos_renderer()         , text=1),
            gtk.TreeViewColumn(names[2], pos_renderer()         , text=2),
            gtk.TreeViewColumn(names[3], pos_renderer()         , text=3),
            gtk.TreeViewColumn(names[4], main_renderer()        , text=4),
            gtk.TreeViewColumn(names[5], CellRendererMultiline(), text=5),
        ]):
            self.append_column(column)
            column.set_clickable(True)
            column.set_resizable(True)
            if not i in conf.editor.visible_cols:
                column.set_visible(False)

            renderer = column.get_cell_renderers()[0]
            if i != 0:
                renderer.set_editable(True)
            renderer.props.font = font

            # Set column label widget wide enough that it fits the focused
            # title without having to grow wider.
            label = gtk.Label(column.get_title())
            column.set_widget(label)
            label.show()
            label.set_attributes(_FOCUS_ATTR)
            width = label.size_request()[0]
            label.set_size_request(width, -1)
            label.set_attributes(_NORMAL_ATTR)

        self.set_enable_search(True)
        self.set_search_column(NUMB)
        gtklib.connect(self, self, 'key-press-event')

    def get_focus(self):
        """
        Get location of current focus.

        Return row, column.
        """
        row, column = self.get_cursor()
        try:
            row = row[0]
        except TypeError:
            pass
        if column is not None:
            col = self.get_columns().index(column)
        else:
            col = None

        return row, col

    def get_selected_rows(self):
        """Get selected rows."""

        selected_rows = self.get_selection().get_selected_rows()[1]
        return list(x[0] for x in selected_rows)

    def _on_key_press_event(self, widget, event):
        """Allow interactive search only for numeric key-presses."""

        self.set_enable_search(False)
        if event.string.isdigit():
            self.set_enable_search(True)
        return False

    def scroll_to_row(self, row):
        """Scroll to row."""

        self.scroll_to_cell(row, None, True, 0.5, 0)

    def select_rows(self, rows):
        """
        Select rows, clearing previous selection.

        rows: Empty list or to unselect all.
        """
        selection = self.get_selection()
        selection.unselect_all()
        if not rows:
            return
        rows = sorted(rows)

        # To avoid sending 'changed' signal on the selection for every single
        # row, the list of rows needs to be broken down into ranges and
        # selected with the 'select_range' method.
        ranges = [[rows[0]]]
        rindex = 0
        for i in range(1, len(rows)):
            if rows[i] == rows[i - 1] + 1:
                ranges[rindex].append(rows[i])
            else:
                ranges.append([rows[i]])
                rindex += 1

        for entry in ranges:
            selection.select_range(entry[0], entry[-1])

    def set_focus(self, row, col):
        """Set focus to row, col."""

        try:
            column = self.get_column(col)
        except TypeError:
            column = None
        self.set_cursor(row, column)

    def set_focus_column(self):
        """Emphasize focused column title."""

        col = self.get_focus()[1]
        if col == self._active_col:
            return

        try:
            label = self.get_column(self._active_col).get_widget()
            label.set_attributes(_NORMAL_ATTR)
        except TypeError:
            pass
        try:
            label = self.get_column(col).get_widget()
            label.set_attributes(_FOCUS_ATTR)
            self._active_col = col
        except TypeError:
            pass
