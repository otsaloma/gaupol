# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Paths to files and directories used."""

import os
import sys

__all__ = ("DATA_DIR", "LIB_DIR", "LOCALE_DIR", "PROFILE_DIR",)

py2exe_subdirectories = {
    "data": ("share", "gaupol"),
    "lib": ("lib", "gaupol"),
    "locale": ("share", "locale"),}

source_subdirectories = {
    "data": ("data",),
    "lib": (),
    "locale": ("locale",),}


def get_directory(child):
    """Return full path to either py2exe or source directory."""

    if hasattr(sys, "frozen"):
        return get_py2exe_directory(child)
    return get_source_directory(child)

def get_profile_directory():
    """Return full path to the user profile directory."""

    if sys.platform == "win32":
        user_home = os.path.expanduser("~")
        directory = os.environ.get("APPDATA", user_home)
        directory = os.path.join(directory, "Gaupol")
        return os.path.abspath(directory)
    return os.path.join(os.path.expanduser("~"), ".gaupol")

def get_py2exe_directory(child):
    """Return full path to py2exe directory."""

    parent = os.path.dirname(sys.argv[0])
    children = py2exe_subdirectories[child]
    directory = os.path.join(parent, *children)
    return os.path.abspath(directory)

def get_source_directory(child):
    """Return full path to source directory."""

    parent = os.path.dirname(os.path.abspath(__file__))
    source = os.path.abspath(os.path.join(parent, ".."))
    children = source_subdirectories[child]
    directory = os.path.join(source, *children)
    return os.path.abspath(directory)

DATA_DIR = get_directory("data")
LIB_DIR = get_directory("lib")
LOCALE_DIR = get_directory("locale")
PROFILE_DIR = get_profile_directory()
