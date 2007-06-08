# Copyright (C) 2005-2007 Osmo Salomaa
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


import gaupol
from gaupol import unittest


class TestSaveAgent(unittest.TestCase):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = self.project.save_main.im_self

    def test__copy_file(self):

        source = self.get_subrip_path()
        destination = self.get_subrip_path()
        self.delegate._copy_file(source, destination)

    def test__move_file(self):

        source = self.get_subrip_path()
        destination = self.get_subrip_path()
        self.delegate._move_file(source, destination)

    def test__remove_file(self):

        path = self.get_subrip_path()
        self.delegate._remove_file(path)

    def test_save(self):

        self.project.save(gaupol.DOCUMENT.MAIN, ())
        self.project.save(gaupol.DOCUMENT.TRAN, ())

    def test_save_main(self):

        path = self.project.main_file.path
        unix = gaupol.NEWLINE.UNIX
        for format in gaupol.FORMAT.members:
            self.project.clear_texts([0], gaupol.DOCUMENT.MAIN)
            props = (path, format, "ascii", unix)
            self.project.save_main(props, False)
            assert self.project.main_changed == 1
            self.project.save_main(props, True)
            assert self.project.main_changed == 0

    def test_save_translation(self):

        path = self.project.tran_file.path
        unix = gaupol.NEWLINE.UNIX
        for format in gaupol.FORMAT.members:
            self.project.clear_texts([0], gaupol.DOCUMENT.TRAN)
            props = (path, format, "ascii", unix)
            self.project.save_translation(props, False)
            assert self.project.tran_changed == 1
            self.project.save_translation(props, True)
            assert self.project.tran_changed == 0
