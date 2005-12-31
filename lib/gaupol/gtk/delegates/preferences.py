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


"""Editing preferences."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk
import pango

from gaupol.gtk.delegates           import Delegate, UIMAction
from gaupol.gtk.dialogs.preferences import PreferencesDialog
from gaupol.gtk.util                import config, gtklib


class EditPreferencesAction(UIMAction):

    """Editing settings."""

    uim_action_item = (
        'edit_preferences',
        gtk.STOCK_PREFERENCES,
        _('Pre_ferences'),
        None,
        _('Configure Gaupol'),
        'on_edit_preferences_activated'
    )

    uim_paths = ['/ui/menubar/edit/preferences']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return True


class PreferencesDelegate(Delegate):

    """Configuring Gaupol."""

    def _enforce_new_font(self, font):
        """Apply new font and repaint the view."""

        if not self.pages:
            return

        # Enforce new font choice.
        for page in self.pages:
            for tree_view_column in page.view.get_columns():
                for cell_renderer in tree_view_column.get_cell_renderers():
                    cell_renderer.props.font = font

        # Resize view columns and thus repaint the view.
        page = self.get_current_page()
        page.view.columns_autosize()

    def _enforce_new_undo_levels(self, levels):
        """Cut projects' undo and redo stacks to levels."""

        if not self.pages:
            return

        for page in self.pages:
            while len(page.project.undoables) > levels:
                page.project.undoables.pop()
            while len(page.project.redoables) > levels:
                page.project.redoables.pop()

        self.set_sensitivities()

    def _on_destroyed(self, dialog):
        """Delete dialog."""

        gtklib.destroy_gobject(dialog)

    def _on_font_set(self, dialog, font):
        """Set custom font."""

        if not config.editor.use_default_font:
            self._enforce_new_font(font)

    def _on_limit_undo_toggled(self, dialog, limit):
        """Limit or unlimit undoing."""

        if limit:
            levels = config.editor.undo_levels
            self._enforce_new_undo_levels(levels)

    def on_edit_preferences_activated(self, *args):
        """Show the preferences dialog."""

        dialog = PreferencesDialog(self.window)

        connect = dialog.connect
        connect('destroyed'               , self._on_destroyed               )
        connect('limit-undo-toggled'      , self._on_limit_undo_toggled      )
        connect('undo-levels-changed'     , self._on_undo_levels_changed     )
        connect('use-default-font-toggled', self._on_use_default_font_toggled)
        connect('font-set'                , self._on_font_set                )

        dialog.show()

    def _on_undo_levels_changed(self, dialog, levels):
        """Change amount of undo levels."""

        if config.editor.limit_undo:
            self._enforce_new_undo_levels(levels)

    def _on_use_default_font_toggled(self, dialog, use_default):
        """Change between using default or custom font."""

        if use_default:
            font = ''
        else:
            font = config.editor.font

        self._enforce_new_font(font)
