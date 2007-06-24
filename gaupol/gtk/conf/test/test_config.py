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


import gaupol
import os

from gaupol.gtk import unittest
from .. import config


class TestConfig(unittest.TestCase):

    def setup_method(self, method):

        self.spec_file = os.path.join(gaupol.DATA_DIR, "conf.spec")
        self.config = config.Config(None, self.spec_file)

    def test_translate_none(self):

        assert self.config["editor"]["custom_font"] is None
        self.config.translate_none("editor", "custom_font", "")
        assert self.config["editor"]["custom_font"] == ""
        assert "custom_font" in self.config["editor"].defaults

    def test_write_to_file(self):

        self.config.filename = self.get_subrip_path()
        self.config.write_to_file()
        config.Config(self.config.filename, self.spec_file)
