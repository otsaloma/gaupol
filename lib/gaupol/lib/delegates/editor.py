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


"""Data value editor."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.lib.constants import SHOW, HIDE, DURN, ORIG, TRAN
from gaupol.lib.delegates.delegate import Delegate


class Editor(Delegate):
    
    """Data value editor."""

    def clear_text(self, row, col):
        """Clear text to blank."""
        
        self.set_text(row, col, u'')

    def insert_subtitles(self, start_row, count):
        """Insert count amount of blank subtitles staring at start_row."""

        pass

    def remove_subtitles(self, rows):
        """Remove subtitles."""

        pass

    def _set_durations(self, row):
        """Set duration for row based on show and hide."""

        show = self.times[row][SHOW]
        hide = self.times[row][HIDE]
        self.times[row][DURN] = self.tf_conv.get_time_duration(show, hide)

        show = self.frames[row][SHOW]
        hide = self.frames[row][HIDE]
        self.frames[row][DURN] = self.tf_conv.get_frame_duration(show, hide)

    def set_frame(self, row, col, value):
        """
        Set value of frame.
        
        Return: new index of row
        """
        self.frames[row][col] = value
    
        if col in [SHOW, HIDE]:
            self.times[row][col] = self.tf_conv.frame_to_time(value)
            self._set_durations(row)
            
        elif col == DURN:
            self.times[row][col] = self.tf_conv.frame_to_time(value)
            self._set_hidings(row)

        if col == SHOW:
            return self._sort_data(row)

        return row

    def _set_hidings(self, row):
        """Set hides for row based on shows and durations."""
        
        show = self.times[row][SHOW]
        durn = self.times[row][DURN]
        self.times[row][HIDE] = self.tf_conv.add_times(show, durn)

        show = self.frames[row][SHOW]
        durn = self.frames[row][DURN]
        self.frames[row][HIDE] = show + durn

    def set_text(self, row, col, value):
        """Set text."""

        self.texts[row][col] = value

    def set_time(self, row, col, value):
        """
        Set time.

        Return: new index of row
        """
        self.times[row][col] = value
    
        if col in [SHOW, HIDE]:
            self.frames[row][col] = self.tf_conv.time_to_frame(value)
            self._set_durations(row)
            
        elif col == DURN:
            self.frames[row][col] = self.tf_conv.time_to_frame(value)
            self._set_hidings(row)

        if col == SHOW:
            return self._sort_data(row)

        return row

    def _sort_data(self, row):
        """
        Sort data after show value in row has changed.
        
        Return: new index of row
        """
        # Time is the default mode for an unsaved subtitled.
        try:
            mode = self.main_file.MODE
        except AttributeError:
            mode = 'time'

        # Get native timings for comparison.
        if mode == 'time':
            timings = self.times
        elif mode == 'frame':
            timings = self.frames

        direction = None
        length = len(timings)
        
        # Get direction to move to.
        if row < length - 1 and timings[row][SHOW] > timings[row + 1][SHOW]:
            direction = 'later'
        elif row > 0 and timings[row][SHOW] < timings[row - 1][SHOW]:
            direction = 'earlier'

        if direction is None:
            return row

        # Get new row, where to move row to.
        new_row = row

        if direction == 'later':
            for i in range(row + 1, length):
                if timings[row][SHOW] > timings[i][SHOW]:
                    new_row = i + 1
                else:
                    break
            remove_row = row
            result_row = new_row - 1

        if direction == 'earlier':
            for i in reversed(range(row)):
                if timings[row][SHOW] < timings[i][SHOW]:
                    new_row = i
                else:
                    break
            remove_row = row + 1
            result_row = new_row

        # Move row in data.
        for data in [self.times, self.frames, self.texts]:
            data.insert(new_row, data[row])
            data.pop(remove_row)

        return result_row
