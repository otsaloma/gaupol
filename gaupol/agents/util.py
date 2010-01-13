# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Miscellaneous methods for use with application data editing."""

import gaupol
import gtk


class UtilityAgent(aeidon.Delegate):

    """Miscellaneous methods for use with application data editing."""

    __metaclass__ = aeidon.Contractual

    def get_action_ensure(self, value, name):
        assert value is not None

    def get_action(self, name):
        """Return action from the UI manager by name."""

        for action_group in self.uim.get_action_groups():
            action = action_group.get_action(name)
            if action is not None: return action
        raise ValueError("Action group %s not found" % repr(name))

    def get_action_group(self, name):
        """Return action group from the UI manager."""

        groups = self.uim.get_action_groups()
        return [x for x in groups if x.get_name() == name][0]

    def get_column_action(self, field):
        """Return action from UI manager to toggle visibility of column."""

        name = gaupol.field_actions[field]
        return self.get_action(name)

    def get_current_page(self):
        """Return the currently active page or None."""

        index = self.notebook.get_current_page()
        if index < 0: return None
        return self.pages[index]

    def get_framerate_action(self, framerate):
        """Return action from UI manager to select framerate."""

        name = gaupol.framerate_actions[framerate]
        return self.get_action(name)

    def get_menu_item(self, name):
        """Return menu item from UI manager by name."""

        widgets = self.get_action(name).get_proxies()
        return [x for x in widgets if isinstance(x, gtk.MenuItem)][0]

    def get_mode_action(self, mode):
        """Return action from UI manager to select mode."""

        name = gaupol.mode_actions[mode]
        return self.get_action(name)

    def get_target_pages(self, target):
        """Return a sequence of pages corresponding to target."""

        if target == gaupol.targets.SELECTED:
            return (self.get_current_page(),)
        if target == gaupol.targets.CURRENT:
            return (self.get_current_page(),)
        if target == gaupol.targets.ALL:
            return tuple(self.pages)
        raise ValueError("Invalid target: %s" % repr(target))

    def get_target_rows(self, target):
        """Return the selected rows or None if targeting all rows."""

        if target != gaupol.targets.SELECTED: return None
        page = self.get_current_page()
        return page.view.get_selected_rows()

    def get_tool_item(self, name):
        """Return tool item from UI manager by name."""

        widgets = self.get_action(name).get_proxies()
        return [x for x in widgets if isinstance(x, gtk.ToolItem)][0]

    def set_current_page_require(self, page):
        assert page in self.pages

    def set_current_page(self, page):
        """Set the currently active page."""

        index = self.pages.index(page)
        self.notebook.set_current_page(index)
