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


"""Framerate converter."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.lib.constants import SHOW, HIDE, DURN
from gaupol.lib.delegates.delegate import Delegate


class FramerateConverter(Delegate):
    
    """Framerate converter."""

    def change_framerate(self, framerate):
        """
        Change the framerate and update data.
        
        This method only changes what is assumed to be the video framerate and
        thus affects only how non-native timing data is calculated. Native
        timings will remain unchanged.

        Raise TypeError if main file does not exist.
        """
        if self.main_file is None:
            raise TypeError('Main file does not exist.')
            
        self.framerate         = framerate
        self.tf_conv.framerate = float(framerate)

        conv = self.tf_conv

        if self.main_file.MODE == 'time':

            for i in range(len(self.times)):

                show = conv.time_to_frame(self.times[i][SHOW])
                hide = conv.time_to_frame(self.times[i][HIDE])
                durn = conv.get_frame_duration(show, hide)

                self.frames[i][SHOW] = show
                self.frames[i][HIDE] = hide
                self.frames[i][DURN] = durn

        elif self.main_file.MODE == 'frame':

            for i in range(len(self.times)):

                show = conv.frame_to_time(self.frames[i][SHOW])
                hide = conv.frame_to_time(self.frames[i][HIDE])
                durn = conv.get_time_duration(show, hide)

                self.times[i][SHOW] = show
                self.times[i][HIDE] = hide
                self.times[i][DURN] = durn        
