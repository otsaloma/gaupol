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

"""Formatting text."""

import aeidon


class FormatAgent(aeidon.Delegate):

    """Formatting text."""

    @aeidon.deco.export
    def _on_toggle_dialogue_dashes_activate(self, *args):
        """Add or remove dialogue dashes on the selected texts."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = page.text_column_to_document(col)
        page.project.toggle_dialogue_dashes(rows, doc)

    @aeidon.deco.export
    def _on_toggle_italicization_activate(self, *args):
        """Italicize or unitalicize the selected texts."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = page.text_column_to_document(col)
        page.project.toggle_italicization(rows, doc)

    @aeidon.deco.export
    def _on_use_lower_case_activate(self, *args):
        """Change the selected texts to lower case."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = page.text_column_to_document(col)
        page.project.change_case(rows, doc, "lower")

    @aeidon.deco.export
    def _on_use_sentence_case_activate(self, *args):
        """Change the selected texts to sentence case."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = page.text_column_to_document(col)
        page.project.change_case(rows, doc, "capitalize")

    @aeidon.deco.export
    def _on_use_title_case_activate(self, *args):
        """Change the selected texts to title case."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = page.text_column_to_document(col)
        page.project.change_case(rows, doc, "title")

    @aeidon.deco.export
    def _on_use_upper_case_activate(self, *args):
        """Change the selected texts to upper case."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = page.text_column_to_document(col)
        page.project.change_case(rows, doc, "upper")
