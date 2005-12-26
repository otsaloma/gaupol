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


"""Formatting text."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.gtk.colconstants import *
from gaupol.gtk.delegates    import Action, Delegate


class FormatAction(Action):

    """Base class for text formatting actions."""

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False

        selection = bool(page.view.get_selected_rows())
        focus = page.view.get_focus()[1] in (MTXT, TTXT)
        return bool(selection and focus)


class ToggleDialogLinesAction(FormatAction):

    """Toggling dialog lines."""

    uim_action_item = (
        'toggle_dialog_lines',
        None,
        _('_Dialog'),
        '<control>D',
        _('Toggle dialog lines on the selected texts'),
        'on_toggle_dialog_lines_activated'
    )

    uim_paths = ['/ui/menubar/format/dialog']


class PreferencesDelegate(Delegate):

    """Formatting text."""

    def on_toggle_dialog_lines_activated(self, *args):
        """Toggle dialog lines."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col  = page.view.get_focus()[1]
        doc  = col - 4

        page.project.toggle_dialog_lines(rows, doc)
        self.set_sensitivities(page)


