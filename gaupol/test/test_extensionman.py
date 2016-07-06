# -*- coding: utf-8 -*-

# Copyright (C) 2008 Osmo Salomaa
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


class TestExtensionManager(gaupol.TestCase):

    def setup_method(self, method):
        gaupol.conf.path = aeidon.temp.create(".conf")
        self.manager = gaupol.ExtensionManager(self.new_application())
        gaupol.conf.extensions.active = ["custom-framerates", "none"]
        self.manager.find_extensions()
        self.manager.setup_extensions()

    def teardown_method(self, method):
        self.manager.teardown_extensions()
        gaupol.TestCase.teardown_method(self, method)

    def test_setup_extension(self):
        self.manager.setup_extension("custom-framerates")
        assert self.manager.is_active("custom-framerates")

    def test_teardown_extension(self):
        self.manager.setup_extension("custom-framerates")
        self.manager.teardown_extension("custom-framerates")
        assert not self.manager.is_active("custom-framerates")
