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

from gaupol.constants import FRAMERATE, MODE, TYPE
from gaupol.gui.cellrend.integer import CellRendererInteger
from gaupol.gui.cellrend.multiline import CellRendererMultilineText
from gaupol.gui.cellrend.time import CellRendererTime
from gaupol.gui.colcons import *
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

        framerate_name = config.get('editor', 'framerate')
        framerate = FRAMERATE.NAMES.index(framerate_name)

        edit_mode_name = config.get('editor', 'edit_mode')
        edit_mode = MODE.NAMES.index(edit_mode_name)

        self.data      = Data(framerate)
        self.untitle   = _('Untitled %d') % counter
        self.edit_mode = edit_mode

        # True, if translation file exists or any action affecting translation
        # only has been performed.
        self.tran_active = False

        # Doing and redoing will increase changed value by one. Undoing will
        # decrease changed value by one. At zero the document is at its
        # unchanged (saved) state.
        self.main_changed = 0
        self.tran_changed = 0

        # Stacks of actions of type DURAction.  
        self.undoables = []
        self.redoables = []

        # Widgets
        self.tab_label      = None
        self.tab_menu_label = None
        self.tree_view      = None
        self.tooltips       = gtk.Tooltips()

        self.build_tree_view()

    def build_tree_view(self):
        """Build the TreeView used to display subtitle data."""
        
        self.tree_view = gtk.TreeView()

        self.tree_view.set_headers_visible(True)
        self.tree_view.set_rules_hint(True)
        self.tree_view.set_enable_search(False)
        self.tree_view.columns_autosize()

        method = self._on_tree_view_cursor_moved
        self.tree_view.connect_after('move-cursor', method)

        method = self._on_tree_view_button_press_event
        self.tree_view.connect('button-press-event', method)

        selection = self.tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_MULTIPLE)
        selection.unselect_all()
        selection.connect('changed', self._on_tree_view_selection_changed)

        if self.edit_mode == MODE.TIME:
            columns = [gobject.TYPE_INT] + [gobject.TYPE_STRING] * 5
            cell_renderer_1 = CellRendererTime()
            cell_renderer_2 = CellRendererTime()
            cell_renderer_3 = CellRendererTime()

        elif self.edit_mode == MODE.FRAME:
            columns = [gobject.TYPE_INT] * 4 + [gobject.TYPE_STRING] * 2
            cell_renderer_1 = CellRendererInteger()
            cell_renderer_2 = CellRendererInteger()
            cell_renderer_3 = CellRendererInteger()

        cell_renderer_0 = CellRendererInteger()
        cell_renderer_4 = CellRendererMultilineText()
        cell_renderer_5 = CellRendererMultilineText()

        font = self._config.get('view', 'font')

        signals   = (
            'editing-started',
            'edited',
        )
        callbacks = (
            self._on_tree_view_cell_editing_started,
            self._on_tree_view_cell_edited,
        )

        # Set CellRenderer properties.
        for i in range(6):
        
            cell_renderer = eval('cell_renderer_%d' % i)
            
            if i != 0:
                cell_renderer.set_editable(True)
            cell_renderer.set_property('font', font)

            for k in range(len(signals)):
                cell_renderer.connect(signals[k], callbacks[k], i)

        model = gtk.ListStore(*columns)
        self.tree_view.set_model(model)

        TVC = gtk.TreeViewColumn

        tree_view_column_0 = TVC(_('No')         , cell_renderer_0, text=0)
        tree_view_column_1 = TVC(_('Show')       , cell_renderer_1, text=1)
        tree_view_column_2 = TVC(_('Hide')       , cell_renderer_2, text=2)
        tree_view_column_3 = TVC(_('Duration')   , cell_renderer_3, text=3)
        tree_view_column_4 = TVC(_('Text')       , cell_renderer_4, text=4)
        tree_view_column_5 = TVC(_('Translation'), cell_renderer_5, text=5)

        visible_columns = self._config.getlist('view', 'columns')
        
        # Set column properties and append them to the TreeView.
        for i in range(6):
        
            tree_view_column = eval('tree_view_column_%d' % i)
            self.tree_view.append_column(tree_view_column)

            tree_view_column.set_clickable(True)
            tree_view_column.set_resizable(True)

            column_name = COLUMN.NAMES[i]
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
            widget = tree_view_column.get_widget()
            button = gui.get_parent_widget(widget, gtk.Button)

            # Allow TreeViewColumn header to be clicked.
            signal = 'button-press-event'
            method = self._on_tree_view_headers_clicked
            button.connect(signal, method)

    def get_data_column(self, col):
        """Get Data column to match ListStore column."""
        
        if col == NO:
            return None
        if col in [SHOW, HIDE, DURN]:
            return col - 1
        if col in [TEXT, TRAN]:
            return col - 4

    def get_document_type(self, col):
        """Get constant for the type of document in col."""
        
        if col == TRAN:
            return TYPE.TRAN
        else:
            return TYPE.MAIN

    def get_focus(self):
        """
        Get the location of current TreeView focus.
        
        Return: row, column, gtk.TreeViewColumn (any of which could be None)
        """
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

    def get_selected_rows(self):
        """Get rows selected in TreeView."""

        selection = self.tree_view.get_selection()
        selected_rows = selection.get_selected_rows()[1]

        # selected_rows is a list of one-tuples of integers. Change that to a
        # list of integers.
        return [row[0] for row in selected_rows]

    def get_tab_widget(self):
        """Build notebook tab labels and return notebook tab widget."""

        title = self.get_main_basename()
        
        # Tab label
        self.tab_label = gtk.Label(title)
        self.tab_label.set_ellipsize(pango.ELLIPSIZE_MIDDLE)
        self.tab_label.set_max_width_chars(24)

        # Event box for tooltip
        event_box = gtk.EventBox()
        event_box.add(self.tab_label)
        self.tooltips.set_tip(event_box, title)

        # Tab close image
        image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        width, height = image.size_request()

        # Tab close button
        button = gtk.Button()
        button.add(image)
        button.set_relief(gtk.RELIEF_NONE)
        button.set_size_request(width + 2, height + 2)
        button.connect('clicked', self._on_notebook_tab_close_button_clicked)

        # Tab horizontal box
        tab_widget = gtk.HBox(False, 4)
        tab_widget.pack_start(event_box, True , True , 0)
        tab_widget.pack_start(button   , False, False, 0)
        tab_widget.show_all()

        # Tab menu label.
        self.tab_menu_label = gtk.Label(title)
        self.tab_menu_label.set_property('xalign', 0)

        return tab_widget

    def get_timings(self):
        """Return time or frame data depending on edit mode."""
        
        if self.edit_mode == MODE.TIME:
            return self.data.times
        elif self.edit_mode == MODE.FRAME:
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
        """Emit signal that the focus in the TreeView has moved."""

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

        model = self.tree_view.get_model()
        self.tree_view.set_model(None)
        model.clear()

        timings = self.get_timings()
        texts   = self.data.texts

        for i in range(len(self.data.times)):
            model.append([i + 1] + timings[i] + texts[i])
            
        self.tree_view.set_model(model)

    def reload_data_between_rows(self, row_x, row_y):
        """Reload TreeView data between row_x and row_y."""

        start_row = min(row_x, row_y)
        end_row   = max(row_x, row_y)

        model   = self.tree_view.get_model()
        self.tree_view.set_model(None)
        
        timings = self.get_timings()
        texts   = self.data.texts

        for i in range(start_row, end_row + 1):
            model[i] = [i + 1] + timings[i] + texts[i]

        self.tree_view.set_model(model)

    def reload_data_in_columns(self, cols):
        """
        Reload all data in given columns.
        
        cols: string (for single column) or list (for multiple columns)
        """
        if isinstance(cols, basestring):
            cols = [cols]

        model = self.tree_view.get_model()
        self.tree_view.set_model(None)

        for col in cols:

            if col == NO:
            
                for i in range(len(model)):
                    model[i][col] = i + 1
            
            elif col in [SHOW, HIDE, DURN]:

                timings  = self.get_timings()
                data_col = self.get_data_column(col)
                
                for i in range(len(model)):
                    model[i][col] = timings[i][data_col]
                            
            elif col in [TEXT, TRAN]:

                texts    = self.data.texts
                data_col = self.get_data_column(col)
            
                for i in range(len(model)):
                    model[i][col] = self.data.texts[i][data_col]

        self.tree_view.set_model(model)

    def reload_data_in_row(self, row):
        """Reload TreeView data in given row."""

        model = self.tree_view.get_model()
        timings = self.get_timings()
        texts   = self.data.texts

        model[row] = [row + 1] + timings[row] + texts[row]

    def set_active_column(self, *args):
        """Emphasize the active column title."""

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
        if self.main_changed:
            title = '*' + title
        elif self.tran_active and self.tran_changed:
            title = '*' + title
        
        self.tab_label.set_text(title)
        self.tab_menu_label.set_text(title)

        event_box = gui.get_event_box(self.tab_label)
        self.tooltips.set_tip(event_box, title)

        return title


gobject.type_register(Project)
