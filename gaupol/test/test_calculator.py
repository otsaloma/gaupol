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


from gaupol import const
from gaupol.unittest import TestCase
from .. import calculator


class TestCalculator(TestCase):

    def setup_method(self, method):

        self.calc = calculator.Calculator()

    def test___new__(self):

        for framerate in const.FRAMERATE.members:
            a = calculator.Calculator(framerate)
            b = calculator.Calculator(framerate)
            assert a is b

    def test_add_seconds_to_time(self):

        time = self.calc.add_seconds_to_time("00:00:00.001", 5)
        assert time == "00:00:05.001"
        time = self.calc.add_seconds_to_time("00:00:00.001", -5)
        assert time == "-00:00:04.999"

    def test_add_times(self):

        time = self.calc.add_times("33:33:33.333", "44:44:44.444")
        assert time == "78:18:17.777"

    def test_frame_to_seconds(self):

        seconds = self.calc.frame_to_seconds(127)
        assert seconds == 127 / 23.976

    def test_frame_to_time(self):

        time = self.calc.frame_to_time(2658)
        assert time == "00:01:50.861"

    def test_get_frame_duration(self):

        duration = self.calc.get_frame_duration(561, 1048)
        assert duration == 487
        duration = self.calc.get_frame_duration(561, 560)
        assert duration == -1

    def test_get_middle(self):

        middle = self.calc.get_middle("00:00:01.000", "00:00:02.000")
        assert middle == "00:00:01.500"
        middle = self.calc.get_middle("00:00:01.000", "00:00:02.001")
        assert middle == "00:00:01.501"

        middle = self.calc.get_middle(300, 400)
        assert middle == 350
        middle = self.calc.get_middle(300, 401)
        assert middle == 351

    def test_get_time_duration(self):

        duration = self.calc.get_time_duration("00:01:22.500", "00:01:45.100")
        assert duration == "00:00:22.600"
        duration = self.calc.get_time_duration("00:01:22.500", "00:01:00.100")
        assert duration == "-00:00:22.400"

    def test_round_time(self):

        time = self.calc.round_time("02:36:35.857", 3)
        assert time == "02:36:35.857"
        time = self.calc.round_time("02:36:35.857", 2)
        assert time == "02:36:35.860"
        time = self.calc.round_time("02:36:35.857", 1)
        assert time == "02:36:35.900"
        time = self.calc.round_time("02:36:35.857", 0)
        assert time == "02:36:36.000"

    def test_seconds_to_frame(self):

        frame = self.calc.seconds_to_frame(6552)
        assert frame == 157091

    def test_seconds_to_time(self):

        time = self.calc.seconds_to_time(68951.15388)
        assert time == "19:09:11.154"
        time = self.calc.seconds_to_time(999999.0)
        assert time == "99:59:59.999"
        time = self.calc.seconds_to_time(-12.0)
        assert time == "-00:00:12.000"

    def test_time_to_frame(self):

        frame = self.calc.time_to_frame("01:22:36.144")
        assert frame == 118829

    def test_time_to_seconds(self):

        seconds = self.calc.time_to_seconds("03:45:22.117")
        assert seconds == 13522.117
        seconds = self.calc.time_to_seconds("-00:00:45.000")
        assert seconds == -45.0
