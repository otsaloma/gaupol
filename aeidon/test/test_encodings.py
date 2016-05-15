# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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
import codecs

from aeidon.i18n   import _
from unittest.mock import patch


class TestModule(aeidon.TestCase):

    def test_code_to_description(self):
        code_to_description = aeidon.encodings.code_to_description
        assert code_to_description("cp1006") == _("Urdu")
        assert code_to_description("hz") == _("Chinese simplified")
        assert code_to_description("shift_jis") == _("Japanese")

    def test_code_to_long_name(self):
        code, name, description = ("cp1140", "IBM1140", _("Western"))
        long_name = aeidon.encodings.code_to_long_name(code)
        assert long_name == _("{description} ({name})").format(**locals())

    def test_code_to_name(self):
        code_to_name = aeidon.encodings.code_to_name
        assert code_to_name("big5hkscs") == "Big5-HKSCS"
        assert code_to_name("cp949") == "IBM949"
        assert code_to_name("mac_roman") == "MacRoman"

    def test_detect(self):
        name = aeidon.encodings.detect(self.new_subrip_file())
        assert aeidon.encodings.is_valid_code(name)

    def test_detect_bom__none(self):
        path = self.new_subrip_file()
        encoding = aeidon.encodings.detect_bom(path)
        assert encoding is None

    @patch("aeidon.encodings.is_valid_code", lambda x: True)
    def test_detect_bom__utf_16_be(self):
        path = self.new_subrip_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF16_BE + blob)
        encoding = aeidon.encodings.detect_bom(path)
        assert encoding == "utf_16_be"

    @patch("aeidon.encodings.is_valid_code", lambda x: True)
    def test_detect_bom__utf_16_le(self):
        path = self.new_subrip_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF16_LE + blob)
        encoding = aeidon.encodings.detect_bom(path)
        assert encoding == "utf_16_le"

    @patch("aeidon.encodings.is_valid_code", lambda x: True)
    def test_detect_bom__utf_32_be(self):
        path = self.new_subrip_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF32_BE + blob)
        encoding = aeidon.encodings.detect_bom(path)
        assert encoding == "utf_32_be"

    @patch("aeidon.encodings.is_valid_code", lambda x: True)
    def test_detect_bom__utf_32_le(self):
        path = self.new_subrip_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF32_LE + blob)
        encoding = aeidon.encodings.detect_bom(path)
        assert encoding == "utf_32_le"

    @patch("aeidon.encodings.is_valid_code", lambda x: True)
    def test_detect_bom__utf_8_sig(self):
        path = self.new_subrip_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF8 + blob)
        encoding = aeidon.encodings.detect_bom(path)
        assert encoding == "utf_8_sig"

    def test_get_locale_code(self):
        code = aeidon.encodings.get_locale_code()
        assert aeidon.encodings.is_valid_code(code)

    def test_get_locale_long_name(self):
        long_name = aeidon.encodings.get_locale_long_name()
        code = aeidon.encodings.get_locale_code()
        name = aeidon.encodings.code_to_name(code)
        assert long_name == _("Current locale ({})").format(name)

    def test_get_valid(self):
        assert aeidon.encodings.get_valid()
        for item in aeidon.encodings.get_valid():
            code, name, description = item
            assert aeidon.encodings.is_valid_code(code)

    def test_is_valid_code(self):
        assert aeidon.encodings.is_valid_code("gbk")
        assert aeidon.encodings.is_valid_code("utf_16_be")
        assert not aeidon.encodings.is_valid_code("xxxxx")

    def test_name_to_code(self):
        name_to_code = aeidon.encodings.name_to_code
        assert name_to_code("IBM037") == "cp037"
        assert name_to_code("GB2312") == "gb2312"
        assert name_to_code("PTCP154") == "ptcp154"

    def test_translate_code(self):
        translate_code = aeidon.encodings.translate_code
        assert translate_code("johab") == "johab"
        assert translate_code("UTF-8") == "utf_8"
        assert translate_code("ISO-8859-1") == "latin_1"
