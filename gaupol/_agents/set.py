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


"""Setting values of single subtitle data units."""


import bisect
from gettext import gettext as _

from gaupol import cons
from gaupol.base import Delegate, notify_frozen
from .index import SHOW, HIDE, DURN
from .register import revertable


class SetAgent(Delegate):

    """Setting values of single subtitle data units."""

    # pylint: disable-msg=E0203,W0201

    def _complete_positions(self, row, col, value):
        """Set values of units affected."""

        if isinstance(value, basestring):
            self.frames[row][col] = self.calc.time_to_frame(value)
        elif isinstance(value, int):
            self.times[row][col] = self.calc.frame_to_time(value)

        if col in (SHOW, HIDE):
            self.times[row][DURN], self.frames[row][DURN] = \
                self._get_durations(row)
        elif col == DURN:
            self.times[row][HIDE], self.frames[row][HIDE] = \
                self._get_hides(row)

    def _get_durations(self, row):
        """Set durations for row based on shows and hides."""

        time = self.calc.get_time_duration(
            self.times[row][SHOW], self.times[row][HIDE])
        frame = self.calc.get_frame_duration(
            self.frames[row][SHOW], self.frames[row][HIDE])
        return time, frame

    def _get_hides(self, row):
        """Set hides for row based on shows and durations."""

        time = self.calc.add_times(
            self.times[row][SHOW], self.times[row][DURN])
        frame = sum((self.frames[row][SHOW], self.frames[row][DURN]))
        return time, frame

    def _move_if_needed(self, row):
        """Move row if it's show position so demands.

        Return the new row or row if not moved.
        """
        positions = self.get_positions()
        lst = positions[:row] + positions[row + 1:]
        item = positions[row]
        new_row = bisect.bisect_right(lst, item)
        if new_row == row:
            return row
        time = self.times.pop(row)
        frame = self.frames.pop(row)
        main_text = self.main_texts.pop(row)
        tran_text = self.tran_texts.pop(row)
        self.emit("subtitles-removed", [row])
        self.times.insert(new_row, time)
        self.frames.insert(new_row, frame)
        self.main_texts.insert(new_row, main_text)
        self.tran_texts.insert(new_row, tran_text)
        self.emit("subtitles-inserted", [new_row])
        return new_row

    def needs_resort(self, row, show):
        """Return True if resort is needed after changing the show value."""

        mode = self.get_mode()
        positions = self.get_positions()
        if isinstance(show, basestring):
            if mode == cons.MODE.FRAME:
                show = self.calc.time_to_frame(show)
        elif isinstance(show, int):
            if mode == cons.MODE.TIME:
                show = self.calc.frame_to_time(show)

        lst = positions[:row] + positions[row + 1:]
        item = [show] + positions[row][1:]
        new_row = bisect.bisect_right(lst, item)
        return new_row != row

    @revertable
    @notify_frozen
    def set_position(self, row, col, value, register=-1):
        """Set the value of position.

        Return new row or row if not moved.
        """
        if isinstance(value, basestring):
            positions = self.times
        elif isinstance(value, int):
            positions = self.frames
        if value == positions[row][col]:
            return row
        natives = self.get_positions()
        orig_value = natives[row][col]
        positions[row][col] = value
        self._complete_positions(row, col, value)
        new_row = (self._move_if_needed(row) if col == SHOW else row)

        self.register_action(
            register=register,
            docs=[cons.DOCUMENT.MAIN],
            description=_("Editing position"),
            revert_method=self.set_position,
            revert_args=[new_row, col, orig_value],)

        self.emit("positions-changed", [new_row])
        return new_row

    @revertable
    def set_text(self, row, doc, value, register=-1):
        """Set the value of text."""

        value = unicode(value)
        texts = self.get_texts(doc)
        orig_value = texts[row]
        texts[row] = value
        if value == orig_value:
            return

        self.register_action(
            register=register,
            docs=[doc],
            description=_("Editing text"),
            revert_method=self.set_text,
            revert_args=[row, doc, orig_value],)

        signal = ("main-texts-changed", "translation-texts-changed")[doc]
        self.emit(signal, [row])
