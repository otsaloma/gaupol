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
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Checking and correcting spelling."""

import aeidon

with aeidon.util.silent(Exception):
    from gi.repository import Gspell

__all__ = ("SpellChecker",)


class SpellChecker(aeidon.SpellChecker):

    """Checking the spelling of an individual word."""

    def attach(self, text_view):
        """Attach inline spell-check to `text_view`."""
        text_buffer = text_view.get_buffer()
        gspell_buffer = Gspell.TextBuffer.get_from_gtk_text_buffer(text_buffer)
        gspell_buffer.set_spell_checker(self.checker)
        gspell_view = Gspell.TextView.get_from_gtk_text_view(text_view)
        gspell_view.set_inline_spell_checking(True)
        return gspell_view
