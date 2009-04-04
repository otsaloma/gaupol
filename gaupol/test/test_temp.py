# Copyright (C) 2007-2008 Osmo Salomaa
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
import os


class TestModule(gaupol.TestCase):

    def test_close(self):

        path = gaupol.temp.create()
        gaupol.temp.close(path)
        gaupol.temp.remove(path)

    def test_create(self):

        path = gaupol.temp.create()
        gaupol.temp.remove(path)

    def test_create_directory(self):

        path = gaupol.temp.create_directory()
        gaupol.temp.remove_directory(path)

    def test_get_handle(self):

        path = gaupol.temp.create()
        gaupol.temp.get_handle(path)
        gaupol.temp.remove(path)

    def test_remove(self):

        path = gaupol.temp.create()
        gaupol.temp.remove(path)
        assert not os.path.isfile(path)
        gaupol.temp.remove(path)

    def test_remove_all(self):

        path_1 = gaupol.temp.create()
        path_2 = gaupol.temp.create()
        gaupol.temp.remove_all()
        assert not os.path.isfile(path_1)
        assert not os.path.isfile(path_2)

    def test_remove_directory(self):

        path = gaupol.temp.create_directory()
        open(os.path.join(path, "a"), "w").write("a")
        open(os.path.join(path, "b"), "w").write("b")
        gaupol.temp.remove_directory(path)
        assert not os.path.isdir(path)
        gaupol.temp.remove_directory(path)
