# -*- coding: utf-8 -*-

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

    def test___setattr____master(self):
        self.delegate.name = "slave"
        assert self.master.name == "slave"

    def test___setattr____delegate(self):
        self.delegate.none = None
        assert "none" in self.delegate.__dict__
        assert "none" not in self.master.__dict__
