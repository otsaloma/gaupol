# -*- coding: utf-8 -*-

# Copyright (C) 2006 Osmo Salomaa
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

import gaupol


class TestAttrDict(gaupol.TestCase):

    def setup_method(self, method):
        self.root = dict(test=1, rest=0)
        self.attr_dict = gaupol.AttributeDictionary(self.root)

    def test___getattr__(self):
        assert self.attr_dict.test == 1
        assert self.attr_dict.rest == 0

    def test___setattr__(self):
        self.attr_dict.test = 5
        assert self.attr_dict.test == 5
        assert self.root["test"] == 5

    def test_add_attribute(self):
        self.attr_dict.add_attribute("best", 2)
        assert self.attr_dict.best == 2
        assert self.root["best"] == 2

    def test_add_attribute__nested(self):
        root = dict(test=1, rest=0)
        self.attr_dict.add_attribute("nest", root)
        assert self.attr_dict.nest.test == 1
        assert self.attr_dict.nest.rest == 0
        assert self.root["nest"]["test"] == 1
        assert self.root["nest"]["rest"] == 0

    def test_extend(self):
        root = dict(test=3, pest=4)
        self.attr_dict.extend(root)
        assert self.attr_dict.test == 1
        assert self.attr_dict.rest == 0
        assert self.attr_dict.pest == 4
        assert self.root["test"] == 1
        assert self.root["rest"] == 0
        assert self.root["pest"] == 4

    def test_extend__nested(self):
        root = dict(test=1, rest=0)
        self.attr_dict.add_attribute("nest", root)
        root = dict(nest=dict(test=3, pest=4))
        self.attr_dict.extend(root)
        assert self.attr_dict.nest.test == 1
        assert self.attr_dict.nest.rest == 0
        assert self.attr_dict.nest.pest == 4
        assert self.root["nest"]["test"] == 1
        assert self.root["nest"]["rest"] == 0
        assert self.root["nest"]["pest"] == 4

    def test_update(self):
        root = dict(test=3, pest=4)
        self.attr_dict.update(root)
        assert self.attr_dict.test == 3
        assert self.attr_dict.rest == 0
        assert self.attr_dict.pest == 4
        assert self.root["test"] == 3
        assert self.root["rest"] == 0
        assert self.root["pest"] == 4

    def test_update__nested(self):
        root = dict(test=1, rest=0)
        self.attr_dict.add_attribute("nest", root)
        root = dict(nest=dict(test=3, pest=4))
        self.attr_dict.update(root)
        assert self.attr_dict.nest.test == 3
        assert self.attr_dict.nest.rest == 0
        assert self.attr_dict.nest.pest == 4
        assert self.root["nest"]["test"] == 3
        assert self.root["nest"]["rest"] == 0
        assert self.root["nest"]["pest"] == 4
