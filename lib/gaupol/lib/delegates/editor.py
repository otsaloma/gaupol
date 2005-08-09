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

        # Time is the default mode for an unsaved subtitled.
        try:
            mode = self.main_file.MODE
        except AttributeError:
            mode = 'time'

        # Get native timings for comparison.
        if mode == 'time':
            timings = self.times
            start = '00:00:00,000'
        elif mode == 'frame':
            timings = self.frames
            start = 0

        if start_row > 0:
            start = timings[start_row - 1][HIDE]
        
        try:
            end = timings[start_row][SHOW]
        except IndexError:
            if mode == 'time':
                sec = self.tf_conv.time_to_seconds(start)
                sec += (3 * count)
                end = self.tf_conv.seconds_to_time(sec)
            elif mode == 'frame':
                end = start + (80 * count)

        for i in range(count):
            self.times.insert(start_row, ['00:00:00,000'] * 3)
            self.frames.insert(start_row, [0] * 3)
            self.texts.insert(start_row, [''] * 2)

        for i in range(start_row, start_row + count):
            if mode == 'time':
                start_sec = self.tf_conv.time_to_seconds(start)
                end_sec   = self.tf_conv.time_to_seconds(end)
                dur_sec = (end_sec - start_sec) / count
                pos = i - start_row
                start_time = self.tf_conv.seconds_to_time(start_sec + (pos * dur_sec))
                end_time = self.tf_conv.seconds_to_time(start_sec + (pos * dur_sec) + dur_sec)
                self.times[i][SHOW] = start_time
                self.times[i][HIDE] = end_time
                self.frames[i][SHOW] = self.tf_conv.time_to_frame(start_time)
                self.frames[i][HIDE] = self.tf_conv.time_to_frame(end_time)
                self._set_durations(i)
            elif mode == 'frame':
                dur = int((end - start) / count)
                pos = i - start_row
                start_frame = start + (pos * dur)
                end_frame = start + (pos * dur) + dur
                self.frames[i][SHOW] = start_frame
                self.frames[i][HIDE] = end_frame
                self.times[i][SHOW] = self.tf_conv.frame_to_time(start_frame)
                self.times[i][HIDE] = self.tf_conv.frame_to_time(end_frame)
                self._set_durations(i)

        

    def remove_subtitles(self, rows):
        """Remove subtitles."""

        rows.sort()
        rows.reverse()
        
        for row in rows:
            self.texts.pop(row)
            self.times.pop(row)
            self.frames.pop(row)

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
