# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


from gaupol.base.timeframe.calc import TimeFrameCalculator
from gaupol.constants           import Framerate
from gaupol.test                import Test


class TestTimeFrameCalculator(Test):

    def setup_method(self, method):

        self.calc = TimeFrameCalculator(Framerate.FR_23_976)
        self.framerate = Framerate.values[Framerate.FR_23_976]

    def test_init(self):

        TimeFrameCalculator()
        TimeFrameCalculator(Framerate.FR_23_976)

    def test_add_seconds_to_time(self):

        time = self.calc.add_seconds_to_time('33:33:33,333', 5)
        assert time == '33:33:38,333'

    def test_add_times(self):

        time = self.calc.add_times('33:33:33,333', '44:44:44,444')
        assert time == '78:18:17,777'

    def test_frame_to_seconds(self):

        seconds = self.calc.frame_to_seconds(333)
        assert seconds == 333 / self.framerate

    def test_frame_to_time(self):

        time = self.calc.frame_to_time(333333)
        assert time == '03:51:42,778'

    def test_get_frame_duration(self):

        duration = self.calc.get_frame_duration(333, 444)
        assert duration == 111

        duration = self.calc.get_frame_duration(444, 333)
        assert duration == 0

    def test_get_time_duration(self):

        duration = self.calc.get_time_duration('33:33:33,333', '44:44:44,444')
        assert duration == '11:11:11,111'

        duration = self.calc.get_time_duration('44:44:44,444', '33:33:33,333')
        assert duration == '00:00:00,000'

    def test_round_time(self):

        time = self.calc.round_time('33:33:33,333', 1)
        assert time == '33:33:33,300'

    def test_seconds_to_frame(self):

        seconds = self.calc.seconds_to_frame(333)
        assert seconds == 7984

    def test_seconds_to_time(self):

        time = self.calc.seconds_to_time(33333.33)
        assert time == '09:15:33,330'

        time = self.calc.seconds_to_time(999999)
        assert time == '99:59:59,999'

    def test_set_framerate(self):

        self.calc.set_framerate(Framerate.FR_25)
        assert self.calc.framerate == 25.000

    def test_time_to_frame(self):

        frame = self.calc.time_to_frame('33:33:33,333')
        assert frame == int(round(120813.333 * self.framerate, 0))

    def test_time_to_seconds(self):

        seconds = self.calc.time_to_seconds('33:33:33,333')
        assert seconds == 120813.333
