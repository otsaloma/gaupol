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

from aeidon.markups.test.test_ssa import TestSubStationAlpha


class TestAdvSubStationAlpha(TestSubStationAlpha):

    text = ("All things weird are normal\n"
            "in this whore of cities.")

    def setup_method(self, method):
        self.markup = aeidon.markups.new(aeidon.formats.ASS)

    def test_decode__bold_weight(self):
        text = ("All things weird are normal\n"
                "in {\\b500}this{\\b0} whore of cities.")
        assert self.markup.decode(text) == (
            "All things weird are normal\n"
            "in <b>this</b> whore of cities.")

    def test_decode__underline(self):
        text = ("{\\u1}All things weird are normal\n"
                "in this whore of cities{\\rDefault}.")
        assert self.markup.decode(text) == (
            "<u>All things weird are normal\n"
            "in this whore of cities</u>.")

    def test_encode__underline(self):
        text = ("All things weird are normal\n"
                "<u>in this whore of cities.</u>")
        assert self.markup.encode(text) == (
            "All things weird are normal\n"
            "{\\u1}in this whore of cities.{\\u0}")
