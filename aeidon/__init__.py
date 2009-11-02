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

:var align_methods: Enumerations for subtitle align methods
:var documents: Enumerations for document types
:var formats: Enumerations for subtitle file format types
:var framerates: Enumerations for framerate types
:var modes: Enumerations for position unit types
:var newlines: Enumerations for newline character types
:var players: Enumerations for video player application types
:var registers: Enumerations for action action reversion register types
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
from aeidon.errors import *
from aeidon.enum import *
from aeidon.enums.align import *
from aeidon.enums.documents import *
from aeidon.enums.formats import *
from aeidon.enums.framerates import *
from aeidon.enums.modes import *
from aeidon.enums.newlines import *
from aeidon.enums.players import *
from aeidon.enums.registers import *
from aeidon import encodings
from aeidon import languages
from aeidon import countries
from aeidon import locales
from aeidon import scripts
from aeidon.metadata import *
from aeidon.calculator import *
from aeidon.finder import *
from aeidon.parser import *
from aeidon.liner import *
from aeidon import containers
from aeidon.subtitle import *
from aeidon.file import *
from aeidon import files
from aeidon.markup import *
from aeidon import tags
from aeidon.converter import *
from aeidon.pattern import *
from aeidon.patternman import *
from aeidon.clipboard import *
from aeidon.revertable import *
from aeidon.unittest import *
