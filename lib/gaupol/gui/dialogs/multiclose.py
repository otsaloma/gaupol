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


"""Warning dialog displayed when trying to close multiple documents."""


import logging
import os
import sys

try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk
import gtk.glade

from gaupol.paths import GLADE_DIR


logger = logging.getLogger()


GLADE_XML_PATH = os.path.join(GLADE_DIR, 'multi-close-dialog.glade')
SAVE, PROJ = 0, 1


class MultiCloseWarningDialog(gtk.Dialog):
    
    """
    Warning dialog displayed when trying to close multiple documents.

    Will be displayed when quitting or closing a tab with at least two
    documents open with unsaved changes.
    """
    
    def __init__(self, parent, projects):
        """
        Initialize a MultiCloseWarningDialog object.
        
        All projects or only a subset list can be given. Changed-ness will
        be checked in this class.
        """
        try:
            glade_xml = gtk.glade.XML(GLADE_XML_PATH)
        except RuntimeError:
            logger.critical('Failed to import Glade XML file "%s".' \
                            % GLADE_XML_PATH) 
            sys.exit()

        self._projects   = projects

        self._main_count = 0
        self._tran_count = 0

        # Widgets
        self._dialog         = glade_xml.get_widget('dialog')
        self._main_tree_view = glade_xml.get_widget('main_document_tree_view')
        self._tran_tree_view = glade_xml.get_widget( \
                                             'translation_document_tree_view')
        self._save_button    = glade_xml.get_widget('save_button')
        self._title_label    = glade_xml.get_widget('title_label')

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_YES)

        self._build_main_tree_view(glade_xml)
        self._build_translation_tree_view(glade_xml)
        self._set_title()

        self._save_button.grab_focus()

        self._dialog.show()

    def _build_main_tree_view(self, glade_xml):
        """Build the list of main documents."""
        
        label = glade_xml.get_widget('main_document_label')
        label.set_mnemonic_widget(self._main_tree_view)
        self._main_tree_view, store = \
            self._build_tree_view(self._main_tree_view, 'main')

        # Insert data.
        for project in self._projects:
            if project.main_changed:
                self._main_count += 1
                store.append([True, project])

        # Set sensible size for TreeView. 24 pixels are added to account for
        # possible scroll bar.
        width, height = self._main_tree_view.size_request()
        width  = min(150, width  + 24)
        height = min(126, height + 24)
        self._main_tree_view.set_size_request(width, height)
        
        if self._main_count == 0:
            glade_xml.get_widget('main_document_label').hide()
            glade_xml.get_widget('main_document_scrolled_window').hide()

    def _build_translation_tree_view(self, glade_xml):
        """Build the list of translation documents."""
        
        label = glade_xml.get_widget('translation_document_label')
        label.set_mnemonic_widget(self._tran_tree_view)
        self._tran_tree_view, store = \
            self._build_tree_view(self._tran_tree_view, 'translation')

        # Insert data.
        for project in self._projects:
            if project.tran_changed:
                self._tran_count += 1
                store.append([True, project])

        # Set sensible size for TreeView. 24 pixels are added to account for
        # possible scroll bar.
        width, height = self._tran_tree_view.size_request()
        width  = min(150, width  + 24)
        height = min(126, height + 24)
        self._tran_tree_view.set_size_request(width, height)

        if self._tran_count == 0:
            glade_xml.get_widget('translation_document_label').hide()
            glade_xml.get_widget('translation_document_scrolled_window').hide()

    def _build_tree_view(self, tree_view, file_type):
        """
        Build properties for tree_view.
        
        file_type: "main" or "translation"
        """
        # This method adaptively copied from Gazpacho by Lorenzo Gil Sanchez.
        # Gazpacho has a similar dialog made without using glade. 
    
        store = gtk.ListStore(gobject.TYPE_BOOLEAN, object)

        tree_view.set_model(store)
        tree_view.set_headers_visible(False)
        
        # Check-box column.
        cr_toggle = gtk.CellRendererToggle()
        cr_toggle.set_property('activatable', True)
        cr_toggle.connect('toggled', self._on_tree_view_cell_toggled, store)
        toggle_col = gtk.TreeViewColumn('Save', cr_toggle)
        toggle_col.add_attribute(cr_toggle, 'active', SAVE)
        tree_view.append_column(toggle_col)

        # File basename column rendering function.
        def render_basename_column(tree_col, cell_rend, store, tree_iter):
            project = store.get_value(tree_iter, PROJ)
            basename = eval('project.get_%s_basename()' % file_type)
            cell_rend.set_property('text', basename)

        # File basename column.
        cr_text = gtk.CellRendererText()        
        text_col = gtk.TreeViewColumn('Document', cr_text)
        text_col.set_cell_data_func(cr_text, render_basename_column)
        tree_view.append_column(text_col)

        return tree_view, store

    def destroy(self):
        """Destroy the dialog."""
        
        self._dialog.destroy()

    def get_main_projects_to_save(self):
        """Get projects, whose main files were chosen to be saved."""
        
        store    = self._main_tree_view.get_model()
        projects = []
        
        for i in range(len(store)):
            if store[i][SAVE]:
                projects.append(store[i][PROJ])
                
        return projects

    def get_translation_projects_to_save(self):
        """Get projects, whose translation files were chosen to be saved."""
        
        store   = self._tran_tree_view.get_model()
        projects = []
        
        for i in range(len(store)):
            if store[i][SAVE]:
                projects.append(store[i][PROJ])
                
        return projects

    def _on_tree_view_cell_toggled(self, cell_rend, path, store):
        """Toggle the value on the checkmark column."""

        store[path][SAVE] = not store[path][SAVE]

        mains = self.get_main_projects_to_save()
        trans = self.get_translation_projects_to_save()

        # Set save button's sensitivity.
        if not mains and not trans:
            self._save_button.set_sensitive(False)
        else:
            self._save_button.set_sensitive(True)

    def run(self):
        """Run the dialog."""
        
        return self._dialog.run()
        
    def _set_title(self):
        """Set dialog title based on amount of documents."""
        
        title = ''

        if self._main_count > 1 and self._tran_count == 0:
            title = _('There are %d subtitle documents with unsaved changes.') \
                    % self._main_count

        elif self._main_count == 1 and self._tran_count == 0:
            title = _('There is %d subtitle document with unsaved changes.') \
                    % self._main_count

        elif self._main_count > 1 and self._tran_count > 1:
            title = _('There are %d subtitle documents and %d translation documents with unsaved changes.') \
                    % (self._main_count, self._tran_count)

        elif self._main_count == 1 and self._tran_count > 1:
            title = _('There is %d subtitle document and %d translation documents with unsaved changes.') \
                    % (self._main_count, self._tran_count)

        elif self._main_count > 1 and self._tran_count == 1:
            title = _('There are %d subtitle documents and %d translation document with unsaved changes.') \
                    % (self._main_count, self._tran_count)
                    
        elif self._main_count == 0 and self._tran_count > 1:
            title = _('There are %d translation documents with unsaved changes.') \
                    % self._tran_count

        elif self._main_count == 0 and self._tran_count == 1:
            title = _('There is %d translation document with unsaved changes.') \
                    % self._tran_count

        title       = _('%s Save changes before closing?') % title
        fancy_title = '<span weight="bold" size="larger">%s</span>\n' % title
        
        self._title_label.set_text(fancy_title)
        self._title_label.set_use_markup(True)
