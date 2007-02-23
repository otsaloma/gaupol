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


"""Opening subtitle files."""


from gaupol import cons
from gaupol.base import Delegate, notify_frozen
from gaupol.determiner import FormatDeterminer
from gaupol.files import *
from .index import SHOW, HIDE, DURN


class OpenAgent(Delegate):

    """Opening subtitle files.

    Instance variables:

        _sort_count: The amount of sort operations made
    """

    # pylint: disable-msg=E0203,W0201

    def __init__(self, master):

        Delegate.__init__(self, master)

        self._sort_count = 0

    def _adapt_translation(self, shows, hides, texts):
        """Open translation file data in an adaptive manner."""

        m = 0
        t = 0
        positions = self.get_positions(self.tran_file.mode)
        while t < len(shows):
            middle = self.calc.get_middle(shows[t], hides[t])
            time, frame = self.expand_positions(shows[t], hides[t])
            if m == len(self.times) or middle < positions[m][SHOW]:
                self.insert_subtitles(
                    [m], [time], [frame], [u""], [texts[t]], register=None)
                m += 1
                t += 1
                continue
            if middle > positions[m][HIDE]:
                m += 1
                continue
            self.tran_texts[m] = texts[t]
            m += 1
            t += 1

    def _sort(self, shows, hides, texts):
        """Sort data based on show positions.

        Return shows, hides, texts.
        """
        def sort(x, y):
            value = cmp(x[0], y[0])
            if value == -1:
                self._sort_count += 1
            return value
        self._sort_count = 0
        data = list([shows[i], hides[i], texts[i]] for i in range(len(shows)))
        data.sort(sort)
        shows = list(x[0] for x in data)
        hides = list(x[1] for x in data)
        texts = list(x[2] for x in data)
        return shows, hides, texts

    @notify_frozen
    def open_main(self, path, encoding):
        """Open main file reading positions and texts.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FormatError if unable to detect the format.
        Return sort count.
        """
        format = FormatDeterminer(path, encoding).determine()
        main_file = eval(format.class_name)(path, encoding)
        shows, hides, texts = self._sort(*main_file.read())
        self.main_file = main_file

        self.times = []
        self.frames = []
        self.main_texts = []
        self.tran_texts = []
        for i in range(len(shows)):
            time, frame = self.expand_positions(shows[i], hides[i])
            self.times.append(time)
            self.frames.append(frame)
            self.main_texts.append(texts[i])
            self.tran_texts.append(u"")

        # Get framerate from MPsub header.
        if self.main_file.format == cons.FORMAT.MPSUB:
            if self.main_file.framerate is not None:
                self.set_framerate(self.main_file.framerate, register=None)

        self.main_changed = 0
        self.tran_changed = 0
        self.tran_active = False
        self.emit("main-file-opened", self.main_file)
        return self._sort_count

    @notify_frozen
    def open_translation(self, path, encoding, smart=True):
        """Open translation file reading texts.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FileFormatError if unable to detect the format.
        Return sort count.
        """
        format = FormatDeterminer(path, encoding).determine()
        tran_file = eval(format.class_name)(path, encoding)
        shows, hides, texts = self._sort(*tran_file.read())
        self.tran_file = tran_file

        blocked = self.block("subtitles-inserted")
        self.tran_texts = [u""] * len(self.tran_texts)
        if smart:
            self._adapt_translation(shows, hides, texts)
        else:
            excess = len(texts) - len(self.main_texts)
            if excess > 0:
                rows = range(len(self.times), len(self.times) + excess)
                self.insert_blank_subtitles(rows, register=None)
            self.tran_texts[:len(texts)] = texts
        self.unblock("subtitles-inserted", blocked)

        self.tran_changed = 0
        self.tran_active = True
        self.emit("translation-file-opened", self.tran_file)
        return self._sort_count
