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


"""Subtitle file reader."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.lib.constants import SHOW, HIDE, DURN, ORIG, TRAN
from gaupol.lib.delegates.delegate import Delegate
from gaupol.lib.formats.all import *
from gaupol.lib.formats.determiner import FileFormatDeterminer
from gaupol.lib.time.timeframe import TimeFrameConverter


class FileReader(Delegate):
    
    """Subtitle file reader."""
    
    def read_main_file(self, path=None, encoding=None):
        """
        Read times/frames and texts from main file.
        
        path and encoding can be omitted if reading an existing main file.
        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise UnknownFileFormatError if unable to detect file format.
        """
        path     = path     or self.main_file.path
        encoding = encoding or self.main_file.encoding
        
        determiner = FileFormatDeterminer(path, encoding)
        format = determiner.determine_file_format()

        main_file = eval(format)(path, encoding)
        shows, hides, texts = main_file.read()
        shows, hides, texts = self._sort_data(shows, hides, texts)

        # After successful reading, instance variables can be set.
        self.main_file = main_file

        # Blank possible existing data.
        self.times  = []
        self.frames = []
        self.texts  = []

        conv = self.tf_conv

        if self.main_file.MODE == 'time':
            
            for i in range(len(shows)):

                show_time = shows[i]
                hide_time = hides[i]
                text = texts[i]
                
                durn_time  = conv.get_time_duration(show_time, hide_time)
                show_frame = conv.time_to_frame(show_time)
                hide_frame = conv.time_to_frame(hide_time)
                durn_frame = conv.get_frame_duration(show_frame, hide_frame)
                            
                self.times.append([show_time, hide_time, durn_time])
                self.frames.append([show_frame, hide_frame, durn_frame])
                self.texts.append([text, u''])

        elif self.main_file.MODE == 'frame':
            
            for i in range(len(shows)):

                show_frame = shows[i]
                hide_frame = hides[i]
                text = texts[i]

                durn_frame = conv.get_frame_duration(show_frame, hide_frame)
                show_time  = conv.frame_to_time(show_frame)
                hide_time  = conv.frame_to_time(hide_frame)
                durn_time  = conv.get_time_duration(show_time, hide_time)

                self.times.append([show_time, hide_time, durn_time])
                self.frames.append([show_frame, hide_frame, durn_frame])
                self.texts.append([text, u''])

    def read_translation_file(self, path, encoding):
        """
        Read texts from translation file.
        
        Main file should always exist before reading translations.
        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise UnknownFileFormatError if unable to detect file format.
        """
        determiner = FileFormatDeterminer(path, encoding)
        format = determiner.determine_file_format()

        tran_file = eval(format)(path, encoding)
        shows, hides, trans = tran_file.read()
        shows, hides, trans = self._sort_data(shows, hides, trans)
        
        # After successful reading, instance variables can be set.
        self.tran_file = tran_file

        # Blank possible existing translations.
        for i in range(len(self.texts)):
            self.texts[i][TRAN] = u''

        # Get time and frame values to be appended if translation file is
        # longer than main file.

        if self.times:
            final_time = self.times[-1][HIDE]
        else:
            final_time = u'00:00:00,000'
            
        if self.frames:
            final_frame = self.frames[-1][HIDE]
        else:
            final_frame = 0

        texts_length = len(self.texts)

        for i in range(len(trans)):
            if texts_length > i:
                self.texts[i][TRAN] = trans[i]
            else:
                self.times.append([final_time] * 2 + [u'00:00:00,000'])
                self.frames.append([final_frame] * 2 + [0])
                self.texts.append([u'', trans[i]])

    def _sort_data(self, shows, hides, texts):
        """
        Sort data based on show times/frames.

        Return: shows, hides, texts
        """
        data = [[shows[i], hides[i], texts[i]] for i in range(len(shows))]
        data.sort(lambda x, y: cmp(x[0], y[0]))

        shows = []
        hides = []
        texts = []
        
        for i in range(len(data)):
            shows.append(data[i][0])
            hides.append(data[i][1])
            texts.append(data[i][2])

        return shows, hides, texts
