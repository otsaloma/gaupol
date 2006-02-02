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
from gaupol.constants         import Action, Document


class TimingDelegate(Delegate):

    """Shifting, adjusting and fixing timings."""

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
            times[row] = new_times[i]
            frames[row] = new_frames[i]

        self.register_action(
            register=register,
            documents=[Document.MAIN, Document.TRAN],
            description=_('Replacing timings'),
            revert_method=self.replace_timings,
            revert_method_args=[rows, orig_times, orig_frames],
            timing_rows_updated=rows,
        )

    def shift_frames(self, rows, shift, register=Action.DO):
        """
        Shift timings shift amount of frames.

        rows can be None to process all rows.
        """
        rows = rows or range(len(self.times))

        new_times  = []
        new_frames = []
        times  = self.times
        frames = self.frames
        calc   = self.calc

        for row in rows:

            show_frame = max(0, frames[row][SHOW] + shift)
            hide_frame = max(0, frames[row][HIDE] + shift)
            durn_frame = calc.get_frame_duration(show_frame, hide_frame)
            new_frames.append([show_frame, hide_frame, durn_frame])

            show_time = calc.frame_to_time(show_frame)
            hide_time = calc.frame_to_time(hide_frame)
            durn_time = calc.get_time_duration(show_time, hide_time)
            new_times.append([show_time, hide_time, durn_time])

        self.replace_timings(rows, new_times, new_frames, register)
        self.modify_action_description(register, _('Shifting frames'))

    def shift_seconds(self, rows, shift, register=Action.DO):
        """
        Shift timings shift amount of seconds.

        rows can be None to process all rows.
        """
        rows = rows or range(len(self.times))

        new_times  = []
        new_frames = []
        times  = self.times
        frames = self.frames
        calc   = self.calc

        for row in rows:

            show_time = calc.add_seconds_to_time(times[row][SHOW], shift)
            hide_time = calc.add_seconds_to_time(times[row][HIDE], shift)
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
