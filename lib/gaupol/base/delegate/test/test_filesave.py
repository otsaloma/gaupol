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


import os

from gaupol.base          import cons
from gaupol.base.delegate import filesave
from gaupol.test          import Test


class TestModule(Test):

    def setup_method(self, method):

        self.path_1 = self.get_subrip_path()
        self.path_2 = self.get_subrip_path()
        self.paths = [self.path_1, self.path_2]

        self.files.append(self.path_1)
        self.files.append(self.path_2)

    def test_create_backup(self):

        success = filesave._create_backup(*self.paths)
        assert success is True

    def test_remove_backup(self):

        filesave._remove_backup(self.path_1)
        assert not os.path.isfile(self.path_1)

    def test_remove_failed(self):

        filesave._remove_failed(self.path_1)
        assert not os.path.isfile(self.path_1)

    def test_restore_original(self):

        filesave._restore_original(*self.paths)


class TestFileSaveDelegate(Test):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = filesave.FileSaveDelegate(self.project)

    def test_save_files(self):

        self.project.save_main_file()
        self.project.save_translation_file()

    def test_save_files_changed(self):

        self.project.clear_texts([0], cons.Document.MAIN)
        self.project.save_main_file()
        assert self.project.main_changed == 0

        self.project.clear_texts([0], cons.Document.TRAN)
        self.project.save_translation_file()
        assert self.project.tran_changed == 0

    def test_save_files_formats(self):

        props = [
            self.project.main_file.path,
            cons.Format.MPL2,
            'utf_8',
            cons.Newlines.UNIX
        ]

        for i in range(len(cons.Format.class_names)):
            props[1] = i
            self.project.save_main_file(props=props)
            self.project.save_translation_file(props=props)
