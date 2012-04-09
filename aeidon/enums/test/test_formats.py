# -*- coding: utf-8-unix -*-

# Copyright (C) 2005-2009 Osmo Salomaa
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


class TestModule(aeidon.TestCase):

    def test_attributes(self):
        for format in aeidon.formats:
            assert hasattr(format, "container")
            assert hasattr(format, "extension")
            assert hasattr(format, "has_header")
            assert hasattr(format, "identifier")
            assert hasattr(format, "label")
            assert hasattr(format, "mime_type")

    def test_items(self):
        assert hasattr(aeidon.formats, "ASS")
        assert hasattr(aeidon.formats, "MICRODVD")
        assert hasattr(aeidon.formats, "MPL2")
        assert hasattr(aeidon.formats, "MPSUB")
        assert hasattr(aeidon.formats, "SSA")
        assert hasattr(aeidon.formats, "SUBRIP")
        assert hasattr(aeidon.formats, "SUBVIEWER2")
        assert hasattr(aeidon.formats, "TMPLAYER")
