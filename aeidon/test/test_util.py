# -*- coding: utf-8 -*-

# Copyright (C) 2006-2009,2011-2012 Osmo Salomaa
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
import imp
import os
import sys
import time


class TestModule(aeidon.TestCase):

    def test_affirm__false(self):
        self.assert_raises(aeidon.AffirmationError,
                           aeidon.util.affirm,
                           1 == 0)

    def test_affirm__true(self):
        aeidon.util.affirm(0 == 0)

    def test_atomic_open__existing_file(self):
        path = self.new_subrip_file()
        with aeidon.util.atomic_open(path, "w") as fobj:
            fobj.write("test\n")
        text = open(path, "r").read()
        assert text == "test\n"

    def test_atomic_open__existing_file__io_error(self):
        path = self.new_subrip_file()
        os.chmod(path, 0000)
        try:
            with aeidon.util.atomic_open(path, "w") as fobj:
                fobj.write("test\n")
        except IOError:
            pass
        os.chmod(path, 0o777)

    def test_atomic_open__no_existing_file(self):
        path = aeidon.temp.create()
        with aeidon.util.atomic_open(path, "w") as fobj:
            fobj.write("test\n")
        text = open(path, "r").read()
        assert text == "test\n"

    def test_chardet_available(self):
        imp.reload(aeidon.util)
        assert aeidon.util.chardet_available()

    def test_compare_versions(self):
        compare_versions = aeidon.util.compare_versions
        assert compare_versions("0.1.1", "0.1"  ) ==  1
        assert compare_versions("0.2"  , "0.1"  ) ==  1
        assert compare_versions("0.3"  , "0.3"  ) ==  0
        assert compare_versions("0.4"  , "0.4.1") == -1
        assert compare_versions("0.4"  , "0.5"  ) == -1

    def test_connect__private(self):
        self.project = self.new_project()
        self._on_project_action_done = lambda *args: None
        aeidon.util.connect(self, "project", "action-done")

    def test_connect__public(self):
        self.project = self.new_project()
        self.on_project_action_done = lambda *args: None
        aeidon.util.connect(self, "project", "action-done")

    def test_copy_dict(self):
        aeidon.util.copy_dict({1: 2, 3: {1: 2}})
        aeidon.util.copy_dict({1: 2, 3: [1, 2]})
        aeidon.util.copy_dict({1: 2, 3: set((1, 2))})

    def test_copy_list(self):
        aeidon.util.copy_list([1, 2, {1: 2}])
        aeidon.util.copy_list([1, 2, [1, 2]])
        aeidon.util.copy_list([1, 2, set((1, 2))])

    def test_detect_format(self):
        for format in aeidon.formats:
            path = self.new_temp_file(format)
            assert aeidon.util.detect_format(path, "ascii") == format

    def test_detect_format__format_error(self):
        path = self.new_subrip_file()
        aeidon.util.write(path, "xxx\n", "ascii")
        self.assert_raises(aeidon.FormatError,
                           aeidon.util.detect_format,
                           path, "ascii")

    def test_detect_newlines(self):
        newlines = aeidon.util.detect_newlines(self.new_subrip_file())
        assert newlines is not None

    def test_enchant_available(self):
        imp.reload(aeidon.util)
        assert aeidon.util.enchant_available()

    def test_enchant_and_dicts_available(self):
        imp.reload(aeidon.util)
        assert aeidon.util.enchant_and_dicts_available()

    def test_flatten(self):
        lst = [1, 2, [3, 4, [5, 6, [7]], 8], 9]
        lst = aeidon.util.flatten(lst)
        assert lst == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_get_chardet_version(self):
        imp.reload(aeidon.util)
        assert aeidon.util.get_chardet_version()

    def test_get_default_encoding(self):
        assert aeidon.util.get_default_encoding()

    def test_get_default_newline(self):
        assert aeidon.util.get_default_newline()

    def test_get_enchant_version(self):
        imp.reload(aeidon.util)
        assert aeidon.util.get_enchant_version()

    def test_get_encoding_alias(self):
        assert aeidon.util.get_encoding_alias("utf8") == "utf_8"
        assert aeidon.util.get_encoding_alias("johab") == "johab"

    def test_get_ranges__empty(self):
        assert aeidon.util.get_ranges([]) == []

    def test_get_ranges__non_empty(self):
        lst = [0, 0, 4, 5, 3, 7, 8, 2, 7]
        lst = aeidon.util.get_ranges(lst)
        assert lst == [[0], [2, 3, 4, 5], [7, 8]]

    def test_get_sorted_unique(self):
        lst = [4, 1, 5, 5, 1, 1, 3, 6, 4, 4]
        lst = aeidon.util.get_sorted_unique(lst)
        assert lst == [1, 3, 4, 5, 6]

    @aeidon.deco.monkey_patch(aeidon, "DATA_DIR")
    @aeidon.deco.monkey_patch(aeidon, "DATA_HOME_DIR")
    def test_get_template_header(self):
        for format in (x for x in aeidon.formats if x.has_header):
            if format == aeidon.formats.MICRODVD: continue
            assert aeidon.util.get_template_header(format)
            dirs = aeidon.DATA_DIR, aeidon.DATA_HOME_DIR
            aeidon.DATA_HOME_DIR, aeidon.DATA_DIR = dirs
            assert aeidon.util.get_template_header(format)

    def test_get_unique__first(self):
        lst = [4, 1, 5, 5, 1, 1, 3, 6, 4, 4]
        lst = aeidon.util.get_unique(lst)
        assert lst == [4, 1, 5, 3, 6]

    def test_get_unique__last(self):
        lst = [4, 1, 5, 5, 1, 1, 3, 6, 4, 4]
        lst = aeidon.util.get_unique(lst, keep_last=True)
        assert lst == [5, 1, 3, 6, 4]

    def test_is_command__false(self):
        assert not aeidon.util.is_command("???")

    def test_is_command__true(self):
        assert aeidon.util.is_command("echo")

    def test_last(self):
        assert aeidon.util.last(iter((1, 2, 3))) == 3

    def test_makedirs(self):
        path = "{}-{:.0f}".format(self.new_subrip_file(), time.time())
        aeidon.util.makedirs(path)
        aeidon.util.makedirs(path)
        os.rmdir(path)

    def test_normalize_newlines__mac(self):
        value = aeidon.util.normalize_newlines("test\rtest\r")
        assert value == "test\ntest\n"

    def test_normalize_newlines__unix(self):
        value = aeidon.util.normalize_newlines("test\ntest\n")
        assert value == "test\ntest\n"

    def test_normalize_newlines__windows(self):
        value = aeidon.util.normalize_newlines("test\r\ntest\r\n")
        assert value == "test\ntest\n"

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_path_to_uri__unix(self):
        sys.platform = "linux2"
        path = "/home/aeidon/a file.srt"
        uri = aeidon.util.path_to_uri(path)
        assert uri == "file:///home/aeidon/a%20file.srt"

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_path_to_uri__windows(self):
        sys.platform = "win32"
        path = "c:\\aeidon\\a file.srt"
        uri = aeidon.util.path_to_uri(path)
        assert uri == "file:///c%3A/aeidon/a%20file.srt"

    def test_print_read_io(self):
        try:
            open("/////", "r").read()
            raise AssertionError
        except IOError:
            aeidon.util.print_read_io(sys.exc_info(),
                                      "/////")

    def test_print_read_unicode(self):
        try:
            path = self.new_subrip_file()
            open(path, "r", encoding="undefined").read()
            raise AssertionError
        except UnicodeError:
            aeidon.util.print_read_unicode(sys.exc_info(),
                                           path,
                                           "undefined")

    def test_print_remove_os(self):
        try:
            os.remove("/////")
        except OSError:
            aeidon.util.print_remove_os(sys.exc_info(),
                                        "/////")

    def test_print_write_io(self):
        try:
            open("/////", "w").write("\n")
            raise AssertionError
        except IOError:
            aeidon.util.print_write_io(sys.exc_info(),
                                       "/////")

    def test_print_write_unicode(self):
        try:
            path = self.new_subrip_file()
            text = bytes("\xc3\xb6\n", "ascii")
            open(path, "r", encoding="ascii").write(text)
            raise AssertionError
        except UnicodeError:
            aeidon.util.print_write_unicode(sys.exc_info(),
                                            path,
                                            "ascii")

    def test_read__basic(self):
        path = self.new_subrip_file()
        text = open(path, "r", encoding="ascii").read().strip()
        assert aeidon.util.read(path) == text

    def test_read__fallback(self):
        path = self.new_subrip_file()
        open(path, "w", encoding="utf_8").write("\xc3\xb6\n")
        assert aeidon.util.read(path, "ascii") == "\xc3\xb6"

    def test_read__unicode_error(self):
        path = self.new_subrip_file()
        open(path, "w", encoding="latin1").write("\xc3\xb6\n")
        self.assert_raises(UnicodeError,
                           aeidon.util.read,
                           path, "ascii", None)

    def test_readlines__basic(self):
        path = self.new_subrip_file()
        lines = [x.rstrip() for x in open(path, "r").readlines()]
        assert aeidon.util.readlines(path) == lines

    def test_readlines__fallback(self):
        path = self.new_subrip_file()
        open(path, "w", encoding="utf_8").write("\xc3\xb6\n")
        assert aeidon.util.readlines(path, "ascii") == ["\xc3\xb6"]

    def test_readlines__unicode_error(self):
        path = self.new_subrip_file()
        open(path, "w", encoding="latin1").write("\xc3\xb6\n")
        self.assert_raises(UnicodeError,
                           aeidon.util.readlines,
                           path, "ascii", None)

    def test_replace_extension(self):
        format = aeidon.formats.SUBRIP
        value = aeidon.util.replace_extension("test.txt", format)
        assert value == "test.srt"

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_shell_quote__unix(self):
        sys.platform = "linux2"
        path = '/home/aeidon/a "file"\\.srt'
        path = aeidon.util.shell_quote(path)
        assert path == '"/home/aeidon/a \\"file\\"\\\\.srt"'

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_shell_quote__windows(self):
        sys.platform = "win32"
        path = 'c:\\aeidon\\a file.srt'
        path = aeidon.util.shell_quote(path)
        assert path == '"c:\\aeidon\\a file.srt"'

    def test_start_process(self):
        process = aeidon.util.start_process("echo")
        assert process.wait() == 0

    def test_title_to_lower_case(self):
        assert aeidon.util.title_to_lower_case("Test") == "test"
        assert aeidon.util.title_to_lower_case("TestCase") == "test_case"

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_uri_to_path__unix(self):
        sys.platform = "linux2"
        uri = "file:///home/aeidon/a%20file.srt"
        path = aeidon.util.uri_to_path(uri)
        assert path == "/home/aeidon/a file.srt"

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_uri_to_path__windows(self):
        sys.platform = "win32"
        uri = "file:///c:/aeidon/a%20file.srt"
        path = aeidon.util.uri_to_path(uri)
        assert path == "c:\\aeidon\\a file.srt"

    def test_write__basic(self):
        text = "test\ntest\n"
        path = self.new_subrip_file()
        aeidon.util.write(path, text)
        fobj = open(path, "r", encoding="ascii")
        assert fobj.read() == text

    def test_write__fallback(self):
        text = "\xc3\xb6\n"
        path = self.new_subrip_file()
        aeidon.util.write(path, text, "ascii")
        fobj = open(path, "r", encoding="utf_8")
        assert fobj.read() == text

    def test_write__unicode_error(self):
        path = self.new_subrip_file()
        self.assert_raises(UnicodeError,
                           aeidon.util.write,
                           path, "\xc3\xb6\n", "ascii", None)

    def test_writelines__basic(self):
        lines = ("test", "test")
        path = self.new_subrip_file()
        aeidon.util.writelines(path, lines)
        fobj = open(path, "r", encoding="ascii")
        assert fobj.read() == "test\ntest\n"

    def test_writelines__fallback(self):
        text = "\xc3\xb6"
        path = self.new_subrip_file()
        aeidon.util.writelines(path, (text,), "ascii")
        fobj = open(path, "r", encoding="utf_8")
        assert fobj.read() == text + os.linesep

    def test_writelines__unicode_error(self):
        path = self.new_subrip_file()
        self.assert_raises(UnicodeError,
                           aeidon.util.writelines,
                           path, ("\xc3\xb6\n",), "ascii", None)
