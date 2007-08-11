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

"""Editor for text-based subtitle files.

Module variables:
 * __version__: Version number as string
 * check_contracts: True to check contracts
"""

__version__ = "0.9"
check_contracts = True

from gaupol.paths import *
from gaupol.urls import *
from gaupol import util
from gaupol import temp
from gaupol.base import *
from gaupol import i18n
from gaupol.errors import *
from gaupol.const import *
from gaupol import encodings
from gaupol import languages
from gaupol import countries
from gaupol import locales
from gaupol import scripts
from gaupol.calculator import *
from gaupol.finder import *
from gaupol.parser import *
from gaupol.liner import *
from gaupol import files
from gaupol.determiner import *
from gaupol import tags
from gaupol.converter import *
from gaupol.subtitle import *
from gaupol.pattern import *
from gaupol.patternman import *
from gaupol.clipboard import *
from gaupol.revertable import *
from gaupol import agents
from gaupol.project import *
