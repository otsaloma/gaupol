# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009,2011-2012 Osmo Salomaa
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

"""Time and frame calculator."""

import aeidon

__all__ = ("Calculator",)


class Calculator(object, metaclass=aeidon.Contractual):

    """
    Time and frame calculator.

    Times are handled as strings, frames as integers and seconds as floats.
    Only one instance of :class:`Calculator` exists for a given framerate.
    """

    _instances = {}

    def __init__(self, framerate=None):
        """
        Initialize a :class:`Calculator` object.

        `framerate` can be either an :attr:`aeidon.framerates` item (preferred
        to be able to reuse instances) or an exact float value.
        """
        if framerate is None:
            framerate = aeidon.framerates.FPS_23_976
        if framerate in aeidon.framerates:
            self._framerate = framerate.value
        else:
            # Use non-constant values as is.
            self._framerate = float(framerate)

    def __new__(cls, framerate=None):
        """
        Return possibly existing instance for `framerate`.

        `framerate` can be either an :attr:`aeidon.framerates` item (preferred
        to be able to reuse instances) or an exact float value.
        """
        if framerate is None:
            framerate = aeidon.framerates.FPS_23_976
        if not framerate in aeidon.framerates:
            # Always return a new instance for float values.
            return object.__new__(cls)
        if not framerate in cls._instances:
            cls._instances[framerate] = object.__new__(cls)
        return cls._instances[framerate]

    def add_ensure(self, value, x, y):
        assert aeidon.is_same_type(value, x)

    def add(self, x, y):
        """Add position `y` to `x`."""
        if aeidon.is_time(x):
            x = self.to_seconds(x)
            y = self.to_seconds(y)
            return self.seconds_to_time(x + y)
        if aeidon.is_frame(x):
            y = self.to_frame(y)
            return x + y
        if aeidon.is_seconds(x):
            y = self.to_seconds(y)
            return x + y
        raise ValueError("Invalid type for x: {}"
                         .format(repr(type(x))))

    def frame_to_seconds_ensure(self, value, frame):
        assert aeidon.is_seconds(value)

    def frame_to_seconds(self, frame):
        """Convert `frame` to seconds."""
        return aeidon.as_seconds(frame / self._framerate)

    def frame_to_time_ensure(self, value, frame):
        assert aeidon.is_time(value)

    def frame_to_time(self, frame):
        """Convert `frame` to time."""
        seconds = self.frame_to_seconds(frame)
        return self.seconds_to_time(seconds)

    def get_middle_ensure(self, value, x, y):
        assert aeidon.is_same_type(value, x)

    def get_middle(self, x, y):
        """
        Return time, frame or seconds halfway between `x` and `y`.

        >>> calc = aeidon.Calculator()
        >>> calc.get_middle(0, 100)
        50
        >>> calc.get_middle("00:00:00.000", "00:00:10.000")
        '00:00:05.000'
        """
        if aeidon.is_time(x):
            x = self.time_to_seconds(x)
            y = self.to_seconds(y)
            return self.seconds_to_time((x+y)/2)
        if aeidon.is_frame(x):
            y = self.to_frame(y)
            return aeidon.as_frame(round((x+y)/2, 0))
        if aeidon.is_seconds(x):
            y = self.to_seconds(y)
            return aeidon.as_seconds(((x+y)/2))
        raise ValueError("Invalid type for x: {}"
                         .format(repr(type(x))))

    def is_earlier(self, x, y):
        """Return ``True`` if `x` is earlier than `y`."""
        if aeidon.is_time(x):
            x = self.time_to_seconds(x)
            return self.is_earlier(x, y)
        if aeidon.is_frame(x):
            y = self.to_frame(y)
            return (x < y)
        if aeidon.is_seconds(x):
            y = self.to_seconds(y)
            return (x < y)
        raise ValueError("Invalid type for x: {}"
                         .format(repr(type(x))))

    def is_later(self, x, y):
        """Return ``True`` if `x` is later than `y`."""
        if aeidon.is_time(x):
            x = self.time_to_seconds(x)
            return self.is_later(x, y)
        if aeidon.is_frame(x):
            y = self.to_frame(y)
            return (x > y)
        if aeidon.is_seconds(x):
            y = self.to_seconds(y)
            return (x > y)
        raise ValueError("Invalid type for x: {}"
                         .format(repr(type(x))))

    def is_valid_time(self, time):
        """Return ``True`` if `time` is a valid time string."""
        if time.startswith("-"):
            time = time[1:]
        try:
            hours    = int(time[ :2])
            minutes  = int(time[3:5])
            seconds  = int(time[6:8])
            mseconds = int(time[9: ])
        except ValueError:
            return False
        return (0 <= hours    <=  99 and
                0 <= minutes  <=  59 and
                0 <= seconds  <=  59 and
                0 <= mseconds <= 999)

    def normalize_time(self, time):
        """
        Convert `time` to valid format.

        >>> calc = aeidon.Calculator()
        >>> calc.normalize_time("1:2:3,4")
        '01:02:03.400'
        """
        time = time.strip()
        sign = ("-" if time.startswith("-") else "")
        time = time.replace("-", "")
        time = time.replace(",", ".")
        hours, minutes, seconds = time.split(":")
        return ("{}{:02.0f}:{:02.0f}:{:02.0f}.{:03.0f}"
                .format(sign,
                        int(hours),
                        int(minutes),
                        int(float(seconds)),
                        (float(seconds) % 1) * 1000))

    def round_ensure(self, value, pos, ndigits):
        assert aeidon.is_same_type(value, pos)

    def round(self, pos, ndigits):
        """
        Round `pos` to given precision in decimal digits.

        `ndigits` may be negative. For frames zero will be used
        if given `ndigits` is greater than zero.
        """
        if aeidon.is_time(pos):
            pos = self.time_to_seconds(pos)
            pos = round(pos, ndigits)
            return self.seconds_to_time(pos)
        if aeidon.is_frame(pos):
            ndigits = min(0, ndigits)
            pos = round(pos, ndigits)
            return aeidon.as_frame(pos)
        if aeidon.is_seconds(pos):
            pos = round(pos, ndigits)
            return aeidon.as_seconds(pos)
        raise ValueError("Invalid type for pos: {}"
                         .format(repr(type(pos))))

    def seconds_to_frame_ensure(self, value, seconds):
        assert aeidon.is_frame(value)

    def seconds_to_frame(self, seconds):
        """Convert `seconds` to frame."""
        return int(round(seconds * self._framerate, 0))

    def seconds_to_time_ensure(self, value, seconds):
        assert aeidon.is_time(value)

    def seconds_to_time(self, seconds):
        """Convert `seconds` to time."""
        sign = ("-" if seconds < 0 else "")
        seconds = abs(round(seconds, 3))
        if seconds > 359999.999:
            return "{}99:59:59.999".format(sign)
        return ("{}{:02.0f}:{:02.0f}:{:02.0f}.{:03.0f}"
                .format(sign,
                        seconds // 3600,
                        (seconds % 3600) // 60,
                        int(seconds % 60),
                        (seconds % 1) * 1000))

    def time_to_frame_require(self, time):
        assert aeidon.is_time(time)

    def time_to_frame_ensure(self, value, time):
        assert aeidon.is_frame(value)

    def time_to_frame(self, time):
        """Convert `time` to frame."""
        seconds = self.time_to_seconds(time)
        return self.seconds_to_frame(seconds)

    def time_to_seconds_require(self, time):
        assert aeidon.is_time(time)

    def time_to_seconds_ensure(self, value, time):
        assert aeidon.is_seconds(value)

    def time_to_seconds(self, time):
        """Convert `time` to seconds."""
        coefficient = (-1 if time.startswith("-") else 1)
        time = (time[1:] if time.startswith("-") else time)
        return coefficient * sum((float(time[ :2]) * 3600,
                                  float(time[3:5]) * 60,
                                  float(time[6:8]),
                                  float(time[9: ]) / 1000))

    def to_frame_ensure(self, value, pos):
        assert aeidon.is_frame(value)

    def to_frame(self, pos):
        """Convert `pos` to frame."""
        if aeidon.is_time(pos):
            return self.time_to_frame(pos)
        if aeidon.is_frame(pos):
            return pos
        if aeidon.is_seconds(pos):
            return self.seconds_to_frame(pos)
        raise ValueError("Invalid type for pos: {}"
                         .format(repr(type(pos))))

    def to_seconds_ensure(self, value, pos):
        assert aeidon.is_seconds(value)

    def to_seconds(self, pos):
        """Convert `pos` to secods."""
        if aeidon.is_time(pos):
            return self.time_to_seconds(pos)
        if aeidon.is_frame(pos):
            return self.frame_to_seconds(pos)
        if aeidon.is_seconds(pos):
            return pos
        raise ValueError("Invalid type for pos: {}"
                         .format(repr(type(pos))))

    def to_time_ensure(self, value, pos):
        assert aeidon.is_time(value)

    def to_time(self, pos):
        """Convert `pos` to time."""
        if aeidon.is_time(pos):
            return pos
        if aeidon.is_frame(pos):
            return self.frame_to_time(pos)
        if aeidon.is_seconds(pos):
            return self.seconds_to_time(pos)
        raise ValueError("Invalid type for pos: {}"
                         .format(repr(type(pos))))
