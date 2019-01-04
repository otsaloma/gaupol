# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Manipulating times and frames."""

import aeidon

from aeidon.i18n import _


class PositionAgent(aeidon.Delegate):

    """Manipulating times and frames."""

    @aeidon.deco.export
    @aeidon.deco.revertable
    def adjust_durations(self, indices=None, speed=None, lengthen=False,
                         shorten=False, minimum=None, maximum=None, gap=None,
                         register=-1):
        """
        Lengthen or shorten durations by changing end positions.

        `indices` can be ``None`` to process all subtitles. `speed` is reading
        speed in characters per second. `lengthen` is ``True`` to increase
        durations to match reading speed. `shorten` is ``True`` to decrease
        durations to match reading speed. `maximum` is the longest allowed
        duration in seconds. `minimum` is the shortest allowed duration in
        seconds. `gap` is seconds to be left between consecutive subtitles.
        Using a gap of at least zero is always a good idea if overlapping
        is not desired. Return changed indices.
        """
        new_indices = []
        new_subtitles = []
        for index in indices or self.get_all_indices():
            start = self.subtitles[index].start_seconds
            end = self.subtitles[index].end_seconds
            if speed is not None:
                length = self.get_text_length(index, aeidon.documents.MAIN)
                optimal_duration = length / speed
                dol = lengthen and end - start < optimal_duration
                dos = shorten  and end - start > optimal_duration
                end = start + optimal_duration if dol or dos else end
            domin = minimum and end - start < minimum
            domax = maximum and end - start > maximum
            end = start + minimum if domin else end
            end = start + maximum if domax else end
            end_max = (self.subtitles[index + 1].start_seconds
                       if index < len(self.subtitles) - 1
                       else 360000)

            dogap = gap is not None and end_max - end < gap
            end = max(start, end_max - gap) if dogap else end
            if end != self.subtitles[index].end_seconds:
                new_indices.append(index)
                subtitle = self.subtitles[index].copy()
                subtitle.end_seconds = end
                new_subtitles.append(subtitle)
        if not new_indices: return []
        self.replace_positions(new_indices, new_subtitles, register=register)
        self.set_action_description(register, _("Adjusting durations"))
        return new_indices

    @aeidon.deco.export
    @aeidon.deco.revertable
    def convert_framerate(self, indices, framerate_in, framerate_out,
                          register=-1):
        """
        Set the value of framerate and convert subtitles to it.

        `indices` can be ``None`` to process all subtitles. `framerate_in` and
        `framerate_out` should be constants from :attr:`aeidon.framerates`.
        """
        new_subtitles = []
        indices = indices or self.get_all_indices()
        self.set_framerate(framerate_in, register=None)
        for index in indices:
            subtitle = self.subtitles[index].copy()
            subtitle.convert_framerate(framerate_out)
            new_subtitles.append(subtitle)
        self.set_framerate(framerate_out)
        self.replace_positions(indices, new_subtitles, register=register)
        self.group_actions(register, 2, _("Converting framerate"))

    def _get_frame_transform(self, p1, p2):
        """Return a formula for linear correction of positions."""
        # Think of this as a linear transformation where input positions
        # are located on the x-axis and output positions on the y-axis.
        x1 = self.subtitles[p1[0]].start_frame
        x2 = self.subtitles[p2[0]].start_frame
        y1 = p1[1]
        y2 = p2[1]
        coefficient = (y2 - y1) / (x2 - x1)
        constant = int(round(-coefficient * x1 + y1, 0))
        return coefficient, constant

    def _get_seconds_transform(self, p1, p2):
        """Return a formula for linear correction of positions."""
        # Think of this as a linear transformation where input positions
        # are located on the x-axis and output positions on the y-axis.
        x1 = self.subtitles[p1[0]].start_seconds
        x2 = self.subtitles[p2[0]].start_seconds
        y1 = p1[1]
        y2 = p2[1]
        coefficient = (y2 - y1) / (x2 - x1)
        constant = -coefficient * x1 + y1
        return coefficient, constant

    def _get_time_transform(self, p1, p2):
        """Return a formula for linear correction of positions."""
        p1 = [p1[0], self.calc.time_to_seconds(p1[1])]
        p2 = [p2[0], self.calc.time_to_seconds(p2[1])]
        return self._get_seconds_transform(p1, p2)

    def _get_transform(self, p1, p2):
        """Return a formula for linear correction of positions."""
        if aeidon.is_time(p1[1]): return self._get_time_transform(p1, p2)
        if aeidon.is_frame(p1[1]): return self._get_frame_transform(p1, p2)
        if aeidon.is_seconds(p1[1]): return self._get_seconds_transform(p1, p2)
        raise ValueError("Bad position argument: {!r}".format(p1))

    @aeidon.deco.export
    @aeidon.deco.revertable
    def set_framerate(self, framerate, register=-1):
        """Set the value of framerate."""
        orig_framerate = self.framerate
        self.framerate = framerate
        self.calc = aeidon.Calculator(framerate)
        for subtitle in self.subtitles:
            subtitle.framerate = framerate
        action = aeidon.RevertableAction(register=register)
        action.docs = tuple(aeidon.documents)
        action.description = _("Setting framerate")
        action.revert_function = self.set_framerate
        action.revert_args = (orig_framerate,)
        self.register_action(action)

    @aeidon.deco.export
    @aeidon.deco.revertable
    def shift_positions(self, indices, value, register=-1):
        """
        Make subtitles appear earlier or later.

        `indices` can be ``None`` to process all subtitles.
        `value` can be any valid position type, negative to make subtitles
        appear ealier, positive to make subtitles appear later.
        """
        new_subtitles = []
        indices = indices or self.get_all_indices()
        for index in indices:
            subtitle = self.subtitles[index].copy()
            subtitle.shift_positions(value)
            new_subtitles.append(subtitle)
        self.replace_positions(indices, new_subtitles, register=register)
        self.set_action_description(register, _("Shifting positions"))

    @aeidon.deco.export
    @aeidon.deco.revertable
    def transform_positions(self, indices, p1, p2, register=-1):
        """
        Change positions by a linear two-point correction.

        `indices` can be ``None`` to process all subtitles.
        `p1` and `p2` should be tuples of index, position.
        """
        new_subtitles = []
        indices = indices or self.get_all_indices()
        coefficient, constant = self._get_transform(p1, p2)
        for index in indices:
            subtitle = self.subtitles[index].copy()
            subtitle.scale_positions(coefficient)
            subtitle.shift_positions(constant)
            new_subtitles.append(subtitle)
        self.replace_positions(indices, new_subtitles, register=register)
        self.set_action_description(register, _("Transforming positions"))
