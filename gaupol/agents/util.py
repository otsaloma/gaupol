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


class UtilityAgent(aeidon.Delegate):

    """Miscellaneous helper methods."""

    @aeidon.deco.export
    def get_action(self, name):
        """Return user-activatable action by `name`."""
        return self.window.lookup_action(name)

    @aeidon.deco.export
    def get_column_action(self, field):
        """Return action to hide or show column."""
        return self.get_action({
            gaupol.fields.NUMBER:    "toggle-number-column",
            gaupol.fields.START:     "toggle-start-column",
            gaupol.fields.END:       "toggle-end-column",
            gaupol.fields.DURATION:  "toggle-duration-column",
            gaupol.fields.MAIN_TEXT: "toggle-main-text-column",
            gaupol.fields.TRAN_TEXT: "toggle-translation-text-column",
        }[field])

    @aeidon.deco.export
    def get_current_page(self):
        """Return the currently active page or ``None``."""
        index = self.notebook.get_current_page()
        if index < 0: return None
        return self.pages[index]

    @aeidon.deco.export
    def get_menubar_section(self, id):
        """Return menubar section by its `id` attribute."""
        if not hasattr(gaupol, "appman"): return None
        return gaupol.appman.menubar_builder.get_object(id)

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
        raise ValueError("Invalid target: {!r}"
                         .format(target))

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
        if target == gaupol.targets.CURRENT: return None
        if target == gaupol.targets.ALL: return None
        raise ValueError("Invalid target: {!r}"
                         .format(target))

    @aeidon.deco.export
    def set_current_page(self, page):
        """Set the currently active page."""
        if page is None: return
        index = self.pages.index(page)
        self.notebook.set_current_page(index)
