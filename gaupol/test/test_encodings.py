# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

import gaupol
_ = gaupol.i18n._

from gaupol import unittest
from .. import encodings


class TestModule(unittest.TestCase):

    def test__translate_code(self):

        assert encodings._translate_code("johab") == "johab"
        assert encodings._translate_code("UTF-8") == "utf_8"
        assert encodings._translate_code("ISO-8859-1") == "latin_1"

    def test_code_to_description(self):

        description = encodings.code_to_description("cp1006")
        assert description == _("Urdu")

    def test_code_to_long_name(self):

        long_name = encodings.code_to_long_name("cp1140")
        description = _("Western")
        name = "IBM1140"
        assert long_name == _("%(description)s (%(name)s)") % locals()

    def test_code_to_name(self):

        name = encodings.code_to_name("mac_roman")
        assert name == _("MacRoman")

    def test_detect(self):

        name = encodings.detect(self.get_subrip_path())
        assert encodings.is_valid_code(name)

    def test_get_locale_code(self):

        code = encodings.get_locale_code()
        assert encodings.is_valid_code(code)

    def test_get_locale_long_name(self):

        long_name = encodings.get_locale_long_name()
        code = encodings.get_locale_code()
        name = encodings.code_to_name(code)
        assert long_name == _("Current locale (%s)") % name

    def test_get_valid_encodings(self):

        assert encodings.get_valid_encodings()
        for item in encodings.get_valid_encodings():
            assert encodings.is_valid_code(item[0])
            assert isinstance(item[1], basestring)
            assert isinstance(item[2], basestring)

    def test_is_valid_code(self):

        assert encodings.is_valid_code("utf_16_be")
        assert not encodings.is_valid_code("xxxxx")

    def test_name_to_code(self):

        assert encodings.name_to_code(_("GB2312")) == "gb2312"
