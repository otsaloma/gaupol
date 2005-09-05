# Copyright (C) 2005 Osmo Salomaa
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


import floor

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.constants import FRAMERATE


class TimeFrameCalculator(object):
    
    """
    Time and frame calculations.

    time     : string in format hh:mm:ss,sss
    frame    : integer
    seconds  : float
    framerate: float
    """
    
    def __init__(self, framerate):

        self.framerate = FRAMERATE.VALUES[framerate]

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
        return max(y - x, 0)

    def get_time_duration(self, x, y):
        """
        Get duration from time x to time y.

        For negative durations, return zero (00:00:00,000).
        """
        
        x = self.time_to_seconds(x)
        y = self.time_to_seconds(y)
        
        duration = y - x

        if duration > 0:
            return self.seconds_to_time(duration)
        else:
            return '00:00:00,000'

    def seconds_to_frame(self, seconds):
        """Convert seconds to frame."""

        return int(round(seconds * self.framerate, 0))

    def seconds_to_time(self, seconds):
        """
        Convert seconds to time.
        
        Do not return a time greater that 99:59:59,999.
        """
        seconds_left = round(seconds, 3)
        
        hours = math.floor(seconds_left / 3600)
        seconds_left -= hours * 3600

        if hours > 99:
            return '99:59:59,999'
        
        minutes = math.floor(seconds_left / 60)
        seconds_left -= minutes * 60
        
        seconds = math.floor(seconds_left)
        seconds_left -= seconds

        milliseconds = seconds_left * 1000

        return '%02.0f:%02.0f:%02.0f,%03.0f' \
               % (hours, minutes, seconds, milliseconds)

    def time_to_frame(self, time):
        """Convert time to frame."""

        seconds = self.time_to_seconds(time)
        
        return self.seconds_to_frame(seconds)
        
    def time_to_seconds(self, time):
        """Convert time to seconds."""
        
        hours        = float(time[ :2])
        minutes      = float(time[3:5])
        seconds      = float(time[6:8])
        milliseconds = float(time[9: ])
            
        return (hours * 3600) + (minutes * 60) + seconds \
               + (milliseconds / 1000)
