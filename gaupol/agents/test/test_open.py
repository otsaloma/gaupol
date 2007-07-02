# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.


import gaupol
from gaupol import unittest


class TestOpenAgent(unittest.TestCase):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = self.project.open_main.im_self

    def test_open_main_file(self):

        for format in gaupol.FORMAT.members:
            path = self.get_file_path(format)
            self.project.remove_subtitles([0])
            self.project.open_main(path, "ascii")
            assert self.project.subtitles

    def test_open_translation_file__smart(self):

        for format in gaupol.FORMAT.members:
            path = self.get_file_path(format)
            self.project.remove_subtitles([0])
            self.project.open_translation(path, "ascii", True)

    def test_open_translation_file__stupid(self):

        for format in gaupol.FORMAT.members:
            path = self.get_file_path(format)
            self.project.remove_subtitles([0])
            self.project.open_translation(path, "ascii", False)
