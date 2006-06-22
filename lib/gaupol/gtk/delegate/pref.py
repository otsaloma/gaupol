# Copyright (C) 2005-2006 Osmo Salomaa
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


from gettext import gettext as _

import gtk

from gaupol.gtk.delegate    import Delegate, UIMAction
from gaupol.gtk.dialog.pref import PreferencesDialog
from gaupol.gtk.util        import conf, gtklib


class EditPreferencesAction(UIMAction):

    """Editing settings."""

    action_item = (
        'edit_preferences',
        gtk.STOCK_PREFERENCES,
        _('Pre_ferences'),
        None,
        _('Configure Gaupol'),
        'on_edit_preferences_activate'
    )

    paths = ['/ui/menubar/edit/preferences']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return True


class PreferencesDelegate(Delegate):

    """Editing preferences."""

    def __init__(self, *args, **kwargs):

        Delegate.__init__(self, *args, **kwargs)

        self._dialog = None

    def _enforce_font(self, font):
        """Apply new font and redraw view."""

        for page in self.pages:
            for column in page.view.get_columns():
                for renderer in column.get_cell_renderers():
                    renderer.props.font = font

        if self.pages:
            page = self.get_current_page()
            page.view.columns_autosize()

    def _enforce_undo_levels(self, levels):
        """Cut undo and redo stacks to levels."""

        for page in self.pages:
            while len(page.project.undoables) > levels:
                page.project.undoables.pop()
            while len(page.project.redoables) > levels:
                page.project.redoables.pop()

        self.set_sensitivities()

    def _on_dialog_destroyed(self, dialog):
        """Destroy dialog."""

        gtklib.destroy_gobject(dialog)
        self._dialog = None

    def _on_dialog_font_set(self, dialog, font):
        """Set custom font."""

        if not conf.editor.use_default_font:
            self._enforce_font(font)

    def _on_dialog_limit_undo_toggled(self, dialog, limit):
        """Limit or unlimit undo levels."""

        if limit:
            self._enforce_undo_levels(conf.editor.undo_levels)

    def _on_dialog_undo_levels_changed(self, dialog, levels):
        """Change amount of undo levels."""

        if conf.editor.limit_undo:
            self._enforce_undo_levels(levels)

    def _on_dialog_use_default_font_toggled(self, dialog, use_default):
        """Use default or custom font."""

        if use_default:
            self._enforce_font('')
        else:
            self._enforce_font(conf.editor.font)

    def _on_dialog_video_player_set(self, dialog):
        """Set sensitivities."""

        self.set_sensitivities()

    def on_edit_preferences_activate(self, *args):
        """Show preferences dialog."""

        if self._dialog is not None:
            self._dialog.present()
            return

        self._dialog = PreferencesDialog()
        gtklib.connect(self, '_dialog', 'destroyed'               )
        gtklib.connect(self, '_dialog', 'font-set'                )
        gtklib.connect(self, '_dialog', 'limit-undo-toggled'      )
        gtklib.connect(self, '_dialog', 'undo-levels-changed'     )
        gtklib.connect(self, '_dialog', 'use-default-font-toggled')
        gtklib.connect(self, '_dialog', 'video-player-set'        )
        self._dialog.show()
