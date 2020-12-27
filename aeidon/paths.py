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
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Paths to files and directories used."""

import os
import sys

__all__ = ("CONFIG_HOME_DIR", "DATA_DIR", "DATA_HOME_DIR", "LOCALE_DIR",)


def get_config_home_directory():
    """Return path to the user's configuration directory."""
    if sys.platform == "win32":
        return get_config_home_directory_windows()
    return get_config_home_directory_xdg()

def get_config_home_directory_windows():
    """Return path to the user's configuration directory on Windows."""
    directory = os.path.expanduser("~")
    directory = os.environ.get("APPDATA", directory)
    directory = os.path.join(directory, "Gaupol")
    return os.path.abspath(directory)

def get_config_home_directory_xdg():
    """Return path to the user's XDG configuration directory."""
    directory = os.path.join(os.path.expanduser("~"), ".config")
    directory = os.environ.get("XDG_CONFIG_HOME", directory)
    directory = os.path.join(directory, "gaupol")
    return os.path.abspath(directory)

def get_data_directory():
    """Return path to the global data directory."""
    if hasattr(sys, "frozen"):
        return get_data_directory_frozen()
    if os.path.isdir(get_data_directory_package()):
        return get_data_directory_package()
    return get_data_directory_source()

def get_data_directory_frozen():
    """Return path to the global data directory on ``frozen``."""
    directory = os.path.dirname(sys.argv[0])
    directory = os.path.join(directory, "share", "gaupol")
    return os.path.abspath(directory)

def get_data_directory_package():
    """Return path to the global data directory when data in the package."""
    directory = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(directory, "data")
    return os.path.abspath(directory)

def get_data_directory_source():
    """Return path to the global data directory when running from source."""
    directory = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.abspath(os.path.join(directory, ".."))
    directory = os.path.join(directory, "data")
    return os.path.abspath(directory)

def get_data_home_directory():
    """Return path to the user's data directory."""
    if sys.platform == "win32":
        return get_data_home_directory_windows()
    return get_data_home_directory_xdg()

def get_data_home_directory_windows():
    """Return path to the user's data directory on Windows."""
    directory = os.path.expanduser("~")
    directory = os.environ.get("APPDATA", directory)
    directory = os.path.join(directory, "Gaupol")
    return os.path.abspath(directory)

def get_data_home_directory_xdg():
    """Return path to the user's XDG data directory."""
    directory = os.path.expanduser("~/.local/share")
    directory = os.environ.get("XDG_DATA_HOME", directory)
    directory = os.path.join(directory, "gaupol")
    return os.path.abspath(directory)

def get_locale_directory():
    """Return path to the locale directory."""
    if hasattr(sys, "frozen"):
        return get_locale_directory_frozen()
    return get_locale_directory_source()

def get_locale_directory_frozen():
    """Return path to the locale directory on ``frozen``."""
    directory = os.path.dirname(sys.argv[0])
    directory = os.path.join(directory, "share", "locale")
    return os.path.abspath(directory)

def get_locale_directory_source():
    """Return path to the locale directory when running from source."""
    directory = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.abspath(os.path.join(directory, ".."))
    directory = os.path.join(directory, "locale")
    return os.path.abspath(directory)

CONFIG_HOME_DIR = get_config_home_directory()
DATA_DIR = get_data_directory()
DATA_HOME_DIR = get_data_home_directory()
LOCALE_DIR = get_locale_directory()
