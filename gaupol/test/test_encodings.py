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


from gaupol import unittest
from gaupol.i18n import _
from .. import encodings


class TestModule(unittest.TestCase):

    def test__translate(self):

        assert encodings._translate("johab") == "johab"
        assert encodings._translate("UTF-8") == "utf_8"
        assert encodings._translate("ISO-8859-1") == "latin_1"

    def test_detect(self):

        name = encodings.detect(self.get_subrip_path())
        assert encodings.is_valid(name)

    def test_get_description(self):

        description = encodings.get_description("cp1006")
        assert description == _("Urdu")

    def test_get_display_name(self):

        name = encodings.get_display_name("mac_roman")
        assert name == _("MacRoman")

    def test_get_locale_long_name(self):

        name = encodings.get_locale_long_name()
        encoding = encodings.get_locale_python_name()
        encoding = encodings.get_display_name(encoding)
        assert name == _("Current locale (%s)") % encoding

    def test_get_locale_python_name(self):

        name = encodings.get_locale_python_name()
        assert encodings.is_valid(name)

    def test_get_long_name(self):

        name = encodings.get_long_name("cp1140")
        assert name == _("%s (%s)") % (_("Western"), "IBM1140")

    def test_get_python_name(self):

        name = encodings.get_python_name(_("GB2312"))
        assert name == "gb2312"

    def test_get_valid_encodings(self):

        items = encodings.get_valid_encodings()
        assert items
        for item in items:
            assert encodings.is_valid(item[0])
            assert isinstance(item[1], basestring)
            assert isinstance(item[2], basestring)

    def test_is_valid(self):

        assert encodings.is_valid("utf_16_be")
        assert not encodings.is_valid("xxxxx")
