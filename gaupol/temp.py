# Copyright (C) 2007 Osmo Salomaa
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

"""Creating and removing temporary files."""

import gaupol
import os
import tempfile

_handles = {}


def close(path):
    """Close the OS-level handle to the file at path."""

    os.close(_handles[path])
    del _handles[path]

def create(suffix=""):
    """Create and new temporary file and return its path."""

    handle, path = tempfile.mkstemp(suffix, "gaupol.")
    _handles[path] = handle
    return path

def get_handle(path):
    """Get the OS-level handle to the file at path."""

    return _handles[path]

@gaupol.util.silent(OSError)
def remove(path):
    """Remove remporary file after closing its handle."""

    if path in _handles:
        close(path)
    os.remove(path)
