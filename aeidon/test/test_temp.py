# -*- coding: utf-8 -*-

# Copyright (C) 2007 Osmo Salomaa
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import aeidon

class TestModule(aeidon.TestCase):

    def test_create(self):
        path = aeidon.temp.create()
        aeidon.temp.remove(path)

    def test_create_directory(self):
        path = aeidon.temp.create_directory()
        aeidon.temp.remove(path)

    def test_remove__directory(self):
        path = aeidon.temp.create_directory()
        (path / "a").write_text("a")
        (path / "b").write_text("b")
        (path / "c").mkdir()
        aeidon.temp.remove(path)
        assert not path.is_dir()
        aeidon.temp.remove(path)

    def test_remove__file(self):
        path = aeidon.temp.create()
        aeidon.temp.remove(path)
        assert not path.is_file()
        aeidon.temp.remove(path)

    def test_remove_all(self):
        path_1 = aeidon.temp.create()
        path_2 = aeidon.temp.create()
        aeidon.temp.remove_all()
        assert not path_1.is_file()
        assert not path_2.is_file()
