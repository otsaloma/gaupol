# Copyright (C) 2006-2008 Osmo Salomaa
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
import os


class TestConfig(gaupol.TestCase):

    def setup_method(self, method):

        name = "gaupol.conf.spec"
        self.spec_file = os.path.join(aeidon.DATA_DIR, name)
        self.config = gaupol.conf.Config(None, self.spec_file)

    def test___check_enum(self):

        path = self.new_subrip_file()
        fobj = open(path, "w")
        fobj.write("[editor]\n")
        fobj.write("mode = XXX\n")
        fobj.close()
        gaupol.conf.Config(path, self.spec_file)

    def test___check_enum_list(self):

        path = self.new_subrip_file()
        fobj = open(path, "w")
        fobj.write("[editor]\n")
        fobj.write("visible_fields = XXX, YYY, ZZZ\n")
        fobj.close()
        gaupol.conf.Config(path, self.spec_file)

    def test___init____config_obj_error(self):

        path = self.new_subrip_file()
        function = gaupol.conf.Config
        args = (path, self.spec_file)
        self.raises(gaupol.ConfigParseError, function, *args)

    def test___init____io_error(self):

        path = self.new_subrip_file()
        os.chmod(path, 0000)
        gaupol.conf.Config(path, self.spec_file)
        os.chmod(path, 0777)

    def test___init____unicode_error(self):

        path = self.new_subrip_file()
        fobj = open(path, "w")
        fobj.write("[file]\n")
        fobj.write("directory = \303\266\n")
        fobj.close()
        get_encoding = aeidon.util.get_default_encoding
        aeidon.util.get_default_encoding = lambda *args: "ascii"
        gaupol.conf.Config(path, self.spec_file)
        aeidon.util.get_default_encoding = get_encoding

    def test___remove_options(self):

        path = self.new_subrip_file()
        fobj = open(path, "w")
        fobj.write("[editor]\n")
        fobj.write("xxx = yyy\n")
        fobj.close()
        gaupol.conf.Config(path, self.spec_file)

    def test___remove_sections(self):

        path = self.new_subrip_file()
        fobj = open(path, "w")
        fobj.write("[xxx]\n")
        fobj.write("yyy = zzz\n")
        fobj.close()
        gaupol.conf.Config(path, self.spec_file)

    def test___validate(self):

        path = self.new_subrip_file()
        fobj = open(path, "w")
        fobj.write("[editor]\n")
        fobj.write("limit_undo = xxx\n")
        fobj.close()
        gaupol.conf.Config(path, self.spec_file)

    def test_write_to_file(self):

        path = self.new_subrip_file()
        self.config.filename = path
        self.config.write_to_file()
        gaupol.conf.Config(path, self.spec_file)

    def test_write_to_file__io_error(self):

        path = self.new_subrip_file()
        self.config.filename = path
        os.chmod(path, 0000)
        self.config.write_to_file()
        os.chmod(path, 0777)

    def test_write_to_file__unicode_error(self):

        path = self.new_subrip_file()
        self.config.filename = path
        self.config.encoding = "ascii"
        self.config["file"]["directory"] = "\303\266"
        self.config.write_to_file()
        gaupol.conf.Config(path, self.spec_file)
