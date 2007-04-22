# Copyright (C) 2007 Osmo Salomaa
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


from gaupol import const
from gaupol.unittest import TestCase
from .. import subtitle


class TestSubtitle(TestCase):

    def setup_method(self, method):

        self.time_sub = subtitle.Subtitle()
        self.time_sub.mode = const.MODE.TIME
        self.time_sub.framerate = const.FRAMERATE.P25
        self.time_sub.start = "00:00:01.000"
        self.time_sub.end = "00:00:03.000"
        self.time_sub.main_text = "main"
        self.time_sub.tran_text = "translation"

        self.frame_sub = subtitle.Subtitle()
        self.frame_sub.mode = const.MODE.FRAME
        self.frame_sub.framerate = const.FRAMERATE.P25
        self.frame_sub.start = 100
        self.frame_sub.end = 300
        self.frame_sub.main_text = "main"
        self.frame_sub.tran_text = "translation"

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

        assert self.time_sub.framerate == const.FRAMERATE.P25
        assert self.frame_sub.framerate == const.FRAMERATE.P25

    def test__get_main_text(self):

        assert self.time_sub.main_text == u"main"
        assert self.frame_sub.main_text == u"main"

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

        self.time_sub.framerate = const.FRAMERATE.P30
        assert self.time_sub.framerate == const.FRAMERATE.P30
        assert self.time_sub._calc.framerate == 29.97

    def test__set_main_text(self):

        self.time_sub.main_text = "test"
        assert self.time_sub.main_text == u"test"

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
