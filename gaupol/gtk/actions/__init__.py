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

"""UI manager actions."""

import gaupol.gtk

from gaupol.gtk.actions.edit import *
from gaupol.gtk.actions.file import *
from gaupol.gtk.actions.format import *
from gaupol.gtk.actions.help import *
from gaupol.gtk.actions.menu import *
from gaupol.gtk.actions.position import *
from gaupol.gtk.actions.search import *
from gaupol.gtk.actions.text import *
from gaupol.gtk.actions.view import *

__all__ = gaupol.util.get_all(dir(), r"Action$")
