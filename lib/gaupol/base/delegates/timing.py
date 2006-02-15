# Copyright (C) 2005 Osmo Salomaa
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


"""Shifting, adjusting and fixing timings."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _

from gaupol.base.colconstants import *
from gaupol.base.delegates    import Delegate
from gaupol.constants         import Action, Document, Framerate, Mode


class TimingDelegate(Delegate):

    """Shifting, adjusting and fixing timings."""

    def adjust_frames(self, rows, point_1, point_2, register=Action.DO):
        """
        Adjust timings in rows.

        point_1 and point_2 are two tuples of row and new show frame.
        rows can be None to process all rows.
        """
        rows = rows or range(len(self.times))

        new_times  = []
        new_frames = []
        times  = self.times
        frames = self.frames
        calc   = self.calc

        # Think of this as a linear transformation where current times are
        # located on the x-axis and correct times on the y-axis.
        x_1 = frames[point_1[0]][SHOW]
        x_2 = frames[point_2[0]][SHOW]
        y_1 = point_1[1]
        y_2 = point_2[1]

        coefficient = float(y_2 - y_1) / float(x_2 - x_1)
        constant    = - coefficient * x_1 + y_1

        def get_correct(current):
            return max(0, int(round(coefficient * current + constant, 0)))

        for row in rows:

            show_frame = get_correct(frames[row][SHOW])
            hide_frame = get_correct(frames[row][HIDE])
            durn_frame = calc.get_frame_duration(show_frame, hide_frame)
            new_frames.append([show_frame, hide_frame, durn_frame])

            show_time = calc.frame_to_time(show_frame)
            hide_time = calc.frame_to_time(hide_frame)
            durn_time = calc.get_time_duration(show_time, hide_time)
            new_times.append([show_time, hide_time, durn_time])

        self.replace_timings(rows, new_times, new_frames, register)
        self.modify_action_description(register, _('Adjusting frames'))

    def adjust_times(self, rows, point_1, point_2, register=Action.DO):
        """
        Adjust timings in rows.

        point_1 and point_2 are two tuples of row and new show time.
        rows can be None to process all rows.
        """
        rows = rows or range(len(self.times))

        new_times  = []
        new_frames = []
        times  = self.times
        frames = self.frames
        calc   = self.calc

        # Think of this as a linear transformation where current times are
        # located on the x-axis and correct times on the y-axis.
        x_1 = calc.time_to_seconds(times[point_1[0]][SHOW])
        x_2 = calc.time_to_seconds(times[point_2[0]][SHOW])
        y_1 = calc.time_to_seconds(point_1[1])
        y_2 = calc.time_to_seconds(point_2[1])

        coefficient = float(y_2 - y_1) / float(x_2 - x_1)
        constant    = - coefficient * x_1 + y_1

        def get_correct(current):
            seconds = calc.time_to_seconds(current)
            seconds = max(0, coefficient * seconds + constant)
            return calc.seconds_to_time(seconds)

        for row in rows:

            show_time = get_correct(times[row][SHOW])
            hide_time = get_correct(times[row][HIDE])
            durn_time = calc.get_time_duration(show_time, hide_time)
            new_times.append([show_time, hide_time, durn_time])

            show_frame = calc.time_to_frame(show_time)
            hide_frame = calc.time_to_frame(hide_time)
            durn_frame = calc.get_frame_duration(show_frame, hide_frame)
            new_frames.append([show_frame, hide_frame, durn_frame])

        self.replace_timings(rows, new_times, new_frames, register)
        self.modify_action_description(register, _('Adjusting times'))

    def change_framerate(self, framerate):
        """
        Change the framerate and update data.

        This method only changes what is assumed to be the video framerate and
        thus affects only how non-native timing data is calculated. Native
        timings will remain unchanged.
        """
        assert self.main_file is not None

        self.framerate = framerate
        self.calc.set_framerate(framerate)

        calc   = self.calc
        times  = self.times
        frames = self.frames

        if self.main_file.mode == Mode.TIME:
            for i in range(len(times)):

                show = calc.time_to_frame(times[i][SHOW])
                hide = calc.time_to_frame(times[i][HIDE])
                durn = calc.get_frame_duration(show, hide)

                frames[i][SHOW] = show
                frames[i][HIDE] = hide
                frames[i][DURN] = durn

        elif self.main_file.mode == Mode.FRAME:
            for i in range(len(times)):

                show = calc.frame_to_time(frames[i][SHOW])
                hide = calc.frame_to_time(frames[i][HIDE])
                durn = calc.get_time_duration(show, hide)

                times[i][SHOW] = show
                times[i][HIDE] = hide
                times[i][DURN] = durn

    def convert_framerate(self, current_fr, correct_fr, register=Action.DO):
        """Convert and set framerate."""

        self.framerate = correct_fr
        self.calc.set_framerate(correct_fr)

        rows = range(len(self.times))

        orig_times  = []
        orig_frames = []
        times  = self.times
        frames = self.frames
        calc   = self.calc

        values = Framerate.values
        coefficient = values[correct_fr] / values[current_fr]

        for row in rows:

            orig_frames.append(frames[row])
            orig_times.append(times[row])

            show_frame = int(round(coefficient * frames[row][SHOW], 0))
            hide_frame = int(round(coefficient * frames[row][HIDE], 0))
            durn_frame = calc.get_frame_duration(show_frame, hide_frame)
            frames[row] = [show_frame, hide_frame, durn_frame]

            show_time = calc.frame_to_time(show_frame)
            hide_time = calc.frame_to_time(hide_frame)
            durn_time = calc.get_time_duration(show_time, hide_time)
            times[row] = [show_time, hide_time, durn_time]

        self.register_action(
            register=register,
            documents=[Document.MAIN, Document.TRAN],
            description=_('Converting framerate'),
            revert_method=self.revert_framerate_conversion,
            revert_method_args=[current_fr, orig_times, orig_frames],
            timing_rows_updated=rows,
        )

    def replace_timings(self, rows, new_times, new_frames, register=Action.DO):
        """
        Replace timings in rows with new_times and new_frames.

        rows can be None to process all rows.
        """
        rows = rows or range(len(self.times))

        orig_times  = []
        orig_frames = []
        times  = self.times
        frames = self.frames

        for i, row in enumerate(rows):
            orig_times.append(times[row])
            orig_frames.append(frames[row])
            times[row]  = new_times[i]
            frames[row] = new_frames[i]

        self.register_action(
            register=register,
            documents=[Document.MAIN, Document.TRAN],
            description=_('Replacing timings'),
            revert_method=self.replace_timings,
            revert_method_args=[rows, orig_times, orig_frames],
            timing_rows_updated=rows,
        )

    def revert_framerate_conversion(self, framerate, new_times, new_frames,
                                    register=Action.DO):
        """
        Revert framerate and data after conversion.

        *args, **kwargs are passed to replace_timings().
        """
        orig_framerate = self.framerate
        self.framerate = framerate
        self.calc.set_framerate(framerate)

        rows = range(len(self.times))

        orig_times  = []
        orig_frames = []
        times  = self.times
        frames = self.frames

        for i, row in enumerate(rows):
            orig_times.append(times[row])
            orig_frames.append(frames[row])
            times[row]  = new_times[i]
            frames[row] = new_frames[i]

        self.register_action(
            register=register,
            documents=[Document.MAIN, Document.TRAN],
            description=_('Converting framerate'),
            revert_method=self.revert_framerate_conversion,
            revert_method_args=[orig_framerate, orig_times, orig_frames],
            timing_rows_updated=rows,
        )

    def shift_frames(self, rows, amount, register=Action.DO):
        """
        Shift timings by amount of frames.

        rows: None to process all rows
        """
        rows = rows or range(len(self.times))

        new_times  = []
        new_frames = []
        times  = self.times
        frames = self.frames
        calc   = self.calc

        for row in rows:

            show_frame = max(0, frames[row][SHOW] + amount)
            hide_frame = max(0, frames[row][HIDE] + amount)
            durn_frame = calc.get_frame_duration(show_frame, hide_frame)
            new_frames.append([show_frame, hide_frame, durn_frame])

            show_time = calc.frame_to_time(show_frame)
            hide_time = calc.frame_to_time(hide_frame)
            durn_time = calc.get_time_duration(show_time, hide_time)
            new_times.append([show_time, hide_time, durn_time])

        self.replace_timings(rows, new_times, new_frames, register)
        self.modify_action_description(register, _('Shifting frames'))

    def shift_seconds(self, rows, amount, register=Action.DO):
        """
        Shift timings by amount of seconds.

        rows: None to process all rows
        """
        rows = rows or range(len(self.times))

        new_times  = []
        new_frames = []
        times  = self.times
        frames = self.frames
        calc   = self.calc

        for row in rows:

            show_time = calc.add_seconds_to_time(times[row][SHOW], amount)
            hide_time = calc.add_seconds_to_time(times[row][HIDE], amount)
            durn_time = calc.get_time_duration(show_time, hide_time)
            new_times.append([show_time, hide_time, durn_time])

            show_frame = calc.time_to_frame(show_time)
            hide_frame = calc.time_to_frame(hide_time)
            durn_frame = calc.get_frame_duration(show_frame, hide_frame)
            new_frames.append([show_frame, hide_frame, durn_frame])

        self.replace_timings(rows, new_times, new_frames, register)
        self.modify_action_description(register, _('Shifting times'))


if __name__ == '__main__':

    from gaupol.test import Test

    class TestTimingDelegate(Test):

        def __init__(self):

            Test.__init__(self)
            self.project = self.get_project()

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

        def test_adjust_times(self):

            times = self.project.times

            times[0] = ['00:00:01,000', '00:00:02,000', '00:00:01,000']
            times[1] = ['00:00:03,000', '00:00:04,000', '00:00:01,000']
            times[2] = ['00:00:05,000', '00:00:06,000', '00:00:01,000']

            point_1 = (0, '00:00:02,000')
            point_2 = (2, '00:00:05,500')
            self.project.adjust_times(None, point_1, point_2)
            assert times[0] == ['00:00:02,000', '00:00:02,875', '00:00:00,875']
            assert times[1] == ['00:00:03,750', '00:00:04,625', '00:00:00,875']
            assert times[2] == ['00:00:05,500', '00:00:06,375', '00:00:00,875']

            self.project.undo()
            assert times[0] == ['00:00:01,000', '00:00:02,000', '00:00:01,000']
            assert times[1] == ['00:00:03,000', '00:00:04,000', '00:00:01,000']
            assert times[2] == ['00:00:05,000', '00:00:06,000', '00:00:01,000']

        def test_change_framerate(self):

            self.project.change_framerate(Framerate.FR_23_976)
            frame_1 = self.project.frames[5][SHOW]
            self.project.change_framerate(Framerate.FR_25)
            frame_2 = self.project.frames[5][SHOW]
            assert frame_2 == int(round((frame_1 / 23.976) * 25, 0))

        def test_convert_framerate(self):

            frames = self.project.frames
            times  = self.project.times

            frames[0][0] = 100
            frames[1][0] = 500

            self.project.convert_framerate(Framerate.FR_25, Framerate.FR_29_97)
            assert self.project.framerate == Framerate.FR_29_97
            assert self.project.calc.framerate == 29.97
            assert frames[0][0] == 120
            assert frames[1][0] == 599
            assert  times[0][0] == '00:00:04,004'
            assert  times[1][0] == '00:00:19,987'

            self.project.undo()
            assert self.project.framerate == Framerate.FR_25
            assert self.project.calc.framerate == 25.00
            assert frames[0][0] == 100
            assert frames[1][0] == 500

        def test_shift_frames(self):

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

            self.project.shift_frames([1, 2], -5)
            assert frames[0] == [10, 20, 10]
            assert frames[1] == [25, 35, 10]
            assert frames[2] == [45, 55, 10]

            self.project.undo()
            assert frames[0] == [10, 20, 10]
            assert frames[1] == [30, 40, 10]
            assert frames[2] == [50, 60, 10]

        def test_shift_seconds(self):

            times = self.project.times

            times[0] = ['00:00:01,000', '00:00:02,000', '00:00:01,000']
            times[1] = ['00:00:03,000', '00:00:04,000', '00:00:01,000']
            times[2] = ['00:00:05,000', '00:00:06,000', '00:00:01,000']

            self.project.shift_seconds(None, 0.5)
            assert times[0] == ['00:00:01,500', '00:00:02,500', '00:00:01,000']
            assert times[1] == ['00:00:03,500', '00:00:04,500', '00:00:01,000']
            assert times[2] == ['00:00:05,500', '00:00:06,500', '00:00:01,000']

            self.project.undo()
            assert times[0] == ['00:00:01,000', '00:00:02,000', '00:00:01,000']
            assert times[1] == ['00:00:03,000', '00:00:04,000', '00:00:01,000']
            assert times[2] == ['00:00:05,000', '00:00:06,000', '00:00:01,000']

            self.project.shift_seconds([1, 2], -0.5)
            assert times[0] == ['00:00:01,000', '00:00:02,000', '00:00:01,000']
            assert times[1] == ['00:00:02,500', '00:00:03,500', '00:00:01,000']
            assert times[2] == ['00:00:04,500', '00:00:05,500', '00:00:01,000']

            self.project.undo()
            assert times[0] == ['00:00:01,000', '00:00:02,000', '00:00:01,000']
            assert times[1] == ['00:00:03,000', '00:00:04,000', '00:00:01,000']
            assert times[2] == ['00:00:05,000', '00:00:06,000', '00:00:01,000']

    TestTimingDelegate().run()
