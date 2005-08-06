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


"""Alterer of how documents and application are displayed."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.gui.constants import COLUMN_NAMES
from gaupol.gui.constants import FRAMERATE_NAMES
from gaupol.gui.constants import NO, SHOW, HIDE, DURN, ORIG, TRAN
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.util import gui


class Viewer(Delegate):

    """Alterer of how documents and application are displayed."""

    def on_edit_mode_toggled(self, some_action, new_action):
        """Change edit mode."""

        project = self.get_current_project()

        # Cut off the plural "s".
        new_edit_mode = new_action.get_name()[:-1]

        # Return if only refreshing widget state.
        if new_edit_mode == project.edit_mode:
            return

        gui.set_cursor_busy(self.window)
        store = project.tree_view.get_model()
        has_focus = project.tree_view.get_property('has-focus')

        project.edit_mode = new_edit_mode
        self.config.set('editor', 'edit_mode', new_edit_mode)

        # Get sort order.
        sort_col, sort_order = store.get_sort_column_id()

        # Get focus.
        focus_row, focus_col = project.get_store_focus()

        # Get selection.
        sel_data_rows = project.get_selected_data_rows()
        sel_subs      = [i + 1 for i in sel_data_rows]

        # Remove tree view.
        scroller = project.tree_view.get_parent()
        scroller.remove(project.tree_view)
        
        project.build_tree_view()

        # Add tree view.
        scroller.add(project.tree_view)
        scroller.show_all()
        
        project.reload_all_data()
        project.tree_view.columns_autosize()
        store = project.tree_view.get_model()

        # Set sort order.
        store.set_sort_column_id(sort_col, sort_order)

        # Restore focus.
        tree_col = project.tree_view.get_column(focus_col)
        project.tree_view.set_cursor(focus_row, tree_col)

        # Set selection.
        selection = project.tree_view.get_selection()
        for i in range(len(store)):
            if store[i][NO] in sel_subs:
                selection.select_path(i)

        project.tree_view.set_property('has-focus', has_focus)
        gui.set_cursor_normal(self.window)

    def on_framerate_changed(self, *args):
        """
        Change framerate.
        
        This method is called from the framerate combo box.
        """
        project = self.get_current_project()

        # Get new framerate.
        index     = self.fr_cmbox.get_active()
        framerate = FRAMERATE_NAMES[index]

        # Return if only refreshing widget state.
        if framerate == project.data.framerate:
            return

        gui.set_cursor_busy(self.window)

        # Set new framerate and save setting.
        project.data.change_framerate(framerate)
        self.config.set('editor', 'framerate', framerate)

        # Set the correct framerate menu item active.
        path = '/ui/menubar/view/framerate/%s' % framerate
        self.uim.get_widget(path).set_active(True)
        
        if project.edit_mode != project.data.main_file.MODE:
            project.reload_data_in_columns([SHOW, HIDE, DURN])

        gui.set_cursor_normal(self.window)

    def on_framerate_toggled(self, some_action, new_action):
        """
         Change framerate.
        
        This method is called from the menu.
        """
        project = self.get_current_project()

        # Get new framerate.
        framerate = new_action.get_name()
        index     = FRAMERATE_NAMES.index(framerate)

        # Return if only refreshing widget state.
        if framerate == project.data.framerate:
            return

        gui.set_cursor_busy(self.window)

        # Set new framerate and save setting.
        project.data.change_framerate(framerate)
        self.config.set('editor', 'framerate', framerate)

        # Set the correct framerate combo box entry active.
        self.fr_cmbox.set_active(index)
        
        if project.edit_mode != project.data.main_file.MODE:
            project.reload_data_in_columns([SHOW, HIDE, DURN])

        gui.set_cursor_normal(self.window)

    def on_statusbar_toggled(self, *args):
        """Toggle visibility of the statusbar."""

        visible = not self.stbar_hbox.get_property('visible')
        
        self.stbar_hbox.set_property('visible', visible)
        self.config.setboolean('view', 'statusbar', visible)

    def on_toolbar_toggled(self, *args):
        """Toggle visibility of the toolbar."""
        
        toolbar = self.uim.get_widget('/ui/toolbar')
        visible = not toolbar.get_property('visible')
        
        toolbar.set_property('visible', visible)
        self.config.setboolean('view', 'toolbar', visible)

    def on_tree_view_column_toggled(self, toggle_action):
        """Toggle visibility of TreeView column."""

        project = self.get_current_project()

        name  = toggle_action.get_name()
        index = COLUMN_NAMES.index(name)

        tree_col = project.tree_view.get_column(index)
        visible = tree_col.get_visible()

        path = '/ui/menubar/view/columns/%s' % name
        action = self.uim.get_action(path)
        active = action.get_active()

        # Return if only refreshing widget state.
        if active is visible:
            return

        gui.set_cursor_busy(self.window)
        tree_col.set_visible(not visible)
        vis_cols = []
        
        for i in range(len(COLUMN_NAMES)):
            if project.tree_view.get_column(i).get_visible():
                vis_cols.append(COLUMN_NAMES[i])
        
        self.config.setlist('view', 'columns', vis_cols)

        self.set_sensitivities()
        gui.set_cursor_normal(self.window)

    def on_tree_view_headers_clicked(self, button, event):
        """
        Show a popup menu when list headers are right-clicked.
        
        Popup menu allows showing/hiding list columns.
        """
        if event.button == 3:
            menu = self.uim.get_widget('/ui/column_popup')
            menu.popup(None, None, None, event.button, event.time)
