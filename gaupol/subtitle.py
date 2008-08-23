# Copyright (C) 2007-2008 Osmo Salomaa
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

"""Single subtitle."""

import copy
import gaupol

__all__ = ("Subtitle",)


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
     * calc (get, set)
     * framerate (get, set)
     * mode (get, set)

    Positions can be set as strings for times, integers for frames or floats
    for seconds. Positions are saved internally in only one mode.

    Additional format-specific attributes are kept under separate containers,
    e.g. "ssa" for Sub Station Alpha formats, accessed as subtitle.ssa.*.
    These containers are lazily created upon first use in order to avoid slow
    instantiation and excessive memory use when handling simpler formats.
    """

    def __cmp__(self, other):
        """Compare start positions in this subtitle's mode.

        Return 1 if this subtitle appears later, 0 if they appear at the same
        time and -1 if other appears later.
        """
        if self._mode == gaupol.modes.TIME:
            times = (self._start, other.start_time)
            return self.calc.compare_times(*times)
        if self._mode == gaupol.modes.FRAME:
            return cmp(self._start, other.start_frame)
        raise ValueError

    def __getattr__(self, name):

        if name in (x.container for x in gaupol.formats):
            # Lazily instantiate a new container.
            container = gaupol.containers.new(name)
            object.__setattr__(self, name, container)
            return container
        raise AttributeError

    def __init__(self, mode=None, framerate=None):

        self._start = "00:00:00.000"
        self._end = "00:00:00.000"
        self._main_text = ""
        self._tran_text = ""

        self._mode = mode or gaupol.modes.TIME
        self._framerate = framerate or gaupol.framerates.FPS_24
        self.calc = gaupol.Calculator(self._framerate)

    def _convert_position(self, value):
        """Return value of position in correct mode."""

        if isinstance(value, basestring):
            if self._mode == gaupol.modes.TIME:
                return value
            if self._mode == gaupol.modes.FRAME:
                return self.calc.time_to_frame(value)
        if isinstance(value, int):
            if self._mode == gaupol.modes.TIME:
                return self.calc.frame_to_time(value)
            if self._mode == gaupol.modes.FRAME:
                return value
        if isinstance(value, float):
            if self._mode == gaupol.modes.TIME:
                return self.calc.seconds_to_time(value)
            if self._mode == gaupol.modes.FRAME:
                return self.calc.seconds_to_frame(value)
        raise ValueError

    def _get_duration(self):
        """Return the duration in correct mode."""

        if self._mode == gaupol.modes.TIME:
            return self._get_duration_time()
        if self._mode == gaupol.modes.FRAME:
            return self._get_duration_frame()
        raise ValueError

    def _get_duration_frame(self):
        """Return the duration as frames."""

        bounds = (self.start_frame, self.end_frame)
        return self.calc.get_frame_duration(*bounds)

    def _get_duration_seconds(self):
        """Return the duration as seconds."""

        time = self._get_duration_time()
        return self.calc.time_to_seconds(time)

    def _get_duration_time(self):
        """Return the duration as time."""

        bounds = (self.start_time, self.end_time)
        return self.calc.get_time_duration(*bounds)

    def _get_end(self):
        """Return the end position in correct mode."""

        return self._end

    def _get_end_frame(self):
        """Return the end position as frames."""

        if self._mode == gaupol.modes.TIME:
            return self.calc.time_to_frame(self._end)
        if self._mode == gaupol.modes.FRAME:
            return self._end
        raise ValueError

    def _get_end_seconds(self):
        """Return the end position as seconds."""

        time = self._get_end_time()
        return self.calc.time_to_seconds(time)

    def _get_end_time(self):
        """Return the end position as time."""

        if self._mode == gaupol.modes.TIME:
            return self._end
        if self._mode == gaupol.modes.FRAME:
            return self.calc.frame_to_time(self._end)
        raise ValueError

    def _get_framerate(self):
        """Return the framerate."""

        return self._framerate

    def _get_main_text(self):
        """Return the main text."""

        return self._main_text

    def _get_mode(self):
        """Return the current position mode."""

        return self._mode

    def _get_start(self):
        """Return the start position in correct mode."""

        return self._start

    def _get_start_frame(self):
        """Return the start position as frames."""

        if self._mode == gaupol.modes.TIME:
            return self.calc.time_to_frame(self._start)
        if self._mode == gaupol.modes.FRAME:
            return self._start
        raise ValueError

    def _get_start_seconds(self):
        """Return the start position as seconds."""

        time = self._get_start_time()
        return self.calc.time_to_seconds(time)

    def _get_start_time(self):
        """Return the start positions as time."""

        if self._mode == gaupol.modes.TIME:
            return self._start
        if self._mode == gaupol.modes.FRAME:
            return self.calc.frame_to_time(self._start)
        raise ValueError

    def _get_tran_text(self):
        """Return the translation text."""

        return self._tran_text

    def _set_duration(self, value):
        """Set the duration from value."""

        value = self._convert_position(value)
        if self._mode == gaupol.modes.TIME:
            times = (self.start_time, value)
            self._end = self.calc.add_times(*times)
        elif self._mode == gaupol.modes.FRAME:
            self._end = self.start_frame + value

    def _set_end(self, value):
        """Set the end position from value."""

        self._end = self._convert_position(value)

    def _set_framerate(self, value):
        """Set the framerate."""

        self._framerate = value
        self.calc = gaupol.Calculator(value)

    def _set_main_text(self, value):
        """Set the main text."""

        self._main_text = unicode(value)

    def _set_mode(self, mode):
        """Set the current position mode."""

        if mode == gaupol.modes.TIME:
            self._start = self.start_time
            self._end = self.end_time
        elif mode == gaupol.modes.FRAME:
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
        if self._mode == gaupol.modes.TIME:
            self.start = self.start_seconds / coefficient
            self.end = self.end_seconds / coefficient
        elif self._mode == gaupol.modes.FRAME:
            convert = lambda x: int(round(x, 0))
            self.start = convert(coefficient * self.start_frame)
            self.end = convert(coefficient * self.end_frame)

    def copy(self):
        """Return a new subtitle instance with the same values."""

        subtitle = Subtitle(self._mode, self._framerate)
        subtitle._start = self._start
        subtitle._end = self._end
        subtitle._main_text = self._main_text
        subtitle._tran_text = self._tran_text
        # Copy all containers that have been instantiated.
        containers = (x.container for x in gaupol.formats)
        for name in (set(dir(self)) & set(containers)):
            container = copy.deepcopy(getattr(self, name))
            setattr(subtitle, name, container)
        return subtitle

    def get_duration(self, mode):
        """Return the duration in mode."""

        if mode == gaupol.modes.TIME:
            return self.duration_time
        if mode == gaupol.modes.FRAME:
            return self.duration_frame
        raise ValueError

    def get_end(self, mode):
        """Return the end position in mode."""

        if mode == gaupol.modes.TIME:
            return self.end_time
        if mode == gaupol.modes.FRAME:
            return self.end_frame
        raise ValueError

    def get_start(self, mode):
        """Return the start position in mode."""

        if mode == gaupol.modes.TIME:
            return self.start_time
        if mode == gaupol.modes.FRAME:
            return self.start_frame
        raise ValueError

    def get_text(self, doc):
        """Return the text corresponding to document."""

        if doc == gaupol.documents.MAIN:
            return self._main_text
        if doc == gaupol.documents.TRAN:
            return self._tran_text
        raise ValueError

    def has_container(self, name):
        """Return True if container has been instantiated."""

        return name in dir(self)

    def set_text(self, doc, value):
        """Set the text corresponding to document."""

        if doc == gaupol.documents.MAIN:
            return self._set_main_text(value)
        if doc == gaupol.documents.TRAN:
            return self._set_tran_text(value)
        raise ValueError

    def scale_positions(self, value):
        """Multiply start and end positions by value."""

        if self._mode == gaupol.modes.TIME:
            self.start = self._get_start_seconds() * value
            self.end = self._get_end_seconds() * value
        elif self._mode == gaupol.modes.FRAME:
            self.start = int(round(self._start * value, 0))
            self.end = int(round(self._end * value, 0))

    def shift_positions(self, value):
        """Add value to start and end positions."""

        if isinstance(value, basestring):
            start = self.calc.add_times(self.start_time, value)
            end = self.calc.add_times(self.end_time, value)
        elif isinstance(value, int):
            start = self.start_frame + value
            end = self.end_frame + value
        elif isinstance(value, float):
            start = self.start_seconds + value
            end = self.end_seconds + value
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
