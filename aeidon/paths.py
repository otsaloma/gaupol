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

def get_config_home_directory():
    """Return path to the user's configuration directory."""
    if sys.platform == "win32":
        directory = os.environ.get("APPDATA") or os.path.expanduser("~")
        return os.path.abspath(os.path.join(directory, "Gaupol"))
    default = os.path.join(os.path.expanduser("~"), ".config")
    directory = os.environ.get("XDG_CONFIG_HOME") or default
    return os.path.abspath(os.path.join(directory, "gaupol"))

def get_data_directory():
    """Return path to the global data directory."""
    if hasattr(sys, "frozen"):
        # Windows bundled exe
        directory = os.path.dirname(sys.argv[0])
        return os.path.abspath(os.path.join(directory, "share", "gaupol"))
    directory = os.path.dirname(os.path.abspath(__file__))
    if os.path.isdir(os.path.join(directory, "data")):
        # Data files installed as part of the package.
        return os.path.join(directory, "data")
    # Running from the source directory.
    return os.path.abspath(os.path.join(directory, "..", "data"))

def get_data_home_directory():
    """Return path to the user's data directory."""
    if sys.platform == "win32":
        directory = os.environ.get("APPDATA") or os.path.expanduser("~")
        return os.path.abspath(os.path.join(directory, "Gaupol"))
    default = os.path.expanduser("~/.local/share")
    directory = os.environ.get("XDG_DATA_HOME") or default
    return os.path.abspath(os.path.join(directory, "gaupol"))

def get_locale_directory():
    """Return path to the locale directory."""
    if hasattr(sys, "frozen"):
        directory = os.path.dirname(sys.argv[0])
        return os.path.abspath(os.path.join(directory, "share", "locale"))
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(directory, "..", "locale"))

CONFIG_HOME_DIR = get_config_home_directory()
DATA_DIR = get_data_directory()
DATA_HOME_DIR = get_data_home_directory()
LOCALE_DIR = get_locale_directory()
