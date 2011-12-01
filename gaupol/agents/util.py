# Copyright (C) 2005-2008,2010 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Miscellaneous helper methods."""

import aeidon
import gaupol
from gi.repository import Gtk


class UtilityAgent(aeidon.Delegate, metaclass=aeidon.Contractual):

    """Miscellaneous helper methods."""

    def get_action_ensure(self, value, name):
        assert value is not None

    @aeidon.deco.export
    def get_action(self, name):
        """Return action from UI manager by `name`."""
        for action_group in self.uim.get_action_groups():
            action = action_group.get_action(name)
            if action is not None: return action
        raise ValueError("Action {} not found".format(repr(name)))

    @aeidon.deco.export
    def get_action_group(self, name):
        """Return action group from UI manager by `name`."""
        groups = self.uim.get_action_groups()
        return [x for x in groups if x.get_name() == name][0]

    @aeidon.deco.export
    def get_column_action(self, field):
        """Return action from UI manager to hide or show column."""
        name = gaupol.field_actions[field]
        return self.get_action(name)

    @aeidon.deco.export
    def get_current_page(self):
        """Return the currently active page or ``None``."""
        index = self.notebook.get_current_page()
        if index < 0: return None
        return self.pages[index]

    @aeidon.deco.export
    def get_framerate_action(self, framerate):
        """Return action from UI manager to select framerate."""
        name = gaupol.framerate_actions[framerate]
        return self.get_action(name)

    @aeidon.deco.export
    def get_menu_item(self, name):
        """Return menu item from UI manager by `name`."""
        widgets = self.get_action(name).get_proxies()
        return [x for x in widgets if isinstance(x, Gtk.MenuItem)][0]

    @aeidon.deco.export
    def get_mode_action(self, mode):
        """Return action from UI manager to select mode."""
        name = gaupol.mode_actions[mode]
        return self.get_action(name)

    @aeidon.deco.export
    def get_target_pages(self, target):
        """Return a sequence of pages corresponding to `target`."""
        if target == gaupol.targets.SELECTED:
            return (self.get_current_page(),)
        if target == gaupol.targets.CURRENT:
            return (self.get_current_page(),)
        if target == gaupol.targets.ALL:
            return tuple(self.pages)
        raise ValueError("Invalid target: {}".format(repr(target)))

    @aeidon.deco.export
    def get_target_rows(self, target):
        """Return rows corresponding to `target` or ``None`` for all."""
        if target != gaupol.targets.SELECTED: return None
        page = self.get_current_page()
        return page.view.get_selected_rows()

    @aeidon.deco.export
    def get_tool_item(self, name):
        """Return tool item from UI manager by `name`."""
        widgets = self.get_action(name).get_proxies()
        return [x for x in widgets if isinstance(x, Gtk.ToolItem)][0]

    def set_current_page_require(self, page):
        assert page in self.pages

    @aeidon.deco.export
    def set_current_page(self, page):
        """Set the currently active page."""
        index = self.pages.index(page)
        self.notebook.set_current_page(index)
