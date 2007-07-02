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


"""Basic subtitle data editing."""


from __future__ import division

import gaupol
_ = gaupol.i18n._


class EditAgent(gaupol.Delegate):

    """Basic subtitle data editing."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = gaupol.Contractual

    def clear_texts_require(self, indexes, doc, register=-1):
        for index in indexes:
            assert 0 <= index < len(self.subtitles)

    @gaupol.util.revertable
    def clear_texts(self, indexes, doc, register=-1):
        """Set texts to blank strings."""

        new_texts = [""] * len(indexes)
        self.replace_texts(indexes, doc, new_texts, register=register)
        self.set_action_description(register, _("Clearing texts"))

    @gaupol.util.revertable
    @gaupol.util.notify_frozen
    def insert_blank_subtitles(self, indexes, register=-1):
        """Insert blank subtitles with fitting positions."""

        for these_indexes in gaupol.util.get_ranges(indexes):
            first_start = 0.0
            if these_indexes[0] > 0:
                subtitle = self.subtitles[these_indexes[0] - 1]
                first_start = subtitle.end_seconds
            duration = 3.0
            if these_indexes[0] < len(self.subtitles):
                subtitle = self.subtitles[these_indexes[0]]
                window = subtitle.start_seconds - first_start
                duration = window / len(these_indexes)
            for i, index in enumerate(these_indexes):
                subtitle = self.get_subtitle()
                subtitle.start = first_start + (i * duration)
                subtitle.end = first_start + ((i + 1) * duration)
                self.subtitles.insert(index, subtitle)

        action = self.get_revertable_action(register)
        action.docs = gaupol.DOCUMENT.members
        action.description = _("Inserting subtitles")
        action.revert_method = self.remove_subtitles
        action.revert_args = (indexes,)
        self.register_action(action)
        self.emit("subtitles-inserted", indexes)

    @gaupol.util.revertable
    @gaupol.util.notify_frozen
    def insert_subtitles(self, indexes, subtitles, register=-1):
        """Insert given subtitles."""

        for i, index in enumerate(indexes):
            self.subtitles.insert(index, subtitles[i])

        action = self.get_revertable_action(register)
        action.docs = gaupol.DOCUMENT.members
        action.description = _("Inserting subtitles")
        action.revert_method = self.remove_subtitles
        action.revert_args = (indexes,)
        self.register_action(action)
        self.emit("subtitles-inserted", indexes)

    def merge_subtitles_require(self, indexes, register=-1):
        assert len(indexes) > 1
        for index in indexes:
            assert 0 <= index < len(self.subtitles)
        assert indexes == range(indexes[0], indexes[-1] + 1)

    @gaupol.util.revertable
    def merge_subtitles(self, indexes, register=-1):
        """Merge subtitles in indexes to form one subtitle."""

        subtitle = self.get_subtitle()
        subtitle.start = self.subtitles[indexes[0]].start
        subtitle.end = self.subtitles[indexes[-1]].end
        main_texts = [self.subtitles[x].main_text for x in indexes]
        main_texts = [x for x in main_texts if x]
        subtitle.main_text = "\n".join(main_texts)
        tran_texts = [self.subtitles[x].tran_text for x in indexes]
        tran_texts = [x for x in tran_texts if x]
        subtitle.tran_text = "\n".join(tran_texts)

        self.remove_subtitles(indexes, register=register)
        self.insert_subtitles([indexes[0]], [subtitle], register=register)
        self.group_actions(register, 2, _("Merging subtitles"))

    def remove_subtitles_require(self, indexes, register=-1):
        for index in indexes:
            assert 0 <= index < len(self.subtitles)

    @gaupol.util.revertable
    @gaupol.util.notify_frozen
    def remove_subtitles(self, indexes, register=-1):
        """Remove subtitles in indexes."""

        subtitles = []
        indexes = sorted(indexes)
        for index in reversed(indexes):
            subtitles.insert(0, self.subtitles.pop(index))

        action = self.get_revertable_action(register)
        action.docs = gaupol.DOCUMENT.members
        action.description = _("Removing subtitles")
        action.revert_method = self.insert_subtitles
        action.revert_args = (indexes, subtitles)
        self.register_action(action)
        self.emit("subtitles-removed", indexes)

    def replace_positions_require(self, indexes, subtitles, register=-1):
        for index in indexes:
            assert 0 <= index < len(self.subtitles)
        assert len(indexes) == len(subtitles)

    @gaupol.util.revertable
    @gaupol.util.notify_frozen
    def replace_positions(self, indexes, subtitles, register=-1):
        """Replace positions in indexes with those in subtitles."""

        orig_subtitles = []
        for i, index in enumerate(indexes):
            subtitle = self.subtitles[index]
            orig_subtitles.append(subtitle.copy())
            subtitle.start = subtitles[i].start
            subtitle.end = subtitles[i].end

        action = self.get_revertable_action(register)
        action.docs = gaupol.DOCUMENT.members
        action.description = _("Replacing positions")
        action.revert_method = self.replace_positions
        action.revert_args = (indexes, orig_subtitles)
        self.register_action(action)
        self.emit("positions-changed", indexes)

    def replace_texts_require(self, indexes, doc, texts, register=-1):
        for index in indexes:
            assert 0 <= index < len(self.subtitles)
        assert len(indexes) == len(texts)

    @gaupol.util.revertable
    @gaupol.util.notify_frozen
    def replace_texts(self, indexes, doc, texts, register=-1):
        """Replace texts in document's indexes with new_texts."""

        orig_texts = []
        for i, index in enumerate(indexes):
            subtitle = self.subtitles[index]
            orig_texts.append(subtitle.get_text(doc))
            subtitle.set_text(doc, texts[i])

        action = self.get_revertable_action(register)
        action.docs = [doc]
        action.description = _("Replacing texts")
        action.revert_method = self.replace_texts
        action.revert_args = (indexes, doc, orig_texts)
        self.register_action(action)
        signal = self.get_text_signal(doc)
        self.emit(signal, indexes)

    def split_subtitle_require(self, index, register=-1):
        assert 0 <= index < len(self.subtitles)

    @gaupol.util.revertable
    def split_subtitle(self, index, register=-1):
        """Split subtitle in two subtitles with the same durations."""

        start = self.subtitles[index].start
        end = self.subtitles[index].end
        middle = self.calc.get_middle(start, end)
        main_text = self.subtitles[index].main_text
        tran_text = self.subtitles[index].tran_text

        subtitles = []
        indexes = [index, index + 1]
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
        self.insert_subtitles(indexes, subtitles, register=register)
        self.group_actions(register, 2, _("Splitting subtitle"))
