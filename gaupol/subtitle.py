# Copyright (C) 2007 Osmo Salomaa
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


"""Single subtitle."""


import gaupol

__all__ = ["Subtitle"]


class Subtitle(object):

    """Single subtitle.

    Instance variables and properties:
     * start (get, set)
     * start_time (get)
     * start_frame (get)
     * start_seconds (get)
     * end (get, set)
     * end_time (get)
     * end_frame (get)
     * end_seconds (get)
     * duration (get, set)
     * duration_time (get)
     * duration_frame (get)
     * duration_seconds (get)
     * main_text (get, set)
     * tran_text (get, set)
     * mode (get, set)
     * framerate (get, set)

    Positions can be set as strings for times, ints for frames or floats for
    seconds. Positions are saved internally in only one mode.
    """

    def __cmp__(self, other):
        """Compare start positions in this subtitle's mode."""

        if self.mode == gaupol.MODE.TIME:
            times = (self.start_time, other.start_time)
            return self._calc.compare_times(*times)
        if self.mode == gaupol.MODE.FRAME:
            return cmp(self.start_frame, other.start_frame)
        raise ValueError

    def __init__(self):

        self._start = "00:00:00.000"
        self._end = "00:00:00.000"
        self._main_text = ""
        self._tran_text = ""

        self._mode = gaupol.MODE.TIME
        self._framerate = gaupol.FRAMERATE.P24
        self._calc = gaupol.Calculator(self._framerate)

    def _convert_position(self, value):
        """Return value of position in correct mode."""

        if isinstance(value, basestring):
            if self.mode == gaupol.MODE.TIME:
                return value
            if self.mode == gaupol.MODE.FRAME:
                return self._calc.time_to_frame(value)
        if isinstance(value, int):
            if self.mode == gaupol.MODE.TIME:
                return self._calc.frame_to_time(value)
            if self.mode == gaupol.MODE.FRAME:
                return value
        if isinstance(value, float):
            if self.mode == gaupol.MODE.TIME:
                return self._calc.seconds_to_time(value)
            if self.mode == gaupol.MODE.FRAME:
                return self._calc.seconds_to_frame(value)
        raise ValueError

    def _get_duration(self):
        """Get the duration in correct mode."""

        if self.mode == gaupol.MODE.TIME:
            return self._get_duration_time()
        if self.mode == gaupol.MODE.FRAME:
            return self._get_duration_frame()
        raise ValueError

    def _get_duration_frame(self):
        """Get the duration as frame."""

        bounds = (self.start_frame, self.end_frame)
        return self._calc.get_frame_duration(*bounds)

    def _get_duration_seconds(self):
        """Get the duration as seconds."""

        time = self._get_duration_time()
        return self._calc.time_to_seconds(time)

    def _get_duration_time(self):
        """Get the duration as time."""

        bounds = (self.start_time, self.end_time)
        return self._calc.get_time_duration(*bounds)

    def _get_end(self):
        """Get the end position in correct mode."""

        return self._end

    def _get_end_frame(self):
        """Get the end position as frame."""

        if self.mode == gaupol.MODE.TIME:
            return self._calc.time_to_frame(self._end)
        if self.mode == gaupol.MODE.FRAME:
            return self._end
        raise ValueError

    def _get_end_seconds(self):
        """Get the end position as seconds."""

        time = self._get_end_time()
        return self._calc.time_to_seconds(time)

    def _get_end_time(self):
        """Get the end position as time."""

        if self.mode == gaupol.MODE.TIME:
            return self._end
        if self.mode == gaupol.MODE.FRAME:
            return self._calc.frame_to_time(self._end)
        raise ValueError

    def _get_framerate(self):
        """Get the framerate."""

        return self._framerate

    def _get_main_text(self):
        """Get the main text."""

        return self._main_text

    def _get_mode(self):
        """Get the current position mode."""

        return self._mode

    def _get_start(self):
        """Get the start position in correct mode."""

        return self._start

    def _get_start_frame(self):
        """Get the start position as frame."""

        if self.mode == gaupol.MODE.TIME:
            return self._calc.time_to_frame(self._start)
        if self.mode == gaupol.MODE.FRAME:
            return self._start
        raise ValueError

    def _get_start_seconds(self):
        """Get the start position as seconds."""

        time = self._get_start_time()
        return self._calc.time_to_seconds(time)

    def _get_start_time(self):
        """Get the start positions as time."""

        if self.mode == gaupol.MODE.TIME:
            return self._start
        if self.mode == gaupol.MODE.FRAME:
            return self._calc.frame_to_time(self._start)
        raise ValueError

    def _get_tran_text(self):
        """Get the translation text."""

        return self._tran_text

    def _set_duration(self, value):
        """Set the duration from value."""

        if isinstance(value, basestring):
            value = self._calc.add_times(self.start_time, value)
        elif isinstance(value, int):
            value = self.start_frame + value
        elif isinstance(value, float):
            value = self._calc.seconds_to_time(value)
            value = self._calc.add_times(self.start_time, value)
        self.end = self._convert_position(value)

    def _set_end(self, value):
        """Set the end position from value."""

        self._end = self._convert_position(value)

    def _set_framerate(self, value):
        """Set the framerate."""

        self._framerate = value
        self._calc = gaupol.Calculator(value)

    def _set_main_text(self, value):
        """Set the main text."""

        self._main_text = unicode(value)

    def _set_mode(self, mode):
        """Set the current position mode."""

        if mode == gaupol.MODE.TIME:
            self._start = self.start_time
            self._end = self.end_time
        elif mode == gaupol.MODE.FRAME:
            self._start = self.start_frame
            self._end = self.end_frame
        self._mode = mode

    def _set_start(self, value):
        """Set the start position from value."""

        self._start = self._convert_position(value)

    def _set_tran_text(self, value):
        """Set the translation text."""

        self._tran_text = unicode(value)

    def convert_framerate(self, framerate):
        """Set the framerate and convert positions to it."""

        coefficient = framerate.value / self._framerate.value
        self._set_framerate(framerate)
        if self.mode == gaupol.MODE.TIME:
            start = self.start_seconds / coefficient
            end = self.end_seconds / coefficient
        elif self.mode == gaupol.MODE.FRAME:
            start = int(round(coefficient * self.start_frame, 0))
            end = int(round(coefficient * self.end_frame, 0))
        self._set_start(start)
        self._set_end(end)

    def copy(self):
        """Return a copy with the same values."""

        subtitle = Subtitle()
        subtitle._start = self._start
        subtitle._end = self._end
        subtitle._main_text = self._main_text
        subtitle._tran_text = self._tran_text
        subtitle._mode = self._mode
        subtitle._framerate = self._framerate
        subtitle._calc = self._calc
        return subtitle

    def get_duration(self, mode):
        """Get the duration in mode."""

        if mode == gaupol.MODE.TIME:
            return self.duration_time
        if mode == gaupol.MODE.FRAME:
            return self.duration_frame
        raise ValueError

    def get_end(self, mode):
        """Get the end position in mode."""

        if mode == gaupol.MODE.TIME:
            return self.end_time
        if mode == gaupol.MODE.FRAME:
            return self.end_frame
        raise ValueError

    def get_start(self, mode):
        """Get the start position in mode."""

        if mode == gaupol.MODE.TIME:
            return self.start_time
        if mode == gaupol.MODE.FRAME:
            return self.start_frame
        raise ValueError

    def get_text(self, doc):
        """Get the text corresponding to document."""

        if doc == gaupol.DOCUMENT.MAIN:
            return self.main_text
        if doc == gaupol.DOCUMENT.TRAN:
            return self.tran_text
        raise ValueError

    def set_text(self, doc, value):
        """Set the text corresponding to document."""

        if doc == gaupol.DOCUMENT.MAIN:
            return self._set_main_text(value)
        if doc == gaupol.DOCUMENT.TRAN:
            return self._set_tran_text(value)
        raise ValueError

    def scale_positions(self, value):
        """Multiply start and end positions by value."""

        if self.mode == gaupol.MODE.TIME:
            self.start = self._get_start_seconds() * value
            self.end = self._get_end_seconds() * value
        elif self.mode == gaupol.MODE.FRAME:
            self.start = int(round(self._start * value, 0))
            self.end = int(round(self._end * value, 0))

    def shift_positions(self, value):
        """Add value to start and end positions."""

        if isinstance(value, basestring):
            start = self._get_start_time()
            start = self._calc.add_times(start, value)
            end = self._get_end_time()
            end = self._calc.add_times(end, value)
        elif isinstance(value, int):
            start = self._get_start_frame() + value
            end = self._get_end_frame() + value
        elif isinstance(value, float):
            start = self._get_start_seconds() + value
            end = self._get_end_seconds() + value
        self._set_start(start)
        self._set_end(end)

    start = property(_get_start, _set_start)
    start_frame = property(_get_start_frame, None)
    start_time = property(_get_start_time, None)
    start_seconds = property(_get_start_seconds, None)
    end = property(_get_end, _set_end)
    end_frame = property(_get_end_frame, None)
    end_time = property(_get_end_time, None)
    end_seconds = property(_get_end_seconds, None)
    duration = property(_get_duration, _set_duration)
    duration_frame = property(_get_duration_frame, None)
    duration_time = property(_get_duration_time, None)
    duration_seconds = property(_get_duration_seconds, None)
    main_text = property(_get_main_text, _set_main_text)
    tran_text = property(_get_tran_text, _set_tran_text)
    mode = property(_get_mode, _set_mode)
    framerate = property(_get_framerate, _set_framerate)
