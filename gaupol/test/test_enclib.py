# Copyright (C) 2005-2007 Osmo Salomaa
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


from gettext import gettext as _

from gaupol.unittest import TestCase
from .. import enclib


class TestModule(TestCase):

    def test__translate(self):

        output = enclib._translate("koi8_r")
        assert isinstance(output, tuple)
        assert len(output) == 3

        assert enclib._translate("johab")[0] == "johab"
        assert enclib._translate("UTF-8")[0] == "utf_8"
        assert enclib._translate("ISO-8859-1")[0] == "latin_1"

        try:
            enclib._translate("xxx")
            raise AssertionError
        except ValueError:
            pass

    def test_detect(self):

        name = enclib.detect(self.get_subrip_path())
        assert enclib.is_valid(name)

    def test_get_display_name(self):

        name = enclib.get_display_name("mac_roman")
        assert name == _("MacRoman")

        try:
            enclib.get_display_name("xxx")
            raise AssertionError
        except ValueError:
            pass

    def test_get_locale_long_name(self):

        name = enclib.get_locale_long_name()
        encoding = enclib.get_locale_python_name()
        encoding = enclib.get_display_name(encoding)
        assert name == _("Current locale (%s)") % encoding

    def test_get_locale_python_name(self):

        output = enclib.get_locale_python_name()
        if output is not None:
            assert enclib.is_valid(output)

    def test_get_long_name(self):

        name = enclib.get_long_name("cp1140")
        assert name == _("%s (%s)") % (_("Western"), "IBM1140")

        try:
            enclib.get_long_name("xxx")
            raise AssertionError
        except ValueError:
            pass

    def test_get_python_name(self):

        name = enclib.get_python_name(_("GB2312"))
        assert name == "gb2312"

        try:
            enclib.get_python_name("xxx")
            raise AssertionError
        except ValueError:
            pass

    def test_get_valid_encodings(self):

        encodings = enclib.get_valid_encodings()
        assert isinstance(encodings, list)
        assert len(encodings) > 10
        for seq in encodings:
            assert isinstance(seq, tuple)
            assert len(seq) == 3
            assert enclib.is_valid(seq[0])
            assert isinstance(seq[1], basestring)
            assert isinstance(seq[2], basestring)

    def test_is_valid(self):

        assert enclib.is_valid("utf_16_be")
        assert not enclib.is_valid("xxxxx")
