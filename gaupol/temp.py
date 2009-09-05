# Copyright (C) 2007-2008 Osmo Salomaa
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

"""Creating and removing temporary files."""

import atexit
import gaupol
import os
import tempfile

_handles = {}


def close(path):
    """Close the OS-level handle to the file at path."""

    os.close(_handles[path])
    del _handles[path]

def create_ensure(value, suffix=""):
    assert os.path.isfile(value)

@gaupol.deco.contractual
def create(suffix=""):
    """Create a new temporary file and return its path."""

    handle, path = tempfile.mkstemp(suffix, "gaupol.")
    _handles[path] = handle
    return path

def create_directory_ensure(value, suffix=""):
    assert os.path.isdir(value)

@gaupol.deco.contractual
def create_directory(suffix=""):
    """Create a new temporary directory and return its path."""

    return tempfile.mkdtemp(suffix, "gaupol-")

def get_handle(path):
    """Return the OS-level handle to the file at path."""

    return _handles[path]

@gaupol.deco.silent(OSError)
def remove(path):
    """Remove temporary file after closing its handle."""

    if path in _handles:
        close(path)
    os.remove(path)

def remove_all():
    """Remove all temporary files after closing their handles."""

    for path in set(_handles.keys()):
        remove(path)

@gaupol.deco.silent(OSError)
def remove_directory(root):
    """Remove temporary directory and all its contents."""

    for name in os.listdir(root):
        path = os.path.join(root, name)
        if os.path.isdir(path):
            remove_directory(path)
        elif os.path.isfile(path):
            remove(path)
    os.rmdir(root)

atexit.register(remove_all)
