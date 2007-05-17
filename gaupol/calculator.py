# Copyright (C) 2005-2007 Osmo Salomaa
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


"""Time and frame calculator."""


from __future__ import division

from gaupol import const


class Calculator(object):

    """Time and frame calculator.

    Instance variables:

        framerate: Video framerate as float

    Times are handled as strings, frames as integers and seconds as floats.
    Only one instance of Calculator exists for a given framerate.
    """

    _instances = {}

    def __init__(self, framerate=const.FRAMERATE.P24):

        self.framerate = framerate.value

    def __new__(cls, framerate=const.FRAMERATE.P24):

        if not framerate in cls._instances:
            cls._instances[framerate] = object.__new__(cls)
        return cls._instances[framerate]

    def add_seconds_to_time(self, time, seconds):
        """Add amount of seconds to time."""

        seconds = self.time_to_seconds(time) + seconds
        return self.seconds_to_time(seconds)

    def add_times(self, x, y):
        """Add time y to time x."""

        x = self.time_to_seconds(x)
        y = self.time_to_seconds(y)
        return self.seconds_to_time(x + y)

    def frame_to_seconds(self, frame):
        """Convert frame to seconds."""

        return frame / self.framerate

    def frame_to_time(self, frame):
        """Convert frame to time."""

        seconds = self.frame_to_seconds(frame)
        return self.seconds_to_time(seconds)

    def get_frame_duration(self, x, y):
        """Get duration from frame x to frame y."""

        return y - x

    def get_middle(self, x, y):
        """Get time or frame halfway between x and y."""

        if isinstance(x, basestring):
            x = self.time_to_seconds(x)
            y = self.time_to_seconds(y)
            return self.seconds_to_time((x + y) / 2)
        if isinstance(x, int):
            return int(round((x + y) / 2, 0))

    def get_time_duration(self, x, y):
        """Get duration from time x to time y."""

        x = self.time_to_seconds(x)
        y = self.time_to_seconds(y)
        return self.seconds_to_time(y - x)

    def round_time(self, time, decimals):
        """Round time to amount of decimals in seconds."""

        seconds = self.time_to_seconds(time)
        seconds = round(seconds, decimals)
        return self.seconds_to_time(seconds)

    def seconds_to_frame(self, seconds):
        """Convert seconds to frame."""

        return int(round(seconds * self.framerate, 0))

    def seconds_to_time(self, seconds):
        """Convert seconds to time."""

        sign = ("-" if seconds < 0 else "")
        seconds = abs(round(seconds, 3))
        if seconds > 359999.999:
            return "%s99:59:59.999" % sign

        return "%s%02.0f:%02.0f:%02.0f.%03.0f" % (
            sign, seconds // 3600,
            (seconds % 3600) // 60,
            int(seconds % 60),
            (seconds % 1) * 1000)

    def time_to_frame(self, time):
        """Convert time to frame."""

        seconds = self.time_to_seconds(time)
        return self.seconds_to_frame(seconds)

    def time_to_seconds(self, time):
        """Convert time to seconds."""

        coefficient = 1
        if time.startswith("-"):
            coefficient = -1
            time = time[1:]

        return coefficient * sum((
            float(time[ :2]) * 3600,
            float(time[3:5]) *   60,
            float(time[6:8])       ,
            float(time[9: ]) / 1000,))
