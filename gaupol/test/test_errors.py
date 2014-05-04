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
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import aeidon
import gaupol


class TestDefault(gaupol.TestCase):

    def test_raise__default(self):
        try:
            raise gaupol.Default
        except gaupol.Default:
            pass

    def test_raise__error(self):
        try:
            raise gaupol.Default
        except aeidon.Error:
            pass


class TestDependencyError(gaupol.TestCase):

    def test_raise__dependency_error(self):
        try:
            raise gaupol.DependencyError
        except gaupol.DependencyError:
            pass

    def test_raise__error(self):
        try:
            raise gaupol.Default
        except aeidon.Error:
            pass
