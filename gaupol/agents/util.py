# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Miscellaneous helper methods."""

import aeidon
import gaupol

from gi.repository import Gtk


class UtilityAgent(aeidon.Delegate):

    """Miscellaneous helper methods."""

    @aeidon.deco.export
    def get_action(self, name):
        """Return action from UI manager by `name`."""
        for action_group in self.uim.get_action_groups():
            action = action_group.get_action(name)
            if action is not None:
                return action
        raise ValueError("Action {} not found"
                         .format(repr(name)))

    @aeidon.deco.export
    def get_action_group(self, name):
        """Return action group from UI manager by `name`."""
        for group in self.uim.get_action_groups():
            if group.get_name() == name:
                return group
        raise ValueError("Action group {} not found"
                         .format(repr(name)))

    @aeidon.deco.export
    def get_column_action(self, field):
        """Return action from UI manager to hide or show column."""
        return self.get_action(gaupol.field_actions[field])

    @aeidon.deco.export
    def get_current_page(self):
        """Return the currently active page or ``None``."""
        index = self.notebook.get_current_page()
        if index < 0: return None
        return self.pages[index]

    @aeidon.deco.export
    def get_framerate_action(self, framerate):
        """Return action from UI manager to select framerate."""
        return self.get_action(gaupol.framerate_actions[framerate])

    @aeidon.deco.export
    def get_menu_item(self, name):
        """Return menu item from UI manager by `name`."""
        for widget in self.get_action(name).get_proxies():
            if isinstance(widget, Gtk.MenuItem):
                return widget
        raise ValueError("No menu item found for action {}"
                         .format(name))

    @aeidon.deco.export
    def get_mode_action(self, mode):
        """Return action from UI manager to select mode."""
        return self.get_action(gaupol.mode_actions[mode])

    @aeidon.deco.export
    def get_target_pages(self, target):
        """Return a sequence of pages corresponding to `target`."""
        if target == gaupol.targets.SELECTED:
            return (self.get_current_page(),)
        if target == gaupol.targets.SELECTED_TO_END:
            return (self.get_current_page(),)
        if target == gaupol.targets.CURRENT:
            return (self.get_current_page(),)
        if target == gaupol.targets.ALL:
            return tuple(self.pages)
        raise ValueError("Invalid target: {}"
                         .format(repr(target)))

    @aeidon.deco.export
    def get_target_rows(self, target):
        """Return rows corresponding to `target` or ``None`` for all."""
        if target == gaupol.targets.SELECTED:
            page = self.get_current_page()
            return page.view.get_selected_rows()
        if target == gaupol.targets.SELECTED_TO_END:
            page = self.get_current_page()
            rows = page.view.get_selected_rows()
            return list(range(min(rows), len(page.project.subtitles)))
        if target == gaupol.targets.CURRENT:
            return None
        if target == gaupol.targets.ALL:
            return None
        raise ValueError("Invalid target: {}"
                         .format(repr(target)))

    @aeidon.deco.export
    def get_tool_item(self, name):
        """Return tool item from UI manager by `name`."""
        for widget in self.get_action(name).get_proxies():
            if isinstance(widget, Gtk.ToolItem):
                return widget
        raise ValueError("No menu item found for action {}"
                         .format(name))

    @aeidon.deco.export
    def set_current_page(self, page):
        """Set the currently active page."""
        index = self.pages.index(page)
        self.notebook.set_current_page(index)
