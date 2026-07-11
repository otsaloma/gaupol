# -*- coding: utf-8 -*-

# Copyright (C) 2019 Osmo Salomaa
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Checking and correcting spelling."""

import aeidon
import contextlib

with contextlib.suppress(Exception):
    from gi.repository import GtkSource
    from gi.repository import Spelling

__all__ = ("SpellChecker",)

class SpellChecker(aeidon.SpellChecker):

    """Checking the spelling of an individual word."""

    def attach(self, text_view):
        """Attach inline spell-check to `text_view`."""
        # Spelling.TextBufferAdapter requires a GtkSource.Buffer,
        # replace the text view's blank default buffer with one.
        text_buffer = GtkSource.Buffer()
        text_buffer.set_highlight_matching_brackets(False)
        text_view.set_buffer(text_buffer)
        adapter = Spelling.TextBufferAdapter.new(text_buffer, self.checker)
        text_view.set_extra_menu(adapter.get_menu_model())
        text_view.insert_action_group("spelling", adapter)
        adapter.set_enabled(True)
        return adapter
