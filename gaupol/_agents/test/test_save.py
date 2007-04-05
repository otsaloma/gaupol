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


import os

from gaupol import const
from gaupol.unittest import TestCase
from .. import save


class TestModule(TestCase):

    def test__create_backup(self):

        path = self.get_subrip_path()
        assert save._create_backup(path, path + "x")
        assert os.path.isfile(path + "x")
        self.files.append(path + "x")

    def test__remove_backup(self):

        path = self.get_subrip_path()
        assert save._remove_backup(path)
        assert not os.path.isfile(path)

    def test__remove_failed(self):

        path = self.get_subrip_path()
        assert save._remove_failed(path)
        assert not os.path.isfile(path)

    def test__restore_original(self):

        path = self.get_subrip_path()
        assert save._restore_original(path + "x", path)
        assert os.path.isfile(path + "x")
        assert not os.path.isfile(path)
        self.files.append(path + "x")


class TestSaveAgent(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()

    def test_save(self):

        # pylint: disable-msg=E1101
        unix = const.NEWLINE.UNIX
        for format in const.FORMAT.members:

            # MAIN, keep changes
            doc = const.DOCUMENT.MAIN
            self.project.clear_texts([0], doc)
            path = self.project.main_file.path
            self.project.save(doc, (path, format, "ascii", unix), True)
            assert self.project.main_changed == 0

            # MAIN, discard changes
            self.project.clear_texts([1], doc)
            path = self.project.main_file.path
            self.project.save(doc, (path, format, "ascii", unix), False)
            assert self.project.main_changed == 1

            # TRAN, keep changes
            doc = const.DOCUMENT.TRAN
            self.project.clear_texts([0], doc)
            path = self.project.tran_file.path
            self.project.save(doc, (path, format, "ascii", unix), True)
            assert self.project.tran_changed == 0
            assert self.project.tran_active

            # TRAN, discard changes
            self.project.clear_texts([1], doc)
            path = self.project.tran_file.path
            self.project.save(doc, (path, format, "ascii", unix), False)
            assert self.project.tran_changed == 1
            assert self.project.tran_active
