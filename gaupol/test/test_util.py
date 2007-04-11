# Copyright (C) 2006-2007 Osmo Salomaa
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


import codecs
import sys
import tempfile

from gaupol.unittest import TestCase
from .. import util


class TestModule(TestCase):

    # pylint: disable-msg=E0102

    def test_memoize(self):

        @util.memoize
        def square(x):
            return x ** 2
        assert square(2) == 4
        assert square(2) == 4

    def test_browse_url(self):

        util.browse_url("http://home.gna.org/gaupol")

    def test_chardet_available(self):

        assert util.chardet_available()

    def test_compare_versions(self):

        assert util.compare_versions("0.1.1", "0.1"  ) ==  1
        assert util.compare_versions("0.2"  , "0.1"  ) ==  1
        assert util.compare_versions("0.3"  , "0.3"  ) ==  0
        assert util.compare_versions("0.4"  , "0.4.1") == -1
        assert util.compare_versions("0.4"  , "0.5"  ) == -1

    def test_enchant_available(self):

        assert util.enchant_available()

    def test_get_chardet_version(self):

        util.get_chardet_version()

    def test_get_default_encoding(self):

        util.get_default_encoding()

    def test_get_desktop_environment(self):

        desktop = util.get_desktop_environment()
        assert desktop in ("GNOME", "KDE", None)

    def test_get_enchant_version(self):

        util.get_enchant_version()

    def test_get_ranges(self):

        lst = [0, 0, 4, 5, 3, 7, 8, 2, 7]
        value = util.get_ranges(lst)
        assert value == [[0], [2, 3, 4, 5], [7, 8]]

    def test_get_sorted_unique(self):

        lst = [4, 1, 5, 5, 1, 1, 3, 6, 4, 4]
        value = util.get_sorted_unique(lst)
        assert value == [1, 3, 4, 5, 6]

    def test_get_unique(self):

        lst = [4, 1, 5, 5, 1, 1, 3, 6, 4, 4]
        value = util.get_unique(lst)
        assert value == [4, 1, 5, 3, 6]

    def test_handle_read_io(self):

        try:
            open("/////", "r").read()
            raise AssertionError
        except IOError:
            util.handle_read_io(sys.exc_info(), "/////")

    def test_handle_read_unicode(self):

        try:
            path = self.get_subrip_path()
            codecs.open(path, "r", "undefined").read()
            raise AssertionError
        except UnicodeError:
            util.handle_read_unicode(sys.exc_info(), path, "undefined")

    def test_handle_write_io(self):

        try:
            open("/////", "w").write("\n")
            raise AssertionError
        except IOError:
            util.handle_write_io(sys.exc_info(), "/////")

    def test_handle_write_unicode(self):

        try:
            path = self.get_subrip_path()
            codecs.open(path, "r", "ascii").write(u"\303\266")
            raise AssertionError
        except UnicodeError:
            util.handle_write_unicode(sys.exc_info(), path, "ascii")

    def test_last(self):

        assert util.last(iter((1, 2, 3))) == 3

    def test_makedirs(self):

        util.makedirs(tempfile.gettempdir())

    def test_path_to_uri(self):

        uri = util.path_to_uri("/home/tester/my file.ext")
        assert uri == "file:///home/tester/my%20file.ext"

    def test_read(self):

        path = self.get_subrip_path()
        text = open(path, "r").read().strip()
        assert util.read(path) == text

    def test_readlines(self):

        path = self.get_subrip_path()
        lines = [x.rstrip() for x in open(path, "r").readlines()]
        assert util.readlines(path) == lines

    def test_shell_quote(self):

        path = util.shell_quote(r'/home/tester/my "file"\.ext')
        assert path == r'"/home/tester/my \"file\"\\.ext"'

    def test_silent(self):

        @util.silent(ValueError)
        def erroneous_do():
            [].remove(None)
        erroneous_do()

    def test_start_process(self):

        process = util.start_process("echo test")
        assert process.wait() == 0

    def test_uri_to_path(self):

        path = util.uri_to_path("file:///home/tester/my%20file.ext")
        assert path == "/home/tester/my file.ext"

    def test_write(self):

        text = "test\ntest\n"
        path = self.get_subrip_path()
        util.write(path, text)
        assert open(path, "r").read() == text
