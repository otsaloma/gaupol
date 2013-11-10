# -*- coding: utf-8 -*-

# Copyright (C) 2007-2009,2013 Osmo Salomaa
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

"""Creating and removing temporary files and directories."""

import aeidon
import atexit
import os
import tempfile

_paths = []


def create_ensure(value, suffix=""):
    assert os.path.isfile(value)

@aeidon.deco.contractual
def create(suffix=""):
    """Create a new temporary file and return its path."""
    handle, path = tempfile.mkstemp(suffix, "gaupol-")
    # Avoid PermissionErrors etc. on Windows by closing
    # the handle and returning only the path which will
    # be opened and closed separately.
    os.close(handle)
    _paths.append(path)
    return path

def create_directory_ensure(value, suffix=""):
    assert os.path.isdir(value)

@aeidon.deco.contractual
def create_directory(suffix=""):
    """Create a new temporary directory and return its path."""
    path = tempfile.mkdtemp(suffix, "gaupol-")
    _paths.append(path)
    return path

def remove(path):
    """Remove temporary file or directory at `path`."""
    if os.path.isfile(path):
        try: os.remove(path)
        except OSError: pass
    if os.path.isdir(path):
        for name in os.listdir(path):
            remove(os.path.join(path, name))
        try: os.rmdir(path)
        except OSError: pass

def remove_all():
    """Remove all temporary files and directories."""
    for path in _paths:
        remove(path)

atexit.register(remove_all)
