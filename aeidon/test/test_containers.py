# -*- coding: utf-8 -*-

# Copyright (C) 2008 Osmo Salomaa
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


class TestSubRip(aeidon.TestCase):

    def setup_method(self, method):
        self.container = aeidon.containers.new("subrip")

    def test_attributes(self):
        assert hasattr(self.container, "x1")
        assert hasattr(self.container, "y1")
        assert hasattr(self.container, "x2")
        assert hasattr(self.container, "y2")


class TestSubStationAlpha(aeidon.TestCase):

    def setup_method(self, method):
        self.container = aeidon.containers.new("ssa")

    def test_attributes(self):
        assert hasattr(self.container, "marked")
        assert hasattr(self.container, "layer")
        assert hasattr(self.container, "style")
        assert hasattr(self.container, "name")
        assert hasattr(self.container, "margin_l")
        assert hasattr(self.container, "margin_r")
        assert hasattr(self.container, "margin_v")
        assert hasattr(self.container, "effect")


class TestModule(aeidon.TestCase):

    def test_new(self):
        aeidon.containers.new("ssa")
        aeidon.containers.new("subrip")

    def test_new__value_error(self):
        self.assert_raises(ValueError,
                           aeidon.containers.new,
                           "xxx")
