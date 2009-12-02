# Copyright (C) 2005-2008 Osmo Salomaa
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

import gaupol


class TestSaveAgent(gaupol.TestCase):

    def setup_method(self, method):

        self.project = self.new_project()
        self.delegate = self.project.save_main.im_self

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

    def test_save(self):

        self.project.save(gaupol.documents.MAIN, ())
        self.project.save(gaupol.documents.TRAN, ())
        self.raises(ValueError, self.project.save, 99, ())

    def test_save_main(self):

        path = self.project.main_file.path
        newline = gaupol.newlines.UNIX
        for format in gaupol.formats:
            self.project.clear_texts((0,), gaupol.documents.MAIN)
            props = (path, format, "ascii", newline)
            self.project.save_main(props, False)
            assert self.project.main_changed == 1
            self.project.save_main(props, True)
            assert self.project.main_changed == 0

    def test_save_main__copy_from(self):

        path = self.new_subrip_file()
        format = self.project.main_file.format
        newline = gaupol.newlines.UNIX
        props = (path, format, "ascii", newline)
        self.project.save_main(props)

    def test_save_main__io_error(self):

        function = self.project.save_main
        format = gaupol.formats.SUBRIP
        newline = gaupol.newlines.UNIX
        props = ("/////", format, "ascii", newline)
        self.raises(IOError, function, props)

    def test_save_main__unicode_error(self):

        function = self.project.save_main
        path = self.new_subrip_file()
        format = gaupol.formats.SUBRIP
        newline = gaupol.newlines.UNIX
        props = (path, format, "undefined", newline)
        self.raises(UnicodeError, function, props)

    def test_save_translation(self):

        path = self.project.tran_file.path
        newline = gaupol.newlines.UNIX
        for format in gaupol.formats:
            self.project.clear_texts((0,), gaupol.documents.TRAN)
            props = (path, format, "ascii", newline)
            self.project.save_translation(props, False)
            assert self.project.tran_changed == 1
            self.project.save_translation(props, True)
            assert self.project.tran_changed == 0
