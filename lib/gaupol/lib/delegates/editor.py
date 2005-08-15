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


"""Editing of data values."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.constants import MODE
from gaupol.lib.constants import *
from gaupol.lib.delegates.delegate import Delegate


class Editor(Delegate):
    
    """Editing of data values."""

    def clear_text(self, row, col):
        """Clear text to blank."""
        
        self.set_text(row, col, u'')

    def get_mode(self):
        """
        Get main file's mode.
        
        If main file does not exist return time mode (because of its greater
        accuracy).
        """
        try:
            return self.main_file.MODE
        except AttributeError:
            return MODE.TIME

    def get_timings(self):
        """Return self.times or self.frames depending on main file's mode."""
        
        mode = self.get_mode()
        
        if mode == MODE.TIME:
            return self.times
        elif mode == MODE.FRAME:
            return self.frames

    def insert_subtitles(self, start_row, amount):
        """Insert blank subtitles starting at start_row."""

        OPTIMAL_SECOND_DURATION = 3
        OPTIMAL_FRAME_DURATION  = 80

        calc   = self.calc
        times  = self.times
        frames = self.frames
        texts  = self.texts

        mode    = self.get_mode()
        timings = self.get_timings()

        # Get time window start edge.
        if start_row > 0:
            start = timings[start_row - 1][HIDE]
        else:
            if mode == MODE.TIME:
                start = '00:00:00,000'
            elif mode == MODE.FRAME:
                start = 0

        # Get time window end edge.
        try:
            end = timings[start_row][SHOW]
        except IndexError:
            if mode == MODE.TIME:
                end = calc.time_to_seconds(start)
                end += (OPTIMAL_SECOND_DURATION * amount)
                end = calc.seconds_to_time(end)
            elif mode == MODE.FRAME:
                end = start + (OPTIMAL_FRAME_DURATION * amount)

        # Insert new subtitles with sensible timings.
        if mode == MODE.TIME:
        
            start    = calc.time_to_seconds(start)
            end      = calc.time_to_seconds(end)
            duration = (end - start) / amount
            
            for i in range(amount):

                show_time = calc.seconds_to_time(start + ( i      * duration))
                hide_time = calc.seconds_to_time(start + ((i + 1) * duration))
                durn_time = calc.get_time_duration(show_time, hide_time)

                show_frame = calc.time_to_frame(show_time)
                hide_frame = calc.time_to_frame(hide_time)
                durn_frame = conv.get_frame_duration(show_frame, hide_frame)

                row = start_row + i

                times.insert( row, [show_time , hide_time , durn_time ])
                frames.insert(row, [show_frame, hide_frame, durn_frame])
                texts.insert( row, [text, u''])
            
        elif mode == MODE.FRAME:

            duration = int(round((end - start) / amount, 0))
            
            for i in range(amount):

                show_frame = start + ( i      * duration)
                hide_frame = start + ((i + 1) * duration)
                durn_frame = calc.get_frame_duration(show_frame, hide_frame)

                show_time = calc.frame_to_time(show_frame)
                hide_time = calc.frame_to_time(hide_frame)
                durn_time = conv.get_time_duration(show_time, hide_time)

                row = start_row + i

                times.insert( row, [show_time , hide_time , durn_time ])
                frames.insert(row, [show_frame, hide_frame, durn_frame])
                texts.insert( row, [text, u''])

    def remove_subtitles(self, rows):
        """Remove subtitles."""

        rows.sort()
        rows.reverse()
        
        for row in rows:
            for entry in [self.times, self.frames, self.texts]
                entry.pop(row)

    def _set_durations(self, row):
        """Set durations for row based on shows and hides."""

        show = self.times[row][SHOW]
        hide = self.times[row][HIDE]
        self.times[row][DURN] = self.calc.get_time_duration(show, hide)

        show = self.frames[row][SHOW]
        hide = self.frames[row][HIDE]
        self.frames[row][DURN] = self.calc.get_frame_duration(show, hide)

    def set_frame(self, row, col, value):
        """
        Set value of frame.
        
        Return: new index of row
        """
        self.frames[row][col] = value
        self.times[row][col]  = self.calc.frame_to_time(value)

        # Calculate affected data.
        if col in [SHOW, HIDE]:
            self._set_durations(row)
        elif col == DURN:
            self._set_hidings(row)

        # Resort if show frame drastically changed.
        if col == SHOW:
            return self._sort_data(row)

        return row

    def _set_hidings(self, row):
        """Set hides for row based on shows and durations."""
        
        show = self.times[row][SHOW]
        durn = self.times[row][DURN]
        self.times[row][HIDE] = self.calc.add_times(show, durn)

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
        self.times[row][col]  = value
        self.frames[row][col] = self.calc.time_to_frame(value)

        # Calculate affected data.
        if col in [SHOW, HIDE]:
            self._set_durations(row)
        elif col == DURN:
            self._set_hidings(row)

        # Resort if show frame drastically changed.
        if col == SHOW:
            return self._sort_data(row)

        return row

    def _sort_data(self, row):
        """
        Sort data after show value in row has changed.
        
        Return: new index of row
        """
        timings = self.get_timings()
        length = len(timings)
        direction = None

        EARLIER, LATER = 0, 1

        # Get direction to move to.
        if   row > 0          and timings[row][SHOW] < timings[row - 1][SHOW]:
            direction = EARLIER
        elif row < length - 1 and timings[row][SHOW] > timings[row + 1][SHOW]:
            direction = LATER

        if direction is None:
            return row

        # New row, where to move row to.
        new_row = row

        if direction == EARLIER:

            # Get new row.
            for i in reversed(range(row)):
                if timings[row][SHOW] < timings[i][SHOW]:
                    new_row = i
                else:
                    break

            # Move rows.
            for entry in [self.times, self.frames, self.texts]:
                data = entry.pop(row)
                entry.insert(new_row, data)

            return new_row

        if direction == LATER:

            # Get new row.
            for i in range(row + 1, length):
                if timings[row][SHOW] > timings[i][SHOW]:
                    new_row = i + 1
                else:
                    break

            # Move rows.
            for entry in [self.times, self.frames, self.texts]:
                entry.insert(new_row, entry[row])
                entry.pop(row)
                
            return new_row - 1
