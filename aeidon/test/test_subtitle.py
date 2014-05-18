# -*- coding: utf-8 -*-

# Copyright (C) 2007 Osmo Salomaa
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

MAIN  = aeidon.documents.MAIN
TRAN  = aeidon.documents.TRAN

FRAME = aeidon.modes.FRAME
TIME  = aeidon.modes.TIME


class TestSubtitle(aeidon.TestCase):

    def setup_method(self, method):
        self.tsub = aeidon.Subtitle()
        self.tsub.mode = TIME
        self.tsub.framerate = aeidon.framerates.FPS_25_000
        self.tsub.start = "00:00:01.000"
        self.tsub.end = "00:00:03.000"
        self.tsub.main_text = "main"
        self.tsub.tran_text = "translation"
        self.fsub = aeidon.Subtitle()
        self.fsub.mode = FRAME
        self.fsub.framerate = aeidon.framerates.FPS_25_000
        self.fsub.start = 100
        self.fsub.end = 300
        self.fsub.main_text = "main"
        self.fsub.tran_text = "translation"

    def test_convert_framerate__frame(self):
        self.fsub.start = 100
        self.fsub.end = 200
        framerate = aeidon.framerates.FPS_23_976
        self.fsub.convert_framerate(framerate)
        assert self.fsub.framerate == framerate
        assert self.fsub.start == 96
        assert self.fsub.end == 192

    def test_convert_framerate__time(self):
        self.tsub.start = "00:00:01.000"
        self.tsub.end = "00:00:02.000"
        framerate = aeidon.framerates.FPS_23_976
        self.tsub.convert_framerate(framerate)
        assert self.tsub.framerate == framerate
        assert self.tsub.start == "00:00:01.043"
        assert self.tsub.end == "00:00:02.085"

    def test_duration__get(self):
        assert self.tsub.duration == "00:00:02.000"
        assert self.fsub.duration == 200

    def test_duration__set_frame(self):
        self.fsub.duration = 500
        assert self.fsub.end_frame == 600
        self.fsub.duration = "00:00:10.000"
        assert self.fsub.end_frame == 350
        self.fsub.duration = 5.0
        assert self.fsub.end_frame == 225

    def test_duration__set_time(self):
        self.tsub.duration = "00:00:10.000"
        assert self.tsub.end_time == "00:00:11.000"
        self.tsub.duration = 500
        assert self.tsub.end_time == "00:00:21.000"
        self.tsub.duration = 10.0
        assert self.tsub.end_time == "00:00:11.000"

    def test_duration_frame__get(self):
        assert self.tsub.duration_frame == 50
        assert self.fsub.duration_frame == 200

    def test_duration_frame__set(self):
        self.fsub.duration_frame = 500
        assert self.fsub.end_frame == 600

    def test_duration_seconds__get(self):
        assert self.tsub.duration_seconds == 2.0
        assert self.fsub.duration_seconds == 8.0

    def test_duration_seconds__set(self):
        self.tsub.duration_seconds = 3.0
        assert self.tsub.end_seconds == 4.0

    def test_duration_time__get(self):
        assert self.tsub.duration_time == "00:00:02.000"
        assert self.fsub.duration_time == "00:00:08.000"

    def test_duration_time__set(self):
        self.tsub.duration_time = "00:00:03.000"
        assert self.tsub.end_time == "00:00:04.000"

    def test_end__get(self):
        assert self.tsub.end == "00:00:03.000"
        assert self.fsub.end == 300

    def test_end__set_frame(self):
        self.fsub.end = 500
        assert self.fsub.end_frame == 500
        self.fsub.end = "00:00:10.000"
        assert self.fsub.end_frame == 250
        self.fsub.end = 5.0
        assert self.fsub.end_frame == 125

    def test_end__set_time(self):
        self.tsub.end = "00:00:10.000"
        assert self.tsub.end_time == "00:00:10.000"
        self.tsub.end = 500
        assert self.tsub.end_time == "00:00:20.000"
        self.tsub.end = 5.0
        assert self.tsub.end_time == "00:00:05.000"

    def test_end_frame__get(self):
        assert self.tsub.end_frame == 75
        assert self.fsub.end_frame == 300

    def test_end_frame__set(self):
        self.fsub.end_frame = 300
        assert self.fsub.end_frame == 300

    def test_end_seconds__get(self):
        assert self.tsub.end_seconds == 3.0
        assert self.fsub.end_seconds == 12.0

    def test_end_seconds__set(self):
        self.tsub.end_seconds = 4.0
        assert self.tsub.end_seconds == 4.0

    def test_end_time__get(self):
        assert self.tsub.end_time == "00:00:03.000"
        assert self.fsub.end_time == "00:00:12.000"

    def test_end_time__set(self):
        self.tsub.end_time = "00:00:04.000"
        assert self.tsub.end_time == "00:00:04.000"

    def test_framerate__get(self):
        assert self.tsub.framerate == aeidon.framerates.FPS_25_000
        assert self.fsub.framerate == aeidon.framerates.FPS_25_000

    def test_framerate__set(self):
        self.tsub.framerate = aeidon.framerates.FPS_29_970
        assert self.tsub.framerate == aeidon.framerates.FPS_29_970

    def test_get_duration(self):
        assert self.tsub.get_duration(TIME) == "00:00:02.000"
        assert self.tsub.get_duration(FRAME) == 50
        assert self.fsub.get_duration(TIME) == "00:00:08.000"
        assert self.fsub.get_duration(FRAME) == 200

    def test_get_end(self):
        assert self.tsub.get_end(TIME) == "00:00:03.000"
        assert self.tsub.get_end(FRAME) == 75
        assert self.fsub.get_end(TIME) == "00:00:12.000"
        assert self.fsub.get_end(FRAME) == 300

    def test_get_start(self):
        assert self.tsub.get_start(TIME) == "00:00:01.000"
        assert self.tsub.get_start(FRAME) == 25
        assert self.fsub.get_start(TIME) == "00:00:04.000"
        assert self.fsub.get_start(FRAME) == 100

    def test_get_text(self):
        assert self.tsub.get_text(MAIN) == "main"
        assert self.tsub.get_text(TRAN) == "translation"

    def test_main_text__get(self):
        assert self.tsub.main_text == "main"
        assert self.fsub.main_text == "main"

    def test_main_text__set(self):
        self.tsub.main_text = "test"
        assert self.tsub.main_text == "test"

    def test_mode__get(self):
        assert self.tsub.mode == TIME
        assert self.fsub.mode == FRAME

    def test_mode__set_frame(self):
        self.fsub.mode = FRAME
        self.fsub.mode = TIME
        assert self.fsub._start == "00:00:04.000"
        assert self.fsub._end == "00:00:12.000"

    def test_mode__set_time(self):
        self.tsub.mode = TIME
        self.tsub.mode = FRAME
        assert self.tsub._start == 25
        assert self.tsub._end == 75

    def test_scale_positions__frame(self):
        self.fsub.scale_positions(2.0)
        assert self.fsub.start == 200
        assert self.fsub.end == 600

    def test_scale_positions__time(self):
        self.tsub.scale_positions(2.0)
        assert self.tsub.start == "00:00:02.000"
        assert self.tsub.end == "00:00:06.000"

    def test_set_text(self):
        self.tsub.set_text(MAIN, "")
        assert self.tsub.main_text == ""
        self.tsub.set_text(TRAN, "")
        assert self.tsub.tran_text == ""

    def test_shift_positions__frame(self):
        self.fsub.shift_positions(-10)
        assert self.fsub._start == 90
        assert self.fsub._end == 290

    def test_shift_positions__seconds(self):
        self.tsub.shift_positions(1.0)
        assert self.tsub._start == "00:00:02.000"
        assert self.tsub._end == "00:00:04.000"

    def test_shift_positions__time(self):
        self.tsub.shift_positions("00:00:01.000")
        assert self.tsub._start == "00:00:02.000"
        assert self.tsub._end == "00:00:04.000"

    def test_start__get(self):
        assert self.tsub.start == "00:00:01.000"
        assert self.fsub.start == 100

    def test_start__set_frame(self):
        self.fsub.start = 500
        assert self.fsub.start_frame == 500
        self.fsub.start = "00:00:10.000"
        assert self.fsub.start_frame == 250
        self.fsub.start = 5.0
        assert self.fsub.start_frame == 125

    def test_start__set_time(self):
        self.tsub.start = "00:00:10.000"
        assert self.tsub.start_time == "00:00:10.000"
        self.tsub.start = 500
        assert self.tsub.start_time == "00:00:20.000"
        self.tsub.start = 5.0
        assert self.tsub.start_time == "00:00:05.000"

    def test_start_frame__get(self):
        assert self.tsub.start_frame == 25
        assert self.fsub.start_frame == 100

    def test_start_frame__set(self):
        self.fsub.start_frame = 25
        assert self.fsub.start_frame == 25

    def test_start_seconds__get(self):
        assert self.tsub.start_seconds == 1.0
        assert self.fsub.start_seconds == 4.0

    def test_start_seconds__set(self):
        self.tsub.start_seconds = 0.1
        assert self.tsub.start_seconds == 0.1

    def test_start_time__get(self):
        assert self.tsub.start_time == "00:00:01.000"
        assert self.fsub.start_time == "00:00:04.000"

    def test_start_time__set(self):
        self.tsub.start_time = "00:00:00.100"
        assert self.tsub.start_time == "00:00:00.100"

    def test_tran_text__get(self):
        assert self.tsub.tran_text == "translation"
        assert self.fsub.tran_text == "translation"

    def test_tran_text_set(self):
        self.tsub.tran_text = "test"
        assert self.tsub.tran_text == "test"
