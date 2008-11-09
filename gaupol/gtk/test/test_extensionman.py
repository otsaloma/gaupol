# Copyright (C) 2008 Osmo Salomaa
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

import gaupol.gtk


class TestExtensionManager(gaupol.gtk.TestCase):

    # TODO: Change 'null' to whatever module we ship with gaupol.

    def setup_method(self, method):

        self.manager = gaupol.gtk.ExtensionManager(self.get_application())
        gaupol.gtk.conf.extensions.active = ["null", "none"]
        self.manager.find_extensions()
        self.manager.setup_extensions()

    def test_find_extensions(self):

        self.manager.find_extensions()
        assert self.manager.get_modules()

    def test_get_metadata(self):

        metadata = self.manager.get_metadata("null")
        assert metadata.has_field("GaupolVersion")
        assert metadata.has_field("Module")
        assert metadata.has_field("Name")
        assert metadata.has_field("Description")

    def test_get_modules(self):

        modules = self.manager.get_modules()
        assert "null" in modules

    def test_setup_extension(self):

        self.manager.setup_extension("null")

    def test_setup_extensions(self):

        self.manager.setup_extensions()

    def test_teardown_extension(self):

        self.manager.setup_extension("null")
        self.manager.teardown_extension("null")

    def test_teardown_extensions(self):

        self.manager.teardown_extensions()

    def test_update_extensions(self):

        page = self.manager.application.get_current_page()
        self.manager.update_extensions(page)
