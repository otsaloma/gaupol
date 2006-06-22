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


from gaupol.base                   import cons
from gaupol.base.icons             import *
from gaupol.base.delegate.position import PositionDelegate
from gaupol.test                   import Test


class TestPositionDelegate(Test):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = PositionDelegate(self.project)

    def test_adjust_durations_gap(self):

        times = self.project.times
        times[0] = ['00:00:00.000', '00:00:01.000', '00:00:01.000']
        times[1] = ['00:00:10.000', '00:00:11.000', '00:00:01.000']
        times[2] = ['00:00:20.000', '00:00:21.000', '00:00:01.000']

        self.project.adjust_durations(None, gap=9.5)
        assert times[0] == ['00:00:00.000', '00:00:00.500', '00:00:00.500']
        assert times[1] == ['00:00:10.000', '00:00:10.500', '00:00:00.500']
        assert times[2] == ['00:00:20.000', '00:00:21.000', '00:00:01.000']

        self.project.undo()
        assert times[0] == ['00:00:00.000', '00:00:01.000', '00:00:01.000']
        assert times[1] == ['00:00:10.000', '00:00:11.000', '00:00:01.000']
        assert times[2] == ['00:00:20.000', '00:00:21.000', '00:00:01.000']

        self.project.redo()
        assert times[0] == ['00:00:00.000', '00:00:00.500', '00:00:00.500']
        assert times[1] == ['00:00:10.000', '00:00:10.500', '00:00:00.500']
        assert times[2] == ['00:00:20.000', '00:00:21.000', '00:00:01.000']

    def test_adjust_durations_minimum(self):

        times = self.project.times
        times[0] = ['00:00:00.000', '00:00:01.000', '00:00:01.000']
        times[1] = ['00:00:10.000', '00:00:11.000', '00:00:01.000']
        times[2] = ['00:00:20.000', '00:00:21.000', '00:00:01.000']

        self.project.adjust_durations(None, minimum=2)
        assert times[0] == ['00:00:00.000', '00:00:02.000', '00:00:02.000']
        assert times[1] == ['00:00:10.000', '00:00:12.000', '00:00:02.000']
        assert times[2] == ['00:00:20.000', '00:00:22.000', '00:00:02.000']

        self.project.undo()
        assert times[0] == ['00:00:00.000', '00:00:01.000', '00:00:01.000']
        assert times[1] == ['00:00:10.000', '00:00:11.000', '00:00:01.000']
        assert times[2] == ['00:00:20.000', '00:00:21.000', '00:00:01.000']

        self.project.redo()
        assert times[0] == ['00:00:00.000', '00:00:02.000', '00:00:02.000']
        assert times[1] == ['00:00:10.000', '00:00:12.000', '00:00:02.000']
        assert times[2] == ['00:00:20.000', '00:00:22.000', '00:00:02.000']

    def test_adjust_durations_optimal(self):

        times = self.project.times
        texts = self.project.main_texts
        times[0] = ['00:00:00.000', '00:00:01.000', '00:00:01.000']
        times[1] = ['00:00:10.000', '00:00:11.000', '00:00:01.000']
        times[2] = ['00:00:20.000', '00:00:21.000', '00:00:01.000']
        texts[0] = '12345'
        texts[1] = '123456'
        texts[2] = '1234567'

        self.project.adjust_durations(None, optimal=1, lengthen=True)
        assert times[0] == ['00:00:00.000', '00:00:05.000', '00:00:05.000']
        assert times[1] == ['00:00:10.000', '00:00:16.000', '00:00:06.000']
        assert times[2] == ['00:00:20.000', '00:00:27.000', '00:00:07.000']

        self.project.undo()
        assert times[0] == ['00:00:00.000', '00:00:01.000', '00:00:01.000']
        assert times[1] == ['00:00:10.000', '00:00:11.000', '00:00:01.000']
        assert times[2] == ['00:00:20.000', '00:00:21.000', '00:00:01.000']

        self.project.redo()
        assert times[0] == ['00:00:00.000', '00:00:05.000', '00:00:05.000']
        assert times[1] == ['00:00:10.000', '00:00:16.000', '00:00:06.000']
        assert times[2] == ['00:00:20.000', '00:00:27.000', '00:00:07.000']

    def test_adjust_frames(self):

        frames = self.project.frames
        frames[0] = [10, 20, 10]
        frames[1] = [30, 40, 10]
        frames[2] = [50, 60, 10]

        self.project.adjust_frames(None, (0, 20), (2, 55))
        assert frames[0] == [20, 29, 9]
        assert frames[1] == [38, 46, 8]
        assert frames[2] == [55, 64, 9]

        self.project.undo()
        assert frames[0] == [10, 20, 10]
        assert frames[1] == [30, 40, 10]
        assert frames[2] == [50, 60, 10]

        self.project.redo()
        assert frames[0] == [20, 29, 9]
        assert frames[1] == [38, 46, 8]
        assert frames[2] == [55, 64, 9]

    def test_adjust_times(self):

        times = self.project.times
        times[0] = ['00:00:01.000', '00:00:02.000', '00:00:01.000']
        times[1] = ['00:00:03.000', '00:00:04.000', '00:00:01.000']
        times[2] = ['00:00:05.000', '00:00:06.000', '00:00:01.000']

        point_1 = (0, '00:00:02.000')
        point_2 = (2, '00:00:05.500')
        self.project.adjust_times(None, point_1, point_2)
        assert times[0] == ['00:00:02.000', '00:00:02.875', '00:00:00.875']
        assert times[1] == ['00:00:03.750', '00:00:04.625', '00:00:00.875']
        assert times[2] == ['00:00:05.500', '00:00:06.375', '00:00:00.875']

        self.project.undo()
        assert times[0] == ['00:00:01.000', '00:00:02.000', '00:00:01.000']
        assert times[1] == ['00:00:03.000', '00:00:04.000', '00:00:01.000']
        assert times[2] == ['00:00:05.000', '00:00:06.000', '00:00:01.000']

        self.project.redo()
        assert times[0] == ['00:00:02.000', '00:00:02.875', '00:00:00.875']
        assert times[1] == ['00:00:03.750', '00:00:04.625', '00:00:00.875']
        assert times[2] == ['00:00:05.500', '00:00:06.375', '00:00:00.875']

    def test_change_framerate(self):

        self.project.change_framerate(cons.Framerate.FR_23_976)
        frame_1 = self.project.frames[5][SHOW]
        self.project.change_framerate(cons.Framerate.FR_25)
        frame_2 = self.project.frames[5][SHOW]
        assert frame_2 == int(round((frame_1 / 23.976) * 25, 0))

    def test_convert_framerate_frame(self):

        frames = self.project.frames
        times  = self.project.times
        frames[0][0] = 100
        frames[1][0] = 500

        self.project.main_file = self.project.tran_file
        self.project.convert_framerate(
            None, cons.Framerate.FR_25, cons.Framerate.FR_29_97)
        assert self.project.framerate == cons.Framerate.FR_29_97
        assert self.project.calc.framerate == 29.97
        assert frames[0][0] == 120
        assert frames[1][0] == 599
        assert  times[0][0] == '00:00:04.004'
        assert  times[1][0] == '00:00:19.987'

        self.project.undo()
        assert self.project.framerate == cons.Framerate.FR_25
        assert self.project.calc.framerate == 25.00
        assert frames[0][0] == 100
        assert frames[1][0] == 500

        self.project.redo()
        assert self.project.framerate == cons.Framerate.FR_29_97
        assert self.project.calc.framerate == 29.97
        assert frames[0][0] == 120
        assert frames[1][0] == 599
        assert  times[0][0] == '00:00:04.004'
        assert  times[1][0] == '00:00:19.987'

    def test_convert_framerate_time(self):

        frames = self.project.frames
        times  = self.project.times
        times[0][0] = '00:00:01.000'
        times[1][0] = '00:00:02.000'

        self.project.convert_framerate(
            None, cons.Framerate.FR_25, cons.Framerate.FR_29_97)
        assert self.project.framerate == cons.Framerate.FR_29_97
        assert self.project.calc.framerate == 29.97
        assert  times[0][0] == '00:00:00.834'
        assert  times[1][0] == '00:00:01.668'
        assert frames[0][0] == 25
        assert frames[1][0] == 50

        self.project.undo()
        assert self.project.framerate == cons.Framerate.FR_25
        assert self.project.calc.framerate == 25.00
        assert  times[0][0] == '00:00:01.000'
        assert  times[1][0] == '00:00:02.000'

        self.project.redo()
        assert self.project.framerate == cons.Framerate.FR_29_97
        assert self.project.calc.framerate == 29.97
        assert  times[0][0] == '00:00:00.834'
        assert  times[1][0] == '00:00:01.668'
        assert frames[0][0] == 25
        assert frames[1][0] == 50

    def test_shift_frames_backward(self):

        frames = self.project.frames
        frames[0] = [10, 20, 10]
        frames[1] = [30, 40, 10]
        frames[2] = [50, 60, 10]

        self.project.shift_frames([1, 2], -5)
        assert frames[0] == [10, 20, 10]
        assert frames[1] == [25, 35, 10]
        assert frames[2] == [45, 55, 10]

        self.project.undo()
        assert frames[0] == [10, 20, 10]
        assert frames[1] == [30, 40, 10]
        assert frames[2] == [50, 60, 10]

        self.project.redo()
        assert frames[0] == [10, 20, 10]
        assert frames[1] == [25, 35, 10]
        assert frames[2] == [45, 55, 10]

    def test_shift_frames_forward(self):

        frames = self.project.frames
        frames[0] = [10, 20, 10]
        frames[1] = [30, 40, 10]
        frames[2] = [50, 60, 10]

        self.project.shift_frames(None, 5)
        assert frames[0] == [15, 25, 10]
        assert frames[1] == [35, 45, 10]
        assert frames[2] == [55, 65, 10]

        self.project.undo()
        assert frames[0] == [10, 20, 10]
        assert frames[1] == [30, 40, 10]
        assert frames[2] == [50, 60, 10]

        self.project.redo()
        assert frames[0] == [15, 25, 10]
        assert frames[1] == [35, 45, 10]
        assert frames[2] == [55, 65, 10]

    def test_shift_seconds_backward(self):

        times = self.project.times
        times[0] = ['00:00:01.000', '00:00:02.000', '00:00:01.000']
        times[1] = ['00:00:03.000', '00:00:04.000', '00:00:01.000']
        times[2] = ['00:00:05.000', '00:00:06.000', '00:00:01.000']

        self.project.shift_seconds([1, 2], -0.5)
        assert times[0] == ['00:00:01.000', '00:00:02.000', '00:00:01.000']
        assert times[1] == ['00:00:02.500', '00:00:03.500', '00:00:01.000']
        assert times[2] == ['00:00:04.500', '00:00:05.500', '00:00:01.000']

        self.project.undo()
        assert times[0] == ['00:00:01.000', '00:00:02.000', '00:00:01.000']
        assert times[1] == ['00:00:03.000', '00:00:04.000', '00:00:01.000']
        assert times[2] == ['00:00:05.000', '00:00:06.000', '00:00:01.000']

        self.project.redo()
        assert times[0] == ['00:00:01.000', '00:00:02.000', '00:00:01.000']
        assert times[1] == ['00:00:02.500', '00:00:03.500', '00:00:01.000']
        assert times[2] == ['00:00:04.500', '00:00:05.500', '00:00:01.000']

    def test_shift_seconds_forward(self):

        times = self.project.times
        times[0] = ['00:00:01.000', '00:00:02.000', '00:00:01.000']
        times[1] = ['00:00:03.000', '00:00:04.000', '00:00:01.000']
        times[2] = ['00:00:05.000', '00:00:06.000', '00:00:01.000']

        self.project.shift_seconds(None, 0.5)
        assert times[0] == ['00:00:01.500', '00:00:02.500', '00:00:01.000']
        assert times[1] == ['00:00:03.500', '00:00:04.500', '00:00:01.000']
        assert times[2] == ['00:00:05.500', '00:00:06.500', '00:00:01.000']

        self.project.undo()
        assert times[0] == ['00:00:01.000', '00:00:02.000', '00:00:01.000']
        assert times[1] == ['00:00:03.000', '00:00:04.000', '00:00:01.000']
        assert times[2] == ['00:00:05.000', '00:00:06.000', '00:00:01.000']

        self.project.redo()
        assert times[0] == ['00:00:01.500', '00:00:02.500', '00:00:01.000']
        assert times[1] == ['00:00:03.500', '00:00:04.500', '00:00:01.000']
        assert times[2] == ['00:00:05.500', '00:00:06.500', '00:00:01.000']
