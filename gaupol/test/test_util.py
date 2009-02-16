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

import codecs
import gaupol
import os
import sys
import tempfile
import time


class TestModule(gaupol.TestCase):

    url = "http://home.gna.org/gaupol"

    @gaupol.deco.silent(OSError)
    def browse_url_silent(self, url):

        return gaupol.util.browse_url(url)

    def setup_method(self, method):

        self.project = self.get_project()

    def test_affirm(self):

        gaupol.util.affirm(0 == 0)
        error = gaupol.AffirmationError
        self.raises(error, gaupol.util.affirm, 1 == 0)

    def test_browse_url(self):

        gaupol.util.browse_url(self.url)
        gaupol.util.browse_url(self.url, "echo")

    def test_browse_url__command(self):

        environment = os.environ.copy()
        os.environ.clear()
        platform = sys.platform
        sys.platform = "linux2"
        is_command = gaupol.util.is_command
        gaupol.util.is_command = lambda x: (x == "xdg-open")
        self.browse_url_silent(self.url)
        gaupol.util.is_command = lambda x: (x == "exo-open")
        self.browse_url_silent(self.url)
        os.environ = environment
        sys.platform = platform
        gaupol.util.is_command = is_command

    def test_browse_url__environment(self):

        environment = os.environ.copy()
        os.environ.clear()
        platform = sys.platform
        sys.platform = "linux2"
        os.environ["GNOME_DESKTOP_SESSION_ID"] = "1"
        self.browse_url_silent(self.url)
        os.environ.clear()
        os.environ["KDE_FULL_SESSION"] = "1"
        self.browse_url_silent(self.url)
        os.environ = environment
        sys.platform = platform

    def test_browse_url__platform(self):

        environment = os.environ.copy()
        os.environ.clear()
        platform = sys.platform
        sys.platform = "darwin"
        self.browse_url_silent(self.url)
        sys.platform = "win32"
        self.browse_url_silent(self.url)
        os.environ = environment
        sys.platform = platform

    def test_browse_url__webbrowser(self):

        environment = os.environ.copy()
        os.environ.clear()
        platform = sys.platform
        sys.platform = "linux2"
        gaupol.util.browse_url(self.url)
        os.environ = environment
        sys.platform = platform

    def test_chardet_available(self):

        assert gaupol.util.chardet_available()
        assert gaupol.util.chardet_available()
        reload(gaupol.util)
        real_import = __builtins__["__import__"]
        def bad_import(*args):
            if args[0] == "chardet": raise ImportError
            return real_import(*args)
        __builtins__["__import__"] = bad_import
        assert not gaupol.util.chardet_available()
        assert not gaupol.util.chardet_available()
        __builtins__["__import__"] = real_import
        reload(gaupol.util)

    def test_connect(self):

        # pylint: disable-msg=W0201
        self._on_project_action_done = lambda *args: None
        gaupol.util.connect(self, "project", "action-done")
        self.on_project_action_undone = lambda *args: None
        gaupol.util.connect(self, "project", "action-undone")

    def test_compare_versions(self):

        assert gaupol.util.compare_versions("0.1.1", "0.1"  ) ==  1
        assert gaupol.util.compare_versions("0.2"  , "0.1"  ) ==  1
        assert gaupol.util.compare_versions("0.3"  , "0.3"  ) ==  0
        assert gaupol.util.compare_versions("0.4"  , "0.4.1") == -1
        assert gaupol.util.compare_versions("0.4"  , "0.5"  ) == -1

    def test_copy_dict(self):

        gaupol.util.copy_dict({1: 2, 3: {1: 2}})
        gaupol.util.copy_dict({1: 2, 3: [1, 2]})
        gaupol.util.copy_dict({1: 2, 3: set((1, 2))})

    def test_copy_list(self):

        gaupol.util.copy_list([1, 2, {1: 2}])
        gaupol.util.copy_list([1, 2, [1, 2]])
        gaupol.util.copy_list([1, 2, set((1, 2))])

    def test_enchant_available(self):

        assert gaupol.util.enchant_available()
        assert gaupol.util.enchant_available()
        reload(gaupol.util)
        real_import = __builtins__["__import__"]
        def bad_import(*args):
            if args[0] == "enchant": raise ImportError
            return real_import(*args)
        __builtins__["__import__"] = bad_import
        assert not gaupol.util.enchant_available()
        assert not gaupol.util.enchant_available()
        __builtins__["__import__"] = real_import
        reload(gaupol.util)

    def test_get_all(self):

        assert gaupol.util.get_all(dir()) == ("self",)
        assert not gaupol.util.get_all(dir(), r"^[A-Z]")
        names = gaupol.util.get_all(dir(gaupol.util))
        assert len(names) < len(dir(gaupol.util))

    def test_get_chardet_version(self):

        assert gaupol.util.get_chardet_version()
        reload(gaupol.util)
        real_import = __builtins__["__import__"]
        def bad_import(*args):
            if args[0] == "chardet": raise ImportError
            return real_import(*args)
        __builtins__["__import__"] = bad_import
        assert gaupol.util.get_chardet_version() is None
        __builtins__["__import__"] = real_import
        reload(gaupol.util)

    def test_get_default_encoding(self):

        gaupol.util.get_default_encoding()

    def test_get_enchant_version(self):

        assert gaupol.util.get_enchant_version()
        reload(gaupol.util)
        real_import = __builtins__["__import__"]
        def bad_import(*args):
            if args[0] == "enchant": raise ImportError
            return real_import(*args)
        __builtins__["__import__"] = bad_import
        assert gaupol.util.get_enchant_version() is None
        __builtins__["__import__"] = real_import
        reload(gaupol.util)

    def test_get_encoding_alias(self):

        assert gaupol.util.get_encoding_alias("utf8") == "utf_8"
        assert gaupol.util.get_encoding_alias("johab") == "johab"

    def test_get_ranges(self):

        lst = [0, 0, 4, 5, 3, 7, 8, 2, 7]
        value = gaupol.util.get_ranges(lst)
        assert value == [[0], [2, 3, 4, 5], [7, 8]]
        assert gaupol.util.get_ranges([]) == []

    def test_get_sorted_unique(self):

        lst = [4, 1, 5, 5, 1, 1, 3, 6, 4, 4]
        value = gaupol.util.get_sorted_unique(lst)
        assert value == [1, 3, 4, 5, 6]

    def test_get_unique(self):

        lst = [4, 1, 5, 5, 1, 1, 3, 6, 4, 4]
        value = gaupol.util.get_unique(lst)
        assert value == [4, 1, 5, 3, 6]
        lst = [4, 1, 5, 5, 1, 1, 3, 6, 4, 4]
        value = gaupol.util.get_unique(lst, True)
        assert value == [5, 1, 3, 6, 4]

    def test_is_command(self):

        if os.path.isfile("/bin/sh"):
            assert gaupol.util.is_command("sh")
        assert not gaupol.util.is_command("+?")

    def test_last(self):

        assert gaupol.util.last(iter((1, 2, 3))) == 3

    def test_makedirs(self):

        gaupol.util.makedirs(tempfile.gettempdir())
        path = "%s-%d" % (self.get_subrip_path(), time.time())
        gaupol.util.makedirs(path)
        os.rmdir(path)

    def test_path_to_uri__unix(self):

        platform = sys.platform
        sys.platform = "linux2"
        path = "/home/tester/a file.ext"
        uri = gaupol.util.path_to_uri(path)
        assert uri == "file:///home/tester/a%20file.ext"
        sys.platform = platform

    def test_path_to_uri__windows(self):

        platform = sys.platform
        sys.platform = "win32"
        path = "c:\\tester\\a file.ext"
        uri = gaupol.util.path_to_uri(path)
        assert uri == "file:///c%3A/tester/a%20file.ext"
        sys.platform = platform

    def test_print_read_io(self):

        try:
            open("/tmp/1/2/3/4///", "r").read()
            raise AssertionError
        except IOError:
            args = (sys.exc_info(), "/tmp/1/2/3/4///")
            gaupol.util.print_read_io(*args)

    def test_print_read_unicode(self):

        try:
            path = self.get_subrip_path()
            codecs.open(path, "r", "undefined").read()
            raise AssertionError
        except UnicodeError:
            args = (sys.exc_info(), path, "undefined")
            gaupol.util.print_read_unicode(*args)

    def test_print_remove_os(self):

        try:
            os.remove("/tmp/1/2/3/4///")
        except OSError:
            args = (sys.exc_info(), "/tmp/1/2/3/4///")
            gaupol.util.print_remove_os(*args)

    def test_print_write_io(self):

        try:
            open("/////", "w").write("\n")
            raise AssertionError
        except IOError:
            args = (sys.exc_info(), "/////")
            gaupol.util.print_write_io(*args)

    def test_print_write_unicode(self):

        try:
            path = self.get_subrip_path()
            codecs.open(path, "r", "ascii").write(u"\xc3\xb6\n")
            raise AssertionError
        except UnicodeError:
            args = (sys.exc_info(), path, "ascii")
            gaupol.util.print_write_unicode(*args)

    def test_read(self):

        path = self.get_subrip_path()
        text = codecs.open(path, "r", "ascii").read().strip()
        assert gaupol.util.read(path) == text

    def test_read__fallback(self):

        path = self.get_subrip_path()
        codecs.open(path, "w", "utf_8").write(u"\xc3\xb6\n")
        assert gaupol.util.read(path, "ascii") == u"\xc3\xb6"

    def test_read__unicode_error(self):

        path = self.get_subrip_path()
        codecs.open(path, "w", "latin1").write(u"\xc3\xb6\n")
        args = (path, "ascii", None)
        self.raises(UnicodeError, gaupol.util.read, *args)

    def test_readlines(self):

        path = self.get_subrip_path()
        lines = [x.rstrip() for x in open(path, "r").readlines()]
        assert gaupol.util.readlines(path) == lines

    def test_readlines__fallback(self):

        path = self.get_subrip_path()
        codecs.open(path, "w", "utf_8").write(u"\xc3\xb6\n")
        assert gaupol.util.readlines(path, "ascii") == [u"\xc3\xb6"]

    def test_shell_quote__unix(self):

        platform = sys.platform
        sys.platform = "linux2"
        path = '/home/tester/a "file"\\.ext'
        path = gaupol.util.shell_quote(path)
        assert path == '"/home/tester/a \\"file\\"\\\\.ext"'
        sys.platform = platform

    def test_shell_quote__windows(self):

        platform = sys.platform
        sys.platform = "win32"
        path = 'c:\\tester\\a file.ext'
        path = gaupol.util.shell_quote(path)
        assert path == '"c:\\tester\\a file.ext"'
        sys.platform = platform

    def test_start_process(self):

        process = gaupol.util.start_process("echo")
        assert process.wait() == 0

    def test_title_to_lower_case(self):

        assert gaupol.util.title_to_lower_case("Test") == "test"
        assert gaupol.util.title_to_lower_case("TestCase") == "test_case"

    def test_uri_to_path__unix(self):

        platform = sys.platform
        sys.platform = "linux2"
        uri = "file:///home/tester/a%20file.ext"
        path = gaupol.util.uri_to_path(uri)
        assert path == "/home/tester/a file.ext"
        sys.platform = platform

    def test_uri_to_path__windows(self):

        platform = sys.platform
        sys.platform = "win32"
        uri = "file:///c:/tester/a%20file.ext"
        path = gaupol.util.uri_to_path(uri)
        assert path == "c:\\tester\\a file.ext"
        sys.platform = platform

    def test_write(self):

        text = "test\ntest\n"
        path = self.get_subrip_path()
        gaupol.util.write(path, text)
        assert codecs.open(path, "r", "ascii").read() == text

    def test_write__fallback(self):

        text = u"\xc3\xb6\n"
        path = self.get_subrip_path()
        gaupol.util.write(path, text, "ascii")
        assert codecs.open(path, "r", "utf_8").read() == text

    def test_write__unicode_error(self):

        path = self.get_subrip_path()
        args = (path, u"\xc3\xb6\n", "ascii", None)
        self.raises(UnicodeError, gaupol.util.write, *args)

    def test_writelines(self):

        lines = ["test", "test"]
        path = self.get_subrip_path()
        gaupol.util.writelines(path, lines)
        text = "test\ntest\n"
        assert codecs.open(path, "r", "ascii").read() == text
