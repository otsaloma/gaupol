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


"""Configuring Gaupol."""


import pango

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.dialogs.prefs import PreferencesDialog


class PreferenceEditor(Delegate):

    """Configuring Gaupol."""

    def _enforce_new_font(self, font):
        """Apply new font and repaint the TreeView."""

        if not self.projects:
            return

        # Enforce new font choice.
        for project in self.projects:
            for tree_view_column in project.tree_view.get_columns():
                for cell_renderer in tree_view_column.get_cell_renderers():
                    cell_renderer.set_property('font', font)

        # Resize TreeView columns and thus also repaint the TreeView.
        project = self.get_current_project()
        project.tree_view.columns_autosize()

    def _enforce_new_undo_levels(self, levels):
        """Cut projects' undo and redo stacks to levels."""

        if not self.projects:
            return
        
        for project in self.projects:
            while len(project.undoables) > amount:
                project.undoables.pop()
            while len(project.redoables) > amount:
                project.redoables.pop()
        
        self.set_sensitivities()

    def _get_custom_font(self):
        """
        Get custom font.
        
        This method merges the custom font setting with the default font
        taken from a random widget to create to complete font string.
        """
        
        font = self.config.get('view', 'font')

        # Get the default font description from a random widget.
        context = self.notebook.get_pango_context()
        font_description = context.get_font_description()

        # Create custom font description and merge that with the default.
        custom_font_description = pango.FontDescription(font)
        font_description.merge(custom_font_description, True)

        return font_description.to_string()

    def _on_use_default_font_toggled(self, dialog, use_default):
        """Change between using default or custom font."""
        
        self.config.setboolean('view', 'use_default_font', use_default)

        if use_default:
            font = ''
        else:
            font = self.config.get('view', 'font')

        self._enforce_new_font(font)
        
    def _on_font_set(self, dialog, font):
        """Set custom font."""
        
        self.config.set('view', 'font', font)

        if not self.config.getboolean('view', 'use_default_font'):
            self._enforce_new_font(font)

    def on_preferences_activated(self, *args):
        """Show the preferences dialog."""
        
        dialog = PreferencesDialog(self.window)

        # Get settings.
        limit_undo       = self.config.getboolean('editor', 'limit_undo')
        undo_levels      = self.config.getint('editor', 'undo_levels')
        use_default_font = self.config.getboolean('view', 'use_default_font')
        font             = self._get_custom_font()
        
        # Set settings.
        dialog.set_limit_undo(limit_undo)
        dialog.set_undo_levels(undo_levels)
        dialog.set_use_default_font(use_default_font)
        dialog.set_font(font)

        # Connect signals.
        connect = dialog.connect
        connect('limit-undo-toggled'      , self._on_limit_undo_toggled)
        connect('undo-levels-changed'     , self._on_undo_levels_changed)
        connect('use-default-font-toggled', self._on_use_default_font_toggled)
        connect('font-set'                , self._on_font_set)
        
        dialog.show()

    def _on_undo_levels_changed(self, dialog, levels):
        """Change amount of undo levels."""
        
        old_levels = self.config.getint('editor', 'undo_levels')
        self.config.setint('editor', 'undo_levels', levels)
        
        if levels < old_levels:
            if self.config.getboolean('editor', 'limit_undo'):
                self._enforce_new_undo_levels(levels)

    def _on_limit_undo_toggled(self, dialog, limit):
        """Limit or unlimit undoing."""
        
        self.config.setboolean('editor', 'limit_undo', limit)

        if limit:
            levels = self.config.getint('editor', 'undo_levels')
            self._enforce_new_undo_levels(levels)
