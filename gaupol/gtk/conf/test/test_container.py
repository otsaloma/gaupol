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

from gaupol import paths
from gaupol.gtk.unittest import TestCase
from .. import config, container


class TestContainer(TestCase):

    def setup_method(self, method):

        spec_file = os.path.join(paths.DATA_DIR, "conf.spec")
        root = config.Config(None, spec_file)
        self.root = root["output_window"]
        self.container = container.Container(self.root)

    def test___getattr__(self):

        assert isinstance(self.container.show, bool)
        assert isinstance(self.container.size, list)

    def test___setattr__(self):

        value = self.container.show
        self.container.show = value
        assert self.root["show"] is value
        assert "show" in self.root.defaults
        self.container.show = not value
        assert self.container.show is not value
        assert not "show" in self.root.defaults
