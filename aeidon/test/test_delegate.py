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

import aeidon


class PuppetMaster:

    def __init__(self):
        self.name = "master"


class TestDelegate(aeidon.TestCase):

    def setup_method(self, method):
        self.master = PuppetMaster()
        self.delegate = aeidon.Delegate(self.master)

    def test___getattr__(self):
        assert self.delegate.name == "master"

    def test___setattr____delegate(self):
        self.delegate.none = None
        assert "none" in self.delegate.__dict__
        assert not "none" in self.master.__dict__

    def test___setattr____master(self):
        self.delegate.name = "slave"
        assert self.master.name == "slave"
