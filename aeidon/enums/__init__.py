# Copyright (C) 2009 Osmo Salomaa
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

"""Miscellanous enumerations."""

import aeidon

aeidon.util.install_module("enums", lambda: None)

__all__ = ("align_methods",
           "documents",
           "formats",
           "framerates",
           "modes",
           "newlines",
           "players",)

from aeidon.enums.align import *
from aeidon.enums.documents import *
from aeidon.enums.formats import *
from aeidon.enums.framerates import *
from aeidon.enums.modes import *
from aeidon.enums.newlines import *
from aeidon.enums.players import *
