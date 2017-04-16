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


class TestCalculator(aeidon.TestCase):

    def setup_method(self, method):
        self.framerate = aeidon.framerates.FPS_23_976
        self.calc = aeidon.Calculator(self.framerate)

    def test___new__(self):
        a = aeidon.Calculator(aeidon.framerates.FPS_23_976)
        b = aeidon.Calculator(aeidon.framerates.FPS_23_976)
        assert a is b

    def test___new____float(self):
        a = aeidon.Calculator(48.0)
        b = aeidon.Calculator(96.0)
        assert a is not b

    def test_add__frames(self):
        assert self.calc.add(10, 10) == 20

    def test_add__seconds(self):
        assert self.calc.add(10.0, 10.0) == 20.0

    def test_add__times(self):
        assert self.calc.add("00:00:10.000",
                             "00:00:10.000") == "00:00:20.000"

    def test_frame_to_seconds(self):
        calc = aeidon.Calculator(aeidon.framerates.FPS_25_000)
        assert calc.frame_to_seconds(127) == 5.08

    def test_frame_to_time(self):
        assert self.calc.frame_to_time(2658) == "00:01:50.861"

    def test_get_middle__frame(self):
        assert self.calc.get_middle(300, 400) == 350

    def test_get_middle__seconds(self):
        assert self.calc.get_middle(300.0, 400.0) == 350.0

    def test_get_middle__time(self):
        assert self.calc.get_middle("00:00:01.000",
                                    "00:00:02.000") == "00:00:01.500"

    def test_is_earlier__frame(self):
        assert self.calc.is_earlier(1, 2)
        assert not self.calc.is_earlier(2, 2)
        assert not self.calc.is_earlier(2, 1)

    def test_is_earlier__seconds(self):
        assert self.calc.is_earlier(1.0, 2.0)
        assert not self.calc.is_earlier(2.0, 2.0)
        assert not self.calc.is_earlier(2.0, 1.0)

    def test_is_earlier__time(self):
        assert self.calc.is_earlier("00:00:01.000", "00:00:02.000")
        assert not self.calc.is_earlier("00:00:01.000", "00:00:01.000")
        assert not self.calc.is_earlier("00:00:02.000", "00:00:01.000")

    def test_is_later__frame(self):
        assert self.calc.is_later(2, 1)
        assert not self.calc.is_later(2, 2)
        assert not self.calc.is_later(1, 2)

    def test_is_later__seconds(self):
        assert self.calc.is_later(2.0, 1.0)
        assert not self.calc.is_later(2.0, 2.0)
        assert not self.calc.is_later(1.0, 2.0)

    def test_is_later__time(self):
        assert self.calc.is_later("00:00:02.000", "00:00:01.000")
        assert not self.calc.is_later("00:00:02.000", "00:00:02.000")
        assert not self.calc.is_later("00:00:01.000", "00:00:02.000")

    def test_is_valid_time__false(self):
        assert not self.calc.is_valid_time("2:34:56.789")
        assert not self.calc.is_valid_time("12:60:56.789")

    def test_is_valid_time__true(self):
        assert self.calc.is_valid_time("12:34:56.789")
        assert self.calc.is_valid_time("-12:34:56.789")

    def test_normalize_time(self):
        assert self.calc.normalize_time("1:2:3.4") == "01:02:03.400"
        assert self.calc.normalize_time("-1:2:3,4") == "-01:02:03.400"
        assert self.calc.normalize_time("12:34.567") == "00:12:34.567"

    def test_round__frame(self):
        assert self.calc.round(13, -1) == 10

    def test_round__seconds(self):
        assert self.calc.round(13.33, 0) == 13.0

    def test_round__time(self):
        assert self.calc.round("12:34:56.789", 1) == "12:34:56.800"

    def test_seconds_to_frame(self):
        assert self.calc.seconds_to_frame(6552) == 157091

    def test_seconds_to_time(self):
        assert self.calc.seconds_to_time(68951.15388) == "19:09:11.154"

    def test_time_to_frame(self):
        assert self.calc.time_to_frame("01:22:36.144") == 118829

    def test_time_to_seconds(self):
        assert self.calc.time_to_seconds("03:45:22.117") == 13522.117

    def test_to_frame(self):
        self.calc = aeidon.Calculator(aeidon.framerates.FPS_25_000)
        assert self.calc.to_frame("00:00:01.000") == 25
        assert self.calc.to_frame(25) == 25
        assert self.calc.to_frame(1.0) == 25

    def test_to_seconds(self):
        self.calc = aeidon.Calculator(aeidon.framerates.FPS_25_000)
        assert self.calc.to_seconds("00:00:01.000") == 1.0
        assert self.calc.to_seconds(25) == 1.0
        assert self.calc.to_seconds(1.0) == 1.0

    def test_to_time(self):
        self.calc = aeidon.Calculator(aeidon.framerates.FPS_25_000)
        assert self.calc.to_time("00:00:01.000") == "00:00:01.000"
        assert self.calc.to_time(25) == "00:00:01.000"
        assert self.calc.to_time(1.0) == "00:00:01.000"
