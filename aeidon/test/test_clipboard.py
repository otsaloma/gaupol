# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009 Osmo Salomaa
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


class TestClipboard(aeidon.TestCase):

    def setup_method(self, method):
        self.clipboard = aeidon.Clipboard()

    def test_append(self):
        self.clipboard.set_texts(("", None))
        texts = self.clipboard.get_texts()
        assert texts == ["", None]

    def test_clear(self):
        self.clipboard.set_texts(("", None))
        self.clipboard.clear()
        texts = self.clipboard.get_texts()
        assert texts == []

    def test_get_string(self):
        self.clipboard.set_texts(("test", None, "test", None))
        string = self.clipboard.get_string()
        assert string == "test\n\n\n\ntest\n\n"

    def test_get_texts(self):
        self.clipboard.set_texts(("", None))
        texts = self.clipboard.get_texts()
        assert texts == ["", None]

    def test_set_texts(self):
        self.clipboard.set_texts(("", None))
        texts = self.clipboard.get_texts()
        assert texts == ["", None]

    def test_is_empty(self):
        assert self.clipboard.is_empty()
        self.clipboard.append("")
        assert not self.clipboard.is_empty()
