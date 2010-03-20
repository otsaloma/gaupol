# Copyright (C) 2005-2007,2009 Osmo Salomaa
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

    # pylint: disable-msg=E0203,E1101,W0201

    __metaclass__ = aeidon.Contractual

    def _get_frame_transform_ensure(self, value, p1, p2):
        assert isinstance(value[1], int)

    def _get_frame_transform(self, p1, p2):
        """Return a formula for linear transformation of positions.

        Return coefficient and constant, with which all subtitles
        should be scaled and shifted by to apply correction.
        """
        # Think of this as a linear transformation where input positions
        # are located on the x-axis and output positions on the y-axis.
        x1 = self.subtitles[p1[0]].start_frame
        x2 = self.subtitles[p2[0]].start_frame
        y1 = p1[1]
        y2 = p2[1]
        coefficient = (y2 - y1) / (x2 - x1)
        constant = int(round(- (coefficient * x1) + y1, 0))
        return coefficient, constant

    def _get_seconds_transform_ensure(self, value, p1, p2):
        assert isinstance(value[1], float)

    def _get_seconds_transform(self, p1, p2):
        """Return a formula for linear transformation of positions.

        Return coefficient and constant, with which all subtitles should be
        scaled and shifted by to apply correction.
        """
        # Think of this as a linear transformation where input positions
        # are located on the x-axis and output positions on the y-axis.
        x1 = self.subtitles[p1[0]].start_seconds
        x2 = self.subtitles[p2[0]].start_seconds
        y1 = p1[1]
        y2 = p2[1]
        coefficient = (y2 - y1) / (x2 - x1)
        constant = - (coefficient * x1) + y1
        return coefficient, constant

    def _get_time_transform(self, p1, p2):
        """Return a formula for linear correction of positions.

        Return coefficient and constant, with which all subtitles should be
        scaled and shifted by to apply correction.
        """
        p1 = [p1[0], self.calc.time_to_seconds(p1[1])]
        p2 = [p2[0], self.calc.time_to_seconds(p2[1])]
        return self._get_seconds_transform(p1, p2)

    def adjust_durations_require(self, indices=None, *args, **kwargs):
        for index in indices or ():
            assert 0 <= index < len(self.subtitles)

    @aeidon.deco.export
    @aeidon.deco.revertable
    def adjust_durations(self,
                         indices=None,
                         optimal=None,
                         lengthen=False,
                         shorten=False,
                         minimum=None,
                         maximum=None,
                         gap=None,
                         register=-1):
        """Lengthen or shorten durations by changing end positions.

        `indices` can be ``None`` to process all subtitles. `optimal` is
        duration per character in seconds. `lengthen` is ``True`` to increase
        durations if shorter than optimal. `shorten` is ``True`` to decrease
        durations if longer than optimal. `maximum` is the greatest allowed
        duration in seconds. `minimum` is the smallest allowed duration in
        seconds. `gap` is seconds to be left between consecutive subtitles.
        Using a gap of zero (or a bit more) is always a good idea if dealing
        with subtitles where overlapping is not desirable.

        Return changed indices.
        """
        new_indices = []
        new_subtitles = []
        for index in indices or self.get_all_indices():
            start = self.subtitles[index].start_seconds
            end = self.subtitles[index].end_seconds
            end_max = (self.subtitles[index + 1].start_seconds if
                       index < (len(self.subtitles) - 1) else 360000)

            if (optimal is not None) and (lengthen or shorten):
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
            self.replace_positions(new_indices,
                                   new_subtitles,
                                   register=register)

            self.set_action_description(register, _("Adjusting durations"))
        return new_indices

    def convert_framerate_require(self, indices, *args, **kwargs):
        for index in indices or ():
            assert 0 <= index < len(self.subtitles)

    @aeidon.deco.export
    @aeidon.deco.revertable
    def convert_framerate(self,
                          indices,
                          framerate_in,
                          framerate_out,
                          register=-1):
        """Set the value of framerate and convert subtitles to it.

        `indices` can be ``None`` to process all subtitles.
        """
        self.set_framerate(framerate_in, register=None)
        new_subtitles = []
        indices = indices or self.get_all_indices()
        for index in indices:
            subtitle = self.subtitles[index].copy()
            subtitle.convert_framerate(framerate_out)
            new_subtitles.append(subtitle)
        self.set_framerate(framerate_out)
        self.replace_positions(indices, new_subtitles, register=register)
        self.group_actions(register, 2, _("Converting framerate"))

    @aeidon.deco.export
    @aeidon.deco.revertable
    def set_framerate(self, framerate, register=-1):
        """Set the value of framerate."""
        orig_framerate = self.framerate
        self.framerate = framerate
        self.calc = aeidon.Calculator(framerate)
        for subtitle in self.subtitles:
            subtitle.framerate = framerate
        action = self.new_revertable_action(register)
        action.docs = tuple(aeidon.documents)
        action.description = _("Setting framerate")
        action.revert_function = self.set_framerate
        action.revert_args = (orig_framerate,)
        self.register_action(action)

    def shift_positions_require(self, indices, count, register=-1):
        for index in indices or ():
            assert 0 <= index < len(self.subtitles)

    @aeidon.deco.export
    @aeidon.deco.revertable
    def shift_positions(self, indices, value, register=-1):
        """Make subtitles appear earlier or later.

        `indices` can be ``None`` to process all subtitles. `value` should be a
        string for time, a float for seconds or an integer for frames.
        """
        new_subtitles = []
        indices = indices or self.get_all_indices()
        for index in indices:
            subtitle = self.subtitles[index].copy()
            subtitle.shift_positions(value)
            new_subtitles.append(subtitle)
        self.replace_positions(indices, new_subtitles, register=register)
        self.set_action_description(register, _("Shifting positions"))

    def transform_positions_require(self, indices, *args, **kwargs):
        for index in indices or ():
            assert 0 <= index < len(self.subtitles)

    @aeidon.deco.export
    @aeidon.deco.revertable
    def transform_positions(self, indices, p1, p2, register=-1):
        """Change positions by linear two-point corrections.

        `indices` can be ``None`` to process all subtitles. `p1` and `p2`
        should be tuples of index, position, where position should be a string
        for time, a float for seconds or an integer for frames.
        """
        if isinstance(p1[1], basestring):
            method = self._get_time_transform
        if isinstance(p1[1], int):
            method = self._get_frame_transform
        if isinstance(p1[1], float):
            method = self._get_seconds_transform
        coefficient, constant = method(p1, p2)
        new_subtitles = []
        indices = indices or self.get_all_indices()
        for index in indices:
            subtitle = self.subtitles[index].copy()
            subtitle.scale_positions(coefficient)
            subtitle.shift_positions(constant)
            new_subtitles.append(subtitle)
        self.replace_positions(indices, new_subtitles, register=register)
        self.set_action_description(register, _("Transforming positions"))
