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


"""Conversions between times and frames."""


from math import floor
import re

try:
    from psyco.classes import *
except ImportError:
    pass


RE_TIME = re.compile(r'^(\d\d):(\d\d):(\d\d),(\d\d\d)$')


class TimeFrameConverter(object):
    
    """
    Conversions between times and frames.

    time: string in format hh:mm:ss,sss
    frame: integer
    seconds: float
    framerate: float
    """
    
    def __init__(self, framerate):
        """
        Initialize a TimeFrameConverter object.
        
        framerate can be given as any data type convertable to float.
        """
        self.framerate = float(framerate)

    def frame_to_seconds(self, frame):
        """Convert frame to seconds."""
        
        return frame / self.framerate
        
    def frame_to_time(self, frame):
        """Convert frame to time."""

        seconds = self.frame_to_seconds(frame)
        
        return self.seconds_to_time(seconds)

    def get_frame_duration(self, show_frame, hide_frame):
        """
        Get duration from show_frame to hide_frame.

        For negative durations, return zero (0).
        """
        duration = hide_frame - show_frame

        return max(duration, 0)

    def get_time_duration(self, show_time, hide_time):
        """
        Get duration from show_time to hide_time.

        For negative durations, return zero (00:00:00,000).
        """
        
        show_sec = self.time_to_seconds(show_time)
        hide_sec = self.time_to_seconds(hide_time)
        
        durn_sec = hide_sec - show_sec

        if durn_sec > 0:    
            return self.seconds_to_time(durn_sec)
        else:
            return u'00:00:00,000'

    def seconds_to_frame(self, seconds):
        """Convert seconds to frame."""

        return int(round(seconds * self.framerate, 0))

    def seconds_to_time(self, seconds):
        """Convert seconds to time."""

        seconds_left = round(seconds, 3)
        
        hours = floor(seconds_left / 3600)
        seconds_left -= hours * 3600
        
        minutes = floor(seconds_left / 60)
        seconds_left -= minutes * 60
        
        seconds = floor(seconds_left)
        seconds_left -= seconds

        milliseconds = seconds_left * 1000

        return u'%02.0f:%02.0f:%02.0f,%03.0f' \
               % (hours, minutes, seconds, milliseconds)

    def time_to_frame(self, time):
        """Convert time to frame."""

        seconds = self.time_to_seconds(time)
        
        return self.seconds_to_frame(seconds)
        
    def time_to_seconds(self, time):
        """
        Convert time to seconds.

        Raise ValueError if time is not a valid time.
        """
        match = RE_TIME.match(time)

        if match is not None:
        
            hours        = float(match.group(1))
            minutes      = float(match.group(2))
            seconds      = float(match.group(3))
            milliseconds = float(match.group(4))
            
            return (hours * 3600) + (minutes * 60) + seconds \
                   + (milliseconds / 1000)

        raise ValueError('Invalid time: "%s".' % time)
