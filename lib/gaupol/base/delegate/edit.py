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


"""Basic subtitle data editing."""


from gettext import gettext as _
import bisect

from gaupol.base          import cons
from gaupol.base.colcons  import *
from gaupol.base.delegate import Delegate


_DO = cons.Action.DO


class EditDelegate(Delegate):

    """Basic subtitle data editing."""

    def _insert_blank(self, rows):
        """
        Insert blank subtitles.

        rows: Single range
        """
        mode = self.get_mode()
        positions = self.get_positions()
        optimal = 3

        if min(rows) > 0:
            start = positions[min(rows) - 1][HIDE]
            if mode == cons.Mode.TIME:
                start = self.calc.time_to_seconds(start)
        else:
            start = 0

        if min(rows) < len(self.times):
            end = positions[min(rows)][SHOW]
            if mode == cons.Mode.TIME:
                end = self.calc.time_to_seconds(end)
                duration = float(end - start) / float(len(rows))
            if mode == cons.Mode.FRAME:
                duration = int((end - start) / len(rows))
        else:
            if mode == cons.Mode.TIME:
                duration = optimal
            if mode == cons.Mode.FRAME:
                duration = self.calc.seconds_to_frame(optimal)

        for i in range(len(rows)):
            row = min(rows) + i
            if mode == cons.Mode.TIME:
                time, frame = self.expand_times(
                    self.calc.seconds_to_time(start + ( i      * duration)),
                    self.calc.seconds_to_time(start + ((i + 1) * duration))
                )
            elif mode == cons.Mode.FRAME:
                time, frame = self.expand_frames(
                    start + (i * duration), start + ((i + 1) * duration))
            self.times.insert(row, time)
            self.frames.insert(row, frame)
            self.main_texts.insert(row, u'')
            self.tran_texts.insert(row, u'')

    def _insert_data(self, rows, times, frames, main_texts, tran_texts):
        """
        Insert subtitles with data.

        Subtitles are inserted in ascending order by simply inserting elements
        of data in positions defined by elements of rows. This means that the
        addition of subtitles must be taken into account beforehand in the
        "rows" argument. Data is not resorted, so this method must be called
        with ordered positions.
        """
        for i, row in enumerate(rows):
            self.times.insert(row, times[i])
            self.frames.insert(row, frames[i])
            self.main_texts.insert(row, main_texts[i])
            self.tran_texts.insert(row, tran_texts[i])

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

    def clear_texts(self, rows, doc, register=_DO):
        """Clear texts."""

        new_texts = [u''] * len(rows)
        self.replace_texts(rows, doc, new_texts, register)
        self.set_action_description(register, _('Clearing texts'))

    def copy_texts(self, rows, doc):
        """Copy texts to clipboard."""

        data = []
        texts = (self.main_texts, self.tran_texts)[doc]
        for row in range(min(rows), max(rows) + 1):
            if row in rows:
                data.append(texts[row])
            else:
                data.append(None)
        self.clipboard.data = data

    def cut_texts(self, rows, doc, register=_DO):
        """Cut texts to clipboard."""

        self.copy_texts(rows, doc)
        self.clear_texts(rows, doc, register)
        self.set_action_description(register, _('Cutting texts'))

    def expand_frames(self, show, hide):
        """
        Expand single subtitle position data to all quantities.

        Return times, frames.
        """
        frames = [show, hide, self.calc.get_frame_duration(show, hide)]
        times = list(self.calc.frame_to_time(x) for x in (show, hide))
        times.append(self.calc.get_time_duration(times[0], times[1]))
        return times, frames

    def expand_positions(self, show, hide):
        """
        Expand single subtitle position data to all quantities.

        Return times, frames.
        """
        if isinstance(show, basestring):
            return self.expand_times(show, hide)
        if isinstance(show, int):
            return self.expand_frames(show, hide)
        raise ValueError

    def expand_times(self, show, hide):
        """
        Expand single subtitle position data to all quantities.

        Return times, frames.
        """
        times = [show, hide, self.calc.get_time_duration(show, hide)]
        frames = list(self.calc.time_to_frame(x) for x in (show, hide))
        frames.append(self.calc.get_frame_duration(frames[0], frames[1]))
        return times, frames

    def get_mode(self):
        """Get mode of main file or default."""

        try:
            return self.main_file.mode
        except AttributeError:
            return cons.Mode.TIME

    def get_positions(self):
        """Get either times or frames depending mode."""

        mode = self.get_mode()
        if mode == cons. Mode.TIME:
            return self.times
        if mode == cons.Mode.FRAME:
            return self.frames

    def insert_subtitles(
        self,
        rows,
        times=None,
        frames=None,
        main_texts=None,
        tran_texts=None,
        register=_DO
    ):
        """
        Insert subtitles.

        Subtitles are inserted in ascending order by simply inserting elements
        of data in positions defined by elements of rows. This means that the
        addition of subtitles must be taken into account beforehand in the
        "rows" argument.
        """
        rows = sorted(rows)
        if None in (times, frames, main_texts, tran_texts):
            self._insert_blank(rows)
        else:
            self._insert_data(rows, times, frames, main_texts, tran_texts)

        self.register_action(
            register=register,
            docs=[MAIN, TRAN],
            description=_('Inserting subtitles'),
            revert_method=self.remove_subtitles,
            revert_args=[rows],
            inserted_rows=rows,
        )

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

    def paste_texts(self, row, doc, register=_DO):
        """
        Paste texts from clipboard.

        Return rows that were pasted into.
        """
        data = self.clipboard.data
        excess = len(data) - (len(self.times) - row)
        if excess > 0:
            signal = self.get_signal(register)
            self.block(signal)
            rows = range(len(self.times), len(self.times) + excess)
            self.insert_subtitles(rows, register=register)

        rows = []
        new_texts = []
        for i, value in enumerate(data):
            if value is not None:
                rows.append(row + i)
                new_texts.append(value)
        self.replace_texts(rows, doc, new_texts, register)

        if excess > 0:
            self.unblock(signal)
            self.group_actions(register, 2, '')
        self.set_action_description(register, _('Pasting texts'))

        return rows

    def remove_subtitles(self, rows, register=_DO):
        """Remove subtitles."""

        times      = []
        frames     = []
        main_texts = []
        tran_texts = []
        rows = sorted(rows)
        for row in reversed(rows):
            times.insert(0, self.times.pop(row))
            frames.insert(0, self.frames.pop(row))
            main_texts.insert(0, self.main_texts.pop(row))
            tran_texts.insert(0, self.tran_texts.pop(row))

        self.register_action(
            register=register,
            docs=[MAIN, TRAN],
            description=_('Removing subtitles'),
            revert_method=self.insert_subtitles,
            revert_args=[rows, times, frames, main_texts, tran_texts],
            removed_rows=rows,
        )

    def replace_both_texts(self, rows, new_texts, register=_DO):
        """
        Replace texts in both documents' rows with new_texts.

        rows: Main rows, tran rows
        new_texts: New main texts, new tran texts
        """
        if not rows[0] and not rows[1]:
            return
        if not rows[1]:
            return self.replace_texts(rows[0], MAIN, new_texts[0], register)
        if not rows[0]:
            return self.replace_texts(rows[1], TRAN, new_texts[1], register)

        signal = self.get_signal(register)
        self.block(signal)
        self.replace_texts(rows[0], MAIN, new_texts[0], register)
        self.replace_texts(rows[1], TRAN, new_texts[1], register)
        self.unblock(signal)
        self.group_actions(register, 2, _('Replacing texts'))

    def replace_positions(self, rows, new_times, new_frames, register=_DO):
        """Replace times and frames in rows with new_times and new_frames."""

        orig_times  = []
        orig_frames = []
        for i, row in enumerate(rows):
            orig_times.append(self.times[row])
            orig_frames.append(self.frames[row])
            self.times[row] = new_times[i]
            self.frames[row] = new_frames[i]

        self.register_action(
            register=register,
            docs=[MAIN, TRAN],
            description=_('Replacing positions'),
            revert_method=self.replace_positions,
            revert_args=[rows, orig_times, orig_frames],
            updated_positions=rows,
        )

    def replace_texts(self, rows, doc, new_texts, register=_DO):
        """Replace texts in document's rows with new_texts."""

        if doc == MAIN:
            texts = self.main_texts
            updated_main_texts = rows
            updated_tran_texts = []
        elif doc == TRAN:
            texts = self.tran_texts
            updated_main_texts = []
            updated_tran_texts = rows

        orig_texts = []
        for i, row in enumerate(rows):
            orig_texts.append(texts[row])
            texts[row] = new_texts[i]

        self.register_action(
            register=register,
            docs=[doc],
            description=_('Replacing texts'),
            revert_method=self.replace_texts,
            revert_args=[rows, doc, orig_texts],
            updated_main_texts=updated_main_texts,
            updated_tran_texts=updated_tran_texts
        )

    def set_durations(self, row):
        """Set durations for row based on shows and hides."""

        self.times[row][DURN] = self.calc.get_time_duration(
            self.times[row][SHOW], self.times[row][HIDE])

        self.frames[row][DURN] = self.calc.get_frame_duration(
            self.frames[row][SHOW], self.frames[row][HIDE])

    def set_frame(self, row, col, value, register=_DO):
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

    def set_text(self, row, doc, value, register=_DO):
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

    def set_time(self, row, col, value, register=_DO):
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
