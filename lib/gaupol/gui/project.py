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

from gaupol.constants import MAIN_DOCUMENT, TRAN_DOCUMENT
from gaupol.constants import MODE_TIME, MODE_FRAME
from gaupol.gui.cellrend.integer import CellRendererInteger
from gaupol.gui.cellrend.multiline import CellRendererMultilineText
from gaupol.gui.cellrend.time import CellRendererTime
from gaupol.gui.constants import COLUMN_NAMES, MODE_NAMES
from gaupol.gui.constants import NO, SHOW, HIDE, DURN, TEXT, TRAN
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

        framerate = config.get('editor', 'framerate')
        edit_mode = config.get('editor', 'edit_mode')
        edit_mode = MODE_NAMES.index(edit_mode)

        self.data      = Data(framerate)
        self.untitle   = _('Untitled %d') % counter
        self.edit_mode = edit_mode

        # Undoing will decrease changed value by one. Doing and redoing will
        # increase changed value by one. At zero the document is at its
        # unchanged (saved) state.
        self.main_changed = 0
        self.tran_changed = 0

        self.tran_active = False
        
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

        if self.edit_mode == MODE_TIME:
            columns = [INT] + [STR] * 5
            cr_1 = CellRendererTime()
            cr_2 = CellRendererTime()
            cr_3 = CellRendererTime()

        elif self.edit_mode == MODE_FRAME:
            columns = [INT] * 4 + [STR] * 2
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
        
            cell_renderer = eval('cr_%d' % i)
            
            if i != 0:
                cell_renderer.set_editable(True)
            cell_renderer.set_property('font', font)

            for k in range(len(signals)):
                cell_renderer.connect(signals[k], callbacks[k], i)

        store = gtk.ListStore(*columns)
        self.tree_view.set_model(store)
        
        tree_col_0 = gtk.TreeViewColumn(_('No.')        , cr_0, text=0)
        tree_col_1 = gtk.TreeViewColumn(_('Show')       , cr_1, text=1)
        tree_col_2 = gtk.TreeViewColumn(_('Hide')       , cr_2, text=2)
        tree_col_3 = gtk.TreeViewColumn(_('Duration')   , cr_3, text=3)
        tree_col_4 = gtk.TreeViewColumn(_('Text')       , cr_4, text=4)
        tree_col_5 = gtk.TreeViewColumn(_('Translation'), cr_5, text=5)

        visible_columns = self._config.getlist('view', 'columns')
        
        # Set column properties and append columns.
        for i in range(6):
        
            tree_view_column = eval('tree_col_%d' % i)
            self.tree_view.append_column(tree_view_column)

            tree_view_column.set_resizable(True)

            column_name = COLUMN_NAMES[i]
            if column_name not in visible_columns:
                tree_view_column.set_visible(False)

            # Set a label widget as the column title.
            label = gtk.Label(tree_view_column.get_title())
            tree_view_column.set_widget(label)
            label.show()

            # Set the label wide enough that it fits the emphasized title
            # without having to grow wider.
            label.set_attributes(EMPH_ATTR)
            width = label.size_request()[0]
            label.set_size_request(width, -1)
            label.set_attributes(NORM_ATTR)
            
            # Get button from the column title.
            button = tree_view_column.get_widget()
            while not isinstance(button, gtk.Button):
                button = button.get_parent()

            # Allow TreeViewColumn header to be clicked.
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

    def get_data_column(self, store_col):
        """Get Data column to match ListStore column."""
        
        if store_col == NO:
            return None
        if store_col in [SHOW, HIDE, DURN]:
            return store_col - 1
        if store_col in [TEXT, TRAN]:
            return store_col - 4

    def get_document(self, col):
        """Get constant for document in col."""
        
        if col == TRAN:
            return TRAN_DOCUMENT
        else:
            return MAIN_DOCUMENT

    def get_focus(self):
        """
        Get the location of current focus.
        
        Return: row, column, gtk.TreeViewColumn (any of which could be None)
        """
        store = self.tree_view.get_model()
        row, tree_view_column = self.tree_view.get_cursor()

        if tree_view_column is None:
            col = None
        else:
            tree_view_columns = self.tree_view.get_columns()
            col = tree_view_columns.index(tree_view_column)

        return row, col, tree_view_column

    def get_main_basename(self):
        """Get basename of main document."""
        
        try:
            return os.path.basename(self.data.main_file.path)
        except AttributeError:
            return self.untitle

    def get_main_corename(self):
        """Get basename of main document without extension."""

        try:
            basename = os.path.basename(self.data.main_file.path)
            extension = self.data.main_file.EXTENSION
            return basename[0:-len(extension)]
        except AttributeError:
            return self.untitle

    def get_main_document_properties(self):
        """
        Get properties of main document.

        Return: (path, format, encoding, newlines) or (None, None, None None)
        """
        try:
            path     = self.data.main_file.path
            format   = self.data.main_file.FORMAT
            encoding = self.data.main_file.encoding
            newlines = self.data.main_file.newlines
            return path, format, encoding, newlines
        except AttributeError:
            return None, None, None, None

    def get_selected_rows(self):
        """Get rows selected in TreeView."""

        selection = self.tree_view.get_selection()
        selected_rows = selection.get_selected_rows()[1]

        # selected_rows is a list of one-tuples of integers. Change that to a
        # list of integers.
        return [row[0] for row in selected_rows]

    def get_timings(self):
        """Return time or frame data depending on edit mode."""
        
        if self.edit_mode == MODE_TIME:
            return self.data.times
        elif self.edit_mode == MODE_FRAME:
            return self.data.frames

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

        try:
            basename = os.path.basename(self.data.tran_file.path)
            extension = self.data.tran_file.EXTENSION
            return basename[0:-len(extension)]
        except AttributeError:
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
            return path, format, encoding, newlines

        elif self.data.main_file is not None:
            path     = None
            format   = self.data.main_file.FORMAT
            encoding = self.data.main_file.encoding
            newlines = self.data.main_file.newlines
            return path, format, encoding, newlines

        else:
            return None, None, None, None

    def _on_notebook_tab_close_button_clicked(self, *args):
        """Emit signal that the Notebook tab close button has been clicked."""
        
        self.emit('notebook-tab-close-button-clicked')

    def _on_tree_view_button_press_event(self, tree_view, event):
        """Emit signal that a TreeView cell has been clicked."""

        # Return True to stop other handlers or False to not to.
        return self.emit('tree-view-button-press-event', event)

    def _on_tree_view_cell_edited(self, cell_renderer, new_value, row, col):
        """Emit signal that a TreeView cell has been edited."""

        self.emit('tree-view-cell-edited', new_value, row, col)

    def _on_tree_view_cell_editing_started(self, cell_renderer, editor, row,
                                           col):
        """Emit signal that a TreeView cell editing has started."""

        self.set_active_column()
        self.emit('tree-view-cell-editing-started', col)

    def _on_tree_view_cursor_moved(self, *args):
        """Emit signal that the TreeView cursor has moved."""

        self.set_active_column()
        self.emit('tree-view-cursor-moved')
        
    def _on_tree_view_headers_clicked(self, button, event):
        """Emit signal that a TreeViewColumn header has been clicked."""

        self.emit('tree-view-headers-clicked', event)

    def _on_tree_view_selection_changed(self, *args):
        """Emit signal that the TreeView selection has changed."""

        self.set_active_column()
        self.emit('tree-view-selection-changed')

    def reload_all_data(self):
        """Reload all data in the TreeView."""
        
        store = self.tree_view.get_model()
        store.clear()

        timings = self.get_timings()

        self.tree_view.freeze_child_notify()

        for i in range(len(self.data.times)):
            store.append([i + 1] + timings[i] + self.data.texts[i])

        self.tree_view.thaw_child_notify()

    def reload_data_between_rows(self, row_x, row_y):
        """Reload TreeView data between given rows."""

        start_row = min(row_x, row_y)
        end_row   = max(row_x, row_y)

        store   = self.tree_view.get_model()
        timings = self.get_timings()
        texts   = self.data.texts

        self.tree_view.freeze_child_notify()

        for i in range(start_row, end_row + 1):
            store[i] = [i + 1] + timings[i] + texts[i]
                        
        self.tree_view.thaw_child_notify()

    def reload_data_in_columns(self, col_list):
        """Reload all data in given columns."""
        
        store = self.tree_view.get_model()

        self.tree_view.freeze_child_notify()

        for col in col_list:

            if col == NO:
            
                for i in range(len(store)):
                    store[i][col] = i + 1
            
            elif col in [SHOW, HIDE, DURN]:

                timings  = self.get_timings()
                data_col = self.get_data_column(col)
                
                for i in range(len(store)):
                    store[i][col] = timings[i][data_col]
                            
            elif col in [TEXT, TRAN]:

                data_col = self.get_data_column(col)
            
                for i in range(len(store)):
                    store[i][col] = self.data.texts[i][data_col]

        self.tree_view.thaw_child_notify()

    def reload_data_in_row(self, row):
        """Reload TreeView data in given row."""

        store   = self.tree_view.get_model()
        timings = self.get_timings()
        texts   = self.data.texts

        store[row] = [row + 1] + timings[row] + texts[row]

    def set_active_column(self, *args):
        """Set the active column title emphasized."""

        col = self.get_focus()[1]

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
