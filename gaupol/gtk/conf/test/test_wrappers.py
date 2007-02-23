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


import os

from gaupo.gtk import paths
from gaupol.gtk.unittest import TestCase
from .. import wrappers


CONFIG_FILE = os.path.join(paths.PROFILE_DIR, "gaupol.gtk.conf")
SPEC_FILE = os.path.join(paths.DATA_DIR, "conf.spec")


class TestConfig(TestCase):

    def setup_method(self, method):

        self.config = wrappers.Config(CONFIG_FILE, SPEC_FILE)

    def test_write_to_file(self):

        self.config.filename = self.get_subrip_path()
        self.config.write_to_file()


class TestContainer(TestCase):

    def setup_method(self, method):

        config = wrappers.Config(CONFIG_FILE, SPEC_FILE)
        self.container = wrappers.Container(config["output_window"])

    def test___getattr__(self):

        assert isinstance(self.container.show, bool)
        assert isinstance(self.container.size, list)

    def test___setattr__(self):

        self.container.show = False
        if not "show" in self.container.root.defaults:
            self.container.root.defaults.append("show")
        self.container.show = False
        assert self.container.root["show"] is False
        assert "show" in self.container.root.defaults

        self.container.size = [200, 200]
        if not "size" in self.container.root.defaults:
            self.container.root.defaults.append("size")
        self.container.size = [100, 100]
        assert self.container.root["size"] == [100, 100]
        assert not "size" in self.container.root.defaults
