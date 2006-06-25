# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Opening subtitle files."""


from gaupol.base                 import cons
from gaupol.base.icons           import *
from gaupol.base.delegate        import Delegate
from gaupol.base.file.classes    import *
from gaupol.base.file.determiner import FileFormatDeterminer


class FileOpenDelegate(Delegate):

    """Opening subtitle files."""

    def _sort_data(self, shows, hides, texts):
        """
        Sort data based on show times/frames.

        Return shows, hides, texts, resorts.
        """
        class Count(object):
            resorts = 0

        def sort(x, y):
            value = cmp(x[0], y[0])
            if value == -1:
                Count.resorts += 1
            return value

        data = list([shows[i], hides[i], texts[i]] for i in range(len(shows)))
        data.sort(sort)
        shows = list(x[0] for x in data)
        hides = list(x[1] for x in data)
        texts = list(x[2] for x in data)

        return shows, hides, texts, Count.resorts

    def open_main_file(self, path, encoding):
        """
        Open main file reading times/frames and texts.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FileFormatError if unable to detect file format.
        Return amount of resort operations done.
        """
        format = FileFormatDeterminer(path, encoding).determine()
        main_file = eval(cons.Format.class_names[format])(path, encoding)
        shows, hides, texts, resorts = self._sort_data(*main_file.read())
        self.main_file = main_file

        self.times      = []
        self.frames     = []
        self.main_texts = []
        self.tran_texts = []

        for i in range(len(shows)):
            time, frame = self.expand_positions(shows[i], hides[i])
            self.times.append(time)
            self.frames.append(frame)
            self.main_texts.append(texts[i])
            self.tran_texts.append(u'')

        if self.main_file.format == cons.Format.MPSUB:
            if self.main_file.framerate is not None:
                self.set_framerate(self.main_file.framerate, register=None)

        self.main_changed = 0
        self.tran_changed = 0
        return resorts

    def open_translation_file(self, path, encoding):
        """
        Open translation file reading texts.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FileFormatError if unable to detect file format.
        """
        format = FileFormatDeterminer(path, encoding).determine()
        tran_file = eval(cons.Format.class_names[format])(path, encoding)
        texts, resorts = self._sort_data(*tran_file.read())[2:]
        self.tran_file = tran_file

        self.tran_texts = [u''] * len(self.tran_texts)
        excess = len(texts) - len(self.main_texts)
        if excess > 0:
            rows = range(len(self.times), len(self.times) + excess)
            self.insert_subtitles(rows, register=None)
        self.tran_texts[:len(texts)] = texts

        self.tran_active = True
        self.tran_changed = 0
        return resorts
