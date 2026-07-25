# -*- coding: utf-8 -*-

# Copyright (C) 2026 Osmo Salomaa
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

import sys

from pathlib import Path

def get_data_directory():
    """Return path to the gaupol data directory."""
    # Data files are shipped inside the Python package,
    # which works the same in all contexts.
    return Path(__file__).resolve().parent / "data"

def get_locale_directory():
    """Return path to the locale directory."""
    if hasattr(sys, "frozen"):
        # Windows bundled exe
        prefix = Path(sys.executable).parent.parent
        return (prefix / "share" / "locale").resolve()
    # Running from the source directory.
    root = Path(__file__).resolve().parent.parent
    return (root / "locale").resolve()

DATA_DIR = get_data_directory()

# Overwritten when installing.
LOCALE_DIR = get_locale_directory()
