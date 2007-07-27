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

"""Formatting text."""

import gaupol.gtk


class FormatAgent(gaupol.Delegate):

    """Formatting text."""

    # pylint: disable-msg=E0203,W0201

    def _change_case(self, method):
        """Change the case of the selected texts.

        method should be 'title', 'capitalize', 'upper' or 'lower'.
        """
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = gaupol.gtk.util.text_column_to_document(col)
        page.project.change_case(rows, doc, method)

    def on_toggle_dialogue_lines_activate(self, *args):
        """Toggle dialogue lines on the selected texts."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = gaupol.gtk.util.text_column_to_document(col)
        page.project.toggle_dialogue_lines(rows, doc)

    def on_toggle_italicization_activate(self, *args):
        """Toggle italicization of the selected texts."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = gaupol.gtk.util.text_column_to_document(col)
        page.project.toggle_italicization(rows, doc)

    def on_use_lower_case_activate(self, *args):
        """Change the selected texts to lower case."""

        self._change_case("lower")

    def on_use_sentence_case_activate(self, *args):
        """Change the selected texts to sentence case."""

        self._change_case("capitalize")

    def on_use_title_case_activate(self, *args):
        """Change the selected texts to title case."""

        self._change_case("title")

    def on_use_upper_case_activate(self, *args):
        """Change the selected texts to upper case."""

        self._change_case("upper")
