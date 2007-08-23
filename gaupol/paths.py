# Copyright (C) 2005-2007 Osmo Salomaa
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

"""Paths to files used."""

import os
import sys

__all__ = ["DATA_DIR", "LOCALE_DIR", "PROFILE_DIR"]

def get_directory(child):
    parent = os.path.dirname(os.path.abspath(__file__))
    prefix = os.path.abspath(os.path.join(parent, ".."))
    return os.path.abspath(os.path.join(prefix, child))

DATA_DIR = get_directory("data")
LOCALE_DIR = get_directory("locale")
PROFILE_DIR = os.path.join(os.path.expanduser("~"), ".gaupol")

if hasattr(sys, "frozen"):
    # Handle the special case of py2exe installations.
    DATA_DIR = get_directory(os.path.join("..", "share", "gaupol"))
    LOCALE_DIR = get_directory(os.path.join("..", "share", "locale"))

del get_directory
