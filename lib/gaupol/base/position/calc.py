# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Time and frame calculations."""


from gaupol.base.cons import Framerate


class TimeFrameCalculator(object):

    """
    Time and frame calculations.

    time: string in format hh:mm:ss,sss
    frame: integer
    seconds: float
    framerate: float
    """

    def __init__(self, framerate=None):

        if framerate is not None:
            self.set_framerate(framerate)

    def add_seconds_to_time(self, time, seconds):
        """Add amount of seconds to time."""

        seconds = max(0, self.time_to_seconds(time) + seconds)
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
        """
        Get duration from frame x to frame y.

        For negative durations, return zero (0).
        """
        return max(0, y - x)

    def get_time_duration(self, x, y):
        """
        Get duration from time x to time y.

        For negative durations, return zero (00:00:00,000).
        """
        x = self.time_to_seconds(x)
        y = self.time_to_seconds(y)

        if x > y:
            return '00:00:00,000'
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
        """
        Convert seconds to time.

        Do not return a time greater that 99:59:59,999.
        """
        seconds = round(seconds, 3)
        if seconds > 359999.999:
            return '99:59:59,999'

        return '%02.0f:%02.0f:%02.0f,%03.0f' % (
            seconds // 3600,
            (seconds % 3600) // 60,
            int(seconds % 60),
            (seconds % 1) * 1000
        )

    def set_framerate(self, framerate):
        """Set framerate."""

        self.framerate = Framerate.VALUES[framerate]

    def time_to_frame(self, time):
        """Convert time to frame."""

        seconds = self.time_to_seconds(time)
        return self.seconds_to_frame(seconds)

    def time_to_seconds(self, time):
        """Convert time to seconds."""

        return sum((
            float(time[ :2]) * 3600,
            float(time[3:5]) *   60,
            float(time[6:8])       ,
            float(time[9: ]) / 1000,
        ))
