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


"""Subtitle editing project."""


import os

try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk
import pango

from gaupol.gui.cellrend.integer import CellRendererInteger
from gaupol.gui.cellrend.multiline import CellRendererMultilineText
from gaupol.gui.cellrend.time import CellRendererTime
from gaupol.gui.constants import COLUMN_NAMES
from gaupol.gui.constants import NO, SHOW, HIDE, DURN, ORIG, TRAN
from gaupol.gui.util import gui
from gaupol.lib.data import Data


# Normal column header
NORM_ATTR = pango.AttrList()
NORM_ATTR.insert(pango.AttrWeight(pango.WEIGHT_NORMAL, 0, -1))

# Focused column header
EMPH_ATTR = pango.AttrList()
EMPH_ATTR.insert(pango.AttrWeight(pango.WEIGHT_BOLD, 0, -1))


class Project(gobject.GObject):

    """
    Subtitle editing project.

    This class represents one project, which is one tab in the main window's
    notebook and contains two documents: main and translation.
    
    This class is implemented as a GObject. All UI events will send out a
    signal, that will be responded to in the Application class.
    """

    STAGE = gobject.SIGNAL_RUN_LAST
    BOOL  = gobject.TYPE_BOOLEAN
    INT   = gobject.TYPE_INT
    STR   = gobject.TYPE_STRING
    
    __gsignals__ = {
        'notebook-tab-close-button-clicked': (STAGE, None, ()             ),
        'tree-view-button-press-event'     : (STAGE, BOOL, (object,)      ),
        'tree-view-cell-edited'            : (STAGE, None, (STR, INT, INT)),
        'tree-view-cell-editing-started'   : (STAGE, None, (object,)      ),
        'tree-view-cursor-moved'           : (STAGE, None, ()             ),
        'tree-view-headers-clicked'        : (STAGE, None, (object,)      ),
        'tree-view-selection-changed'      : (STAGE, None, ()             ),
    }

    def __init__(self, config, counter=0):
        """
        Initialize a Project object.
        
        counter: an integer that gives this project a unique ID
        """
        gobject.GObject.__init__(self)
    
        self._config = config
        self.data    = Data(config.get('editor', 'framerate'))

        self.untitle   = _('Untitled %d') % counter
        self.edit_mode = config.get('editor', 'edit_mode')

        # Undoing will decrease changed value by one. Doing and redoing will
        # increase changed value by one. At zero the document is at its
        # unchanged (saved) state.
        self.main_changed = 0
        self.tran_changed = 0
        
        # Stacks of actions of type DURAction.  
        self.undoables = []
        self.redoables = []

        # Widgets
        self.tab_label      = None
        self.tab_menu_label = None
        self.tab_widget     = None
        self.tree_view      = None
        self.tooltips       = gtk.Tooltips()

        self._build_tab_labels()
        self.build_tree_view()

    def _build_tab_labels(self):
        """Build the notebook tab label widgets."""

        title = self.get_main_basename()
        
        # Tab label.
        self.tab_label = gtk.Label(title)
        self.tab_label.set_ellipsize(pango.ELLIPSIZE_MIDDLE)
        self.tab_label.set_max_width_chars(24)

        # Event box for tooltip.
        event_box = gtk.EventBox()
        event_box.add(self.tab_label)
        self.tooltips.set_tip(event_box, title)

        # Tab close image.
        image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        width, height = image.size_request()

        # Tab close button.
        button = gtk.Button()
        button.add(image)
        button.set_relief(gtk.RELIEF_NONE)
        button.set_size_request(width + 2, height + 2)
        button.connect('clicked', self._on_notebook_tab_close_button_clicked)

        # Tab horizontal box.
        self.tab_widget = gtk.HBox(False, 4)
        self.tab_widget.pack_start(event_box, True , True , 0)
        self.tab_widget.pack_start(button   , False, False, 0)
        self.tab_widget.show_all()

        # Tab menu label.
        self.tab_menu_label = gtk.Label(title)
        self.tab_menu_label.set_property('xalign', 0)

    def build_tree_view(self):
        """Build the TreeView used to display subtitle data."""
        
        self.tree_view = gtk.TreeView()

        self.tree_view.set_headers_visible(True)
        self.tree_view.set_rules_hint(True)
        self.tree_view.set_enable_search(False)
        self.tree_view.columns_autosize()

        if self.edit_mode == 'time':
            columns = [gobject.TYPE_INT] + [gobject.TYPE_STRING] * 5
            cr_1 = CellRendererTime()
            cr_2 = CellRendererTime()
            cr_3 = CellRendererTime()

        elif self.edit_mode == 'frame':
            columns = [gobject.TYPE_INT] * 4 + [gobject.TYPE_STRING] * 2
            cr_1 = CellRendererInteger()
            cr_2 = CellRendererInteger()
            cr_3 = CellRendererInteger()

        cr_0 = CellRendererInteger()
        cr_4 = CellRendererMultilineText()
        cr_5 = CellRendererMultilineText()

        font = self._config.get('view', 'font')

        signals   = (
            'editing-started',
            'edited',
        )
        callbacks = (
            self._on_tree_view_cell_editing_started,
            self._on_tree_view_cell_edited,
        )

        for i in range(6):
        
            cell_rend = eval('cr_%d' % i)
            
            if i != 0:
                cell_rend.set_editable(True)
            cell_rend.set_property('font', font)

            for k in range(len(signals)):
                cell_rend.connect(signals[k], callbacks[k], i)

        store = gtk.ListStore(*columns)
        self.tree_view.set_model(store)
        
        tree_col_0 = gtk.TreeViewColumn(_('No.')        , cr_0, text=0)
        tree_col_1 = gtk.TreeViewColumn(_('Show')       , cr_1, text=1)
        tree_col_2 = gtk.TreeViewColumn(_('Hide')       , cr_2, text=2)
        tree_col_3 = gtk.TreeViewColumn(_('Duration')   , cr_3, text=3)
        tree_col_4 = gtk.TreeViewColumn(_('Text')       , cr_4, text=4)
        tree_col_5 = gtk.TreeViewColumn(_('Translation'), cr_5, text=5)

        vis_columns = self._config.getlist('view', 'columns')
        
        # Set column properties and append columns.
        for i in range(6):
        
            tree_col = eval('tree_col_%d' % i)
            self.tree_view.append_column(tree_col)

            tree_col.set_resizable(True)
            tree_col.set_clickable(True)
            
            tree_col.set_sort_column_id(i)
            if i == NO:
                store.set_sort_column_id(NO, gtk.SORT_ASCENDING)

            col_name = COLUMN_NAMES[i]
            if col_name not in vis_columns:
                tree_col.set_visible(False)

            # Set a label widget as the column title.
            label = gtk.Label(tree_col.get_title())
            tree_col.set_widget(label)
            label.show()

            # Set the label wide enough that it fits the emphasized text
            # without having to grow wider.
            label.set_attributes(EMPH_ATTR)
            width = label.size_request()[0]
            label.set_size_request(width, -1)
            label.set_attributes(NORM_ATTR)
            
            # Get button from the column title.
            button = tree_col.get_widget()
            while not isinstance(button, gtk.Button):
                button = button.get_parent()

            # Show a column hide/show popup menu on column header right-click.
            signal = 'button-press-event'
            method = self._on_tree_view_headers_clicked
            button.connect(signal, method)

        selection = self.tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_MULTIPLE)
        selection.unselect_all()
        selection.connect('changed', self._on_tree_view_selection_changed)

        method = self._on_tree_view_cursor_moved
        self.tree_view.connect_after('move-cursor', method)

        method = self._on_tree_view_button_press_event
        self.tree_view.connect('button-press-event', method)

    def get_data_focus(self):
        """
        Get the location in Data where the tree view focus points to.
        
        Return: section, row, column (any one could be None)
        """
        store = self.tree_view.get_model()
        store_row, store_col = self.get_store_focus()
        
        if store_row is None:
            data_row = None
        else:
            data_row = store[store_row][NO] - 1
        
        if store_col is None or store_col == NO:
            data_section = None
            data_col     = None
            
        elif store_col in [SHOW, HIDE, DURN]:
            data_section = self.edit_mode + 's'
            data_col     = store_col - 1
            
        elif store_col in [ORIG, TRAN]:
            data_section = 'texts'
            data_col     = store_col - 4

        return data_section, data_row, data_col

    def get_data_row(self, store_row):
        """Get Data row that corresponds to ListStore row."""
        
        if store_row is None:
            return None
            
        store = self.tree_view.get_model()
        return store[store_row][NO] - 1

    def get_main_basename(self):
        """Get basename of main document."""
        
        if self.data.main_file is not None:
            return os.path.basename(self.data.main_file.path)
        else:
            return self.untitle

    def get_main_corename(self):
        """Get basename of main document without extension."""

        if self.data.main_file is not None:
            basename = os.path.basename(self.data.main_file.path)
            extension = self.data.main_file.EXTENSION
            return basename[0:-len(extension)]
        else:
            return self.untitle

    def get_main_document_properties(self):
        """
        Get properties of main document.

        Return: (path, format, encoding, newlines) or (None, None, None None)
        """
        if self.data.main_file is not None:
            path     = self.data.main_file.path
            format   = self.data.main_file.FORMAT
            encoding = self.data.main_file.encoding
            newlines = self.data.main_file.newlines
            return path, format, encoding, newlines
        else:
            return None, None, None, None

    def get_selected_data_rows(self):
        """Get rows in Data, that match the selection in TreeView."""

        store = self.tree_view.get_model()
        store_rows = self.get_selected_store_rows()
        return [store[i][NO] - 1 for i in store_rows]

    def get_selected_store_rows(self):
        """Get rows in ListStore, that match the selection in TreeView."""

        selection = self.tree_view.get_selection()
        return selection.get_selected_rows()[1]

    def get_store_focus(self):
        """
        Get the location in ListStore where the tree view focus points to.
        
        Return: row, column (either one could be None)
        """
        store = self.tree_view.get_model()
        store_row, tree_col = self.tree_view.get_cursor()

        if tree_col is None:
            return store_row, None

        tree_cols = self.tree_view.get_columns()
        store_col = tree_cols.index(tree_col)

        return store_row, store_col

    def get_store_row(self, data_row):
        """Get ListStore row that corresponds to Data row."""

        if data_row is None:
            return None

        store = self.tree_view.get_model()
        
        if store.get_sort_column_id()[0] == NO:
            return data_row
        
        subtitle = data_row + 1
        for i in range(len(store)):
            if store[i][NO] == subtitle:
                return i

    def get_translation_basename(self):
        """Get basename of translation document."""
        
        if self.data.tran_file is not None:
            return os.path.basename(self.data.tran_file.path)
        elif self.data.main_file is not None:
            return _('%s translation') % self.get_main_corename()
        else:
            return _('%s translation') % self.untitle

    def get_translation_corename(self):
        """Get basename of translation document without extension."""

        if self.data.tran_file is not None:
            basename = os.path.basename(self.data.tran_file.path)
            extension = self.data.tran_file.EXTENSION
            return basename[0:-len(extension)]
        else:
            return self.get_translation_basename()

    def get_translation_document_properties(self):
        """
        Get properties of translation document.

        Properties are inherited from main document if translation file does
        not exist.
        
        Return: path, format, encoding, newlines (of which any can be None)
        """
        if self.data.tran_file is not None:
            path     = self.data.tran_file.path
            format   = self.data.tran_file.FORMAT
            encoding = self.data.tran_file.encoding
            newlines = self.data.tran_file.newlines

        elif self.data.main_file is not None:
            path     = None
            format   = self.data.main_file.FORMAT
            encoding = self.data.main_file.encoding
            newlines = self.data.main_file.newlines

        else:
            return None, None, None, None

        return path, format, encoding, newlines

    def _on_notebook_tab_close_button_clicked(self, *args):
        """Emit signal that the notebook tab close button has been clicked."""
        
        self.emit('notebook-tab-close-button-clicked')

    def _on_tree_view_button_press_event(self, tree_view, event):
        """Emit signal that a tree view cell has been clicked."""

        # Return True to stop other handlers or False to not to.
        return self.emit('tree-view-button-press-event', event)

    def _on_tree_view_cell_edited(self, cell_rend, new_value, row, col):
        """Emit signal that a tree view cell has been edited."""

        self.emit('tree-view-cell-edited', new_value, row, col)

    def _on_tree_view_cell_editing_started(self, cell_rend, editor, row, col):
        """Emit signal that a tree view cell editing has started."""

        self.set_active_column()
        self.emit('tree-view-cell-editing-started', col)

    def _on_tree_view_cursor_moved(self, *args):
        """Emit signal that the tree view cursor has moved."""

        self.set_active_column()
        self.emit('tree-view-cursor-moved')
        
    def _on_tree_view_headers_clicked(self, button, event):
        """Emit signal that a tree view cell header has been clicked."""

        self.emit('tree-view-headers-clicked', event)

    def _on_tree_view_selection_changed(self, *args):
        """Emit signal that a tree view selection has changed."""

        self.set_active_column()
        self.emit('tree-view-selection-changed')

    def reload_all_data(self):
        """
        Reload all data in the TreeView.
        
        Data is reordered by subtitle number. Possible selection is lost.
        """
        store = self.tree_view.get_model()
        store.clear()
        store.set_sort_column_id(NO, gtk.SORT_ASCENDING)

        self.tree_view.freeze_child_notify()

        if self.edit_mode == 'time':
            timings = self.data.times
        elif self.edit_mode == 'frame':
            timings = self.data.frames

        for i in range(len(self.data.times)):
            store.append([i + 1] + timings[i] + self.data.texts[i])

        self.tree_view.thaw_child_notify()

    def reload_data_in_columns(self, col_list):
        """Reload all data in given columns of the TreeView."""
        
        store = self.tree_view.get_model()

        self.tree_view.freeze_child_notify()

        # When looping over the store, the sort order must be unambiguous.
        # New data could change the sort order and ruin looping order.
        # Hence sort order is temporarily changed to No. column.
        sort_col, sort_order = store.get_sort_column_id()
        store.set_sort_column_id(NO, gtk.SORT_ASCENDING)

        for col in col_list:
            
            if col in [SHOW, HIDE, DURN]:

                if self.edit_mode == 'time':
                    timings = self.data.times
                elif self.edit_mode == 'frame':
                    timings = self.data.frames
                
                for i in range(len(store)):
                    store[i][col] = timings[i][col - 1]
                            
            elif col in [ORIG, TRAN]:
            
                for i in range(len(store)):
                    store[i][col] = self.data.texts[i][col - 4]

        store.set_sort_column_id(sort_col, sort_order)

        self.tree_view.thaw_child_notify()

    def reload_data_in_row(self, data_row):
        """Reload TreeView data in given Data row."""

        store = self.tree_view.get_model()
        store_row = self.get_store_row(data_row)

        if self.edit_mode == 'time':
            timings = self.data.times
        elif self.edit_mode == 'frame':
            timings = self.data.frames

        texts = self.data.texts

        store[store_row] = [data_row + 1] + timings[data_row] + texts[data_row]

    def reload_data_in_rows(self, row_a, row_b):
        """Reload TreeView data between given Data rows."""

        start_row = min(row_a, row_b)
        end_row   = max(row_a, row_b)

        store = self.tree_view.get_model()

        self.tree_view.freeze_child_notify()

        # When looping over the store, the sort order must be unambiguous.
        # New data could change the sort order and ruin looping order.
        # Hence sort order is temporarily changed to No. column.
        sort_col, sort_order = store.get_sort_column_id()
        store.set_sort_column_id(NO, gtk.SORT_ASCENDING)

        if self.edit_mode == 'time':
            timings = self.data.times
        elif self.edit_mode == 'frame':
            timings = self.data.frames

        for i in range(start_row, end_row + 1):
            store[i] = [i + 1] + timings[i] + self.data.texts[i]

        store.set_sort_column_id(sort_col, sort_order)
                        
        self.tree_view.thaw_child_notify()

    def set_active_column(self, *args):
        """Set the active column title emphasized."""

        col = self.get_store_focus()[1]

        for i in range(6):

            label = self.tree_view.get_column(i).get_widget()

            if i == col:
                label.set_attributes(EMPH_ATTR)
            else:
                label.set_attributes(NORM_ATTR)

    def set_tab_labels(self):
        """
        Set text in tab labels to reflect current filename and changed state.
        
        Return: tab label title
        """
        title = self.get_main_basename()
        if self.main_changed or self.tran_changed:
            title = '*' + title
        
        self.tab_label.set_text(title)
        self.tab_menu_label.set_text(title)

        event_box = gui.get_event_box(self.tab_label)
        self.tooltips.set_tip(event_box, title)

        return title


gobject.type_register(Project)
