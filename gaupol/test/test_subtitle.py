# Copyright (C) 2007-2008 Osmo Salomaa
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

import gaupol


class TestSubtitle(gaupol.TestCase):

    def setup_method(self, method):

        self.time_sub = gaupol.Subtitle()
        self.time_sub.mode = gaupol.modes.TIME
        self.time_sub.framerate = gaupol.framerates.FPS_25
        self.time_sub.start = "00:00:01.000"
        self.time_sub.end = "00:00:03.000"
        self.time_sub.main_text = "main"
        self.time_sub.tran_text = "translation"

        self.frame_sub = gaupol.Subtitle()
        self.frame_sub.mode = gaupol.modes.FRAME
        self.frame_sub.framerate = gaupol.framerates.FPS_25
        self.frame_sub.start = 100
        self.frame_sub.end = 300
        self.frame_sub.main_text = "main"
        self.frame_sub.tran_text = "translation"

    def test___cmp__(self):

        assert self.time_sub < self.frame_sub
        assert self.frame_sub > self.time_sub
        assert self.time_sub == self.time_sub
        assert self.frame_sub == self.frame_sub

    def test___cmp____value_error(self):

        self.time_sub._mode = None
        self.raises(ValueError, lambda x: x < x, self.time_sub)

    def test___getattr__(self):

        assert "ssa" not in dir(self.time_sub)
        self.time_sub.ssa.style = "test"
        assert "ssa" in dir(self.time_sub)

    def test__get_duration(self):

        assert self.time_sub.duration == "00:00:02.000"
        assert self.frame_sub.duration == 200

    def test__get_duration__value_error(self):

        self.time_sub._mode = None
        self.raises(ValueError, lambda: self.time_sub.duration)

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

    def test__get_end_frame__value_error(self):

        self.time_sub._mode = None
        self.raises(ValueError, lambda: self.time_sub.end_frame)

    def test__get_end_seconds(self):

        assert self.time_sub.end_seconds == 3.0
        assert self.frame_sub.end_seconds == 12.0

    def test__get_end_time(self):

        assert self.time_sub.end_time == "00:00:03.000"
        assert self.frame_sub.end_time == "00:00:12.000"

    def test__get_end_time__value_error(self):

        self.time_sub._mode = None
        self.raises(ValueError, lambda: self.time_sub.end_time)

    def test__get_framerate(self):

        assert self.time_sub.framerate == gaupol.framerates.FPS_25
        assert self.frame_sub.framerate == gaupol.framerates.FPS_25

    def test__get_main_text(self):

        assert self.time_sub.main_text == u"main"
        assert self.frame_sub.main_text == u"main"

    def test__get_mode(self):

        assert self.time_sub.mode == gaupol.modes.TIME
        assert self.frame_sub.mode == gaupol.modes.FRAME

    def test__get_start(self):

        assert self.time_sub.start == "00:00:01.000"
        assert self.frame_sub.start == 100

    def test__get_start_frame(self):

        assert self.time_sub.start_frame == 25
        assert self.frame_sub.start_frame == 100

    def test__get_start_frame__value_error(self):

        self.time_sub._mode = None
        self.raises(ValueError, lambda: self.time_sub.start_frame)

    def test__get_start_seconds(self):

        assert self.time_sub.start_seconds == 1.0
        assert self.frame_sub.start_seconds == 4.0

    def test__get_start_time(self):

        assert self.time_sub.start_time == "00:00:01.000"
        assert self.frame_sub.start_time == "00:00:04.000"

    def test__get_start_time__value_error(self):

        self.time_sub._mode = None
        self.raises(ValueError, lambda: self.time_sub.start_time)

    def test__get_tran_text(self):

        assert self.time_sub.tran_text == u"translation"
        assert self.frame_sub.tran_text == u"translation"

    def test__set_duration__time(self):

        self.time_sub.duration = "00:00:10.000"
        assert self.time_sub.end_time == "00:00:11.000"
        self.time_sub.duration = 500
        assert self.time_sub.end_time == "00:00:21.000"
        self.time_sub.duration = 10.0
        assert self.time_sub.end_time == "00:00:11.000"

    def test__set_duration__frame(self):

        self.frame_sub.duration = 500
        assert self.frame_sub.end_frame == 600
        self.frame_sub.duration = "00:00:10.000"
        assert self.frame_sub.end_frame == 350
        self.frame_sub.duration = 5.0
        assert self.frame_sub.end_frame == 225

    def test__set_end__value_error(self):

        def function(x): self.time_sub.end = x
        self.raises(ValueError, function, ())

    def test__set_end__time(self):

        self.time_sub.end = "00:00:10.000"
        assert self.time_sub.end_time == "00:00:10.000"
        self.time_sub.end = 500
        assert self.time_sub.end_time == "00:00:20.000"
        self.time_sub.end = 5.0
        assert self.time_sub.end_time == "00:00:05.000"

    def test__set_end__frame(self):

        self.frame_sub.end = 500
        assert self.frame_sub.end_frame == 500
        self.frame_sub.end = "00:00:10.000"
        assert self.frame_sub.end_frame == 250
        self.frame_sub.end = 5.0
        assert self.frame_sub.end_frame == 125

    def test__set_framerate(self):

        FPS_30 = gaupol.framerates.FPS_30
        self.time_sub.framerate = FPS_30
        assert self.time_sub.framerate == FPS_30

    def test__set_main_text(self):

        self.time_sub.main_text = "test"
        assert self.time_sub.main_text == u"test"

    def test__set_mode__time(self):

        self.time_sub.mode = gaupol.modes.TIME
        self.time_sub.mode = gaupol.modes.FRAME
        assert self.time_sub._start == 25
        assert self.time_sub._end == 75

    def test__set_mode__frame(self):

        self.frame_sub.mode = gaupol.modes.FRAME
        self.frame_sub.mode = gaupol.modes.TIME
        assert self.frame_sub._start == "00:00:04.000"
        assert self.frame_sub._end == "00:00:12.000"

    def test__set_start__time(self):

        self.time_sub.start = "00:00:10.000"
        assert self.time_sub.start_time == "00:00:10.000"
        self.time_sub.start = 500
        assert self.time_sub.start_time == "00:00:20.000"
        self.time_sub.start = 5.0
        assert self.time_sub.start_time == "00:00:05.000"

    def test__set_start__frame(self):

        self.frame_sub.start = 500
        assert self.frame_sub.start_frame == 500
        self.frame_sub.start = "00:00:10.000"
        assert self.frame_sub.start_frame == 250
        self.frame_sub.start = 5.0
        assert self.frame_sub.start_frame == 125

    def test__set_tran_text(self):

        self.time_sub.tran_text = "test"
        assert self.time_sub.tran_text == u"test"

    def test_convert_framerate__time(self):

        self.time_sub.start = "00:00:01.000"
        self.time_sub.end = "00:00:02.000"
        framerate = gaupol.framerates.FPS_24
        self.time_sub.convert_framerate(framerate)
        assert self.time_sub.framerate == framerate
        assert self.time_sub.start == "00:00:01.043"
        assert self.time_sub.end == "00:00:02.085"

    def test_convert_framerate__frame(self):

        self.frame_sub.start = 100
        self.frame_sub.end = 200
        framerate = gaupol.framerates.FPS_24
        self.frame_sub.convert_framerate(framerate)
        assert self.frame_sub.framerate == framerate
        assert self.frame_sub.start == 96
        assert self.frame_sub.end == 192

    def test_copy(self):

        copy = self.time_sub.copy()
        assert copy == self.time_sub
        assert copy is not self.time_sub
        assert "ssa" not in dir(copy)
        self.time_sub.ssa.style = "test"
        copy = self.time_sub.copy()
        assert copy.ssa.style == "test"
        names = dir(self.time_sub.ssa)
        for name in (x for x in names if not x.startswith("_")):
            value = getattr(self.time_sub.ssa, name)
            assert getattr(copy.ssa, name) == value
        assert copy.ssa is not self.time_sub.ssa

    def test_get_duration(self):

        time, frame = gaupol.modes
        assert self.time_sub.get_duration(time) == "00:00:02.000"
        assert self.time_sub.get_duration(frame) == 50
        assert self.frame_sub.get_duration(time) == "00:00:08.000"
        assert self.frame_sub.get_duration(frame) == 200

    def test_get_duration__value_error(self):

        self.raises(ValueError, self.time_sub.get_duration, None)

    def test_get_end(self):

        time, frame = gaupol.modes
        assert self.time_sub.get_end(time) == "00:00:03.000"
        assert self.time_sub.get_end(frame) == 75
        assert self.frame_sub.get_end(time) == "00:00:12.000"
        assert self.frame_sub.get_end(frame) == 300

    def test_get_end__value_error(self):

        self.raises(ValueError, self.time_sub.get_end, None)

    def test_get_start(self):

        time, frame = gaupol.modes
        assert self.time_sub.get_start(time) == "00:00:01.000"
        assert self.time_sub.get_start(frame) == 25
        assert self.frame_sub.get_start(time) == "00:00:04.000"
        assert self.frame_sub.get_start(frame) == 100

    def test_get_start__value_error(self):

        self.raises(ValueError, self.time_sub.get_start, None)

    def test_get_text(self):

        main, tran = gaupol.documents
        assert self.time_sub.get_text(main) == "main"
        assert self.time_sub.get_text(tran) == "translation"

    def test_get_text__value_error(self):

        self.raises(ValueError, self.time_sub.get_text, None)

    def test_has_container(self):

        assert not self.time_sub.has_container("subrip")
        self.time_sub.subrip.x1 = 100
        assert self.time_sub.has_container("subrip")

    def test_set_text(self):

        main, tran = gaupol.documents
        self.time_sub.set_text(main, "")
        assert self.time_sub.main_text == ""
        self.time_sub.set_text(tran, "")
        assert self.time_sub.tran_text == ""

    def test_set_text__value_error(self):

        self.raises(ValueError, self.time_sub.set_text, None, "")

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
