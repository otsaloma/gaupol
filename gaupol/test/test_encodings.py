# Copyright (C) 2005-2008 Osmo Salomaa
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

import gaupol
_ = gaupol.i18n._


class TestModule(gaupol.TestCase):

    def test__translate_code(self):

        translate_code = gaupol.encodings._translate_code
        assert translate_code("johab") == "johab"
        assert translate_code("UTF-8") == "utf_8"
        assert translate_code("ISO-8859-1") == "latin_1"
        self.raises(ValueError, translate_code, "xxxxx")

    def test_code_to_description(self):

        code_to_description = gaupol.encodings.code_to_description
        assert code_to_description("cp1006") == _("Urdu")
        assert code_to_description("hz") == _("Chinese simplified")
        assert code_to_description("shift_jis") == _("Japanese")
        self.raises(ValueError, code_to_description, "xxxxx")

    def test_code_to_long_name(self):

        code, name, description = ("cp1140", "IBM1140", _("Western"))
        long_name = gaupol.encodings.code_to_long_name(code)
        assert long_name == _("%(description)s (%(name)s)") % locals()
        self.raises(ValueError, gaupol.encodings.code_to_long_name, "xxxxx")

    def test_code_to_name(self):

        code_to_name = gaupol.encodings.code_to_name
        assert code_to_name("big5hkscs") == "Big5-HKSCS"
        assert code_to_name("cp949") == "IBM949"
        assert code_to_name("mac_roman") == "MacRoman"
        self.raises(ValueError, code_to_name, "xxxxx")

    def test_detect(self):

        name = gaupol.encodings.detect(self.get_subrip_path())
        assert gaupol.encodings.is_valid_code(name)

    def test_detect__value_error(self):

        translate_code = gaupol.encodings._translate_code
        def bad_translate_code(code): raise ValueError
        gaupol.encodings._translate_code = bad_translate_code
        assert gaupol.encodings.detect(self.get_subrip_path()) is None
        gaupol.encodings._translate_code = translate_code

    def test_get_locale_code(self):

        code = gaupol.encodings.get_locale_code()
        assert gaupol.encodings.is_valid_code(code)

    def test_get_locale_long_name(self):

        long_name = gaupol.encodings.get_locale_long_name()
        code = gaupol.encodings.get_locale_code()
        name = gaupol.encodings.code_to_name(code)
        assert long_name == _("Current locale (%s)") % name

    def test_get_valid(self):

        assert gaupol.encodings.get_valid()
        for item in gaupol.encodings.get_valid():
            assert gaupol.encodings.is_valid_code(item[0])
            assert isinstance(item[1], basestring)
            assert isinstance(item[2], basestring)

    def test_get_valid__invalid(self):

        is_valid_code = gaupol.encodings.is_valid_code
        bad_is_valid_code = lambda code: not code.startswith("cp")
        gaupol.encodings.is_valid_code = bad_is_valid_code
        assert gaupol.encodings.get_valid()
        gaupol.encodings.is_valid_code = is_valid_code

    def test_is_valid_code(self):

        assert gaupol.encodings.is_valid_code("gbk")
        assert gaupol.encodings.is_valid_code("utf_16_be")
        assert not gaupol.encodings.is_valid_code("xxxxx")

    def test_name_to_code(self):

        name_to_code = gaupol.encodings.name_to_code
        assert name_to_code("IBM037") == "cp037"
        assert name_to_code("GB2312") == "gb2312"
        assert name_to_code("PTCP154") == "ptcp154"
        self.raises(ValueError, name_to_code, "XXXXX")
