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

import gaupol.gtk
import gtk


class UtilityAgent(gaupol.Delegate):

    """Miscellaneous methods for use with application data editing."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = gaupol.Contractual

    def get_action_ensure(self, value, name):
        assert value is not None

    def get_action(self, name):
        """Return action from the UI manager by name."""

        action_group = self.get_action_group("main")
        return action_group.get_action(name)

    def get_action_group_require(self, name):
        assert name in ("main", "projects")

    def get_action_group(self, name):
        """Return action group from the UI manager."""

        groups = self.uim.get_action_groups()
        return [x for x in groups if x.get_name() == name][0]

    def get_column_action(self, field):
        """Return action from UI manager to toggle visibility of column."""

        if field == gaupol.gtk.fields.NUMBER:
            return self.get_action("toggle_number_column")
        if field == gaupol.gtk.fields.START:
            return self.get_action("toggle_start_column")
        if field == gaupol.gtk.fields.END:
            return self.get_action("toggle_end_column")
        if field == gaupol.gtk.fields.DURATION:
            return self.get_action("toggle_duration_column")
        if field == gaupol.gtk.fields.MAIN_TEXT:
            return self.get_action("toggle_main_text_column")
        if field == gaupol.gtk.fields.TRAN_TEXT:
            return self.get_action("toggle_translation_text_column")
        raise ValueError

    def get_current_page(self):
        """Return the currently active page or None."""

        index = self.notebook.get_current_page()
        if index < 0: return None
        return self.pages[index]

    def get_framerate_action(self, framerate):
        """Return action from UI manager to select framerate."""

        if framerate == gaupol.framerates.FPS_24:
            return self.get_action("show_framerate_24")
        if framerate == gaupol.framerates.FPS_25:
            return self.get_action("show_framerate_25")
        if framerate == gaupol.framerates.FPS_30:
            return self.get_action("show_framerate_30")
        raise ValueError

    def get_menu_item(self, name):
        """Return menu item from UI manager by name."""

        widgets = self.get_action(name).get_proxies()
        return [x for x in widgets if isinstance(x, gtk.MenuItem)][0]

    def get_mode_action(self, mode):
        """Return action from UI manager to select mode."""

        if mode == gaupol.modes.TIME:
            return self.get_action("show_times")
        if mode == gaupol.modes.FRAME:
            return self.get_action("show_frames")
        raise ValueError

    def get_target_pages(self, target):
        """Return a sequence of pages corresponding to target."""

        if target == gaupol.gtk.targets.SELECTED:
            return (self.get_current_page(),)
        if target == gaupol.gtk.targets.CURRENT:
            return (self.get_current_page(),)
        if target == gaupol.gtk.targets.ALL:
            return tuple(self.pages)
        raise ValueError

    def get_target_rows(self, target):
        """Return the selected rows or None if targeting all rows."""

        if target != gaupol.gtk.targets.SELECTED: return None
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
