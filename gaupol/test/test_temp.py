# Copyright (C) 2007 Osmo Salomaa
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

import os

from gaupol import unittest
from .. import temp


class TestModule(unittest.TestCase):

    def test_close(self):

        path = temp.create()
        temp.close(path)

    def test_create(self):

        path = temp.create()
        assert os.path.isfile(path)
        temp.remove(path)

    def test_get_handle(self):

        path = temp.create()
        temp.get_handle(path)
        temp.remove(path)

    def test_remove(self):

        path = temp.create()
        temp.remove(path)
        assert not os.path.isfile(path)
        temp.remove(path)
