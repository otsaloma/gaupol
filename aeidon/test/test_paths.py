# Copyright (C) 2005-2009 Osmo Salomaa
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

import aeidon
import imp
import os
import sys


class TestModule(aeidon.TestCase):

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_config_home_dir__windows(self):
        sys.platform = "win32"
        imp.reload(aeidon.paths)
        assert hasattr(aeidon, "CONFIG_HOME_DIR")

    @aeidon.deco.monkey_patch(os, "environ")
    def test_config_home_dir__xdg_environment(self):
        os.environ["XDG_CONFIG_HOME"] = "xdg"
        imp.reload(aeidon.paths)
        assert hasattr(aeidon, "CONFIG_HOME_DIR")

    @aeidon.deco.monkey_patch(os, "environ")
    def test_config_home_dir__xdg_no_environment(self):
        os.environ.clear()
        imp.reload(aeidon.paths)
        assert hasattr(aeidon, "CONFIG_HOME_DIR")

    @aeidon.deco.monkey_patch(sys, "frozen")
    def test_data_dir__py2exe(self):
        sys.frozen = "py2exe"
        imp.reload(aeidon.paths)
        assert hasattr(aeidon, "DATA_DIR")

    def test_data_dir__source(self):
        assert os.path.isdir(aeidon.DATA_DIR)

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_data_home_dir__windows(self):
        sys.platform = "win32"
        imp.reload(aeidon.paths)
        assert hasattr(aeidon, "DATA_HOME_DIR")

    @aeidon.deco.monkey_patch(os, "environ")
    def test_data_home_dir__xdg_environment(self):
        os.environ["XDG_DATA_HOME"] = "xdg"
        imp.reload(aeidon.paths)
        assert hasattr(aeidon, "DATA_HOME_DIR")

    @aeidon.deco.monkey_patch(os, "environ")
    def test_data_home_dir__xdg_no_environment(self):
        os.environ.clear()
        imp.reload(aeidon.paths)
        assert hasattr(aeidon, "DATA_HOME_DIR")

    @aeidon.deco.monkey_patch(sys, "frozen")
    def test_locale_dir__py2exe(self):
        sys.frozen = "py2exe"
        imp.reload(aeidon.paths)
        assert hasattr(aeidon, "LOCALE_DIR")

    def test_locale_dir__source(self):
        assert hasattr(aeidon, "LOCALE_DIR")
