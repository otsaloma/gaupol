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

from .test_ssa import TestSubStationAlpha
from .. import ass


class TestAdvSubStationAlpha(TestSubStationAlpha):

    def setup_method(self, method):

        self.taglib = ass.AdvSubStationAlpha()

    def test_decode(self):

        TestSubStationAlpha.test_decode(self)

        # Underline
        text = \
            "{\\u1}All things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            "<u>All things weird are normal\n" + \
            "in this whore of cities.</u>"

    def test_encode(self):

        TestSubStationAlpha.test_encode(self)

        # Underline.
        text = \
            "<u>All things weird are normal\n" + \
            "in this whore of cities.</u>"
        assert self.taglib.encode(text) == \
            "{\\u1}All things weird are normal\n" + \
            "in this whore of cities."
