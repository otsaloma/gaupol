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


from gaupol import const, enclib, files, util
from gaupol.base import Contractual, Delegate
from gaupol.determiner import FormatDeterminer


class OpenAgent(Delegate):

    """Opening subtitle files."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = Contractual

    def _adapt_translations(self, mode, starts, ends, texts):
        """Open translation file data in an adaptive manner."""

        for subtitle in self.subtitles:
            subtitle.tran_text = ""

        m = 0
        t = 0
        while t < len(starts):
            middle = self.calc.get_middle(starts[t], ends[t])
            main_start = self.subtitles[m].get_start(mode)
            if (m == len(self.subtitles)) or (middle < main_start):
                subtitle = self.get_subtitle()
                subtitle.start = starts[t]
                subtitle.end = ends[t]
                subtitle.tran_text = texts[t]
                self.subtitles.insert(m, subtitle)
                m += 1
                t += 1
                continue
            main_end = self.subtitles[m].get_end(mode)
            if middle > main_end:
                m += 1
                continue
            self.subtitles[t].tran_text = texts[t]
            m += 1
            t += 1

    def _append_translations(self, mode, starts, ends, texts):
        """Open translation file data in a simple appending manner."""

        count = len(self.subtitles)
        excess = len(texts) - count
        if excess > 0:
            indexes = range(count, count + excess)
            self.insert_blank_subtitles(indexes, register=None)
        for i, text in enumerate(texts):
            self.subtitles[i].tran_text = text

    def _sort(self, starts, ends, texts):
        """Sort and return data based on start positions."""

        sorts = []
        def compare_starts(x, y):
            value = cmp(x[0], y[0])
            if value == -1:
                sorts.append(1)
            return value
        data = []
        for i in range(len(starts)):
            data.append((starts[i], ends[i], texts[i]))
        data.sort(compare_starts)
        starts = [x[0] for x in data]
        ends   = [x[1] for x in data]
        texts  = [x[2] for x in data]
        return starts, ends, texts, len(sorts)

    def open_main_require(self, path, encoding):
        assert enclib.is_valid(encoding)

    def open_main_ensure(self, value, path, encoding):
        assert self.main_file is not None
        assert self.main_changed == 0
        assert self.tran_changed == None

    @util.notify_frozen
    def open_main(self, path, encoding):
        """Open main file reading positions and texts.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FormatError if unable to detect the format.
        Return sort count.
        """
        format = FormatDeterminer().determine(path, encoding)
        self.main_file = getattr(files, format.class_name)(path, encoding)
        starts, ends, texts, sort_count = self._sort(*self.main_file.read())

        # Get framerate from MPsub header.
        if self.main_file.format == const.FORMAT.MPSUB:
            if self.main_file.framerate is not None:
                self.set_framerate(self.main_file.framerate, register=None)

        self.subtitles = []
        for i in range(len(starts)):
            subtitle = self.get_subtitle()
            subtitle.start = starts[i]
            subtitle.end = ends[i]
            subtitle.main_text = texts[i]
            self.subtitles.append(subtitle)

        self.main_changed = 0
        self.tran_changed = None
        self.emit("main-file-opened", self.main_file)
        return sort_count

    def open_translation_require(self, path, encoding, smart=True):
        assert self.main_file is not None
        assert enclib.is_valid(encoding)

    def open_translation_ensure(self, value, path, encoding, smart=True):
        assert self.tran_file is not None
        assert self.tran_changed == 0

    @util.notify_frozen
    def open_translation(self, path, encoding, smart=True):
        """Open translation file reading texts.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FileFormatError if unable to detect the format.
        Return sort count.
        """
        format = FormatDeterminer().determine(path, encoding)
        self.tran_file = getattr(files, format.class_name)(path, encoding)
        starts, ends, texts, sort_count = self._sort(*self.tran_file.read())

        blocked = self.block("subtitles-inserted")
        method = (self._append_translations, self._adapt_translations)[smart]
        method(self.tran_file.mode, starts, ends, texts)
        self.unblock("subtitles-inserted", blocked)

        self.tran_changed = 0
        self.emit("translation-file-opened", self.tran_file)
        return sort_count
