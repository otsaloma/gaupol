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


"""Shifting and adjusting times and frames."""


from __future__ import division

from gettext import gettext as _

from gaupol import cons
from gaupol.base import Delegate, notify_frozen
from .index import SHOW, HIDE, DURN
from .register import revertable


class PositionAgent(Delegate):

    """Shifting and adjusting times and frames."""

    # pylint: disable-msg=E0203,W0201

    @revertable
    def adjust_durations(self, rows=None, optimal=None, lengthen=False,
        shorten=False, maximum=None, minimum=None, gap=None, register=-1):
        """Adjust durations.

        rows can be None to process all rows.
        optimal and gap should be in seconds.
        Return the adjusted rows.
        """
        new_rows = []
        new_times = []
        new_frames = []
        rows = rows or range(len(self.times))
        for row in rows:
            show = self.calc.time_to_seconds(self.times[row][SHOW])
            hide = self.calc.time_to_seconds(self.times[row][HIDE])
            hide_max = 360000
            if row < len(self.times) - 1:
                hide_max = self.calc.time_to_seconds(self.times[row + 1][SHOW])
            if optimal is not None:
                length = self.get_text_length(row, cons.DOCUMENT.MAIN)
                optimal_durn = optimal * length
                if hide - show < optimal_durn and lengthen:
                    hide = show + optimal_durn
                if hide - show > optimal_durn and shorten:
                    hide = show + optimal_durn
            if minimum is not None and hide - show < minimum:
                hide = show + minimum
            if maximum is not None and hide - show > maximum:
                hide = show + maximum
            if gap is not None and (hide_max - hide) < gap:
                hide = max(show, hide_max - gap)
            if self.calc.seconds_to_time(hide) == self.times[row][HIDE]:
                continue
            time, frame = self.expand_seconds(show, hide)
            new_rows.append(row)
            new_times.append(time)
            new_frames.append(frame)

        if new_rows:
            self.replace_positions(
                new_rows, new_times, new_frames, register=register)
            self.set_action_description(register, _("Adjusting durations"))
        return new_rows

    @revertable
    def adjust_frames(self, rows, point_1, point_2, register=-1):
        """Adjust times and frames in rows.

        rows can be None to process all rows.
        point_N should be a tuple of row and new show frame.
        """
        # Think of this as a linear transformation where current times are
        # located on the x-axis and correct times on the y-axis.
        x_1 = self.frames[point_1[0]][SHOW]
        x_2 = self.frames[point_2[0]][SHOW]
        y_1 = point_1[1]
        y_2 = point_2[1]
        coefficient = (y_2 - y_1) / (x_2 - x_1)
        constant = - coefficient * x_1 + y_1
        def get_correct(current):
            return max(0, int(round(coefficient * current + constant, 0)))

        new_times = []
        new_frames = []
        rows = rows or range(len(self.times))
        for row in rows:
            show = get_correct(self.frames[row][SHOW])
            hide = get_correct(self.frames[row][HIDE])
            time, frame = self.expand_frames(show, hide)
            new_times.append(time)
            new_frames.append(frame)

        self.replace_positions(rows, new_times, new_frames, register=register)
        self.set_action_description(register, _("Adjusting frames"))

    @revertable
    def adjust_times(self, rows, point_1, point_2, register=-1):
        """Adjust times and frames in rows.

        rows can be None to process all rows.
        point_N should be a tuple of row and new show time.
        """
        # Think of this as a linear transformation where current times are
        # located on the x-axis and correct times on the y-axis.
        x_1 = self.calc.time_to_seconds(self.times[point_1[0]][SHOW])
        x_2 = self.calc.time_to_seconds(self.times[point_2[0]][SHOW])
        y_1 = self.calc.time_to_seconds(point_1[1])
        y_2 = self.calc.time_to_seconds(point_2[1])
        coefficient = (y_2 - y_1) / (x_2 - x_1)
        constant = - coefficient * x_1 + y_1
        def get_correct(current):
            seconds = self.calc.time_to_seconds(current)
            seconds = max(0, coefficient * seconds + constant)
            return self.calc.seconds_to_time(seconds)

        new_times = []
        new_frames = []
        rows = rows or range(len(self.times))
        for row in rows:
            show = get_correct(self.times[row][SHOW])
            hide = get_correct(self.times[row][HIDE])
            time, frame = self.expand_times(show, hide)
            new_times.append(time)
            new_frames.append(frame)

        self.replace_positions(rows, new_times, new_frames, register=register)
        self.set_action_description(register, _("Adjusting times"))

    @notify_frozen
    def change_framerate(self, framerate):
        """Change the framerate and update positions.

        Only change is to what is assumed to be the video framerate and thus
        effect only how non-native position data is calculated. Native
        positions will remain unchanged.
        """
        self.set_framerate(framerate, register=None)
        if self.main_file.mode == cons.MODE.TIME:
            convert = self.calc.time_to_frame
            for i in range(len(self.times)):
                self.frames[i][SHOW] = convert(self.times[i][SHOW])
                self.frames[i][HIDE] = convert(self.times[i][HIDE])
                self.frames[i][DURN] = self.calc.get_frame_duration(
                    self.frames[i][SHOW], self.frames[i][HIDE])
        elif self.main_file.mode == cons.MODE.FRAME:
            convert = self.calc.frame_to_time
            for i in range(len(self.times)):
                self.times[i][SHOW] = convert(self.frames[i][SHOW])
                self.times[i][HIDE] = convert(self.frames[i][HIDE])
                self.times[i][DURN] = self.calc.get_time_duration(
                    self.times[i][SHOW], self.times[i][HIDE])
        self.emit("positions-changed", range(len(self.times)))

    @revertable
    def convert_framerate(self, rows, current, correct, register=-1):
        """Convert and set the framerate.

        rows can be None to process all rows.
        """
        self.set_framerate(current, register=None)
        self.set_framerate(correct)

        new_times = []
        new_frames = []
        rows = rows or range(len(self.times))
        coefficient = correct.value / current.value
        for row in rows:
            if self.main_file.mode == cons.MODE.TIME:
                show = self.calc.time_to_seconds(self.times[row][SHOW])
                hide = self.calc.time_to_seconds(self.times[row][HIDE])
                time, frame = self.expand_seconds(
                    show / coefficient,
                    hide / coefficient)
            elif self.main_file.mode == cons.MODE.FRAME:
                time, frame = self.expand_frames(
                    int(round(coefficient * self.frames[row][SHOW], 0)),
                    int(round(coefficient * self.frames[row][HIDE], 0)))
            new_times.append(time)
            new_frames.append(frame)

        self.replace_positions(rows, new_times, new_frames, register=register)
        self.group_actions(register, 2, _("Converting framerate"))

    @revertable
    def set_framerate(self, framerate, register=-1):
        """Set the framerate."""

        orig_framerate = self.framerate
        self.framerate = framerate
        self.calc.set_framerate(framerate)

        self.register_action(
            register=register,
            docs=[cons.DOCUMENT.MAIN, cons.DOCUMENT.TRAN],
            description=_("Setting framerate"),
            revert_method=self.set_framerate,
            revert_args=[orig_framerate],)

    @revertable
    def shift_frames(self, rows, count, register=-1):
        """Shift times and frames.

        rows can be None to process all rows.
        """
        new_times = []
        new_frames = []
        rows = rows or range(len(self.times))
        for row in rows:
            show = max(0, self.frames[row][SHOW] + count)
            hide = max(0, self.frames[row][HIDE] + count)
            time, frame = self.expand_frames(show, hide)
            new_times.append(time)
            new_frames.append(frame)

        self.replace_positions(rows, new_times, new_frames, register=register)
        self.set_action_description(register, _("Shifting frames"))

    @revertable
    def shift_seconds(self, rows, count, register=-1):
        """Shift times and frames.

        rows can be None to process all rows.
        """
        new_times = []
        new_frames = []
        rows = rows or range(len(self.times))
        for row in rows:
            show = self.calc.add_seconds_to_time(self.times[row][SHOW], count)
            hide = self.calc.add_seconds_to_time(self.times[row][HIDE], count)
            time, frame = self.expand_times(show, hide)
            new_times.append(time)
            new_frames.append(frame)

        self.replace_positions(rows, new_times, new_frames, register=register)
        self.set_action_description(register, _("Shifting times"))
