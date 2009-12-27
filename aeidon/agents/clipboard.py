# Copyright (C) 2005-2007,2009 Osmo Salomaa
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

"""Storing text to the clipboard and pasting from it."""

from __future__ import division

import aeidon
_ = aeidon.i18n._


class ClipboardAgent(aeidon.Delegate):

    """Storing text to the clipboard and pasting from it."""

    __metaclass__ = aeidon.Contractual

    def copy_texts_require(self, indices, doc):
        for index in indices:
            assert 0 <= index < len(self.subtitles)

    def copy_texts_ensure(self, value, indices, doc):
        texts = self.clipboard.get_texts()
        assert len(texts) == len(range(indices[0], indices[-1] + 1))
        while None in texts:
            texts.remove(None)
        assert len(texts) == len(indices)

    def copy_texts(self, indices, doc):
        """Copy texts to the clipboard."""
        self.clipboard.clear()
        for index in range(min(indices), max(indices) + 1):
            subtitle = self.subtitles[index]
            text = (subtitle.get_text(doc) if index in indices else None)
            self.clipboard.append(text)

    def cut_texts_require(self, indices, doc, register=-1):
        for index in indices:
            assert 0 <= index < len(self.subtitles)

    @aeidon.deco.revertable
    def cut_texts(self, indices, doc, register=-1):
        """Cut texts to the clipboard."""
        self.copy_texts(indices, doc)
        self.clear_texts(indices, doc, register=register)
        self.set_action_description(register, _("Cutting texts"))

    def paste_texts_require(self, index, doc, register=-1):
        assert 0 <= index <= len(self.subtitles)
        assert self.clipboard.get_texts()

    @aeidon.deco.revertable
    def paste_texts(self, index, doc, register=-1):
        """Paste texts from the clipboard and return pasted indices."""
        texts = self.clipboard.get_texts()
        length = len(self.subtitles)
        new_count = len(texts) - (length - index)
        if new_count > 0:
            self.insert_blank_subtitles(range(length, length + new_count),
                                        register=register)

        indices = [index + i for i in range(len(texts))
                   if texts[i] is not None]

        new_texts = [x for x in texts if x is not None]
        self.replace_texts(indices, doc, new_texts, register=register)
        if new_count > 0:
            self.group_actions(register, 2, "")
        self.set_action_description(register, _("Pasting texts"))
        return tuple(indices)
