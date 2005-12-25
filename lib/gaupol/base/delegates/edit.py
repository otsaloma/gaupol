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
from gaupol.base.error        import FitError
from gaupol.constants         import Action, Document, Framerate, Mode


class EditDelegate(Delegate):

    """Editing subtitle data."""

    def clear_texts(self, rows, document, register=Action.DO):
        """Clear texts."""

        new_texts = [u''] * len(rows)
        self.replace_texts(rows, document, new_texts, register)
        self.modify_action_description(register, _('Clearing texts'))

    def copy_texts(self, rows, document):
        """Copy texts to the clipboard."""

        start_row = min(rows)
        end_row   = max(rows)
        texts     = (self.main_texts, self.tran_texts)[document]
        data      = []

        for row in range(start_row, end_row + 1):
            if row in rows:
                data.append(texts[row])
            else:
                data.append(None)

        self.clipboard.data = data

    def cut_texts(self, rows, document, register=Action.DO):
        """Cut texts to the clipboard."""

        self.copy_texts(rows, document)
        self.clear_texts(rows, document, register)
        self.modify_action_description(register, _('Cutting texts'))

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

    def _insert_blank(self, rows):
        """
        Insert blank subtitles.

        rows must be a single range.
        """
        times      = self.times
        frames     = self.frames
        main_texts = self.main_texts
        tran_texts = self.tran_texts
        calc       = self.calc
        mode       = self.get_mode()
        timings    = self.get_timings()
        start_row  = min(rows)
        amount     = len(rows)

        # Optimal durations
        opt_sec = 3
        opt_frm = int(round(Framerate.values[self.framerate] * opt_sec, 0))

        # Get the first show time or frame.
        if start_row > 0:
            start = timings[start_row - 1][HIDE]
            if mode == Mode.TIME:
                start = calc.time_to_seconds(start)
        else:
            start = 0

        # Get duration.
        if start_row < len(self.times):
            end = timings[start_row][SHOW]
            if mode == Mode.TIME:
                end = calc.time_to_seconds(end)
                duration = float(end - start) / float(amount)
            if mode == Mode.FRAME:
                duration = int((end - start) / amount)
        else:
            if mode == Mode.TIME:
                duration = 3
            if mode == Mode.FRAME:
                fr_value = Framerate.values[self.framerate]
                duration = int(round(fr_value * 3, 0))

        if mode == Mode.TIME:
            for i in range(amount):

                show_time = calc.seconds_to_time(start + ( i      * duration))
                hide_time = calc.seconds_to_time(start + ((i + 1) * duration))
                durn_time = calc.get_time_duration(show_time, hide_time)

                show_frame = calc.time_to_frame(show_time)
                hide_frame = calc.time_to_frame(hide_time)
                durn_frame = calc.get_frame_duration(show_frame, hide_frame)

                row = start_row + i
                times.insert(row, [show_time, hide_time, durn_time])
                frames.insert(row, [show_frame, hide_frame, durn_frame])
                main_texts.insert(row, u'')
                tran_texts.insert(row, u'')

        elif mode == Mode.FRAME:
            for i in range(amount):

                show_frame = start + ( i      * duration)
                hide_frame = start + ((i + 1) * duration)
                durn_frame = calc.get_frame_duration(show_frame, hide_frame)

                show_time = calc.frame_to_time(show_frame)
                hide_time = calc.frame_to_time(hide_frame)
                durn_time = conv.get_time_duration(show_time, hide_time)

                row = start_row + i
                times.insert(row, [show_time, hide_time, durn_time])
                frames.insert(row, [show_frame, hide_frame, durn_frame])
                main_texts.insert(row, u'')
                tran_texts.insert(row, u'')

    def _insert_data(self, rows, times, frames, main_texts, tran_texts):
        """
        Insert subtitles with data.

        rows, times, frames, main_texts and tran_texts must all have the same
        length. subtitles are inserted in ascending order by simply inserting
        elements of data in positions defined by elements of rows. This means
        that the addition of subtitles must be taken into account beforehand in
        the "rows" argument.
        """
        for i in range(len(rows)):
            row = rows[i]
            self.times.insert(row, times[i])
            self.frames.insert(row, frames[i])
            self.main_texts.insert(row, main_texts[i])
            self.tran_texts.insert(row, tran_texts[i])

    def insert_subtitles(self, rows, times=None, frames=None, main_texts=None,
                         tran_texts=None, register=Action.DO):
        """
        Insert subtitles.

        rows, times, frames, main_texts and tran_texts must all have the same
        length. subtitles are inserted in ascending order by simply inserting
        elements of data in positions defined by elements of rows. This means
        that the addition of subtitles must be taken into account beforehand in
        the "rows" argument.
        """
        rows = rows[:]
        rows.sort()

        if None in (times, frames, main_texts, tran_texts):
            self._insert_blank(rows)
        else:
            args = rows, times, frames, main_texts, tran_texts
            self._insert_data(*args)

        self.register_action(
            register=register,
            documents=[Document.MAIN, Document.TRAN],
            description=_('Inserting subtitles'),
            revert_method=self.remove_subtitles,
            revert_method_args=[rows],
            rows_inserted=rows,
        )

    def paste_texts(self, start_row, document, register=Action.DO):
        """
        Paste texts from the clipboard.

        Raise FitError if clipboard contents don't fit.
        Return rows that were pasted into.
        """
        data = self.clipboard.data
        if len(data) > len(self.times) - start_row:
            raise FitError

        rows      = []
        new_texts = []

        for i in range(len(data)):
            if data[i] is not None:
                rows.append(start_row + i)
                new_texts.append(data[i])

        self.replace_texts(rows, document, new_texts, register)
        self.modify_action_description(register, _('Pasting texts'))
        return rows

    def remove_subtitles(self, rows, register=Action.DO):
        """Remove subtitles."""

        # Removed data.
        times      = []
        frames     = []
        main_texts = []
        tran_texts = []

        rows = rows[:]
        rows.sort()

        for row in reversed(rows):
            times.insert(0, self.times.pop(row))
            frames.insert(0, self.frames.pop(row))
            main_texts.insert(0, self.main_texts.pop(row))
            tran_texts.insert(0, self.tran_texts.pop(row))

        self.register_action(
            register=register,
            documents=[Document.MAIN, Document.TRAN],
            description=_('Removing subtitles'),
            revert_method=self.insert_subtitles,
            revert_method_args=[rows, times, frames, main_texts, tran_texts],
            rows_removed=rows,
        )

    def replace_texts(self, rows, document, new_texts, register=Action.DO):
        """Replace texts in rows with new_texts."""

        if document == Document.MAIN:
            texts = self.main_texts
            main_text_rows_updated = rows
            tran_text_rows_updated = []
        elif document == Document.TRAN:
            texts = self.tran_texts
            main_text_rows_updated = []
            tran_text_rows_updated = rows

        orig_texts = []

        for i in range(len(rows)):
            row = rows[i]
            orig_texts.append(texts[row])
            texts[row] = new_texts[i]

        self.register_action(
            register=register,
            documents=[document],
            description=_('Replacing texts'),
            revert_method=self.replace_texts,
            revert_method_args=[rows, document, orig_texts],
            main_text_rows_updated=main_text_rows_updated,
            tran_text_rows_updated=tran_text_rows_updated
        )

    def _set_durations(self, row):
        """Set durations for row based on shows and hides."""

        show = self.times[row][SHOW]
        hide = self.times[row][HIDE]
        self.times[row][DURN] = self.calc.get_time_duration(show, hide)

        show = self.frames[row][SHOW]
        hide = self.frames[row][HIDE]
        self.frames[row][DURN] = self.calc.get_frame_duration(show, hide)

    def set_frame(self, row, col, value, register=Action.DO):
        """
        Set frame.

        Return new index of row.
        """
        orig_value = self.frames[row][col]
        if value == orig_value:
            return row

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

        self.register_action(
            register=register,
            documents=[Document.MAIN],
            description=_('Editing frame'),
            revert_method=self.set_frame,
            revert_method_args=[revert_row, col, orig_value],
            rows_updated=rows_updated,
            timing_rows_updated=timing_rows_updated,
        )

        return revert_row

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

        self.register_action(
            register=register,
            documents=[document],
            description=_('Editing text'),
            revert_method=self.set_text,
            revert_method_args=[row, document, orig_value],
            main_text_rows_updated=main_text_rows_updated,
            tran_text_rows_updated=tran_text_rows_updated
        )

    def set_time(self, row, col, value, register=Action.DO):
        """
        Set time.

        Return new index of row.
        """
        orig_value = self.times[row][col]
        if value == orig_value:
            return row

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

        self.register_action(
            register=register,
            documents=[Document.MAIN],
            description=_('Editing time'),
            revert_method=self.set_time,
            revert_method_args=[revert_row, col, orig_value],
            rows_updated=rows_updated,
            timing_rows_updated=timing_rows_updated,
        )

        return revert_row

    def _sort_data(self, row):
        """
        Sort data after show value in row has changed.

        Return new index of row.
        """
        timings = self.get_timings()
        data = [self.times, self.frames, self.main_texts, self.tran_texts]

        # Get new row.
        lst = timings[:row] + timings[row + 1:]
        item = timings[row]
        new_row = bisect.bisect_right(lst, item)

        # Move data.
        if new_row != row:
            for entry in data:
                entry.insert(new_row, entry.pop(row))

        return new_row
