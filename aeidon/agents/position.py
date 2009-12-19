# Copyright (C) 2005-2007 Osmo Salomaa
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

"""Manipulating times and frames."""

from __future__ import division

import aeidon
_ = aeidon.i18n._


class PositionAgent(aeidon.Delegate):

    """Manipulating times and frames."""

    __metaclass__ = aeidon.Contractual

    def _get_frame_transform_ensure(self, value, point_1, point_2):
        assert isinstance(value[1], int)

    def _get_frame_transform(self, point_1, point_2):
        """Return a formula for linear correction of positions.

        point_* should be a tuple of index and start frame.
        Return coefficient and constant, with which all subtitles should be
        scaled and shifted by to apply correction.
        """
        # Think of this as a linear transformation where input positions
        # are located on the x-axis and output positions on the y-axis.
        x_1 = self.subtitles[point_1[0]].start_frame
        x_2 = self.subtitles[point_2[0]].start_frame
        y_1 = point_1[1]
        y_2 = point_2[1]
        coefficient = (y_2 - y_1) / (x_2 - x_1)
        constant = int(round(- (coefficient * x_1) + y_1, 0))
        return coefficient, constant

    def _get_seconds_transform_ensure(self, value, point_1, point_2):
        assert isinstance(value[1], float)

    def _get_seconds_transform(self, point_1, point_2):
        """Return a formula for linear correction of positions.

        point_* should be a tuple of index and start seconds.
        Return coefficient and constant, with which all subtitles should be
        scaled and shifted by to apply correction.
        """
        # Think of this as a linear transformation where input positions
        # are located on the x-axis and output positions on the y-axis.
        x_1 = self.subtitles[point_1[0]].start_seconds
        x_2 = self.subtitles[point_2[0]].start_seconds
        y_1 = point_1[1]
        y_2 = point_2[1]
        coefficient = (y_2 - y_1) / (x_2 - x_1)
        constant = - (coefficient * x_1) + y_1
        return coefficient, constant

    def _get_time_transform(self, point_1, point_2):
        """Return a formula for linear correction of positions.

        point_* should be a tuple of index and start time.
        Return coefficient and constant, with which all subtitles should be
        scaled and shifted by to apply correction.
        """
        point_1 = list(point_1)
        point_1[1] = self.calc.time_to_seconds(point_1[1])
        point_2 = list(point_2)
        point_2[1] = self.calc.time_to_seconds(point_2[1])
        return self._get_seconds_transform(point_1, point_2)

    def adjust_durations_require(self, indices=None, *args, **kwargs):
        for index in indices or []:
            assert 0 <= index < len(self.subtitles)

    @aeidon.deco.revertable
    def adjust_durations(self, indices=None, optimal=None, lengthen=False,
        shorten=False, maximum=None, minimum=None, gap=None, register=-1):
        """Lengthen or shorten durations by changing the end positions.

        indices can be None to process all subtitles.
        optimal is duration per character in seconds.
        gap is seconds to be left between consecutive subtitles.
        Return changed indices.
        """
        new_indices = []
        new_subtitles = []
        indices = indices or range(len(self.subtitles))
        for index in indices:
            start = self.subtitles[index].start_seconds
            end = self.subtitles[index].end_seconds
            end_max = 360000
            if index < (len(self.subtitles) - 1):
                end_max = self.subtitles[index + 1].start_seconds
            if optimal is not None:
                length = self.get_text_length(index, aeidon.documents.MAIN)
                optimal_duration = optimal * length
                if ((end - start) < optimal_duration) and lengthen:
                    end = start + optimal_duration
                if ((end - start) > optimal_duration) and shorten:
                    end = start + optimal_duration
            if (minimum is not None) and ((end - start) < minimum):
                end = start + minimum
            if (maximum is not None) and ((end - start) > maximum):
                end = start + maximum
            if (gap is not None) and ((end_max - end) < gap):
                end = max(start, end_max - gap)
            if end != self.subtitles[index].end_seconds:
                new_indices.append(index)
                subtitle = self.subtitles[index].copy()
                subtitle.end = end
                new_subtitles.append(subtitle)

        if new_indices:
            method = self.replace_positions
            method(new_indices, new_subtitles, register=register)
            self.set_action_description(register, _("Adjusting durations"))
        return new_indices

    def convert_framerate_require(self, indices, *args, **kwargs):
        for index in indices or []:
            assert 0 <= index < len(self.subtitles)

    @aeidon.deco.revertable
    def convert_framerate(self, indices, input, output, register=-1):
        """Set the value of the framerate and convert subtitles to it.

        indices can be None to process all subtitles.
        """
        self.set_framerate(input, register=None)
        new_subtitles = []
        indices = indices or range(len(self.subtitles))
        for index in indices:
            subtitle = self.subtitles[index].copy()
            subtitle.convert_framerate(output)
            new_subtitles.append(subtitle)

        self.set_framerate(output)
        self.replace_positions(indices, new_subtitles, register=register)
        self.group_actions(register, 2, _("Converting framerate"))

    @aeidon.deco.revertable
    def set_framerate(self, framerate, register=-1):
        """Set the value of the framerate."""

        orig_framerate = self.framerate
        self.framerate = framerate
        self.calc = aeidon.Calculator(framerate)
        for subtitle in self.subtitles:
            subtitle.framerate = framerate

        action = self.get_revertable_action(register)
        action.docs = tuple(aeidon.documents)
        action.description = _("Setting framerate")
        action.revert_function = self.set_framerate
        action.revert_args = (orig_framerate,)
        self.register_action(action)

    def shift_positions_require(self, indices, count, register=-1):
        for index in indices or []:
            assert 0 <= index < len(self.subtitles)

    @aeidon.deco.revertable
    def shift_positions(self, indices, value, register=-1):
        """Make subtitles appear earlier or later.

        indices can be None to process all subtitles.
        """
        new_subtitles = []
        indices = indices or range(len(self.subtitles))
        for index in indices:
            subtitle = self.subtitles[index].copy()
            subtitle.shift_positions(value)
            new_subtitles.append(subtitle)

        self.replace_positions(indices, new_subtitles, register=register)
        self.set_action_description(register, _("Shifting positions"))

    def transform_positions_require(self, indices, *args, **kwargs):
        for index in indices or []:
            assert 0 <= index < len(self.subtitles)

    @aeidon.deco.revertable
    def transform_positions(self, indices, point_1, point_2, register=-1):
        """Change positions by linear two-point correction.

        indices can be None to process all subtitles.
        point_* should be a tuple of index and start position.
        """
        if isinstance(point_1[1], basestring):
            get_transform = self._get_time_transform
        elif isinstance(point_1[1], int):
            get_transform = self._get_frame_transform
        elif isinstance(point_1[1], float):
            get_transform = self._get_seconds_transform
        coefficient, constant = get_transform(point_1, point_2)
        new_subtitles = []
        indices = indices or range(len(self.subtitles))
        for index in indices:
            subtitle = self.subtitles[index].copy()
            subtitle.scale_positions(coefficient)
            subtitle.shift_positions(constant)
            new_subtitles.append(subtitle)

        self.replace_positions(indices, new_subtitles, register=register)
        self.set_action_description(register, _("Transforming positions"))
