# Copyright (C) 2005-2006 Osmo Salomaa
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


from gettext import gettext as _
import bisect

from gaupol.base          import cons
from gaupol.base.icons    import *
from gaupol.base.delegate import Delegate, revertablemethod


class SetDelegate(Delegate):

    """Setting values of single subtitle data units."""

    def _sort_data(self, row):
        """
        Sort data based on shows.

        Return new row.
        """
        positions = self.get_positions()
        lst = positions[:row] + positions[row + 1:]
        item = positions[row]
        new_row = bisect.bisect_right(lst, item)

        if new_row != row:
            for data in (
                self.times,
                self.frames,
                self.main_texts,
                self.tran_texts
            ):
                data.insert(new_row, data.pop(row))

        return new_row

    def needs_resort(self, row, show):
        """Return True if resorting is needed after changing show value."""

        mode = self.get_mode()
        positions = self.get_positions()

        if isinstance(show, basestring):
            if mode == cons.Mode.FRAME:
                show = self.calc.time_to_frame(show)
        elif isinstance(show, int):
            if mode == cons.Mode.TIME:
                show = self.calc.frame_to_time(show)

        lst = positions[:row] + positions[row + 1:]
        item = [show] + positions[row][1:]
        new_row = bisect.bisect_right(lst, item)
        return bool(new_row != row)

    def set_durations(self, row):
        """Set durations for row based on shows and hides."""

        self.times[row][DURN] = self.calc.get_time_duration(
            self.times[row][SHOW], self.times[row][HIDE])

        self.frames[row][DURN] = self.calc.get_frame_duration(
            self.frames[row][SHOW], self.frames[row][HIDE])

    @revertablemethod
    def set_frame(self, row, col, value, register=-1):
        """
        Set frame.

        Return new row.
        """
        orig_value = self.frames[row][col]
        if value == orig_value:
            return row

        # Avoid rounding errors by mode-dependent revert.
        mode = self.get_mode()
        if mode == cons.Mode.TIME:
            orig_value = self.times[row][col]
            revert_method = self.set_time
        elif mode == cons.Mode.FRAME:
            orig_value = self.frames[row][col]
            revert_method = self.set_frame

        self.frames[row][col] = value
        self.times[row][col] = self.calc.frame_to_time(value)
        if col in (SHOW, HIDE):
            self.set_durations(row)
        elif col == DURN:
            self.set_hides(row)

        revert_row = row
        updated_rows = []
        updated_positions = [row]
        if col == SHOW:
            new_row = self._sort_data(row)
            if new_row != row:
                revert_row = new_row
                updated_rows = range(min(row, new_row), max(row, new_row) + 1)
                updated_positions = []

        self.register_action(
            register=register,
            docs=[MAIN],
            description=_('Editing frame'),
            revert_method=revert_method,
            revert_args=[revert_row, col, orig_value],
            updated_rows=updated_rows,
            updated_positions=updated_positions,
        )

        return revert_row

    def set_hides(self, row):
        """Set hides for row based on shows and durations."""

        self.times[row][HIDE] = self.calc.add_times(
            self.times[row][SHOW], self.times[row][DURN])

        self.frames[row][HIDE] = \
            self.frames[row][SHOW] + self.frames[row][DURN]

    @revertablemethod
    def set_text(self, row, doc, value, register=-1):
        """Set text."""

        value = unicode(value)
        if doc == MAIN:
            orig_value = self.main_texts[row]
            self.main_texts[row] = value
            updated_main_texts = [row]
            updated_tran_texts = []
        elif doc == TRAN:
            orig_value = self.tran_texts[row]
            self.tran_texts[row] = value
            updated_main_texts = []
            updated_tran_texts = [row]
        if value == orig_value:
            return

        self.register_action(
            register=register,
            docs=[doc],
            description=_('Editing text'),
            revert_method=self.set_text,
            revert_args=[row, doc, orig_value],
            updated_main_texts=updated_main_texts,
            updated_tran_texts=updated_tran_texts
        )

    @revertablemethod
    def set_time(self, row, col, value, register=-1):
        """
        Set time.

        Return new row.
        """
        orig_value = self.times[row][col]
        if value == orig_value:
            return row

        # Avoid rounding errors by mode-dependent revert.
        mode = self.get_mode()
        if mode == cons.Mode.TIME:
            orig_value = self.times[row][col]
            revert_method = self.set_time
        elif mode == cons.Mode.FRAME:
            orig_value = self.frames[row][col]
            revert_method = self.set_frame

        self.times[row][col] = value
        self.frames[row][col] = self.calc.time_to_frame(value)
        if col in (SHOW, HIDE):
            self.set_durations(row)
        elif col == DURN:
            self.set_hides(row)

        revert_row = row
        updated_rows = []
        updated_positions = [row]
        if col == SHOW:
            new_row = self._sort_data(row)
            if new_row != row:
                revert_row = new_row
                updated_rows = range(min(row, new_row), max(row, new_row) + 1)
                updated_positions = []

        self.register_action(
            register=register,
            docs=[MAIN],
            description=_('Editing time'),
            revert_method=revert_method,
            revert_args=[revert_row, col, orig_value],
            updated_rows=updated_rows,
            updated_positions=updated_positions,
        )

        return revert_row
