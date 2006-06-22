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


from gettext import gettext as _

from gaupol.base          import cons
from gaupol.base.icons    import *
from gaupol.base.delegate import Delegate


_DO = cons.Action.DO


class PositionDelegate(Delegate):

    """Shifting and adjusting times and frames."""

    def adjust_durations(
        self,
        rows=None,
        optimal=None,
        lengthen=False,
        shorten=False,
        maximum=None,
        minimum=None,
        gap=None,
        register=_DO
    ):
        """
        Adjust durations.

        optimal: Seconds
        gap: Seconds
        rows: None to process all rows
        Return adjusted rows.
        """
        new_rows   = []
        new_times  = []
        new_frames = []
        rows = rows or range(len(self.times))
        for row in rows:
            show = self.calc.time_to_seconds(self.times[row][SHOW])
            hide = self.calc.time_to_seconds(self.times[row][HIDE])
            durn = hide - show
            try:
                hide_max = self.calc.time_to_seconds(self.times[row + 1][SHOW])
            except IndexError:
                hide_max = 360000

            # Remove overlap.
            if hide > hide_max:
                hide = hide_max
                durn = hide - show

            # Adjust to optimal.
            if optimal is not None:
                length = sum(self.get_line_lengths(row, MAIN))
                durn_optimal = optimal * length
                if durn < durn_optimal and lengthen:
                    hide = min(hide_max, show + durn_optimal)
                if durn > durn_optimal and shorten:
                    hide = show + durn_optimal
                durn = hide - show

            # Limit to minimum and maximum.
            if minimum is not None and durn < minimum:
                hide = min(hide_max, show + minimum)
                durn = hide - show
            if maximum is not None and durn > maximum:
                hide = show + maximum
                durn = hide - show

            # Add gap before next subtitle.
            if gap is not None and (hide_max - hide) < gap:
                hide = max(show, hide_max - gap)
                durn = hide - show

            show_time = self.calc.seconds_to_time(show)
            hide_time = self.calc.seconds_to_time(hide)
            if hide_time == self.times[row][HIDE]:
                continue

            time, frame = self.expand_times(show_time, hide_time)
            new_rows.append(row)
            new_times.append(time)
            new_frames.append(frame)

        if new_rows:
            self.replace_positions(new_rows, new_times, new_frames, register)
            self.set_action_description(register, _('Adjusting durations'))
        return new_rows

    def adjust_frames(self, rows, point_1, point_2, register=_DO):
        """
        Adjust times and frames in rows.

        point_N: Tuples of row and new show frame
        rows: None to process all rows
        """
        # Think of this as a linear transformation where current times are
        # located on the x-axis and correct times on the y-axis.
        x_1 = self.frames[point_1[0]][SHOW]
        x_2 = self.frames[point_2[0]][SHOW]
        y_1 = point_1[1]
        y_2 = point_2[1]

        coefficient = float(y_2 - y_1) / float(x_2 - x_1)
        constant = - coefficient * x_1 + y_1
        def get_correct(current):
            return max(0, int(round(coefficient * current + constant, 0)))

        new_times  = []
        new_frames = []
        rows = rows or range(len(self.times))
        for row in rows:
            time, frame = self.expand_frames(
                get_correct(self.frames[row][SHOW]),
                get_correct(self.frames[row][HIDE])
            )
            new_times.append(time)
            new_frames.append(frame)

        self.replace_positions(rows, new_times, new_frames, register)
        self.set_action_description(register, _('Adjusting frames'))

    def adjust_times(self, rows, point_1, point_2, register=_DO):
        """
        Adjust times and frames in rows.

        point_N: Tuples of row and new show time
        rows: None to process all rows
        """
        # Think of this as a linear transformation where current times are
        # located on the x-axis and correct times on the y-axis.
        x_1 = self.calc.time_to_seconds(self.times[point_1[0]][SHOW])
        x_2 = self.calc.time_to_seconds(self.times[point_2[0]][SHOW])
        y_1 = self.calc.time_to_seconds(point_1[1])
        y_2 = self.calc.time_to_seconds(point_2[1])

        coefficient = float(y_2 - y_1) / float(x_2 - x_1)
        constant = - coefficient * x_1 + y_1
        def get_correct(current):
            seconds = self.calc.time_to_seconds(current)
            seconds = max(0, coefficient * seconds + constant)
            return self.calc.seconds_to_time(seconds)

        new_times  = []
        new_frames = []
        rows = rows or range(len(self.times))
        for row in rows:
            time, frame = self.expand_times(
                get_correct(self.times[row][SHOW]),
                get_correct(self.times[row][HIDE])
            )
            new_times.append(time)
            new_frames.append(frame)

        self.replace_positions(rows, new_times, new_frames, register)
        self.set_action_description(register, _('Adjusting times'))

    def change_framerate(self, framerate):
        """
        Change framerate and update positions.

        Only change is to what is assumed to be the video framerate and thus
        affects only how non-native position data is calculated. Native
        positions will remain unchanged.
        """
        self.set_framerate(framerate, register=None)

        if self.main_file.mode == cons.Mode.TIME:
            convert = self.calc.time_to_frame
            for i in range(len(self.times)):
                self.frames[i][SHOW] = convert(self.times[i][SHOW])
                self.frames[i][HIDE] = convert(self.times[i][HIDE])
                self.set_durations(i)
        elif self.main_file.mode == cons.Mode.FRAME:
            convert = self.calc.frame_to_time
            for i in range(len(self.times)):
                self.times[i][SHOW] = convert(self.frames[i][SHOW])
                self.times[i][HIDE] = convert(self.frames[i][HIDE])
                self.set_durations(i)

    def convert_framerate(self, rows, current, correct, register=_DO):
        """
        Convert and set framerate.

        rows: None to process all rows
        """
        signal = self.get_signal(register)
        self.block(signal)
        self.set_framerate(current, register=None)
        self.set_framerate(correct)

        new_times  = []
        new_frames = []
        rows = rows or range(len(self.times))
        values = cons.Framerate.values
        coefficient = values[correct] / values[current]
        for row in rows:
            if self.main_file.mode == cons.Mode.TIME:
                show = self.calc.time_to_seconds(self.times[row][SHOW])
                hide = self.calc.time_to_seconds(self.times[row][HIDE])
                time, frame = self.expand_times(
                    self.calc.seconds_to_time(show / coefficient),
                    self.calc.seconds_to_time(hide / coefficient)
                )
            elif self.main_file.mode == cons.Mode.FRAME:
                time, frame = self.expand_frames(
                    int(round(coefficient * self.frames[row][SHOW], 0)),
                    int(round(coefficient * self.frames[row][HIDE], 0))
                )
            new_times.append(time)
            new_frames.append(frame)

        self.replace_positions(rows, new_times, new_frames, register)
        self.unblock(signal)
        self.group_actions(register, 2, _('Converting framerate'))

    def set_framerate(self, framerate, register=_DO):
        """Set framerate variables."""

        orig_framerate = self.framerate
        self.framerate = framerate
        self.calc.set_framerate(framerate)

        self.register_action(
            register=register,
            docs=[MAIN, TRAN],
            description=_('Setting framerate'),
            revert_method=self.set_framerate,
            revert_args=[orig_framerate],
        )

    def shift_frames(self, rows, count, register=_DO):
        """
        Shift times and frames by amount of frames.

        rows: None to process all rows
        """
        new_times  = []
        new_frames = []
        rows = rows or range(len(self.times))
        for row in rows:
            time, frame = self.expand_frames(
                max(0, self.frames[row][SHOW] + count),
                max(0, self.frames[row][HIDE] + count)
            )
            new_times.append(time)
            new_frames.append(frame)

        self.replace_positions(rows, new_times, new_frames, register)
        self.set_action_description(register, _('Shifting frames'))

    def shift_seconds(self, rows, count, register=_DO):
        """
        Shift times and frames by amount of seconds.

        rows: None to process all rows
        """
        new_times  = []
        new_frames = []
        rows = rows or range(len(self.times))
        for row in rows:
            time, frame = self.expand_times(
                self.calc.add_seconds_to_time(self.times[row][SHOW], count),
                self.calc.add_seconds_to_time(self.times[row][HIDE], count)
            )
            new_times.append(time)
            new_frames.append(frame)

        self.replace_positions(rows, new_times, new_frames, register)
        self.set_action_description(register, _('Shifting times'))
