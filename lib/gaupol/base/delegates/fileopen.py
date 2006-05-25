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


"""Opening subtitle files."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.base.cons import SHOW, HIDE, DURN
from gaupol.base.delegates        import Delegate
from gaupol.base.file.classes    import *
from gaupol.base.file.determiner import FileFormatDeterminer
from gaupol.base.cons             import Format, Mode


class FileOpenDelegate(Delegate):

    """Opening subtitle files."""

    def open_main_file(self, path, encoding):
        """
        Open a main file reading times/frames and texts.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FileFormatError if unable to detect file format.
        """
        # Get format.
        determiner = FileFormatDeterminer(path, encoding)
        format = determiner.determine_file_format()

        # Read file.
        main_file = eval(Format.class_names[format])(path, encoding)
        shows, hides, texts = self._sort_data(*main_file.read())

        # After successful reading, instance variable can be set.
        self.main_file = main_file

        # Blank possible existing data.
        self.times      = []
        self.frames     = []
        self.main_texts = []
        self.tran_texts = []

        times      = self.times
        frames     = self.frames
        main_texts = self.main_texts
        tran_texts = self.tran_texts
        calc       = self.calc

        if self.main_file.mode == Mode.TIME:
            for i in range(len(shows)):

                show_time = shows[i]
                hide_time = hides[i]
                durn_time = calc.get_time_duration(show_time, hide_time)
                times.append([show_time, hide_time, durn_time])

                show_frame = calc.time_to_frame(show_time)
                hide_frame = calc.time_to_frame(hide_time)
                durn_frame = calc.get_frame_duration(show_frame, hide_frame)
                frames.append([show_frame, hide_frame, durn_frame])

        elif self.main_file.mode == Mode.FRAME:
            for i in range(len(shows)):

                show_frame = shows[i]
                hide_frame = hides[i]
                durn_frame = calc.get_frame_duration(show_frame, hide_frame)
                frames.append([show_frame, hide_frame, durn_frame])

                show_time = calc.frame_to_time(show_frame)
                hide_time = calc.frame_to_time(hide_frame)
                durn_time = calc.get_time_duration(show_time, hide_time)
                times.append([show_time, hide_time, durn_time])

        for text in texts:
            main_texts.append(text)
            tran_texts.append(u'')

        self.main_changed = 0
        self.tran_changed = 0

    def open_translation_file(self, path, encoding):
        """
        Open a translation file reading texts.

        Main file should always exist before reading translation file.
        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FileFormatError if unable to detect file format.
        """
        assert self.main_file is not None

        # Get format
        determiner = FileFormatDeterminer(path, encoding)
        format = determiner.determine_file_format()

        # Read file.
        tran_file = eval(Format.class_names[format])(path, encoding)
        shows, hides, texts = self._sort_data(*tran_file.read())

        # After successful reading, instance variable can be set.
        self.tran_file = tran_file

        tran_texts = self.tran_texts

        # Blank possible existing translations.
        for i in range(len(self.main_texts)):
            tran_texts[i] = u''

        # If translation file is longer than main file,
        # new subtitles need to be added.
        difference = len(texts) - len(self.times)
        if difference > 0:
            rows = range(len(self.times), len(self.times) + difference)
            self.insert_subtitles(rows, register=None)

        tran_texts[:len(texts)] = texts

        self.tran_active  = True
        self.tran_changed = 0

    def _sort_data(self, shows, hides, texts):
        """
        Sort data based on show times/frames.

        Return shows, hides, texts.
        """
        def sort(x, y):
            return cmp(x[0], y[0])

        data = []
        for i in range(len(shows)):
            data.append([shows[i], hides[i], texts[i]])
        data.sort(sort)

        shows = list(entry[0] for entry in data)
        hides = list(entry[1] for entry in data)
        texts = list(entry[2] for entry in data)

        return shows, hides, texts


if __name__ == '__main__':

    from gaupol.test import Test

    class TestFileOpenDelegate(Test):

        def __init__(self):

            Test.__init__(self)
            self.project = self.get_project()
            self.delegate = FileOpenDelegate(self.project)

        def test_open_main_file(self):

            path = self.get_subrip_path()
            self.project.open_main_file(path, 'utf_8')
            assert bool(self.project.times)
            assert bool(self.project.frames)
            assert bool(self.project.main_texts)
            assert bool(self.project.tran_texts)

        def test_open_translation_file(self):

            self.project.remove_subtitles([1, 2])
            path = self.get_micro_dvd_path()
            self.project.open_translation_file(path, 'utf_8')
            assert bool(self.project.tran_texts[0])

        def test_sort_data(self):

            shows = [ 2 ,  3 ,  1 ]
            hides = [ 3 ,  4 ,  2 ]
            texts = ['2', '3', '1']
            shows, hides, texts = self.delegate._sort_data(shows, hides, texts)
            assert shows == [ 1 ,  2 ,  3 ]
            assert hides == [ 2 ,  3 ,  4 ]
            assert texts == ['1', '2', '3']

            shows = ['00:00:00,300', '00:00:00,200', '00:00:00,100']
            hides = ['00:00:00,400', '00:00:00,300', '00:00:00,200']
            texts = ['00:00:00,300', '00:00:00,200', '00:00:00,100']
            shows, hides, texts = self.delegate._sort_data(shows, hides, texts)
            assert shows == ['00:00:00,100', '00:00:00,200', '00:00:00,300']
            assert hides == ['00:00:00,200', '00:00:00,300', '00:00:00,400']
            assert texts == ['00:00:00,100', '00:00:00,200', '00:00:00,300']

    TestFileOpenDelegate().run()
