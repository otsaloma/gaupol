# -*- coding: utf-8-unix -*-

# Copyright (C) 2011 Osmo Salomaa
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

    def test_is_frame(self):
        assert aeidon.is_frame(aeidon.as_frame(13))
        assert not aeidon.is_frame(aeidon.as_seconds(13))
        assert not aeidon.is_frame(aeidon.as_time("12:34:56.789"))

    def test_is_seconds(self):
        assert aeidon.is_seconds(aeidon.as_seconds(13))
        assert not aeidon.is_seconds(aeidon.as_frame(13))
        assert not aeidon.is_seconds(aeidon.as_time("12:34:56.789"))

    def test_is_time(self):
        assert aeidon.is_time(aeidon.as_time("12:34:56.789"))
        assert not aeidon.is_time(aeidon.as_frame(13))
        assert not aeidon.is_time(aeidon.as_seconds(13))
