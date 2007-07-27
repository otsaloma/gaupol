# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Opening subtitle files."""

import gaupol


class OpenAgent(gaupol.Delegate):

    """Opening subtitle files."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = gaupol.Contractual

    def _adapt_translations(self, mode, starts, ends, texts):
        """Open translation file data in an adaptive manner."""

        for subtitle in self.subtitles:
            subtitle.tran_text = ""

        m = 0
        t = 0
        while t < len(starts):
            middle = self.calc.get_middle(starts[t], ends[t])
            if m < len(self.subtitles):
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

    def _read_file(self, file):
        """Read file and return starts, ends, texts.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise ParseError if parsing fails.
        """
        try:
            return file.read()
        except (IOError, UnicodeError):
            raise
        except Exception:
            raise gaupol.ParseError

    def _sort(self, starts, ends, texts):
        """Sort and return data based on start positions."""

        sorts = []
        sort_function = cmp
        if starts and isinstance(starts[0], basestring):
            sort_function = self.calc.compare_times
        def compare_starts(x, y):
            value = sort_function(x[0], y[0])
            sorts.append(value == -1)
            return value
        fields = []
        for i in range(len(starts)):
            fields.append((starts[i], ends[i], texts[i]))
        fields.sort(compare_starts)
        starts = [x[0] for x in fields]
        ends =   [x[1] for x in fields]
        texts =  [x[2] for x in fields]
        return starts, ends, texts, sum(sorts)

    def open_main_require(self, path, encoding):
        assert gaupol.encodings.is_valid_code(encoding)

    def open_main_ensure(self, value, path, encoding):
        assert self.main_file is not None
        assert self.main_changed == 0
        assert self.tran_changed == None

    @gaupol.util.notify_frozen
    def open_main(self, path, encoding):
        """Open main file reading positions and texts.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FormatError if unable to detect the format.
        Raise ParseError if parsing fails.
        Return sort count.
        """
        format = gaupol.FormatDeterminer().determine(path, encoding)
        self.main_file = gaupol.files.get_class(format)(path, encoding)
        values = self._read_file(self.main_file)
        starts, ends, texts, sort_count = self._sort(*values)

        # Get framerate from MPsub header.
        if self.main_file.format == gaupol.FORMAT.MPSUB:
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
        assert gaupol.encodings.is_valid_code(encoding)

    def open_translation_ensure(self, value, path, encoding, smart=True):
        assert self.tran_file is not None
        assert self.tran_changed == 0

    @gaupol.util.notify_frozen
    def open_translation(self, path, encoding, smart=True):
        """Open translation file reading texts.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FileFormatError if unable to detect the format.
        Raise ParseError if parsing fails.
        Return sort count.
        """
        format = gaupol.FormatDeterminer().determine(path, encoding)
        self.tran_file = gaupol.files.get_class(format)(path, encoding)
        values = self._read_file(self.tran_file)
        starts, ends, texts, sort_count = self._sort(*values)

        blocked = self.block("subtitles-inserted")
        method = (self._append_translations, self._adapt_translations)[smart]
        method(self.tran_file.mode, starts, ends, texts)
        self.unblock("subtitles-inserted", blocked)

        self.tran_changed = 0
        self.emit("translation-file-opened", self.tran_file)
        return sort_count
