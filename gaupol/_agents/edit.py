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


from __future__ import division
from gettext import gettext as _

from gaupol import cons, util
from gaupol.base import Delegate, notify_frozen
from .index import SHOW, HIDE, DURN
from .register import revertable


class EditAgent(Delegate):

    """Basic subtitle data editing."""

    # pylint: disable-msg=E0203,W0201

    @revertable
    def clear_texts(self, rows, doc, register=-1):
        """Clear texts."""

        new_texts = [u""] * len(rows)
        self.replace_texts(rows, doc, new_texts, register=register)
        self.set_action_description(register, _("Clearing texts"))

    def copy_texts(self, rows, doc):
        """Copy texts to the clipboard."""

        data = []
        texts = self.get_texts(doc)
        for row in range(min(rows), max(rows) + 1):
            item = (texts[row] if row in rows else None)
            data.append(item)
        self.clipboard.data = data

    @revertable
    def cut_texts(self, rows, doc, register=-1):
        """Cut texts to the clipboard."""

        self.copy_texts(rows, doc)
        self.clear_texts(rows, doc, register=register)
        self.set_action_description(register, _("Cutting texts"))

    @revertable
    @notify_frozen
    def insert_blank_subtitles(self, rows, register=-1):
        """Insert blank subtitles."""

        mode = self.get_mode()
        all_rows = util.get_sorted_unique(rows)
        for rows in util.get_ranges(all_rows):
            if mode == cons.MODE.TIME:
                start = 0.0
                if min(rows) > 0:
                    start = self.times[min(rows) - 1][HIDE]
                    start = self.calc.time_to_seconds(start)
                duration = 3.0
                if min(rows) < len(self.times):
                    end = self.times[min(rows)][SHOW]
                    end = self.calc.time_to_seconds(end)
                    duration = (end - start) / len(rows)
            if mode == cons.MODE.FRAME:
                start = 0
                if min(rows) > 0:
                    start = self.frames[min(rows) - 1][HIDE]
                duration = self.calc.seconds_to_frame(3.0)
                if min(rows) < len(self.times):
                    end = self.frames[min(rows)][SHOW]
                    duration = int((end - start) / len(rows))
            for i, row in enumerate(rows):
                time, frame = self.expand_positions(
                    start + (i * duration), start + ((i + 1) * duration))
                self.times.insert(row, time)
                self.frames.insert(row, frame)
                self.main_texts.insert(row, u"")
                self.tran_texts.insert(row, u"")

        self.register_action(
            register=register,
            docs=[cons.DOCUMENT.MAIN, cons.DOCUMENT.TRAN],
            description=_("Inserting subtitles"),
            revert_method=self.remove_subtitles,
            revert_args=[all_rows],)

        self.emit("subtitles-inserted", all_rows)

    @revertable
    def merge_subtitles(self, rows, register=-1):
        """Merge subtitles."""

        rows = sorted(rows)
        positions = self.get_positions()
        show = positions[rows[0]][SHOW]
        hide = positions[rows[-1]][HIDE]
        time, frame = self.expand_positions(show, hide)
        main_texts = list(self.main_texts[x] for x in rows)
        tran_texts = list(self.tran_texts[x] for x in rows)
        for texts in (main_texts, tran_texts):
            while "" in texts:
                texts.remove("")
        main_text = "\n".join(main_texts)
        tran_text = "\n".join(tran_texts)

        self.remove_subtitles(rows, register=register)
        self.insert_subtitles(
            [rows[0]], [time], [frame], [main_text], [tran_text],
            register=register)
        self.group_actions(register, 2, _("Merging subtitles"))

    @revertable
    def paste_texts(self, row, doc, register=-1):
        """Paste texts from the clipboard.

        Return the rows that were pasted into.
        """
        data = self.clipboard.data
        excess = len(data) - (len(self.times) - row)
        if excess > 0:
            rows = range(len(self.times), len(self.times) + excess)
            self.insert_blank_subtitles(rows, register=register)

        rows = []
        new_texts = []
        for i, text in enumerate(data):
            if text is not None:
                rows.append(row + i)
                new_texts.append(text)
        self.replace_texts(rows, doc, new_texts, register=register)
        if excess > 0:
            self.group_actions(register, 2, "")
        self.set_action_description(register, _("Pasting texts"))
        return rows

    @revertable
    @notify_frozen
    def remove_subtitles(self, rows, register=-1):
        """Remove subtitles."""

        times = []
        frames = []
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
            docs=[cons.DOCUMENT.MAIN, cons.DOCUMENT.TRAN],
            description=_("Removing subtitles"),
            revert_method=self.insert_subtitles,
            revert_args=[rows, times, frames, main_texts, tran_texts],)

        self.emit("subtitles-removed", rows)

    @revertable
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
            [main_text, u""],
            [tran_text, u""],
            register=register)
        self.group_actions(register, 2, _("Splitting subtitle"))
