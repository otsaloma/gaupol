# Copyright (C) 2006-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


from gaupol import unittest
from .. import delegate


class TestDelegate(unittest.TestCase):

    def setup_method(self, method):

        self.master = type("test", (object,), {})
        self.delegate = delegate.Delegate(self.master)

    def test___getattr__(self):

        self.master.name = "test"
        assert self.delegate.name == "test"

    def test___setattr___master(self):

        self.master.name = None
        self.delegate.name = "test"
        assert self.master.name == "test"

    def test___setattr___delegate(self):

        self.delegate.name = None
        assert not hasattr(self.master, "name")
