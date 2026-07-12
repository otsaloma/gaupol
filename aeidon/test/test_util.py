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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import aeidon
import pytest

class TestModule(aeidon.TestCase):

    def test_atomic_open__existing_file(self):
        path = self.new_subrip_file()
        with aeidon.util.atomic_open(path, "w") as f:
            f.write("test\n")
        text = path.read_text()
        assert text == "test\n"

    def test_atomic_open__no_existing_file(self):
        path = aeidon.temp.create()
        with aeidon.util.atomic_open(path, "w") as f:
            f.write("test\n")
        text = path.read_text()
        assert text == "test\n"

    def test_compare_versions(self):
        assert aeidon.util.compare_versions("0.1.1", "0.1"  ) ==  1
        assert aeidon.util.compare_versions("0.2"  , "0.1"  ) ==  1
        assert aeidon.util.compare_versions("0.3"  , "0.3"  ) ==  0
        assert aeidon.util.compare_versions("0.4"  , "0.4.1") == -1
        assert aeidon.util.compare_versions("0.4"  , "0.5"  ) == -1

    @pytest.mark.parametrize("format", aeidon.formats)
    def test_detect_format(self, format):
        path = self.new_temp_file(format)
        assert aeidon.util.detect_format(path, "ascii") == format

    def test_detect_newlines__mac(self):
        path = aeidon.temp.create()
        path.write_text("a\rb\rc\r", newline="")
        newlines = aeidon.util.detect_newlines(path)
        assert newlines == aeidon.newlines.MAC

    def test_detect_newlines__unix(self):
        path = aeidon.temp.create()
        path.write_text("a\nb\nc\n", newline="")
        newlines = aeidon.util.detect_newlines(path)
        assert newlines == aeidon.newlines.UNIX

    def test_detect_newlines__windows(self):
        path = aeidon.temp.create()
        path.write_text("a\r\nb\r\nc\r\n", newline="")
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
        text = path.read_text(encoding="ascii").strip()
        assert aeidon.util.read(path) == text

    def test_read__fallback(self):
        path = self.new_subrip_file()
        path.write_text("\xc3\xb6\n", encoding="utf_8")
        assert aeidon.util.read(path, "ascii") == "\xc3\xb6"

    def test_readlines__basic(self):
        path = self.new_subrip_file()
        with open(path, "r") as f:
            lines = [x.rstrip() for x in f.readlines()]
        assert aeidon.util.readlines(path) == lines

    def test_readlines__fallback(self):
        path = self.new_subrip_file()
        path.write_text("\xc3\xb6\n", encoding="utf_8")
        assert aeidon.util.readlines(path, "ascii") == ["\xc3\xb6"]

    def test_write__basic(self):
        text = "test\ntest\n"
        path = self.new_subrip_file()
        aeidon.util.write(path, text)
        assert path.read_text(encoding="ascii") == text

    def test_write__fallback(self):
        text = "\xc3\xb6\n"
        path = self.new_subrip_file()
        aeidon.util.write(path, text, "ascii")
        assert path.read_text(encoding="utf_8") == text

    def test_writelines__basic(self):
        lines = ("test", "test")
        path = self.new_subrip_file()
        aeidon.util.writelines(path, lines)
        assert path.read_text(encoding="ascii") == "test\ntest\n"

    def test_writelines__fallback(self):
        text = "\xc3\xb6"
        path = self.new_subrip_file()
        aeidon.util.writelines(path, (text,), "ascii")
        assert path.read_text(encoding="utf_8") == text + "\n"
