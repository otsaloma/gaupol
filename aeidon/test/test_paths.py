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
import os
import sys


class TestModule(aeidon.TestCase):

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_config_home_dir__win32(self):
        sys.platform = "win32"
        reload(aeidon.paths)
        assert hasattr(aeidon, "CONFIG_HOME_DIR")

    @aeidon.deco.monkey_patch(os, "environ")
    def test_config_home_dir__xdg_environment(self):
        os.environ["XDG_CONFIG_HOME"] = "xdg"
        reload(aeidon.paths)
        assert hasattr(aeidon, "CONFIG_HOME_DIR")

    @aeidon.deco.monkey_patch(os, "environ")
    def test_config_home_dir__xdg_no_environment(self):
        os.environ.clear()
        reload(aeidon.paths)
        assert hasattr(aeidon, "CONFIG_HOME_DIR")

    @aeidon.deco.monkey_patch(sys, "frozen")
    def test_data_dir__py2exe(self):
        sys.frozen = "py2exe"
        reload(aeidon.paths)
        assert hasattr(aeidon, "DATA_DIR")

    def test_data_dir__source(self):
        assert os.path.isdir(nfoview.DATA_DIR)

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_data_home_dir__win32(self):
        sys.platform = "win32"
        reload(aeidon.paths)
        assert hasattr(aeidon, "DATA_HOME_DIR")

    @aeidon.deco.monkey_patch(os, "environ")
    def test_data_home_dir__xdg_environment(self):
        os.environ["XDG_DATA_HOME"] = "xdg"
        reload(aeidon.paths)
        assert hasattr(aeidon, "DATA_HOME_DIR")

    @aeidon.deco.monkey_patch(os, "environ")
    def test_data_home_dir__xdg_no_environment(self):
        os.environ.clear()
        reload(aeidon.paths)
        assert hasattr(aeidon, "DATA_HOME_DIR")

    @aeidon.deco.monkey_patch(sys, "frozen")
    def test_locale_dir__py2exe(self):
        sys.frozen = "py2exe"
        reload(aeidon.paths)
        assert hasattr(aeidon, "LOCALE_DIR")

    def test_locale_dir__source(self):
        assert hasattr(aeidon, "LOCALE_DIR")

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_xdg_copy_config_files(self):
        sys.platform = "linux2"
        mkdir = aeidon.temp.create_directory
        rmdir = aeidon.temp.remove_directory
        aeidon.paths.OBSOLETE_PROFILE_DIR = mkdir()
        aeidon.paths.CONFIG_HOME_DIR = mkdir()
        aeidon.paths.xdg_copy_config_files()
        rmdir(aeidon.paths.OBSOLETE_PROFILE_DIR)
        rmdir(aeidon.paths.CONFIG_HOME_DIR)

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_xdg_copy_data_files(self):
        sys.platform = "linux2"
        mkdir = aeidon.temp.create_directory
        rmdir = aeidon.temp.remove_directory
        aeidon.paths.OBSOLETE_PROFILE_DIR = mkdir()
        aeidon.paths.DATA_HOME_DIR = mkdir()
        aeidon.paths.xdg_copy_data_files()
        rmdir(aeidon.paths.OBSOLETE_PROFILE_DIR)
        rmdir(aeidon.paths.DATA_HOME_DIR)

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_xdg_copy_if_applicable(self):
        sys.platform = "linux2"
        mkdir = aeidon.temp.create_directory
        rmdir = aeidon.temp.remove_directory
        aeidon.paths.OBSOLETE_PROFILE_DIR = mkdir()
        aeidon.paths.CONFIG_HOME_DIR = mkdir()
        rmdir(aeidon.paths.CONFIG_HOME_DIR)
        aeidon.paths.DATA_HOME_DIR = mkdir()
        rmdir(aeidon.paths.DATA_HOME_DIR)
        aeidon.paths.xdg_copy_if_applicable()
        rmdir(aeidon.paths.OBSOLETE_PROFILE_DIR)
