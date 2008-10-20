# Copyright (C) 2006-2008 Osmo Salomaa
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


class TestAttrDict(gaupol.TestCase):

    def setup_method(self, method):

        self.root = {"test": 1, "rest": 0}
        self.attrdict = gaupol.AttrDict(self.root)

    def test___getattr__(self):

        assert isinstance(self.attrdict.test, int)
        assert isinstance(self.attrdict.rest, int)

    def test___setattr__(self):

        self.attrdict.test = 5
        assert self.root["test"] == 5
        self.attrdict.test = 9
        assert self.attrdict.test == 9

    def test_update(self):

        self.attrdict.update(self.root)
