# -*- coding: utf-8 -*-

# Copyright (C) 2006 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import aeidon


class TestModule(aeidon.TestCase):

    def test_atomic_open__existing_file(self):
        path = self.new_subrip_file()
        with aeidon.util.atomic_open(path, "w") as f:
            f.write("test\n")
        text = open(path, "r").read()
        assert text == "test\n"

    def test_atomic_open__no_existing_file(self):
        path = aeidon.temp.create()
        with aeidon.util.atomic_open(path, "w") as f:
            f.write("test\n")
        text = open(path, "r").read()
        assert text == "test\n"

    def test_compare_versions(self):
        assert aeidon.util.compare_versions("0.1.1", "0.1"  ) ==  1
        assert aeidon.util.compare_versions("0.2"  , "0.1"  ) ==  1
        assert aeidon.util.compare_versions("0.3"  , "0.3"  ) ==  0
        assert aeidon.util.compare_versions("0.4"  , "0.4.1") == -1
        assert aeidon.util.compare_versions("0.4"  , "0.5"  ) == -1

    def test_detect_format(self):
        for format in aeidon.formats:
            path = self.new_temp_file(format)
            assert aeidon.util.detect_format(path, "ascii") == format

    def test_detect_newlines__mac(self):
        path = aeidon.temp.create()
        open(path, "w", newline="").write("a\rb\rc\r")
        newlines = aeidon.util.detect_newlines(path)
        assert newlines == aeidon.newlines.MAC

    def test_detect_newlines__unix(self):
        path = aeidon.temp.create()
        open(path, "w", newline="").write("a\nb\nc\n")
        newlines = aeidon.util.detect_newlines(path)
        assert newlines == aeidon.newlines.UNIX

    def test_detect_newlines__windows(self):
        path = aeidon.temp.create()
        open(path, "w", newline="").write("a\r\nb\r\nc\r\n")
        newlines = aeidon.util.detect_newlines(path)
        assert newlines == aeidon.newlines.WINDOWS

    def test_flatten(self):
        lst = [1, 2, [3, 4, [5, 6, [7]], 8], 9]
        lst = aeidon.util.flatten(lst)
        assert lst == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_get_default_encoding(self):
        assert aeidon.util.get_default_encoding()

    def test_get_default_newline(self):
        assert aeidon.util.get_default_newline()

    def test_get_encoding_alias(self):
        assert aeidon.util.get_encoding_alias("utf8") == "utf_8"
        assert aeidon.util.get_encoding_alias("johab") == "johab"

    def test_get_ranges(self):
        lst = [0, 0, 4, 5, 3, 7, 8, 2, 7]
        lst = aeidon.util.get_ranges(lst)
        assert lst == [[0], [2, 3, 4, 5], [7, 8]]

    def test_get_unique__first(self):
        lst = [4, 1, 5, 5, 1, 1, 3, 6, 4, 4]
        lst = aeidon.util.get_unique(lst)
        assert lst == [4, 1, 5, 3, 6]

    def test_get_unique__last(self):
        lst = [4, 1, 5, 5, 1, 1, 3, 6, 4, 4]
        lst = aeidon.util.get_unique(lst, keep_last=True)
        assert lst == [5, 1, 3, 6, 4]

    def test_read__basic(self):
        path = self.new_subrip_file()
        text = open(path, "r", encoding="ascii").read().strip()
        assert aeidon.util.read(path) == text

    def test_read__fallback(self):
        path = self.new_subrip_file()
        open(path, "w", encoding="utf_8").write("\xc3\xb6\n")
        assert aeidon.util.read(path, "ascii") == "\xc3\xb6"

    def test_readlines__basic(self):
        path = self.new_subrip_file()
        lines = [x.rstrip() for x in open(path, "r").readlines()]
        assert aeidon.util.readlines(path) == lines

    def test_readlines__fallback(self):
        path = self.new_subrip_file()
        open(path, "w", encoding="utf_8").write("\xc3\xb6\n")
        assert aeidon.util.readlines(path, "ascii") == ["\xc3\xb6"]

    def test_write__basic(self):
        text = "test\ntest\n"
        path = self.new_subrip_file()
        aeidon.util.write(path, text)
        f = open(path, "r", encoding="ascii")
        assert f.read() == text

    def test_write__fallback(self):
        text = "\xc3\xb6\n"
        path = self.new_subrip_file()
        aeidon.util.write(path, text, "ascii")
        f = open(path, "r", encoding="utf_8")
        assert f.read() == text

    def test_writelines__basic(self):
        lines = ("test", "test")
        path = self.new_subrip_file()
        aeidon.util.writelines(path, lines)
        f = open(path, "r", encoding="ascii")
        assert f.read() == "test\ntest\n"

    def test_writelines__fallback(self):
        text = "\xc3\xb6"
        path = self.new_subrip_file()
        aeidon.util.writelines(path, (text,), "ascii")
        f = open(path, "r", encoding="utf_8")
        assert f.read() == text + "\n"
