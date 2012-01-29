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

"""Setting values of single subtitle fields."""

import aeidon
import bisect
_ = aeidon.i18n._


class SetAgent(aeidon.Delegate, metaclass=aeidon.Contractual):

    """Setting values of single subtitle fields."""

    def _move_if_needed_require(self, index):
        assert 0 <= index < len(self.subtitles)

    def _move_if_needed(self, index):
        """Move subtitle for correct order and return new index."""
        subtitle = self.subtitles[index]
        subtitles = self.subtitles[:index] + self.subtitles[index + 1:]
        new_index = bisect.bisect_right(subtitles, subtitle)
        if new_index == index: return new_index
        subtitle = self.subtitles.pop(index)
        self.emit("subtitles-removed", (index,))
        self.subtitles.insert(new_index, subtitle)
        self.emit("subtitles-inserted", (new_index,))
        return new_index

    def set_duration_require(self, index, value, register=-1):
        assert 0 <= index < len(self.subtitles)

    @aeidon.deco.export
    @aeidon.deco.revertable
    def set_duration(self, index, value, register=-1):
        """
        Set the value of duration position.

        `value` can be time, frame or seconds. Use :func:`aeidon.as_time`,
        :func:`aeidon.as_frame` or :func:`aeidon.as_seconds` if necessary to
        ensure correct type.
        """
        subtitle = self.subtitles[index]
        orig_end = subtitle.end
        subtitle.duration = value
        if subtitle.end == orig_end: return
        action = self.new_revertable_action(register)
        action.docs = tuple(aeidon.documents)
        action.description = _("Editing position")
        action.revert_function = self.set_end
        action.revert_args = (index, orig_end)
        self.register_action(action)
        self.emit("positions-changed", (index,))

    def set_end_require(self, index, value, register=-1):
        assert 0 <= index < len(self.subtitles)

    @aeidon.deco.export
    @aeidon.deco.revertable
    def set_end(self, index, value, register=-1):
        """
        Set the value of end position.

        `value` can be time, frame or seconds. Use :func:`aeidon.as_time`,
        :func:`aeidon.as_frame` or :func:`aeidon.as_seconds` if necessary to
        ensure correct type.
        """
        subtitle = self.subtitles[index]
        orig_value = subtitle.end
        subtitle.end = value
        if subtitle.end == orig_value: return
        action = self.new_revertable_action(register)
        action.docs = tuple(aeidon.documents)
        action.description = _("Editing position")
        action.revert_function = self.set_end
        action.revert_args = (index, orig_value)
        self.register_action(action)
        self.emit("positions-changed", (index,))

    def set_main_text_require(self, index, value, register=-1):
        assert 0 <= index < len(self.subtitles)

    @aeidon.deco.export
    @aeidon.deco.revertable
    def set_main_text(self, index, value, register=-1):
        """Set the value of main document's text."""
        return self.set_text(index,
                             aeidon.documents.MAIN,
                             value,
                             register=register)

    def set_start_require(self, index, value, register=-1):
        assert 0 <= index < len(self.subtitles)

    def set_start_ensure(self, return_value, index, value, register=-1):
        for i in range(len(self.subtitles) - 1):
            assert self.subtitles[i] <= self.subtitles[i + 1]

    @aeidon.deco.export
    @aeidon.deco.revertable
    @aeidon.deco.notify_frozen
    def set_start(self, index, value, register=-1):
        """
        Set the value of start position.

        `value` can be time, frame or seconds. Use :func:`aeidon.as_time`,
        :func:`aeidon.as_frame` or :func:`aeidon.as_seconds` if necessary to
        ensure correct type.
        """
        subtitle = self.subtitles[index]
        orig_value = subtitle.start
        subtitle.start = value
        if subtitle.start == orig_value: return
        index = self._move_if_needed(index)
        action = self.new_revertable_action(register)
        action.docs = tuple(aeidon.documents)
        action.description = _("Editing position")
        action.revert_function = self.set_start
        action.revert_args = (index, orig_value)
        self.register_action(action)
        self.emit("positions-changed", (index,))

    def set_text_require(self, index, doc, value, register=-1):
        assert 0 <= index < len(self.subtitles)

    @aeidon.deco.export
    @aeidon.deco.revertable
    def set_text(self, index, doc, value, register=-1):
        """Set the value of `doc`'s text."""
        subtitle = self.subtitles[index]
        orig_value = subtitle.get_text(doc)
        if value == orig_value: return
        subtitle.set_text(doc, value)
        action = self.new_revertable_action(register)
        action.docs = (doc,)
        action.description = _("Editing text")
        action.revert_function = self.set_text
        action.revert_args = (index, doc, orig_value)
        self.register_action(action)
        signal = self.get_text_signal(doc)
        self.emit(signal, (index,))

    def set_translation_text_require(self, index, value, register=-1):
        assert 0 <= index < len(self.subtitles)

    @aeidon.deco.export
    @aeidon.deco.revertable
    def set_translation_text(self, index, value, register=-1):
        """Set the value of translation document's text."""
        return self.set_text(index,
                             aeidon.documents.TRAN,
                             value,
                             register=register)
