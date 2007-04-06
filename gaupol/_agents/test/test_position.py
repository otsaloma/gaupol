# Copyright (C) 2005-2006 Osmo Salomaa
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


import copy

from gaupol import const
from gaupol.unittest import TestCase, reversion_test


class TestPositionAgent(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = self.project.adjust_times.im_self

        calc = self.project.calc
        times = self.project.times
        frames = self.project.frames
        times[0] = ["00:00:00.000", "00:00:04.000", "00:00:04.000"]
        times[1] = ["00:00:10.000", "00:00:15.000", "00:00:05.000"]
        times[2] = ["00:00:20.000", "00:00:26.000", "00:00:06.000"]
        times[3] = ["00:00:50.000", "00:00:57.000", "00:00:07.000"]
        for i in range(4):
            for j in range(3):
                frames[i][j] = calc.time_to_frame(times[i][j])
        frames[4] = [  0,  40, 40]
        frames[5] = [100, 150, 50]
        frames[6] = [200, 260, 60]
        frames[7] = [500, 570, 70]
        for i in range(4, 8):
            for j in range(3):
                times[i][j] = calc.frame_to_time(frames[i][j])

        texts = self.project.main_texts
        texts[0] = "1234567"
        texts[1] = "123456"
        texts[2] = "12345"
        texts[3] = "1234"

    @reversion_test
    def test_adjust_durations_gap(self):

        times = self.project.times
        self.project.adjust_durations(gap=7)
        assert times[0] == ["00:00:00.000", "00:00:03.000", "00:00:03.000"]
        assert times[1] == ["00:00:10.000", "00:00:13.000", "00:00:03.000"]
        assert times[2] == ["00:00:20.000", "00:00:26.000", "00:00:06.000"]

    @reversion_test
    def test_adjust_durations_maximum(self):

        times = self.project.times
        self.project.adjust_durations(maximum=5)
        assert times[0] == ["00:00:00.000", "00:00:04.000", "00:00:04.000"]
        assert times[1] == ["00:00:10.000", "00:00:15.000", "00:00:05.000"]
        assert times[2] == ["00:00:20.000", "00:00:25.000", "00:00:05.000"]

    @reversion_test
    def test_adjust_durations_minimum(self):

        times = self.project.times
        self.project.adjust_durations(minimum=6)
        assert times[0] == ["00:00:00.000", "00:00:06.000", "00:00:06.000"]
        assert times[1] == ["00:00:10.000", "00:00:16.000", "00:00:06.000"]
        assert times[2] == ["00:00:20.000", "00:00:26.000", "00:00:06.000"]

    @reversion_test
    def test_adjust_durations_optimal_lengthen(self):

        times = self.project.times
        self.project.adjust_durations(optimal=1, lengthen=True)
        assert times[0] == ["00:00:00.000", "00:00:07.000", "00:00:07.000"]
        assert times[1] == ["00:00:10.000", "00:00:16.000", "00:00:06.000"]
        assert times[2] == ["00:00:20.000", "00:00:26.000", "00:00:06.000"]

    @reversion_test
    def test_adjust_durations_optimal_shorten(self):

        times = self.project.times
        self.project.adjust_durations(optimal=1, shorten=True)
        assert times[0] == ["00:00:00.000", "00:00:04.000", "00:00:04.000"]
        assert times[1] == ["00:00:10.000", "00:00:15.000", "00:00:05.000"]
        assert times[2] == ["00:00:20.000", "00:00:25.000", "00:00:05.000"]

    @reversion_test
    def test_adjust_frames(self):

        frames = self.project.frames
        self.project.adjust_frames(None, (4, 10), (7, 100))
        assert frames[4] == [ 10,  17,  7]
        assert frames[5] == [ 28,  37,  9]
        assert frames[6] == [ 46,  57, 11]
        assert frames[7] == [100, 113, 13]

    @reversion_test
    def test_adjust_times(self):

        times = self.project.times
        point_1 = (0, "00:00:01.000")
        point_2 = (3, "00:00:10.000")
        self.project.adjust_times(None, point_1, point_2)
        assert times[0] == ["00:00:01.000", "00:00:01.720", "00:00:00.720"]
        assert times[1] == ["00:00:02.800", "00:00:03.700", "00:00:00.900"]
        assert times[2] == ["00:00:04.600", "00:00:05.680", "00:00:01.080"]
        assert times[3] == ["00:00:10.000", "00:00:11.260", "00:00:01.260"]

    def test_change_framerate(self):

        self.project.change_framerate(const.FRAMERATE.P24)
        self.project.main_file.mode = const.MODE.TIME
        orig_times = copy.deepcopy(self.project.times)
        orig_frames = copy.deepcopy(self.project.frames)
        self.project.change_framerate(const.FRAMERATE.P25)
        assert self.project.framerate == const.FRAMERATE.P25
        assert self.project.times == orig_times
        assert self.project.frames != orig_frames
        assert not self.project.can_undo()

        self.project.main_file.mode = const.MODE.FRAME
        orig_times = copy.deepcopy(self.project.times)
        orig_frames = copy.deepcopy(self.project.frames)
        self.project.change_framerate(const.FRAMERATE.P30)
        assert self.project.framerate == const.FRAMERATE.P30
        assert self.project.times != orig_times
        assert self.project.frames == orig_frames
        assert not self.project.can_undo()

    @reversion_test
    def test_convert_framerate_frame(self):

        frames = self.project.frames
        self.project.main_file = self.project.tran_file
        self.project.convert_framerate(
            [], const.FRAMERATE.P25, const.FRAMERATE.P30)
        assert self.project.framerate == const.FRAMERATE.P30
        assert self.project.calc.framerate == 29.97
        assert frames[4] == [  0,  48, 48]
        assert frames[5] == [120, 180, 60]
        assert frames[6] == [240, 312, 72]
        assert frames[7] == [599, 683, 84]

    @reversion_test
    def test_convert_framerate_time(self):

        times = self.project.times
        self.project.convert_framerate(
            [], const.FRAMERATE.P24, const.FRAMERATE.P25)
        assert self.project.framerate == const.FRAMERATE.P25
        assert self.project.calc.framerate == 25.0
        assert times[0] == ["00:00:00.000", "00:00:03.836", "00:00:03.836"]
        assert times[1] == ["00:00:09.590", "00:00:14.386", "00:00:04.796"]
        assert times[2] == ["00:00:19.181", "00:00:24.935", "00:00:05.754"]
        assert times[3] == ["00:00:47.952", "00:00:54.665", "00:00:06.713"]

    def test_set_framerate(self):

        self.project.set_framerate(const.FRAMERATE.P25)
        self.project.set_framerate(const.FRAMERATE.P30)
        assert self.project.framerate == const.FRAMERATE.P30
        assert self.project.calc.framerate == 29.970
        self.project.undo()
        assert self.project.framerate == const.FRAMERATE.P25
        assert self.project.calc.framerate == 25.000
        self.project.redo()
        assert self.project.framerate == const.FRAMERATE.P30
        assert self.project.calc.framerate == 29.970

    @reversion_test
    def test_shift_frames_back(self):

        frames = self.project.frames
        self.project.shift_frames([4, 5, 6, 7], -5)
        assert frames[4] == [  0,  35, 35]
        assert frames[5] == [ 95, 145, 50]
        assert frames[6] == [195, 255, 60]
        assert frames[7] == [495, 565, 70]

    @reversion_test
    def test_shift_frames_forward(self):

        frames = self.project.frames
        self.project.shift_frames([], 5)
        assert frames[4] == [  5,  45, 40]
        assert frames[5] == [105, 155, 50]
        assert frames[6] == [205, 265, 60]
        assert frames[7] == [505, 575, 70]

    @reversion_test
    def test_shift_seconds_back(self):

        times = self.project.times
        self.project.shift_seconds([0, 1, 2, 3], -0.5)
        assert times[0] == ["00:00:00.000", "00:00:03.500", "00:00:03.500"]
        assert times[1] == ["00:00:09.500", "00:00:14.500", "00:00:05.000"]
        assert times[2] == ["00:00:19.500", "00:00:25.500", "00:00:06.000"]
        assert times[3] == ["00:00:49.500", "00:00:56.500", "00:00:07.000"]

    @reversion_test
    def test_shift_seconds_forward(self):

        times = self.project.times
        self.project.shift_seconds([], 0.5)
        assert times[0] == ["00:00:00.500", "00:00:04.500", "00:00:04.000"]
        assert times[1] == ["00:00:10.500", "00:00:15.500", "00:00:05.000"]
        assert times[2] == ["00:00:20.500", "00:00:26.500", "00:00:06.000"]
        assert times[3] == ["00:00:50.500", "00:00:57.500", "00:00:07.000"]
