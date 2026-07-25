# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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

"""Paths to files and directories used."""

import os
import sys

from pathlib import Path

def get_config_home_directory():
    """Return path to the user's configuration directory."""
    if sys.platform == "win32":
        directory = os.environ.get("APPDATA") or Path.home()
        return (Path(directory) / "Gaupol").resolve()
    directory = os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config"
    return (Path(directory) / "gaupol").resolve()

def get_data_directory():
    """Return path to the aeidon data directory."""
    # Data files are shipped inside the Python package,
    # which works the same in all contexts.
    return Path(__file__).resolve().parent / "data"

def get_data_home_directory():
    """Return path to the user's data directory."""
    if sys.platform == "win32":
        directory = os.environ.get("APPDATA") or Path.home()
        return (Path(directory) / "Gaupol").resolve()
    default = Path.home() / ".local" / "share"
    directory = os.environ.get("XDG_DATA_HOME") or default
    return (Path(directory) / "gaupol").resolve()

CONFIG_HOME_DIR = get_config_home_directory()
DATA_DIR = get_data_directory()
DATA_HOME_DIR = get_data_home_directory()
