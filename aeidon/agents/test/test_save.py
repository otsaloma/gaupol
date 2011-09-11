# Copyright (C) 2005-2009 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

import aeidon


class TestSaveAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()
        self.delegate = self.project.save_main.__self__

    def test__copy_file(self):
        copy_file = self.delegate._copy_file
        source = self.new_subrip_file()
        destination = self.new_subrip_file()
        assert copy_file(source, destination)
        assert not copy_file(source, "/////")

    def test__move_file(self):
        move_file = self.delegate._move_file
        source = self.new_subrip_file()
        destination = self.new_subrip_file()
        assert move_file(source, destination)
        assert not move_file(source, "/////")

    def test__remove_file(self):
        remove_file = self.delegate._remove_file
        path = self.new_subrip_file()
        assert remove_file(path)
        assert not remove_file("/////")

    def test_save__main(self):
        self.project.save(aeidon.documents.MAIN)

    def test_save__translation(self):
        self.project.save(aeidon.documents.TRAN)

    def test_save__value_error(self):
        self.assert_raises(ValueError, self.project.save, None)

    def test_save_main(self):
        for format in aeidon.formats:
            self.project.clear_texts((0,), aeidon.documents.MAIN)
            path = self.project.main_file.path
            sfile = aeidon.files.new(format, path, "ascii")
            self.project.save_main(sfile, False)
            assert self.project.main_changed == 1
            sfile = aeidon.files.new(format, path, "ascii")
            self.project.save_main(sfile, True)
            assert self.project.main_changed == 0

    def test_save_main__io_error(self):
        sfile = aeidon.files.new(aeidon.formats.SUBRIP, "/////", "ascii")
        self.assert_raises(IOError, self.project.save_main, sfile)

    def test_save_main__unicode_error(self):
        path = self.project.main_file.path
        sfile = aeidon.files.new(aeidon.formats.SUBRIP, path, "undefined")
        self.assert_raises(UnicodeError, self.project.save_main, sfile)

    def test_save_translation(self):
        for format in aeidon.formats:
            self.project.clear_texts((0,), aeidon.documents.TRAN)
            path = self.project.tran_file.path
            sfile = aeidon.files.new(format, path, "ascii")
            self.project.save_translation(sfile, False)
            assert self.project.tran_changed == 1
            self.project.save_translation(sfile, True)
            assert self.project.tran_changed == 0
