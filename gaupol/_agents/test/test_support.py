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


from gaupol import cons
from gaupol.unittest import TestCase, reversion_test


class TestSupportAgent(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()

    def test_expand_frames(self):

        calc = self.project.calc
        time, frame = self.project.expand_frames(10, 100)
        assert frame == [10, 100, 90]
        assert time == [calc.frame_to_time(x) for x in frame]

    def test_expand_positions(self):

        output = self.project.expand_positions(10, 100)
        assert self.project.expand_frames(10, 100) == output

        output = self.project.expand_positions(10.0, 100.0)
        assert self.project.expand_seconds(10.0, 100.0) == output

        times = ("00:00:01.000", "00:01:00.000")
        output = self.project.expand_positions(*times)
        assert self.project.expand_times(*times) == output

    def test_expand_seconds(self):

        calc = self.project.calc
        time, frame = self.project.expand_seconds(10.0, 100.0)
        assert time == ["00:00:10.000", "00:01:40.000", "00:01:30.000"]
        assert frame == [calc.time_to_frame(x) for x in time]

    def test_expand_times(self):

        calc = self.project.calc
        times = ("00:00:01.000", "00:01:00.000")
        time, frame = self.project.expand_times(*times)
        assert time == ["00:00:01.000", "00:01:00.000", "00:00:59.000"]
        assert frame == [calc.time_to_frame(x) for x in time]

    def test_get_file(self):

        file = self.project.get_file(cons.DOCUMENT.MAIN)
        assert file == self.project.main_file
        file = self.project.get_file(cons.DOCUMENT.TRAN)
        assert file == self.project.tran_file

    def test_get_format_class_name(self):

        # pylint: disable-msg=E1101
        name = self.project.get_format_class_name(cons.DOCUMENT.MAIN)
        assert name == self.project.main_file.format.class_name
        name = self.project.get_format_class_name(cons.DOCUMENT.TRAN)
        assert name == self.project.tran_file.format.class_name

    def test_get_line_lengths(self):

        self.project.main_texts[0] = "<i>test\ntest.</i>"
        assert self.project.get_line_lengths(0, cons.DOCUMENT.MAIN) == [4, 5]
        self.project.main_texts[0] = ""
        assert self.project.get_line_lengths(0, cons.DOCUMENT.MAIN) == [0]

    def test_get_mode(self):

        self.project.open_main(self.get_subrip_path(), "ascii")
        assert self.project.get_mode() == cons.MODE.TIME
        self.project.open_main(self.get_microdvd_path(), "ascii")
        assert self.project.get_mode() == cons.MODE.FRAME

    def test_get_positions(self):

        self.project.open_main(self.get_subrip_path(), "ascii")
        assert self.project.get_positions() == self.project.times
        self.project.open_main(self.get_microdvd_path(), "ascii")
        assert self.project.get_positions() == self.project.frames

    def test_get_tag_regex(self):

        re_tag = self.project.get_tag_regex(cons.DOCUMENT.MAIN)
        assert self.is_regex(re_tag)

        self.project.main_file = None
        re_tag = self.project.get_tag_regex(cons.DOCUMENT.MAIN)
        assert re_tag is None

    def test_get_text_length(self):

        self.project.main_texts[0] = "<i>test\ntest.</i>"
        assert self.project.get_text_length(0, cons.DOCUMENT.MAIN) == 10
        self.project.main_texts[0] = ""
        assert self.project.get_text_length(0, cons.DOCUMENT.MAIN) == 0

    def test_get_texts(self):

        texts = self.project.get_texts(cons.DOCUMENT.MAIN)
        assert texts == self.project.main_texts
        texts = self.project.get_texts(cons.DOCUMENT.TRAN)
        assert texts == self.project.tran_texts

    @reversion_test
    def test_insert_subtitles(self):

        rows = [0, 1]
        times = self.project.times[0:2]
        frames = self.project.frames[0:2]
        texts = ["0", "1"]
        orig_length = len(self.project.main_texts)
        self.project.insert_subtitles(rows, times, frames, texts, texts)
        assert len(self.project.main_texts) == orig_length + 2
        assert self.project.main_texts[0] == "0"
        assert self.project.main_texts[1] == "1"

    @reversion_test
    def test_insert_subtitles_excess(self):

        orig_length = len(self.project.main_texts)
        rows = [orig_length]
        times = self.project.times[-1]
        frames = self.project.frames[-1]
        texts = [""]
        self.project.insert_subtitles(rows, times, frames, texts, texts)
        assert len(self.project.main_texts) == orig_length + 1
        assert self.project.main_texts[orig_length] == ""

    @reversion_test
    def test_replace_both_texts(self):

        self.project.replace_both_texts(
            [[1, 2], [3, 4]], [["", ""], ["", ""]])
        assert self.project.main_texts[1] == ""
        assert self.project.main_texts[2] == ""
        assert self.project.tran_texts[3] == ""
        assert self.project.tran_texts[4] == ""

    @reversion_test
    def test_replace_both_texts_main(self):

        self.project.replace_both_texts(
            [[1, 2, 3], []], [["", "", ""], []])
        assert self.project.main_texts[1] == ""
        assert self.project.main_texts[2] == ""
        assert self.project.main_texts[3] == ""

    def test_replace_both_texts_none(self):

        self.project.replace_both_texts(
            [[], []], [[], []])
        assert not self.project.can_undo()

    @reversion_test
    def test_replace_both_texts_tran(self):

        self.project.replace_both_texts(
            [[], [1, 2, 3]], [[], ["", "", ""]])
        assert self.project.tran_texts[1] == ""
        assert self.project.tran_texts[2] == ""
        assert self.project.tran_texts[3] == ""

    @reversion_test
    def test_replace_positions(self):

        frame = [10, 20, 10]
        time = ["00:00:01.000", "00:00:02.000", "00:00:01.000"]
        self.project.replace_positions([3], [time], [frame])
        assert self.project.times[3] == time
        assert self.project.frames[3] == frame

    @reversion_test
    def test_replace_texts_main(self):

        self.project.replace_texts(
            [1, 2], cons.DOCUMENT.MAIN, ["", ""])
        assert self.project.main_texts[1] == ""
        assert self.project.main_texts[2] == ""

    @reversion_test
    def test_replace_texts_tran(self):

        self.project.replace_texts(
            [3, 4], cons.DOCUMENT.TRAN, ["", ""])
        assert self.project.tran_texts[3] == ""
        assert self.project.tran_texts[4] == ""
