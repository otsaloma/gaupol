# Copyright (C) 2005-2009 Osmo Salomaa
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


class Calculator(object):

    """
    Time and frame calculator.

    Times are handled as strings, frames as integers and seconds as floats.
    Only one instance of :class:`Calculator` exists for a given framerate.
    """

    _instances = {}

    def __init__(self, framerate=None):
        """Initialize a :class:`Calculator` object."""
        framerate = framerate or aeidon.framerates.FPS_23_976
        self._framerate = framerate.value

    def __new__(cls, framerate=None):
        """Return possibly existing instance for `framerate`."""
        framerate = framerate or aeidon.framerates.FPS_23_976
        if not framerate in cls._instances:
            cls._instances[framerate] = object.__new__(cls)
        return cls._instances[framerate]

    def add_seconds_to_time(self, time, seconds):
        """Add amount of `seconds` to `time`."""
        seconds = self.time_to_seconds(time) + seconds
        return self.seconds_to_time(seconds)

    def add_times(self, x, y):
        """Add time `y` to time `x`."""
        x = self.time_to_seconds(x)
        y = self.time_to_seconds(y)
        return self.seconds_to_time(x + y)

    def compare(self, x, y):
        """Return 1 if `x` is greater, 0 if equal and -1 if `y` greater."""
        if isinstance(x, str):
            return self.compare_times(x, y)
        if isinstance(x, int):
            return cmp(x, y)
        raise ValueError("Invalid type for x: %s" % repr(type(x)))

    def compare_times(self, x, y):
        """Return 1 if `x` is greater, 0 if equal and -1 if `y` greater."""
        negative = (x.startswith("-") and y.startswith("-"))
        return (negative * -2 + 1) * cmp(x, y)

    def frame_to_seconds(self, frame):
        """Convert `frame` to seconds."""
        return frame / self._framerate

    def frame_to_time(self, frame):
        """Convert `frame` to time."""
        seconds = self.frame_to_seconds(frame)
        return self.seconds_to_time(seconds)

    def get_frame_duration(self, x, y):
        """Return duration from frame `x` to frame `y`."""
        return y - x

    def get_middle(self, x, y):
        """
    Return time or frame halfway between `x` and `y`.

        >>> calc = aeidon.Calculator()
        >>> calc.get_middle(33, 77)
        55
        >>> calc.get_middle("00:00:00.123", "00:00:10,456")
        '00:00:05.289'
        """
        if isinstance(x, str):
            x = self.time_to_seconds(x)
            y = self.time_to_seconds(y)
            return self.seconds_to_time((x + y) / 2)
        if isinstance(x, int):
            return int(round((x + y) / 2, 0))
        raise ValueError("Invalid type for x: %s" % repr(type(x)))

    def get_time_duration(self, x, y):
        """Return duration from time `x` to time `y`."""
        x = self.time_to_seconds(x)
        y = self.time_to_seconds(y)
        return self.seconds_to_time(y - x)

    def is_valid_time(self, time):
        """Return ``True`` if `time` is a valid time string."""
        if time.startswith("-"):
            time = time[1:]
        try:
            hours = int(time[:2])
            minutes = int(time[3:5])
            seconds = int(time[6:8])
            mseconds = int(time[9:])
        except ValueError:
            return False
        return (0 <= hours <= 99 and
                0 <= minutes <= 59 and
                0 <= seconds <= 59 and
                0 <= mseconds <= 999)

    def parse_time(self, time):
        """
        Parse syntactically sloppy `time` to valid format.

        >>> calc = aeidon.Calculator()
        >>> calc.parse_time("1:2:3,4")
        '01:02:03.400'
        """
        time = time.strip()
        sign = ("-" if time.startswith("-") else "")
        time = time.replace("-", "")
        time = time.replace(",", ".")
        hours, minutes, seconds = list(map(float, time.split(":")))
        return "%s%02.0f:%02.0f:%02.0f.%03.0f" % (sign,
                                                  hours,
                                                  minutes,
                                                  int(seconds),
                                                  (seconds % 1) * 1000)

    def round_time(self, time, decimals):
        """Round `time` to amount of `decimals` in seconds."""
        seconds = self.time_to_seconds(time)
        seconds = round(seconds, decimals)
        return self.seconds_to_time(seconds)

    def seconds_to_frame(self, seconds):
        """Convert `seconds` to frame."""
        return int(round(seconds * self._framerate, 0))

    def seconds_to_time(self, seconds):
        """Convert `seconds` to time."""
        sign = ("-" if seconds < 0 else "")
        seconds = abs(round(seconds, 3))
        if seconds > 359999.999:
            return "%s99:59:59.999" % sign
        return "%s%02.0f:%02.0f:%02.0f.%03.0f" % (sign, seconds // 3600,
                                                  (seconds % 3600) // 60,
                                                  int(seconds % 60),
                                                  (seconds % 1) * 1000)

    def time_to_frame(self, time):
        """Convert `time` to frame."""
        seconds = self.time_to_seconds(time)
        return self.seconds_to_frame(seconds)

    def time_to_seconds(self, time):
        """Convert `time` to seconds."""
        coefficient = (-1 if time.startswith("-") else 1)
        time = (time[1:] if time.startswith("-") else time)
        return coefficient * sum((float(time[ :2]) * 3600,
                                  float(time[3:5]) * 60,
                                  float(time[6:8]),
                                  float(time[9: ]) / 1000,))

    def to_frame(self, position):
        """Convert `position` to frame."""
        if isinstance(position, str):
            return self.time_to_frame(position)
        if isinstance(position, int):
            return position
        if isinstance(position, float):
            return self.seconds_to_frame(position)
        raise ValueError("Invalid type for position: %s"
                         % repr(type(position)))

    def to_seconds(self, position):
        """Convert `position` to secods."""
        if isinstance(position, str):
            return self.time_to_seconds(position)
        if isinstance(position, int):
            return self.frame_to_seconds(position)
        if isinstance(position, float):
            return position
        raise ValueError("Invalid type for position: %s"
                         % repr(type(position)))

    def to_time(self, position):
        """Convert `position` to time."""
        if isinstance(position, str):
            return position
        if isinstance(position, int):
            return self.frame_to_time(position)
        if isinstance(position, float):
            return self.seconds_to_time(position)
        raise ValueError("Invalid type for position: %s"
                         % repr(type(position)))
