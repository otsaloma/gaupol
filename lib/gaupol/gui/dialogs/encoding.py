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


"""Dialog to select character encodings."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk

from gaupol.gui.util import gui
from gaupol.lib.util import encodings as encodings_module


DESC, NAME, SHOW = 0, 1, 2


class EncodingDialog(object):

    """Dialog to select character encodings."""
    
    def __init__(self, config, parent):

        self._config = config

        glade_xml = gui.get_glade_xml('encoding-dialog.glade')
                            
        self._dialog    = glade_xml.get_widget('dialog')
        self._tree_view = glade_xml.get_widget('tree_view')

        label = glade_xml.get_widget('label')
        label.set_mnemonic_widget(self._tree_view)

        self._build_dialog(parent)
        self._build_tree_view()

    def _build_dialog(self, parent):
        """Build the encoding dialog."""
        
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

        width, height = self._config.getlistint('encoding_dialog', 'size')
        self._dialog.resize(width, height)
    
    def _build_tree_view(self):
        """Build the list of encodings."""

        self._tree_view.columns_autosize()
        
        store = gtk.ListStore(
            gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_BOOLEAN
        )
        self._tree_view.set_model(store)
        
        cr_0 = gtk.CellRendererText()
        cr_1 = gtk.CellRendererText()
        cr_2 = gtk.CellRendererToggle()

        cr_show.connect('toggled', self._on_tree_view_cell_toggled)

        tree_col_0 = gtk.TreeViewColumn(_('Description') , cr_0, text  =0)
        tree_col_1 = gtk.TreeViewColumn(_('Encoding')    , cr_1, text  =1)
        tree_col_2 = gtk.TreeViewColumn(_('Show In Menu'), cr_2, active=2)

        # Set column properties and append columns.
        for i in range(3):
        
            tree_col = eval('tree_col_%d' % i)
            self._tree_view.append_column(tree_col)
            
            tree_col.set_resizable(True)
            tree_col.set_clickable(True)
            
            tree_col.set_sort_column_id(i)
            if i == DESC:
                store.set_sort_column_id(DESC, gtk.SORT_ASCENDING)

        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.unselect_all()

        vis_encs   = self._config.getlist('file', 'visible_encodings')
        valid_encs = encodings_module.get_valid_encodings()
        
        # Insert data.
        for entry in valid_encs:
            store.append([entry[2], entry[1], entry[0] in vis_encs])

    def destroy(self):
        """Destroy the dialog."""
        
        size = self._dialog.get_size()
        self._config.setlistint('encoding_dialog', 'size', size)

        self._dialog.destroy()
        
    def get_encoding(self):
        """
        Get selected encoding.

        Return: encoding or None
        """
        selection = self._tree_view.get_selection()
        store, rows = selection.get_selected_rows()
        
        if not rows:
            return None
        else:
            row = rows[0]
        
        disp_name = store[row][NAME]
        return encodings_module.get_python_name(disp_name)

    def get_visible_encodings(self):
        """Get encodings chosen to be visible."""
        
        store    = self._tree_view.get_model()
        vis_encs = []
        
        for row in range(len(store)):
            if store[row][SHOW]:
                encoding = encodings_module.get_python_name(store[row][NAME])
                vis_encs.append(encoding)
                
        return vis_encs

    def _on_tree_view_cell_toggled(self, cell_rend, row):
        """Toggle the "Show In Menu" column cell value."""

        store = self._tree_view.get_model()
        store[row][SHOW] = not store[row][SHOW]

    def run(self):
        """Show and run the dialog."""
        
        self._dialog.show()
        self._tree_view.grab_focus()
        
        return self._dialog.run()            
