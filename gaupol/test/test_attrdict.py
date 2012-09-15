# -*- coding: utf-8 -*-

# Copyright (C) 2006-2010 Osmo Salomaa
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

    def test_add_attribute__dict(self):
        root = {"test": 1, "rest": 0}
        self.attr_dict.add_attribute("nest", root)
        assert self.attr_dict.nest.test == 1
        assert self.attr_dict.nest.rest == 0
        assert self.root["nest"]["test"] == 1
        assert self.root["nest"]["rest"] == 0

    def test_extend(self):
        root = {"test": 3, "pest": 4}
        self.attr_dict.extend(root)
        assert self.attr_dict.test == 1
        assert self.attr_dict.rest == 0
        assert self.attr_dict.pest == 4
        assert self.root["test"] == 1
        assert self.root["rest"] == 0
        assert self.root["pest"] == 4

    def test_extend__dict(self):
        root = {"test": 1, "rest": 0}
        self.attr_dict.add_attribute("nest", root)
        root = {"nest": {"test": 3, "pest": 4}}
        self.attr_dict.extend(root)
        assert self.attr_dict.nest.test == 1
        assert self.attr_dict.nest.rest == 0
        assert self.attr_dict.nest.pest == 4
        assert self.root["nest"]["test"] == 1
        assert self.root["nest"]["rest"] == 0
        assert self.root["nest"]["pest"] == 4

    def test_remove_attribute(self):
        self.attr_dict.remove_attribute("test")
        assert not hasattr(self.attr_dict, "test")
        assert "test" not in self.root

    def test_update(self):
        root = {"test": 3, "pest": 4}
        self.attr_dict.update(root)
        assert self.attr_dict.test == 3
        assert self.attr_dict.rest == 0
        assert self.attr_dict.pest == 4
        assert self.root["test"] == 3
        assert self.root["rest"] == 0
        assert self.root["pest"] == 4

    def test_update__dict(self):
        root = {"test": 1, "rest": 0}
        self.attr_dict.add_attribute("nest", root)
        root = {"nest": {"test": 3, "pest": 4}}
        self.attr_dict.update(root)
        assert self.attr_dict.nest.test == 3
        assert self.attr_dict.nest.rest == 0
        assert self.attr_dict.nest.pest == 4
        assert self.root["nest"]["test"] == 3
        assert self.root["nest"]["rest"] == 0
        assert self.root["nest"]["pest"] == 4
