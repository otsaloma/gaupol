# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.


"""Miscellaneous methods for use with Application data editing."""


import gaupol.gtk
import gtk


class UtilityAgent(gaupol.Delegate):

    """Miscellaneous methods for use with Application data editing."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = gaupol.Contractual

    def get_action_ensure(self, value, name):
        assert value is not None

    def get_action(self, name):
        """Get action from the UI manager by name."""

        action_group = self.get_action_group("main")
        return action_group.get_action(name)

    def get_action_group_require(self, name):
        assert name in ("main", "projects")

    def get_action_group(self, name):
        """Get action group from the UI manager."""

        groups = self.uim.get_action_groups()
        return [x for x in groups if x.get_name() == name][0]

    @gaupol.gtk.util.asserted_return
    def get_current_page(self):
        """Get the currently active page or None."""

        index = self.notebook.get_current_page()
        assert index >= 0
        return self.pages[index]

    def get_menu_item(self, name):
        """Get menu item from UI manager by name."""

        widgets = self.get_action(name).get_proxies()
        return [x for x in widgets if isinstance(x, gtk.MenuItem)][0]

    def get_target_pages(self, target):
        """Get a list of pages corresponding to target."""

        if target == gaupol.gtk.TARGET.SELECTED:
            return [self.get_current_page()]
        if target == gaupol.gtk.TARGET.CURRENT:
            return [self.get_current_page()]
        if target == gaupol.gtk.TARGET.ALL:
            return self.pages
        raise ValueError

    @gaupol.gtk.util.asserted_return
    def get_target_rows(self, target):
        """Get the selected rows or None if targeting all rows."""

        assert target == gaupol.gtk.TARGET.SELECTED
        page = self.get_current_page()
        return page.view.get_selected_rows()

    def get_tool_item(self, name):
        """Get tool item from UI manager by name."""

        widgets = self.get_action(name).get_proxies()
        return [x for x in widgets if isinstance(x, gtk.ToolItem)][0]

    def set_current_page_require(self, page):
        assert page in self.pages

    def set_current_page(self, page):
        """Set the currently active page."""

        index = self.pages.index(page)
        self.notebook.set_current_page(index)
