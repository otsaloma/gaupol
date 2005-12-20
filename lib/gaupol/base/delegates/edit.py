# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Editing subtitle data."""


try:
    from psyco.classes import *
except ImportError:
    pass

import bisect

from gaupol.base.colconstants import *
from gaupol.base.delegates    import Delegate
from gaupol.constants         import Action, Document, Mode


class EditDelegate(Delegate):

    """Editing subtitle data."""

    def get_mode(self):
        """
        Get main file's mode.

        If main file does not exist, return time mode. Due to its greater
        accuracy, time mode is the preferred mode for new documents.
        """
        try:
            return self.main_file.mode
        except AttributeError:
            return Mode.TIME

    def get_timings(self):
        """Return either times or frames depending on main file's mode."""

        mode = self.get_mode()

        if mode == Mode.TIME:
            return self.times
        elif mode == Mode.FRAME:
            return self.frames

    def insert_subtitles(self, start_row, amount, register=Action.DO):
        """Insert blank subtitles starting at start_row."""
        pass

    def _set_durations(self, row):
        """Set durations for row based on shows and hides."""

        show = self.times[row][SHOW]
        hide = self.times[row][HIDE]
        self.times[row][DURN] = self.calc.get_time_duration(show, hide)

        show = self.frames[row][SHOW]
        hide = self.frames[row][HIDE]
        self.frames[row][DURN] = self.calc.get_frame_duration(show, hide)

    def set_frame(self, row, col, value, register=Action.DO):
        """Set frame."""

        orig_value = self.frames[row][col]
        if value == orig_value:
            return

        rows_updated = []
        timing_rows_updated = [row]
        revert_row = row

        self.frames[row][col] = value
        self.times[row][col]  = self.calc.frame_to_time(value)

        # Calculate affected data.
        if col in (SHOW, HIDE):
            self._set_durations(row)
        elif col == DURN:
            self._set_hides(row)

        # Resort if show frame changed.
        if col == SHOW:
            new_row = self._sort_data(row)
            if new_row != row:
                first_row = min(row, new_row)
                last_row  = max(row, new_row)
                rows_updated = range(first_row, last_row + 1)
                revert_row = new_row
                timing_rows_updated = []

        description = (
            _('Editing show frame'),
            _('Editing hide frame'),
            _('Editing frame duration')
        )[col]

        self.register_action(
            register=register,
            documents=[Document.MAIN],
            description=description,
            revert_method=self.set_frame,
            revert_method_args=[revert_row, col, orig_value],
            rows_updated=rows_updated,
            timing_rows_updated=timing_rows_updated,
        )

    def _set_hides(self, row):
        """Set hides for row based on shows and durations."""

        show = self.times[row][SHOW]
        durn = self.times[row][DURN]
        self.times[row][HIDE] = self.calc.add_times(show, durn)

        show = self.frames[row][SHOW]
        durn = self.frames[row][DURN]
        self.frames[row][HIDE] = show + durn

    def set_text(self, row, document, value, register=Action.DO):
        """Set text."""

        value = unicode(value)
        main_text_rows_updated = []
        tran_text_rows_updated = []

        if document == Document.MAIN:
            orig_value = self.main_texts[row]
            self.main_texts[row] = value
            main_text_rows_updated = [row]

        elif document == Document.TRAN:
            orig_value = self.tran_texts[row]
            self.tran_texts[row] = value
            tran_text_rows_updated = [row]

        if value == orig_value:
            return

        description = (
            _('Editing main text'),
            _('Editing translation text'),
        )[document]

        self.register_action(
            register=register,
            documents=[document],
            description=description,
            revert_method=self.set_text,
            revert_method_args=[row, document, orig_value],
            main_text_rows_updated=main_text_rows_updated,
            tran_text_rows_updated=tran_text_rows_updated
        )

    def set_time(self, row, col, value, register=Action.DO):
        """Set time."""

        orig_value = self.times[row][col]
        if value == orig_value:
            return

        rows_updated = []
        timing_rows_updated = [row]
        revert_row = row

        self.times[row][col]  = value
        self.frames[row][col] = self.calc.time_to_frame(value)

        # Calculate affected data.
        if col in (SHOW, HIDE):
            self._set_durations(row)
        elif col == DURN:
            self._set_hides(row)

        # Resort if show frame changed.
        if col == SHOW:
            new_row = self._sort_data(row)
            if new_row != row:
                first_row = min(row, new_row)
                last_row  = max(row, new_row)
                rows_updated = range(first_row, last_row + 1)
                revert_row = new_row
                timing_rows_updated = []

        description = (
            _('Editing show time'),
            _('Editing hide time'),
            _('Editing time duration')
        )[col]

        self.register_action(
            register=register,
            documents=[Document.MAIN],
            description=description,
            revert_method=self.set_time,
            revert_method_args=[revert_row, col, orig_value],
            rows_updated=rows_updated,
            timing_rows_updated=timing_rows_updated,
        )

    def _sort_data(self, row):
        """
        Sort data after show value in row has changed.

        Return new index of row.
        """
        timings = self.get_timings()
        data = [self.times, self.frames, self.main_texts, self.tran_texts]

        # Get new row.
        lst  = timings[:row] + timings[row + 1:]
        item = timings[row]
        new_row = bisect.bisect_right(lst, item)

        # Move data.
        if new_row != row:
            for entry in data:
                entry.insert(new_row, entry.pop(row))

        return new_row
