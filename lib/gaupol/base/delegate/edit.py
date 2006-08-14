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

from gaupol.base          import cons
from gaupol.base.icons    import *
from gaupol.base.delegate import Delegate, revertablemethod


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

        start = 0
        if min(rows) > 0:
            start = positions[min(rows) - 1][HIDE]
            if mode == cons.Mode.TIME:
                start = self.calc.time_to_seconds(start)

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
        'rows' argument. Data is not resorted, so this method must be called
        with ordered positions.
        """
        for i, row in enumerate(rows):
            self.times.insert(row, times[i])
            self.frames.insert(row, frames[i])
            self.main_texts.insert(row, main_texts[i])
            self.tran_texts.insert(row, tran_texts[i])

    @revertablemethod
    def clear_texts(self, rows, doc, register=-1):
        """Clear texts."""

        new_texts = [u''] * len(rows)
        self.replace_texts(rows, doc, new_texts, register=register)
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

    @revertablemethod
    def cut_texts(self, rows, doc, register=-1):
        """Cut texts to clipboard."""

        self.copy_texts(rows, doc)
        self.clear_texts(rows, doc, register=register)
        self.set_action_description(register, _('Cutting texts'))

    @revertablemethod
    def insert_subtitles(
        self,
        rows,
        times=None,
        frames=None,
        main_texts=None,
        tran_texts=None,
        register=-1
    ):
        """
        Insert subtitles.

        Subtitles are inserted in ascending order by simply inserting elements
        of data in positions defined by elements of rows. This means that the
        addition of subtitles must be taken into account beforehand in the
        'rows' argument.
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

    @revertablemethod
    def merge_subtitles(self, rows, register=-1):
        """Merge subtitles."""

        positions = self.get_positions()
        show = positions[rows[0]][SHOW]
        hide = positions[rows[-1]][HIDE]
        time, frame = self.expand_positions(show, hide)
        main_text = self.main_texts[rows[0]]
        tran_text = self.tran_texts[rows[0]]
        for row in rows[1:]:
            if self.main_texts[row]:
                main_text = main_text + '\n' + self.main_texts[row]
            if self.tran_texts[row]:
                tran_text = tran_text + '\n' + self.tran_texts[row]
        main_text = main_text.lstrip()
        tran_text = tran_text.lstrip()

        self.remove_subtitles(rows, register=register)
        self.insert_subtitles(
            [rows[0]],
            [time],
            [frame],
            [main_text],
            [tran_text],
            register=register
        )
        self.group_actions(register, 2, _('Merging subtitles'))

    @revertablemethod
    def paste_texts(self, row, doc, register=-1):
        """
        Paste texts from clipboard.

        Return rows that were pasted into.
        """
        data = self.clipboard.data
        excess = len(data) - (len(self.times) - row)
        if excess > 0:
            rows = range(len(self.times), len(self.times) + excess)
            self.insert_subtitles(rows, register=register)

        rows = []
        new_texts = []
        for i, value in enumerate(data):
            if value is not None:
                rows.append(row + i)
                new_texts.append(value)
        self.replace_texts(rows, doc, new_texts, register=register)

        if excess > 0:
            self.group_actions(register, 2, _('Pasting texts'))
        self.set_action_description(register, _('Pasting texts'))
        return rows

    @revertablemethod
    def remove_subtitles(self, rows, register=-1):
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

    @revertablemethod
    def split_subtitle(self, row, register=-1):
        """Split subtitle in two."""

        positions = self.get_positions()
        show = positions[row][SHOW]
        hide = positions[row][HIDE]
        middle = self.calc.get_middle(show, hide)
        time_1, frame_1 = self.expand_positions(show, middle)
        time_2, frame_2 = self.expand_positions(middle, hide)
        main_text = self.main_texts[row]
        tran_text = self.tran_texts[row]

        self.remove_subtitles([row], register=register)
        self.insert_subtitles(
            [row, row + 1],
            [time_1, time_2],
            [frame_1, frame_2],
            [main_text, u''],
            [tran_text, u''],
            register=register
        )
        self.group_actions(register, 2, _('Splitting subtitle'))
