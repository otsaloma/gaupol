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


NORM_ATTR = pango.AttrList()
NORM_ATTR.insert(pango.AttrUnderline(pango.UNDERLINE_NONE, 0, -1))

EMPH_ATTR = pango.AttrList()
EMPH_ATTR.insert(pango.AttrUnderline(pango.UNDERLINE_SINGLE, 0, -1))


class Project(gobject.GObject):

    """
    Subtitle editing project.

    This class represents one project, which is one tab in the main window's
    notebook and contains two documents: main and translation.
    
    This class is implemented as a GObject. All UI events will send out a
    signal, that will be responded to in Application class.
    """

    STAGE = gobject.SIGNAL_RUN_LAST
    
    __gsignals__ = {
        'notebook-tab-close-button-clicked': (STAGE, None, ()       ),
        'tree-view-cell-edited'            :
            (STAGE, None, (
                gobject.TYPE_STRING,
                gobject.TYPE_INT,
                gobject.TYPE_INT
            )),
        'tree-view-cell-editing-started'   : (STAGE, None, (object,)),
        'tree-view-headers-clicked'        : (STAGE, None, (object,)),
        'tree-view-selection-changed'      : (STAGE, None, (object,)),
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

        signals   = ['editing-started', 'edited']
        callbacks = [
            self._on_tree_view_cell_editing_started,
            self._on_tree_view_cell_edited
        ]

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
            
            # Get button from the column title.
            button = tree_col.get_widget()
            while not isinstance(button, gtk.Button):
                button = button.get_parent()

            # Show a column hide/show popup menu on column header right-click.
            signal = 'button_release_event'
            method = self._on_tree_view_headers_clicked
            button.connect(signal, method)

        selection = self.tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_MULTIPLE)
        selection.unselect_all()
        selection.connect('changed', self._on_tree_view_selection_changed)

        self.tree_view.connect_after('move-cursor', self._set_active_column)

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

        Properties are inherited from main document, if translation file does
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

    def _on_tree_view_cell_edited(self, cell_rend, new_value, row, col):
        """Emit signal that a tree view cell has been edited."""

        self.emit('tree-view-cell-edited', new_value, row, col)

    def _on_tree_view_cell_editing_started(self, cell_rend, editor, row, col):
        """Emit signal that a tree view cell editing has started."""

        self._set_active_column()
        self.emit('tree-view-cell-editing-started', col)
        
    def _on_tree_view_headers_clicked(self, button, event):
        """Emit signal that a tree view cell header has been clicked."""

        self.emit('tree-view-headers-clicked', event)

    def _on_tree_view_selection_changed(self, tree_sel):
        """Emit signal that a tree view selection has changed."""

        self._set_active_column()
        self.emit('tree-view-selection-changed', tree_sel)

    def reload_all_tree_view_data(self):
        """
        Reload all the subtitle data in the TreeView.
        
        Data is reordered by subtitle number. Possible selection is lost.
        """
        store = self.tree_view.get_model()
        store.clear()
        store.set_sort_column_id(NO, gtk.SORT_ASCENDING)

        # Try to speed up loading large amounts of data. (1)
        self.tree_view.freeze_child_notify()

        if self.edit_mode == 'time':
            timings = self.data.times
        elif self.edit_mode == 'frame':
            timings = self.data.frames

        for i in range(len(self.data.times)):
            store.append([i + 1] + timings[i] + self.data.texts[i])

        # Try to speed up loading large amounts of data. (2)
        self.tree_view.thaw_child_notify()

    def reload_tree_view_data_in_columns(self, col_list):
        """
        Reload the subtitle data in the specified columns.
        
        col_list: list of column indexes; column 0 cannot be reloaded
        """
        store = self.tree_view.get_model()

        # Try to speed up loading large amounts of data. (1)
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
                        
        # Try to speed up loading large amounts of data. (2)
        self.tree_view.thaw_child_notify()

    def reload_tree_view_data_in_row(self, row):
        """Reload the subtitle data in the specified row of ListStore."""

        store = self.tree_view.get_model()
        data_row = store[row][NO] - 1

        if self.edit_mode == 'time':
            timings = self.data.times
        elif self.edit_mode == 'frame':
            timings = self.data.frames

        texts = self.data.texts

        store[row] = [data_row + 1] + timings[data_row] + texts[data_row]

    def reload_tree_view_data_in_rows(self, row_a, row_b):
        """Reload the subtitle data between row_a and row_b of Data."""

        start_row = min(row_a, row_b)
        end_row   = max(row_a, row_b)

        store = self.tree_view.get_model()

        # Try to speed up loading large amounts of data. (1)
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
                        
        # Try to speed up loading large amounts of data. (2)
        self.tree_view.thaw_child_notify()

    def _set_active_column(self, *args):
        """Set the active column title bold."""

        focus_row, focus_tree_col = self.tree_view.get_cursor()

        for i in range(6):

            tree_col = self.tree_view.get_column(i)
            label = tree_col.get_widget()

            if tree_col == focus_tree_col:
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
