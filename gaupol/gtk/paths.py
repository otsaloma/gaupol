# Copyright (C) 2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Paths to files used.

Module variables:

    CONFIG_FILE, SPEC_FILE
"""


import os

from gaupol import paths
from gaupol.paths import *


__all__ = paths.__all__ + ["CONFIG_FILE", "SPEC_FILE"]

CONFIG_FILE = os.path.join(PROFILE_DIR, "gaupol.gtk.conf")
SPEC_FILE = os.path.join(DATA_DIR, "conf.spec")
