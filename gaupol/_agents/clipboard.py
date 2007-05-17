# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Storing text to the clipboard and pasting from it."""


from __future__ import division

from gaupol.base import Contractual, Delegate
from gaupol.i18n import _
from gaupol.reversion import revertable


class ClipboardAgent(Delegate):

    """Storing text to the clipboard and pasting from it."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = Contractual

    def copy_texts_require(self, indexes, doc):
        for index in indexes:
            assert 0 <= index < len(self.subtitles)

    def copy_texts_ensure(self, value, indexes, doc):
        texts = self.clipboard.get_texts()
        assert len(texts) == len(range(indexes[0], indexes[-1] + 1))
        while None in texts:
            texts.remove(None)
        assert len(texts) == len(indexes)

    def copy_texts(self, indexes, doc):
        """Copy texts to the clipboard."""

        self.clipboard.clear()
        for index in range(min(indexes), max(indexes) + 1):
            subtitle = self.subtitles[index]
            text = (subtitle.get_text(doc) if index in indexes else None)
            self.clipboard.append(text)

    def cut_texts_require(self, indexes, doc, register=-1):
        for index in indexes:
            assert 0 <= index < len(self.subtitles)

    @revertable
    def cut_texts(self, indexes, doc, register=-1):
        """Cut texts to the clipboard."""

        self.copy_texts(indexes, doc)
        self.clear_texts(indexes, doc, register=register)
        self.set_action_description(register, _("Cutting texts"))

    def paste_texts_require(self, index, doc, register=-1):
        assert 0 <= index <= len(self.subtitles)
        assert self.clipboard.get_texts()

    @revertable
    def paste_texts(self, index, doc, register=-1):
        """Paste texts from the clipboard and return pasted indexes."""

        texts = self.clipboard.get_texts()
        length = len(self.subtitles)
        excess = len(texts) - (length - index)
        if excess > 0:
            inserts = range(length, length + excess)
            self.insert_blank_subtitles(inserts, register=register)
        entries = [(i, x) for (i, x) in enumerate(texts)]
        entries = [(i, x) for (i, x) in entries if x is not None]
        indexes = [index + i for (i, x) in entries]
        new_texts = [x for (i, x) in entries]
        self.replace_texts(indexes, doc, new_texts, register=register)
        if excess > 0:
            self.group_actions(register, 2, "")
        self.set_action_description(register, _("Pasting texts"))
        return indexes
