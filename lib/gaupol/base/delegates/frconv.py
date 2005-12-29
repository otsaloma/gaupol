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


"""Framerate conversions."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.base.colconstants import *
from gaupol.base.delegates    import Delegate
from gaupol.constants         import Framerate, Mode


class FramerateConverter(Delegate):

    """Framerate conversions."""

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

        self.framerate = framerate
        self.calc.set_framerate(framerate)

        calc   = self.calc
        times  = self.times
        frames = self.frames

        if self.main_file.mode == Mode.TIME:
            for i in range(len(times)):

                show = calc.time_to_frame(times[i][SHOW])
                hide = calc.time_to_frame(times[i][HIDE])
                durn = calc.get_frame_duration(show, hide)

                frames[i][SHOW] = show
                frames[i][HIDE] = hide
                frames[i][DURN] = durn

        elif self.main_file.mode == Mode.FRAME:
            for i in range(len(times)):

                show = calc.frame_to_time(frames[i][SHOW])
                hide = calc.frame_to_time(frames[i][HIDE])
                durn = calc.get_time_duration(show, hide)

                times[i][SHOW] = show
                times[i][HIDE] = hide
                times[i][DURN] = durn
