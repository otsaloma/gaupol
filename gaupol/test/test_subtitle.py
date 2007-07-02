# Copyright (C) 2007 Osmo Salomaa
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


import gaupol

from gaupol import unittest
from .. import subtitle


class TestSubtitle(unittest.TestCase):

    def setup_method(self, method):

        self.time_sub = subtitle.Subtitle()
        self.time_sub.mode = gaupol.MODE.TIME
        self.time_sub.framerate = gaupol.FRAMERATE.P25
        self.time_sub.start = "00:00:01.000"
        self.time_sub.end = "00:00:03.000"
        self.time_sub.main_text = "main"
        self.time_sub.tran_text = "translation"

        self.frame_sub = subtitle.Subtitle()
        self.frame_sub.mode = gaupol.MODE.FRAME
        self.frame_sub.framerate = gaupol.FRAMERATE.P25
        self.frame_sub.start = 100
        self.frame_sub.end = 300
        self.frame_sub.main_text = "main"
        self.frame_sub.tran_text = "translation"

    def test___cmp__(self):

        assert self.time_sub < self.frame_sub

    def test__get_duration(self):

        assert self.time_sub.duration == "00:00:02.000"
        assert self.frame_sub.duration == 200

    def test__get_duration_frame(self):

        assert self.time_sub.duration_frame == 50
        assert self.frame_sub.duration_frame == 200

    def test__get_duration_seconds(self):

        assert self.time_sub.duration_seconds == 2.0
        assert self.frame_sub.duration_seconds == 8.0

    def test__get_duration_time(self):

        assert self.time_sub.duration_time == "00:00:02.000"
        assert self.frame_sub.duration_time == "00:00:08.000"

    def test__get_end(self):

        assert self.time_sub.end == "00:00:03.000"
        assert self.frame_sub.end == 300

    def test__get_end_frame(self):

        assert self.time_sub.end_frame == 75
        assert self.frame_sub.end_frame == 300

    def test__get_end_seconds(self):

        assert self.time_sub.end_seconds == 3.0
        assert self.frame_sub.end_seconds == 12.0

    def test__get_end_time(self):

        assert self.time_sub.end_time == "00:00:03.000"
        assert self.frame_sub.end_time == "00:00:12.000"

    def test__get_framerate(self):

        assert self.time_sub.framerate == gaupol.FRAMERATE.P25
        assert self.frame_sub.framerate == gaupol.FRAMERATE.P25

    def test__get_main_text(self):

        assert self.time_sub.main_text == u"main"
        assert self.frame_sub.main_text == u"main"

    def test__get_mode(self):

        assert self.time_sub.mode == gaupol.MODE.TIME
        assert self.frame_sub.mode == gaupol.MODE.FRAME

    def test__get_start(self):

        assert self.time_sub.start == "00:00:01.000"
        assert self.frame_sub.start == 100

    def test__get_start_frame(self):

        assert self.time_sub.start_frame == 25
        assert self.frame_sub.start_frame == 100

    def test__get_start_seconds(self):

        assert self.time_sub.start_seconds == 1.0
        assert self.frame_sub.start_seconds == 4.0

    def test__get_start_time(self):

        assert self.time_sub.start_time == "00:00:01.000"
        assert self.frame_sub.start_time == "00:00:04.000"

    def test__get_tran_text(self):

        assert self.time_sub.tran_text == u"translation"
        assert self.frame_sub.tran_text == u"translation"

    def test__set_duration(self):

        self.time_sub.duration = "00:00:10.000"
        assert self.time_sub.end_time == "00:00:11.000"
        self.time_sub.duration = 500
        assert self.time_sub.end_time == "00:00:21.000"

        self.frame_sub.duration = 500
        assert self.frame_sub.end_frame == 600
        self.frame_sub.duration = "00:00:10.000"
        assert self.frame_sub.end_frame == 350

    def test__set_end(self):

        self.time_sub.end = "00:00:10.000"
        assert self.time_sub.end_time == "00:00:10.000"
        self.time_sub.end = 500
        assert self.time_sub.end_time == "00:00:20.000"

        self.frame_sub.end = 500
        assert self.frame_sub.end_frame == 500
        self.frame_sub.end = "00:00:10.000"
        assert self.frame_sub.end_frame == 250

    def test__set_framerate(self):

        self.time_sub.framerate = gaupol.FRAMERATE.P30
        assert self.time_sub.framerate == gaupol.FRAMERATE.P30
        assert self.time_sub._calc.framerate == gaupol.FRAMERATE.P30.value

    def test__set_main_text(self):

        self.time_sub.main_text = "test"
        assert self.time_sub.main_text == u"test"

    def test__set_mode(self):

        self.time_sub.mode = gaupol.MODE.TIME
        self.time_sub.mode = gaupol.MODE.FRAME
        assert self.time_sub._start == 25
        assert self.time_sub._end == 75

        self.frame_sub.mode = gaupol.MODE.FRAME
        self.frame_sub.mode = gaupol.MODE.TIME
        assert self.frame_sub._start == "00:00:04.000"
        assert self.frame_sub._end == "00:00:12.000"

    def test__set_start(self):

        self.time_sub.start = "00:00:10.000"
        assert self.time_sub.start_time == "00:00:10.000"
        self.time_sub.start = 500
        assert self.time_sub.start_time == "00:00:20.000"

        self.frame_sub.start = 500
        assert self.frame_sub.start_frame == 500
        self.frame_sub.start = "00:00:10.000"
        assert self.frame_sub.start_frame == 250

    def test__set_tran_text(self):

        self.time_sub.tran_text = "test"
        assert self.time_sub.tran_text == u"test"

    def test_convert_framerate(self):

        self.time_sub.start = "00:00:01.000"
        self.time_sub.end = "00:00:02.000"
        self.time_sub.convert_framerate(gaupol.FRAMERATE.P24)
        assert self.time_sub.framerate == gaupol.FRAMERATE.P24
        assert self.time_sub.start == "00:00:01.043"
        assert self.time_sub.end == "00:00:02.085"

        self.frame_sub.start = 100
        self.frame_sub.end = 200
        self.frame_sub.convert_framerate(gaupol.FRAMERATE.P24)
        assert self.frame_sub.framerate == gaupol.FRAMERATE.P24
        assert self.frame_sub.start == 96
        assert self.frame_sub.end == 192

    def test_copy(self):

        copy = self.time_sub.copy()
        assert copy == self.time_sub
        assert not copy is self.time_sub

    def test_get_duration(self):

        value = self.time_sub.get_duration(gaupol.MODE.TIME)
        assert value == "00:00:02.000"
        value = self.time_sub.get_duration(gaupol.MODE.FRAME)
        assert value == 50

        value = self.frame_sub.get_duration(gaupol.MODE.TIME)
        assert value == "00:00:08.000"
        value = self.frame_sub.get_duration(gaupol.MODE.FRAME)
        assert value == 200

    def test_get_end(self):

        value = self.time_sub.get_end(gaupol.MODE.TIME)
        assert value == "00:00:03.000"
        value = self.time_sub.get_end(gaupol.MODE.FRAME)
        assert value == 75

        value = self.frame_sub.get_end(gaupol.MODE.TIME)
        assert value == "00:00:12.000"
        value = self.frame_sub.get_end(gaupol.MODE.FRAME)
        assert value == 300

    def test_get_start(self):

        value = self.time_sub.get_start(gaupol.MODE.TIME)
        assert value == "00:00:01.000"
        value = self.time_sub.get_start(gaupol.MODE.FRAME)
        assert value == 25

        value = self.frame_sub.get_start(gaupol.MODE.TIME)
        assert value == "00:00:04.000"
        value = self.frame_sub.get_start(gaupol.MODE.FRAME)
        assert value == 100

    def test_get_text(self):

        value = self.time_sub.get_text(gaupol.DOCUMENT.MAIN)
        assert value == "main"
        value = self.time_sub.get_text(gaupol.DOCUMENT.TRAN)
        assert value == "translation"

    def test_set_text(self):

        self.time_sub.set_text(gaupol.DOCUMENT.MAIN, "")
        assert self.time_sub.main_text == ""
        self.time_sub.set_text(gaupol.DOCUMENT.TRAN, "")
        assert self.time_sub.tran_text == ""

    def test_scale_positions(self):

        self.time_sub.scale_positions(2.0)
        assert self.time_sub.start == "00:00:02.000"
        assert self.time_sub.end == "00:00:06.000"
        self.frame_sub.scale_positions(2.0)
        assert self.frame_sub.start == 200
        assert self.frame_sub.end == 600

    def test_shift_positions(self):

        self.time_sub.shift_positions("00:00:01.000")
        assert self.time_sub._start == "00:00:02.000"
        assert self.time_sub._end == "00:00:04.000"
        self.frame_sub.shift_positions(-10)
        assert self.frame_sub._start == 90
        assert self.frame_sub._end == 290
        self.time_sub.shift_positions(2.0)
        assert self.time_sub._start == "00:00:04.000"
        assert self.time_sub._end == "00:00:06.000"
