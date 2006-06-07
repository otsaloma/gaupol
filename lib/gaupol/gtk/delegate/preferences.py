# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Editing preferences."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _

import gtk
import pango

from gaupol.gtk.delegate            import Delegate, UIMAction
from gaupol.gtk.dialog.preferences import PreferencesDialog
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

    def on_edit_preferences_activated(self, *args):
        """Show the preferences dialog."""

        dialog = PreferencesDialog(self.window)

        connections = (
            ('destroyed'               , '_on_destroyed'               ),
            ('limit-undo-toggled'      , '_on_limit_undo_toggled'      ),
            ('undo-levels-changed'     , '_on_undo_levels_changed'     ),
            ('use-default-font-toggled', '_on_use_default_font_toggled'),
            ('font-set'                , '_on_font_set'                ),
        )
        for signal, method in connections:
            method = getattr(self, method)
            dialog.connect(signal, method)

        dialog.show()

    def _on_font_set(self, dialog, font):
        """Set custom font."""

        if not config.Editor.use_default_font:
            self._enforce_new_font(font)

    def _on_limit_undo_toggled(self, dialog, limit):
        """Limit or unlimit undoing."""

        if limit:
            levels = config.Editor.undo_levels
            self._enforce_new_undo_levels(levels)

    def _on_undo_levels_changed(self, dialog, levels):
        """Change amount of undo levels."""

        if config.Editor.limit_undo:
            self._enforce_new_undo_levels(levels)

    def _on_use_default_font_toggled(self, dialog, use_default):
        """Change between using default or custom font."""

        if use_default:
            font = ''
        else:
            font = config.Editor.font
        self._enforce_new_font(font)


if __name__ == '__main__':

    from gaupol.gtk.app import Application
    from gaupol.test            import Test

    class TestPreferencesDelegate(Test):

        def __init__(self):

            Test.__init__(self)
            self.application = Application()
            self.application.open_main_files([self.get_subrip_path()])
            self.delegate = PreferencesDelegate(self.application)

        def destroy(self):

            self.application.window.destroy()

        def test_all(self):

            dialog = None
            self.delegate._enforce_new_font('monospace 10')
            self.delegate._enforce_new_undo_levels(2)
            self.delegate._on_font_set(dialog, 'monospace 9')
            self.delegate._on_limit_undo_toggled(dialog, True)
            self.delegate._on_undo_levels_changed(dialog, 1)
            self.delegate._on_use_default_font_toggled(dialog, False)
            self.application.on_edit_preferences_activated()

    TestPreferencesDelegate().run()

