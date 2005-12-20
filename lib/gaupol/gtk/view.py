# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""A list widget to display subtitle data."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk
import pango

from gaupol.constants            import Mode
from gaupol.gtk.cellrend.classes import *
from gaupol.gtk.colconstants     import *
from gaupol.gtk.util             import config


# Normal column header
norm_attr = pango.AttrList()
norm_attr.insert(pango.AttrWeight(pango.WEIGHT_NORMAL, 0, -1))

# Focused column header
emph_attr = pango.AttrList()
emph_attr.insert(pango.AttrWeight(pango.WEIGHT_BOLD, 0, -1))


class View(gtk.TreeView):

    """A list widget to display subtitle data."""

    def __init__(self, edit_mode):

        gtk.TreeView.__init__(self)

        # Column whose header is currently emphasized. 99 % of the time this
        # should be the same as the column that has focus, but not always.
        self._active_col = None

        # Set general properties.
        self.set_headers_visible(True)
        self.set_rules_hint(True)
        self.columns_autosize()

        # Set selection.
        selection = self.get_selection()
        selection.set_mode(gtk.SELECTION_MULTIPLE)
        selection.unselect_all()

        # Create cell renderers.
        if edit_mode == Mode.TIME:
            columns = [gobject.TYPE_INT] + [gobject.TYPE_STRING] * 5
            cell_renderer_1 = CellRendererTime()
            cell_renderer_2 = CellRendererTime()
            cell_renderer_3 = CellRendererTime()

        elif edit_mode == Mode.FRAME:
            columns = [gobject.TYPE_INT] * 4 + [gobject.TYPE_STRING] * 2
            cell_renderer_1 = CellRendererInteger()
            cell_renderer_2 = CellRendererInteger()
            cell_renderer_3 = CellRendererInteger()

        cell_renderer_0 = CellRendererInteger()
        cell_renderer_4 = CellRendererMultilineText()
        cell_renderer_5 = CellRendererMultilineText()

        if config.editor.use_default_font:
            font = ''
        else:
            font = config.editor.font

        # Set cell renderer properties.
        for i in range(6):
            cell_renderer = eval('cell_renderer_%d' % i)
            if i != 0:
                cell_renderer.set_editable(True)
            cell_renderer.props.font = font

        # Set list store as model.
        store = gtk.ListStore(*columns)
        self.set_model(store)

        # Create columns.
        TVC   = gtk.TreeViewColumn
        names = Column.display_names

        tree_view_column_0 = TVC(names[0], cell_renderer_0, text=0)
        tree_view_column_1 = TVC(names[1], cell_renderer_1, text=1)
        tree_view_column_2 = TVC(names[2], cell_renderer_2, text=2)
        tree_view_column_3 = TVC(names[3], cell_renderer_3, text=3)
        tree_view_column_4 = TVC(names[4], cell_renderer_4, text=4)
        tree_view_column_5 = TVC(names[5], cell_renderer_5, text=5)

        # Set tree_view_column properties and append them.
        for i in range(6):

            tree_view_column = eval('tree_view_column_%d' % i)
            self.append_column(tree_view_column)

            tree_view_column.set_clickable(True)
            tree_view_column.set_resizable(True)

            if not i in config.editor.visible_columns:
                tree_view_column.set_visible(False)

            # Set a label widget as the tree_view_column title.
            label = gtk.Label(tree_view_column.get_title())
            tree_view_column.set_widget(label)
            label.show()

            # Set the label wide enough that it fits the emphasized title
            # without having to grow wider.
            label.set_attributes(emph_attr)
            width = label.size_request()[0]
            label.set_size_request(width, -1)
            label.set_attributes(norm_attr)

        # Enable search for number column.
        self.set_enable_search(True)
        self.set_search_column(NO)

    def get_focus(self):
        """
        Get the location of the current focus.

        Return row, column.
        """
        row, tree_view_column = self.get_cursor()

        if tree_view_column is None:
            col = None
        else:
            tree_view_columns = self.get_columns()
            col = tree_view_columns.index(tree_view_column)

        return row, col

    def get_selected_rows(self):
        """Get selected rows."""

        selection = self.get_selection()
        selected_rows = selection.get_selected_rows()[1]

        # selected_rows is a list of one-tuples of integers (Why?). Change that
        # to a list of integers.
        return [row[0] for row in selected_rows]

    def scroll_to_row(self, row):
        """Scroll to row."""

        self.scroll_to_cell(row, None, True, 0.5, 0)

    def select_rows(self, rows):
       """Select rows clearing previous selection."""

       selection = self.get_selection()
       selection.unselect_all()

       for row in rows:
           selection.select_path(row)

    def set_focus(self, row, col):
        """Move focus to row, col."""

        self.set_cursor(row, self.get_column(col))

    def set_active_column(self):
        """Emphasize the active column title."""

        col = self.get_focus()[1]

        if col == self._active_col:
            return

        try:
            label = self.get_column(self._active_col).get_widget()
            label.set_attributes(norm_attr)
        except TypeError:
            pass

        try:
            label = self.get_column(col).get_widget()
            label.set_attributes(emph_attr)
            self._active_col = col
        except TypeError:
            pass
