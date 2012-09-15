# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009,2011 Osmo Salomaa
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

import aeidon


class TestCalculator(aeidon.TestCase):

    def setup_method(self, method):
        self.framerate = aeidon.framerates.FPS_23_976
        self.calc = aeidon.Calculator(self.framerate)

    def test___new__(self):
        for framerate in aeidon.framerates:
            a = aeidon.Calculator(framerate)
            b = aeidon.Calculator(framerate)
            assert a is b

    def test_add_times(self):
        for x, y, z in (( "33:33:33.333",  "44:44:44.444",  "78:18:17.777"),
                        ("-33:33:33.333", "-44:44:44.444", "-78:18:17.777"),
                        ("-33:33:33.333",  "44:44:44.444",  "11:11:11.111"),
                        ( "33:33:33.333", "-44:44:44.444", "-11:11:11.111")):

            assert self.calc.add_times(x, y) == z

    def test_frame_to_seconds(self):
        calc = aeidon.Calculator(aeidon.framerates.FPS_25_000)
        assert calc.frame_to_seconds( 127) ==  5.08
        assert calc.frame_to_seconds(-127) == -5.08

    def test_frame_to_time(self):
        assert self.calc.frame_to_time( 2658) ==  "00:01:50.861"
        assert self.calc.frame_to_time(-2658) == "-00:01:50.861"

    def test_get_middle__frame(self):
        for x, y, z in (( 300,  400,  350),
                        ( 300,  401,  350),
                        (-300, -400, -350),
                        (-300,  401,   50)):

            x = aeidon.as_frame(x)
            y = aeidon.as_frame(y)
            assert self.calc.get_middle(x, y) == z

    def test_get_middle__seconds(self):
        for x, y, z in (( 300,  400,  350.0),
                        ( 300,  401,  350.5),
                        (-300, -400, -350.0),
                        (-300,  401,   50.5)):

            x = aeidon.as_seconds(x)
            y = aeidon.as_seconds(y)
            assert self.calc.get_middle(x, y) == z

    def test_get_middle__time(self):
        for x, y, z in (( "00:00:01.000",  "00:00:02.000",  "00:00:01.500"),
                        ( "00:00:01.000",  "00:00:02.001",  "00:00:01.500"),
                        ("-00:00:01.000", "-00:00:02.000", "-00:00:01.500"),
                        ( "00:00:01.000", "-00:00:02.002", "-00:00:00.501")):

            x = aeidon.as_time(x)
            y = aeidon.as_time(y)
            assert self.calc.get_middle(x, y) == z

    def test_get_middle__value_error(self):
        self.assert_raises(ValueError,
                           self.calc.get_middle,
                           None,
                           None)

    def test_is_earlier__frame(self):
        a = aeidon.as_frame(1)
        b = aeidon.as_frame(2)
        assert self.calc.is_earlier(a, b)
        assert not self.calc.is_earlier(a, a)
        assert not self.calc.is_earlier(b, a)

    def test_is_earlier__seconds(self):
        a = aeidon.as_seconds(1)
        b = aeidon.as_seconds(2)
        assert self.calc.is_earlier(a, b)
        assert not self.calc.is_earlier(a, a)
        assert not self.calc.is_earlier(b, a)

    def test_is_earlier__time(self):
        a = aeidon.as_time("00:00:01.000")
        b = aeidon.as_time("00:00:02.000")
        assert self.calc.is_earlier(a, b)
        assert not self.calc.is_earlier(a, a)
        assert not self.calc.is_earlier(b, a)

    def test_is_earlier__value_error(self):
        self.assert_raises(ValueError,
                           self.calc.is_earlier,
                           None,
                           None)

    def test_is_later__frame(self):
        a = aeidon.as_frame(1)
        b = aeidon.as_frame(2)
        assert self.calc.is_later(b, a)
        assert not self.calc.is_later(b, b)
        assert not self.calc.is_later(a, b)

    def test_is_later__seconds(self):
        a = aeidon.as_seconds(1)
        b = aeidon.as_seconds(2)
        assert self.calc.is_later(b, a)
        assert not self.calc.is_later(b, b)
        assert not self.calc.is_later(a, b)

    def test_is_later__time(self):
        a = aeidon.as_time("00:00:01.000")
        b = aeidon.as_time("00:00:02.000")
        assert self.calc.is_later(b, a)
        assert not self.calc.is_later(b, b)
        assert not self.calc.is_later(a, b)

    def test_is_later__value_error(self):
        self.assert_raises(ValueError,
                           self.calc.is_later,
                           None,
                           None)

    def test_is_valid_time__false(self):
        assert not self.calc.is_valid_time("2:34:56.789")
        assert not self.calc.is_valid_time("12:60:56.789")

    def test_is_valid_time__true(self):
        assert self.calc.is_valid_time("12:34:56.789")
        assert self.calc.is_valid_time("-12:34:56.789")

    def test_parse_time(self):
        assert self.calc.parse_time("1:2:3.4") == "01:02:03.400"
        assert self.calc.parse_time("1:2:3,4") == "01:02:03.400"
        assert self.calc.parse_time("-00:00:00.400") == "-00:00:00.400"
        assert self.calc.parse_time("-01:02:03.400") == "-01:02:03.400"

    def test_round_time(self):
        round_time = self.calc.round_time
        assert round_time("02:36:35.857", 3) == "02:36:35.857"
        assert round_time("02:36:35.857", 2) == "02:36:35.860"
        assert round_time("02:36:35.857", 1) == "02:36:35.900"
        assert round_time("02:36:35.857", 0) == "02:36:36.000"

    def test_seconds_to_frame(self):
        seconds_to_frame = self.calc.seconds_to_frame
        assert seconds_to_frame(6552) == 157091
        assert seconds_to_frame(-337) ==  -8080

    def test_seconds_to_time(self):
        seconds_to_time = self.calc.seconds_to_time
        assert seconds_to_time(68951.15388) ==  "19:09:11.154"
        assert seconds_to_time(-12.0000000) == "-00:00:12.000"
        assert seconds_to_time(999999.0000) ==  "99:59:59.999"

    def test_time_to_frame(self):
        time_to_frame = self.calc.time_to_frame
        assert time_to_frame( "01:22:36.144") == 118829
        assert time_to_frame("-00:13:43.087") == -19734

    def test_time_to_seconds(self):
        time_to_seconds = self.calc.time_to_seconds
        assert time_to_seconds( "03:45:22.117") == 13522.117
        assert time_to_seconds("-00:00:45.000") ==   -45.000

    def test_to_frame(self):
        self.calc = aeidon.Calculator(aeidon.framerates.FPS_25_000)
        assert self.calc.to_frame(aeidon.as_time("00:00:01.000")) == 25
        assert self.calc.to_frame(aeidon.as_frame(25)) == 25
        assert self.calc.to_frame(aeidon.as_seconds(1.0)) == 25

    def test_to_frame__value_error(self):
        self.assert_raises(ValueError,
                           self.calc.to_frame,
                           None)

    def test_to_seconds(self):
        self.calc = aeidon.Calculator(aeidon.framerates.FPS_25_000)
        assert self.calc.to_seconds(aeidon.as_time("00:00:01.000")) == 1.0
        assert self.calc.to_seconds(aeidon.as_frame(25)) == 1.0
        assert self.calc.to_seconds(aeidon.as_seconds(1.0)) == 1.0

    def test_to_seconds__value_error(self):
        self.assert_raises(ValueError,
                           self.calc.to_seconds,
                           None)

    def test_to_time(self):
        self.calc = aeidon.Calculator(aeidon.framerates.FPS_25_000)
        time = "00:00:01.000"
        assert self.calc.to_time(aeidon.as_time(time)) == time
        assert self.calc.to_time(aeidon.as_frame(25)) == time
        assert self.calc.to_time(aeidon.as_seconds(1.0)) == time

    def test_to_time__value_error(self):
        self.assert_raises(ValueError,
                           self.calc.to_time,
                           None)
