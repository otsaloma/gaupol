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
import os
import sys

from gaupol import enclib, paths
from gaupol.unittest import TestCase
from .. import util


class TestModule(TestCase):

    # pylint: disable-msg=E0102

    def test_memoize(self):

        @util.memoize
        def square(x):
            return x ** 2
        assert square(3) == 9
        assert square(3) == 9

    def test_browse_url(self):

        util.browse_url("http://home.gna.org/gaupol")

    def test_chardet_available(self):

        assert isinstance(util.chardet_available(), bool)

    def test_compare_versions(self):

        assert util.compare_versions("0.0.1", "0.0.0") == 1
        assert util.compare_versions("0.0.0", "0.0.0") == 0
        assert util.compare_versions("0.0.0", "0.0.1") == -1
        assert util.compare_versions("0.0", "0.0.1") == -1
        assert util.compare_versions("0.0", "0.0.0.20070101") == -1

    def test_enchant_available(self):

        assert isinstance(util.enchant_available(), bool)

    def test_exceptional(self):

        def handle_index_error(exc_info, index):
            assert exc_info[0] is IndexError
            assert isinstance(index, int)
        def handle_value_error(exc_info, value):
            assert exc_info[0] is ValueError
            assert isinstance(value, int)
        index_args = (IndexError, handle_index_error, 0)
        value_args = (ValueError, handle_value_error, "value")

        @util.exceptional(*index_args)
        @util.exceptional(*value_args)
        def erroneous_do(index, value=0):
            lst = [0]
            lst.pop(index)
            lst.remove(value)
        erroneous_do(1)
        erroneous_do(0)

        def erroneous_do(index, value=0):
            lst = [0]
            lst.pop(index)
            lst.remove(value)
        util.exceptional(*index_args)(erroneous_do)(1)
        util.exceptional(*value_args)(erroneous_do)(0)

    def test_gc_collected(self):

        @util.gc_collected
        def litter():
            pass
        litter()

    def test_get_chardet_version(self):

        version = util.get_chardet_version()
        if util.chardet_available():
            assert isinstance(version, basestring)
        else:
            assert version is None

    def test_get_default_encoding(self):

        encoding = util.get_default_encoding()
        assert enclib.is_valid(encoding)

    def test_get_desktop_environment(self):

        assert util.get_desktop_environment() in ("GNOME", "KDE", None)

    def test_get_enchant_version(self):

        version = util.get_enchant_version()
        if util.enchant_available():
            assert isinstance(version, basestring)
        else:
            assert version is None

    def test_get_ranges(self):

        lst = [0, 0, 4, 5, 3, 7, 8, 2, 7]
        assert util.get_ranges(lst) == [[0], [2, 3, 4, 5], [7, 8]]
        assert lst == [0, 0, 4, 5, 3, 7, 8, 2, 7]

    def test_get_sorted_unique(self):

        lst = [4, 1, 5, 5, 1, 1, 3, 6, 4, 4]
        assert util.get_sorted_unique(lst) == [1, 3, 4, 5, 6]
        assert lst == [4, 1, 5, 5, 1, 1, 3, 6, 4, 4]

    def test_get_unique(self):

        lst = [4, 1, 5, 5, 1, 1, 3, 6, 4, 4]
        assert util.get_unique(lst) == [4, 1, 5, 3, 6]
        assert lst == [4, 1, 5, 5, 1, 1, 3, 6, 4, 4]

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

    def test_ignore_exceptions(self):

        @util.ignore_exceptions(IndexError, ValueError)
        def erroneous_do():
            lst = []
            lst.pop(0)
            lst.remove(0)
        erroneous_do()

        def erroneous_do():
            lst = []
            lst.pop(0)
            lst.remove(0)
        util.ignore_exceptions(IndexError, ValueError)(erroneous_do)()

    def test_make_profile_dir(self):

        util.make_profile_dir()
        assert os.path.isdir(paths.PROFILE_DIR)

    def test_makedirs(self):

        util.makedirs(paths.PROFILE_DIR)
        assert os.path.isdir(paths.PROFILE_DIR)

    def test_path_to_uri(self):

        uri = util.path_to_uri("/home/tester/my file.ext")
        assert uri == "file:///home/tester/my%20file.ext"

    def test_print_read_io(self):

        util.print_read_io("test", "test")

    def test_print_read_unicode(self):

        util.print_read_unicode("test", "test")

    def test_print_write_io(self):

        util.print_write_io("test", "test")

    def test_print_write_unicode(self):

        util.print_write_unicode("test", "test")

    def test_read(self):

        path = self.get_subrip_path()
        text = open(path, "r").read().strip()
        assert util.read(path) == text

    def test_readlines(self):

        path = self.get_subrip_path()
        lines = list(x.strip() for x in open(path, "r").readlines())
        assert util.readlines(path) == lines

    def test_shell_quote_path(self):

        path = self.get_subrip_path()
        assert util.shell_quote_path(path) == '"%s"' % path

    def test_start_process(self):

        process = util.start_process("echo test")
        assert process.wait() == 0
        process = util.start_process(["echo", "test"])
        assert process.wait() == 0

    def test_uri_to_path(self):

        path = util.uri_to_path("file:///home/tester/my%20file.ext")
        assert path == "/home/tester/my file.ext"

    def test_write(self):

        text = "test\ntest\n"
        path = self.get_subrip_path()
        util.write(path, text)
        assert open(path, "r").read() == text
