# Copyright (C) 2005-2008 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Opening subtitle files."""

import bisect
import gaupol


class OpenAgent(gaupol.Delegate):

    """Opening subtitle files."""

    __metaclass__ = gaupol.Contractual

    def _align_translations(self, subtitles):
        """Add translation texts aligned with main document."""

        m = t = 0
        mode = self.main_file.mode
        while t < len(subtitles):
            ts = subtitles[t].get_start(mode)
            te = subtitles[t].get_end(mode)
            tt = subtitles[t].main_text
            tm = self.calc.get_middle(ts, te)
            if m < len(self.subtitles):
                ms = self.subtitles[m].get_start(mode)
                me = self.subtitles[m].get_end(mode)
                tm_cmp_ms = self.calc.compare(tm, ms)
                tm_cmp_me = self.calc.compare(tm, me)
            if (m == len(self.subtitles)) or (tm_cmp_ms == -1):
                subtitle = self.get_subtitle()
                subtitle.start = subtitles[t].start
                subtitle.end = subtitles[t].end
                subtitle.tran_text = tt
                self.subtitles.insert(m, subtitle)
                ms = subtitle.get_start(mode)
                me = subtitle.get_end(mode)
                tm_cmp_ms = self.calc.compare(tm, ms)
                tm_cmp_me = self.calc.compare(tm, me)
            elif (tm_cmp_ms == 1) and (tm_cmp_me == -1):
                self.subtitles[m].tran_text = tt
            if tm_cmp_me == -1: t += 1
            if tm_cmp_ms ==  1: m += 1

    def _append_translations(self, subtitles):
        """Add translation texts by appending them."""

        current = len(self.subtitles)
        excess = len(subtitles) - current
        indices = range(current, current + excess)
        self.insert_blank_subtitles(indices, register=None)
        for i, subtitle in enumerate(subtitles):
            self.subtitles[i].tran_text = subtitle.main_text

    def _read_file(self, file):
        """Read file and return subtitles.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise ParseError if parsing fails.
        """
        try: return file.read()
        except (IOError, UnicodeError): raise
        except Exception:
            raise gaupol.ParseError("Failed to parse file %s" % repr(file))

    def _sort_subtitles_ensure(self, value, unsorted_subtitles):
        sorted_subtitles, wrong_order_count = value
        for i in range(len(sorted_subtitles) - 1):
            assert sorted_subtitles[i] <= sorted_subtitles[i + 1]

    def _sort_subtitles(self, unsorted_subtitles):
        """Sort and return subtitles and sort count.

        Subtitles are sorted according to their start times.
        Sort count is the amount of subtitles that needed to be moved.
        """
        wrong_order_count = 0
        sorted_subtitles = []
        while unsorted_subtitles:
            subtitle = unsorted_subtitles.pop(0)
            index = bisect.bisect(sorted_subtitles, subtitle)
            if index < len(sorted_subtitles):
                wrong_order_count += 1
            sorted_subtitles.insert(index, subtitle)
        return sorted_subtitles, wrong_order_count

    def open_main_require(self, path, encoding):
        assert gaupol.encodings.is_valid_code(encoding)

    def open_main_ensure(self, value, path, encoding):
        assert self.main_file is not None
        assert self.main_changed == 0
        assert self.tran_file == None
        assert self.tran_changed == None

    @gaupol.deco.notify_frozen
    def open_main(self, path, encoding):
        """Open main file reading all subtitle fields.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FormatError if unable to detect the format.
        Raise ParseError if parsing fails.
        Return sort count.
        """
        # Check for a Unicode BOM first to avoid getting a FormatError in the
        # case where an unsuitable encoding decodes a file into garbage without
        # raising a UnicodeDecodeError. If a Unicode BOM is found, use the
        # corresponding encoding to open the file.
        bom_encoding = gaupol.encodings.detect_bom(path)
        if bom_encoding not in (encoding, None):
            return self.open_main(path, bom_encoding)
        format = gaupol.FormatDeterminer().determine(path, encoding)
        self.main_file = gaupol.files.new(format, path, encoding)
        subtitles = self._read_file(self.main_file)
        self.subtitles, sort_count = self._sort_subtitles(subtitles)
        self.set_framerate(self.framerate, register=None)
        # Get framerate from MPsub header.
        if self.main_file.format == gaupol.formats.MPSUB:
            if self.main_file.framerate is not None:
                self.set_framerate(self.main_file.framerate, register=None)
        self.main_changed = 0
        self.tran_file = None
        self.tran_changed = None
        self.emit("main-file-opened", self.main_file)
        return sort_count

    def open_translation_require(self, path, encoding, align_method=None):
        assert self.main_file is not None
        assert gaupol.encodings.is_valid_code(encoding)

    def open_translation_ensure(self, *args, **kwargs):
        assert self.tran_file is not None
        assert self.tran_changed == 0

    @gaupol.deco.notify_frozen
    def open_translation(self, path, encoding, align_method=None):
        """Open translation file reading texts.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FileFormatError if unable to detect the format.
        Raise ParseError if parsing fails.
        Return sort count.
        """
        if align_method is None:
            align_method = gaupol.align_methods.POSITION
        # Check for a Unicode BOM first to avoid getting a FormatError in the
        # case where an unsuitable encoding decodes a file into garbage without
        # raising a UnicodeDecodeError. If a Unicode BOM is found, use the
        # corresponding encoding to open the file.
        bom_encoding = gaupol.encodings.detect_bom(path)
        if bom_encoding not in (encoding, None):
            return self.open_main(path, bom_encoding)
        format = gaupol.FormatDeterminer().determine(path, encoding)
        self.tran_file = gaupol.files.new(format, path, encoding)
        subtitles = self._read_file(self.tran_file)
        subtitles, sort_count = self._sort_subtitles(subtitles)
        for subtitle in subtitles:
            subtitle.framerate = self.framerate
        for subtitle in self.subtitles:
            subtitle.tran_text = ""
        blocked = self.block("subtitles-inserted")
        if align_method == gaupol.align_methods.POSITION:
            self._align_translations(subtitles)
        elif align_method == gaupol.align_methods.NUMBER:
            self._append_translations(subtitles)
        self.unblock("subtitles-inserted", blocked)
        self.tran_changed = 0
        self.emit("translation-file-opened", self.tran_file)
        return sort_count
