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

"""Basic editing of entire subtitles."""

import aeidon

from aeidon.i18n import _


class EditAgent(aeidon.Delegate):

    """Basic editing of entire subtitles."""

    @aeidon.deco.export
    @aeidon.deco.revertable
    def clear_texts(self, indices, doc, register=-1):
        """Set texts to blank strings."""
        new_texts =  [""] * len(indices)
        self.replace_texts(indices, doc, new_texts, register=register)
        self.set_action_description(register, _("Clearing texts"))

    @aeidon.deco.revertable
    @aeidon.deco.notify_frozen
    def _insert_blank_subtitles(self, indices, register=-1):
        """Insert new blank subtitles at `indices`."""
        for rindices in aeidon.util.get_ranges(indices):
            first_start = 0.0
            if self.subtitles:
                start = self.subtitles[0].start_seconds
                first_start = 0.0 if start >= 0 else start - 3.0
                if rindices[0] > 0:
                    subtitle = self.subtitles[rindices[0] - 1]
                    first_start = subtitle.end_seconds
            duration = 3.0
            if rindices[0] < len(self.subtitles):
                subtitle = self.subtitles[rindices[0]]
                window = subtitle.start_seconds - first_start
                duration = window / len(rindices)
            for i, index in enumerate(rindices):
                subtitle = self.new_subtitle()
                subtitle.start_seconds = first_start + i*duration
                subtitle.duration_seconds = duration
                self.subtitles.insert(index, subtitle)
        action = aeidon.RevertableAction(register=register)
        action.docs = tuple(aeidon.documents)
        action.description = _("Inserting subtitles")
        action.revert_function = self.remove_subtitles
        action.revert_args = (indices,)
        self.register_action(action)
        self.emit("subtitles-inserted", indices)

    @aeidon.deco.export
    @aeidon.deco.revertable
    @aeidon.deco.notify_frozen
    def insert_subtitles(self, indices, subtitles=None, register=-1):
        """Insert `subtitles` at `indices`.

        If `subtitles` is ``None``, insert blank subtitles at `indices` with
        equal durations within time window before the next subtitle or with
        3 second durations if inserting subtitles at the end.
        """
        if subtitles is None:
            return self._insert_blank_subtitles(indices, register=register)
        for i, index in enumerate(indices):
            self.subtitles.insert(index, subtitles[i])
        action = aeidon.RevertableAction(register=register)
        action.docs = tuple(aeidon.documents)
        action.description = _("Inserting subtitles")
        action.revert_function = self.remove_subtitles
        action.revert_args = (indices,)
        self.register_action(action)
        self.emit("subtitles-inserted", indices)

    @aeidon.deco.export
    @aeidon.deco.revertable
    def merge_subtitles(self, indices, register=-1):
        """Merge subtitles at `indices` to form one subtitle."""
        indices = sorted(indices)
        subtitle = self.new_subtitle()
        subtitle.start = self.subtitles[indices[0]].start
        subtitle.end = self.subtitles[indices[-1]].end
        main_texts = [self.subtitles[i].main_text for i in indices]
        tran_texts = [self.subtitles[x].tran_text for x in indices]
        subtitle.main_text = "\n".join(filter(None, main_texts))
        subtitle.tran_text = "\n".join(filter(None, tran_texts))
        self.remove_subtitles(indices, register=register)
        self.insert_subtitles([indices[0]], [subtitle], register=register)
        self.group_actions(register, 2, _("Merging subtitles"))

    @aeidon.deco.export
    @aeidon.deco.revertable
    @aeidon.deco.notify_frozen
    def remove_subtitles(self, indices, register=-1):
        """Remove subtitles at `indices`."""
        indices = sorted(indices)
        subtitles = [self.subtitles.pop(i) for i in reversed(indices)][::-1]
        action = aeidon.RevertableAction(register=register)
        action.docs = tuple(aeidon.documents)
        action.description = _("Removing subtitles")
        action.revert_function = self.insert_subtitles
        action.revert_args = (indices, subtitles)
        self.register_action(action)
        self.emit("subtitles-removed", indices)

    @aeidon.deco.export
    @aeidon.deco.revertable
    @aeidon.deco.notify_frozen
    def replace_positions(self, indices, subtitles, register=-1):
        """Replace positions at `indices` with those from `subtitles`."""
        orig_subtitles = [self.subtitles[i].copy() for i in indices]
        for i, index in enumerate(indices):
            self.subtitles[index].start = subtitles[i].start
            self.subtitles[index].end = subtitles[i].end
        action = aeidon.RevertableAction(register=register)
        action.docs = tuple(aeidon.documents)
        action.description = _("Replacing positions")
        action.revert_function = self.replace_positions
        action.revert_args = (indices, orig_subtitles)
        self.register_action(action)
        self.emit("positions-changed", indices)

    @aeidon.deco.export
    @aeidon.deco.revertable
    @aeidon.deco.notify_frozen
    def replace_texts(self, indices, doc, texts, register=-1):
        """Replace texts in `doc`'s `indices` with `texts`."""
        orig_texts = [self.subtitles[i].get_text(doc) for i in indices]
        for i, index in enumerate(indices):
            self.subtitles[index].set_text(doc, texts[i])
        action = aeidon.RevertableAction(register=register)
        action.docs = (doc,)
        action.description = _("Replacing texts")
        action.revert_function = self.replace_texts
        action.revert_args = (indices, doc, orig_texts)
        self.register_action(action)
        self.emit(self.get_text_signal(doc), indices)

    @aeidon.deco.export
    @aeidon.deco.revertable
    def split_subtitle(self, index, register=-1):
        """Split subtitle in two equal duration ones."""
        subtitle = self.subtitles[index]
        middle = self.calc.get_middle(subtitle.start, subtitle.end)
        subtitle_1 = self.new_subtitle()
        subtitle_1.start = subtitle.start
        subtitle_1.end = middle
        subtitle_1.main_text = subtitle.main_text
        subtitle_1.tran_text = subtitle.tran_text
        subtitle_2 = self.new_subtitle()
        subtitle_2.start = middle
        subtitle_2.end = subtitle.end
        self.remove_subtitles((index,), register=register)
        indices = (index, index + 1)
        subtitles = (subtitle_1, subtitle_2)
        self.insert_subtitles(indices, subtitles, register=register)
        self.group_actions(register, 2, _("Splitting subtitle"))
