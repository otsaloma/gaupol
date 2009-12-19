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

"""Basic subtitle data editing."""

from __future__ import division

import aeidon
_ = aeidon.i18n._


class EditAgent(aeidon.Delegate):

    """Basic subtitle data editing."""

    __metaclass__ = aeidon.Contractual

    def clear_texts_require(self, indices, doc, register=-1):
        for index in indices:
            assert 0 <= index < len(self.subtitles)

    @aeidon.deco.revertable
    def clear_texts(self, indices, doc, register=-1):
        """Set texts to blank strings."""

        new_texts =  ["" for x in indices]
        self.replace_texts(indices, doc, new_texts, register=register)
        self.set_action_description(register, _("Clearing texts"))

    @aeidon.deco.revertable
    @aeidon.deco.notify_frozen
    def insert_blank_subtitles(self, indices, register=-1):
        """Insert blank subtitles with fitting positions."""

        for rindices in aeidon.util.get_ranges(indices):
            first_start = 0.0
            if self.subtitles and (rindices[0] == 0):
                start = self.subtitles[0].start_seconds
                first_start = (0.0 if start >= 0 else start - 3.0)
            if rindices[0] > 0:
                subtitle = self.subtitles[rindices[0] - 1]
                first_start = subtitle.end_seconds
            duration = 3.0
            if rindices[0] < len(self.subtitles):
                subtitle = self.subtitles[rindices[0]]
                window = subtitle.start_seconds - first_start
                duration = window / len(rindices)
            for i, index in enumerate(rindices):
                subtitle = self.get_subtitle()
                subtitle.start = first_start + (i * duration)
                subtitle.end = first_start + ((i + 1) * duration)
                self.subtitles.insert(index, subtitle)

        action = self.get_revertable_action(register)
        action.docs = tuple(aeidon.documents)
        action.description = _("Inserting subtitles")
        action.revert_function = self.remove_subtitles
        action.revert_args = (indices,)
        self.register_action(action)
        self.emit("subtitles-inserted", indices)

    @aeidon.deco.revertable
    @aeidon.deco.notify_frozen
    def insert_subtitles(self, indices, subtitles, register=-1):
        """Insert given subtitles."""

        for i, index in enumerate(indices):
            self.subtitles.insert(index, subtitles[i])

        action = self.get_revertable_action(register)
        action.docs = tuple(aeidon.documents)
        action.description = _("Inserting subtitles")
        action.revert_function = self.remove_subtitles
        action.revert_args = (indices,)
        self.register_action(action)
        self.emit("subtitles-inserted", indices)

    def merge_subtitles_require(self, indices, register=-1):
        assert len(indices) > 1
        for index in indices:
            assert 0 <= index < len(self.subtitles)
        assert list(indices) == range(indices[0], indices[-1] + 1)

    @aeidon.deco.revertable
    def merge_subtitles(self, indices, register=-1):
        """Merge subtitles in indices to form one subtitle."""

        subtitle = self.get_subtitle()
        subtitle.start = self.subtitles[indices[0]].start
        subtitle.end = self.subtitles[indices[-1]].end
        main_texts = [self.subtitles[x].main_text for x in indices]
        main_texts = [x for x in main_texts if x]
        subtitle.main_text = "\n".join(main_texts)
        tran_texts = [self.subtitles[x].tran_text for x in indices]
        tran_texts = [x for x in tran_texts if x]
        subtitle.tran_text = "\n".join(tran_texts)

        self.remove_subtitles(indices, register=register)
        self.insert_subtitles([indices[0]], [subtitle], register=register)
        self.group_actions(register, 2, _("Merging subtitles"))

    def remove_subtitles_require(self, indices, register=-1):
        for index in indices:
            assert 0 <= index < len(self.subtitles)

    @aeidon.deco.revertable
    @aeidon.deco.notify_frozen
    def remove_subtitles(self, indices, register=-1):
        """Remove subtitles in indices."""

        subtitles = []
        indices = sorted(indices)
        for index in reversed(indices):
            subtitles.insert(0, self.subtitles.pop(index))

        action = self.get_revertable_action(register)
        action.docs = tuple(aeidon.documents)
        action.description = _("Removing subtitles")
        action.revert_function = self.insert_subtitles
        action.revert_args = (indices, subtitles)
        self.register_action(action)
        self.emit("subtitles-removed", indices)

    def replace_positions_require(self, indices, subtitles, register=-1):
        for index in indices:
            assert 0 <= index < len(self.subtitles)
        assert len(indices) == len(subtitles)

    @aeidon.deco.revertable
    @aeidon.deco.notify_frozen
    def replace_positions(self, indices, subtitles, register=-1):
        """Replace positions in indices with those in subtitles."""

        orig_subtitles = []
        for i, index in enumerate(indices):
            subtitle = self.subtitles[index]
            orig_subtitles.append(subtitle.copy())
            subtitle.start = subtitles[i].start
            subtitle.end = subtitles[i].end

        action = self.get_revertable_action(register)
        action.docs = tuple(aeidon.documents)
        action.description = _("Replacing positions")
        action.revert_function = self.replace_positions
        action.revert_args = (indices, orig_subtitles)
        self.register_action(action)
        self.emit("positions-changed", indices)

    def replace_texts_require(self, indices, doc, texts, register=-1):
        for index in indices:
            assert 0 <= index < len(self.subtitles)
        assert len(indices) == len(texts)

    @aeidon.deco.revertable
    @aeidon.deco.notify_frozen
    def replace_texts(self, indices, doc, texts, register=-1):
        """Replace texts in document's indices with new_texts."""

        orig_texts = []
        for i, index in enumerate(indices):
            subtitle = self.subtitles[index]
            orig_texts.append(subtitle.get_text(doc))
            subtitle.set_text(doc, texts[i])

        action = self.get_revertable_action(register)
        action.docs = (doc,)
        action.description = _("Replacing texts")
        action.revert_function = self.replace_texts
        action.revert_args = (indices, doc, orig_texts)
        self.register_action(action)
        signal = self.get_text_signal(doc)
        self.emit(signal, indices)

    def split_subtitle_require(self, index, register=-1):
        assert 0 <= index < len(self.subtitles)

    @aeidon.deco.revertable
    def split_subtitle(self, index, register=-1):
        """Split subtitle in two subtitles with the same durations."""

        start = self.subtitles[index].start
        end = self.subtitles[index].end
        middle = self.calc.get_middle(start, end)
        main_text = self.subtitles[index].main_text
        tran_text = self.subtitles[index].tran_text

        subtitles = []
        indices = [index, index + 1]
        subtitle = self.get_subtitle()
        subtitle.start = start
        subtitle.end = middle
        subtitle.main_text = main_text
        subtitle.tran_text = tran_text
        subtitles.append(subtitle)
        subtitle = self.get_subtitle()
        subtitle.start = middle
        subtitle.end = end
        subtitles.append(subtitle)

        self.remove_subtitles([index], register=register)
        self.insert_subtitles(indices, subtitles, register=register)
        self.group_actions(register, 2, _("Splitting subtitle"))
