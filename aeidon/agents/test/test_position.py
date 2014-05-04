# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import aeidon


class TestPositionAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()

    def test_adjust_durations__gap(self):
        subtitles = self.project.subtitles
        subtitles[0].start = "00:00:01.000"
        subtitles[0].end   = "00:00:02.000"
        subtitles[1].start = "00:00:02.000"
        subtitles[1].end   = "00:00:03.000"
        subtitles[2].start = "00:00:04.000"
        self.project.adjust_durations(self.project.get_all_indices(),
                                      gap=0.3)

        assert subtitles[0].start == "00:00:01.000"
        assert subtitles[0].end   == "00:00:01.700"
        assert subtitles[1].start == "00:00:02.000"
        assert subtitles[1].end   == "00:00:03.000"
        assert subtitles[2].start == "00:00:04.000"

    def test_adjust_durations__lengthen(self):
        subtitles = self.project.subtitles
        subtitles[0].start = "00:00:01.000"
        subtitles[0].end   = "00:00:01.100"
        subtitles[1].start = "00:00:02.000"
        subtitles[1].end   = "00:00:02.100"
        subtitles[0].main_text = "1234567890"
        subtitles[1].main_text = "12345678901234567890"
        self.project.adjust_durations(None,
                                      speed=20,
                                      lengthen=True)

        assert subtitles[0].start == "00:00:01.000"
        assert subtitles[0].end   == "00:00:01.500"
        assert subtitles[1].start == "00:00:02.000"
        assert subtitles[1].end   == "00:00:03.000"

    def test_adjust_durations__maximum(self):
        subtitles = self.project.subtitles
        subtitles[0].start = "00:00:01.000"
        subtitles[0].end   = "00:00:01.100"
        subtitles[1].start = "00:00:02.000"
        subtitles[1].end   = "00:00:02.100"
        self.project.adjust_durations(None,
                                      speed=10,
                                      lengthen=True,
                                      maximum=0.5)

        assert subtitles[0].start == "00:00:01.000"
        assert subtitles[0].end   == "00:00:01.500"
        assert subtitles[1].start == "00:00:02.000"
        assert subtitles[1].end   == "00:00:02.500"

    def test_adjust_durations__minimum(self):
        subtitles = self.project.subtitles
        subtitles[0].start = "00:00:01.000"
        subtitles[0].end   = "00:00:01.900"
        subtitles[1].start = "00:00:02.000"
        subtitles[1].end   = "00:00:02.900"
        self.project.adjust_durations(None,
                                      speed=1000,
                                      shorten=True,
                                      minimum=0.5)

        assert subtitles[0].start == "00:00:01.000"
        assert subtitles[0].end   == "00:00:01.500"
        assert subtitles[1].start == "00:00:02.000"
        assert subtitles[1].end   == "00:00:02.500"

    def test_adjust_durations__shorten(self):
        subtitles = self.project.subtitles
        subtitles[0].start = "00:00:01.000"
        subtitles[0].end   = "00:00:01.900"
        subtitles[1].start = "00:00:02.000"
        subtitles[1].end   = "00:00:02.900"
        subtitles[0].main_text = "1234567890"
        subtitles[1].main_text = "12345678901234567890"
        self.project.adjust_durations(None,
                                      speed=100,
                                      shorten=True)

        assert subtitles[0].start == "00:00:01.000"
        assert subtitles[0].end   == "00:00:01.100"
        assert subtitles[1].start == "00:00:02.000"
        assert subtitles[1].end   == "00:00:02.200"

    def test_convert_framerate__frame(self):
        self.project.open_main(self.new_microdvd_file(), "ascii")
        self.project.subtitles[0].start = 100
        self.project.subtitles[1].start = 200
        self.project.convert_framerate(self.project.get_all_indices(),
                                       aeidon.framerates.FPS_23_976,
                                       aeidon.framerates.FPS_25_000)

        assert self.project.framerate == aeidon.framerates.FPS_25_000
        for subtitle in self.project.subtitles:
            assert subtitle.framerate == aeidon.framerates.FPS_25_000
        assert self.project.subtitles[0].start == 104
        assert self.project.subtitles[1].start == 209

    def test_convert_framerate__time(self):
        self.project.open_main(self.new_subrip_file(), "ascii")
        self.project.subtitles[0].start = "00:00:01.000"
        self.project.subtitles[1].start = "00:00:02.000"
        self.project.convert_framerate(None,
                                       aeidon.framerates.FPS_23_976,
                                       aeidon.framerates.FPS_25_000)

        assert self.project.framerate == aeidon.framerates.FPS_25_000
        for subtitle in self.project.subtitles:
            assert subtitle.framerate == aeidon.framerates.FPS_25_000
        assert self.project.subtitles[0].start == "00:00:00.959"
        assert self.project.subtitles[1].start == "00:00:01.918"

    def test_set_framerate(self):
        self.project.set_framerate(aeidon.framerates.FPS_25_000)
        assert self.project.framerate == aeidon.framerates.FPS_25_000
        for subtitle in self.project.subtitles:
            assert subtitle.framerate == aeidon.framerates.FPS_25_000

    @aeidon.deco.reversion_test
    def test_shift_positions__frame(self):
        orig_subtitles = [x.copy() for x in self.project.subtitles]
        indices = self.project.get_all_indices()
        self.project.shift_positions(indices, -10)
        for i, subtitle in enumerate(self.project.subtitles):
            start = orig_subtitles[i].start_frame - 10
            end = orig_subtitles[i].end_frame - 10
            assert subtitle.start_frame == start
            assert subtitle.end_frame == end

    @aeidon.deco.reversion_test
    def test_shift_positions__time(self):
        orig_subtitles = [x.copy() for x in self.project.subtitles]
        self.project.shift_positions(None, "00:00:01.000")
        for i, subtitle in enumerate(self.project.subtitles):
            start = round(orig_subtitles[i].start_seconds + 1.0, 3)
            end = round(orig_subtitles[i].end_seconds + 1.0, 3)
            assert round(subtitle.start_seconds, 3) == start
            assert round(subtitle.end_seconds, 3) == end

    @aeidon.deco.reversion_test
    def test_shift_positions__seconds(self):
        orig_subtitles = [x.copy() for x in self.project.subtitles]
        self.project.shift_positions(None, 1.0)
        for i, subtitle in enumerate(self.project.subtitles):
            start = round(orig_subtitles[i].start_seconds + 1.0, 3)
            end = round(orig_subtitles[i].end_seconds + 1.0, 3)
            assert round(subtitle.start_seconds, 3) == start
            assert round(subtitle.end_seconds, 3) == end

    @aeidon.deco.reversion_test
    def test_transform_positions__frame(self):
        indices = self.project.get_all_indices()
        self.project.transform_positions(indices, (2, 10), (6, 100))
        assert self.project.subtitles[2].start_frame == 10
        for subtitle in self.project.subtitles[3:6]:
            assert 10 < subtitle.start_frame < 100
        assert self.project.subtitles[6].start_frame == 100

    @aeidon.deco.reversion_test
    def test_transform_positions__seconds(self):
        self.project.transform_positions(None, (2, 20.0), (6, 200.0))
        assert self.project.subtitles[2].start_seconds == 20.0
        for subtitle in self.project.subtitles[3:6]:
            assert 20.0 < subtitle.start_seconds < 200.0
        assert self.project.subtitles[6].start_seconds == 200.0

    @aeidon.deco.reversion_test
    def test_transform_positions__time(self):
        a, b = "00:00:01.000", "00:00:45.000"
        self.project.transform_positions(None, (2, a), (6, b))
        assert self.project.subtitles[2].start_time == a
        for subtitle in self.project.subtitles[3:6]:
            assert a < subtitle.start_time < b
        assert self.project.subtitles[6].start_time == b
