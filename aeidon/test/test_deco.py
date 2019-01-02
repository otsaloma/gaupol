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


class TestModule(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()

    def test_silent(self):
        function = lambda: 0 / 0
        aeidon.deco.silent(ZeroDivisionError)(function)()
        aeidon.deco.silent(ZeroDivisionError, tb=True)(function)()
        aeidon.deco.silent(Exception)(function)()
        aeidon.deco.silent(Exception, tb=True)(function)()
