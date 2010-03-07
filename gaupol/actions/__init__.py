# Copyright (C) 2007-2008,2010 Osmo Salomaa
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

""":class:`gtk.UIManager` actions for :class:`gaupol.Application`."""

import aeidon

from gaupol.actions.edit import *
from gaupol.actions.file import *
from gaupol.actions.format import *
from gaupol.actions.help import *
from gaupol.actions.menu import *
from gaupol.actions.position import *
from gaupol.actions.search import *
from gaupol.actions.text import *
from gaupol.actions.view import *

__all__ = tuple(filter(lambda x: x.endswith("Action"), dir()))
