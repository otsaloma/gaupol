# Copyright (C) 2005-2009 Osmo Salomaa
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

"""Reading, writing and manipulating text-based subtitle files.

:var BUG_REPORT_URL: Web page where to submit new bug reports
:var CONFIG_HOME_DIR: Path to the user's local configuration directory
:var DATA_DIR: Path to the global data directory
:var DATA_HOME_DIR: Path to the user's local data directory
:var HOMEPAGE_URL: Web page of the Gaupol project
:var LOCALE_DIR: Path to the global locale directory
:var REGEX_HELP_URL: Web page with documentation on regular expressions
"""

import os

debug = (bool(os.environ.get("AEIDON_DEBUG", "")) or
         bool(os.environ.get("GAUPOL_DEBUG", "")))

from aeidon.paths import *
from aeidon.urls import *
from aeidon import deco
from aeidon import i18n
from aeidon import util
from aeidon import temp
from aeidon.contractual import *
from aeidon.delegate import *
from aeidon.singleton import *
from aeidon.mutables import *
from aeidon.observable import *
from aeidon.enumeration import *
from aeidon.errors import *
from aeidon.unittest import *
