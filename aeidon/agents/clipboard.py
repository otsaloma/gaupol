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

"""Storing text to the clipboard and pasting from it."""

import aeidon

from aeidon.i18n import _


class ClipboardAgent(aeidon.Delegate):

    """Storing text to the clipboard and pasting from it."""

    @aeidon.deco.export
    def copy_texts(self, indices, doc):
        """Copy texts to the clipboard."""
        self.clipboard.clear()
        for index in range(min(indices), max(indices) + 1):
            subtitle = self.subtitles[index]
            text = subtitle.get_text(doc) if index in indices else None
            self.clipboard.append(text)

    @aeidon.deco.export
    @aeidon.deco.revertable
    def cut_texts(self, indices, doc, register=-1):
        """Cut texts to the clipboard."""
        self.copy_texts(indices, doc)
        self.clear_texts(indices, doc, register=register)
        self.set_action_description(register, _("Cutting texts"))

    @aeidon.deco.export
    @aeidon.deco.revertable
    def paste_texts(self, index, doc, register=-1):
        """Paste texts from the clipboard and return pasted indices."""
        texts = self.clipboard.get_texts()
        length = len(self.subtitles)
        new_count = len(texts) - (length - index)
        if new_count > 0:
            indices = list(range(length, length + new_count))
            self.insert_subtitles(indices, register=register)
        indices = [index+i for i in range(len(texts)) if texts[i] is not None]
        new_texts = [x for x in texts if x is not None]
        self.replace_texts(indices, doc, new_texts, register=register)
        if new_count > 0:
            self.group_actions(register, 2, "")
        self.set_action_description(register, _("Pasting texts"))
        return tuple(indices)
