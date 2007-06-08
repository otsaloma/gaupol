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
from .. import clipboard


class TestClipboard(unittest.TestCase):

    def setup_method(self, method):

        self.clipboard = clipboard.Clipboard()

    def test_append(self):

        self.clipboard.append("")
        self.clipboard.append(None)
        texts = self.clipboard.get_texts()
        assert texts == ["", None]

    def test_clear(self):

        self.clipboard.append("")
        self.clipboard.append(None)
        self.clipboard.clear()
        texts = self.clipboard.get_texts()
        assert texts == []

    def test_get_string(self):

        self.clipboard._texts = ["test", None, "test", None]
        string = self.clipboard.get_string()
        assert string == "test\n\n\n\ntest\n\n"

    def test_get_texts(self):

        self.clipboard.append("")
        self.clipboard.append(None)
        texts = self.clipboard.get_texts()
        assert texts == ["", None]

    def test_is_empty(self):

        assert self.clipboard.is_empty()
        self.clipboard.append("")
        assert not self.clipboard.is_empty()
