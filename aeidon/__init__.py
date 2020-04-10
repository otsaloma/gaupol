# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Reading, writing and manipulating text-based subtitle files.

:mod:`aeidon` is a Python package that provides classes and functions for
dealing with text-based subtitle files of many different formats. Functions
exist for reading and writing subtitle files as well as manipulating subtitle
data, i.e. positions (times or frames) and texts. Two examples of basic use
of the :mod:`aeidon` package follow below.

Converting a file from the SubRip format to the MicroDVD format::

    project = aeidon.Project()
    project.open_main("/path/to/file.srt", "utf_8")
    project.set_framerate(aeidon.framerates.FPS_23_976)
    project.save_main(aeidon.files.new(aeidon.formats.MICRODVD,
                                       "/path/to/file.sub",
                                       "utf_8"))

Making all subtitles in a file appear two seconds earlier::

    project = aeidon.Project()
    project.open_main("/path/to/file.srt", "utf_8")
    project.shift_positions(None, aeidon.as_seconds(-2))
    project.save_main()

:mod:`aeidon` handles positions as either times (as strings of form
``HH:MM:SS.SSS``), frames (as integers) or in some cases seconds (as floats).
All these can be used with functions that edit subtitle data regardless of what
the native position type of the file format used is.

:mod:`aeidon` handles two separate documents that comprise a project -- a main
and a translation document. These correspond to separate files, but the
subtitles are common since positions are shared.

:mod:`aeidon` includes an undo/redo-system. Any subtitle data-editing methods
of :class:`aeidon.Project` (ones marked with the :func:`aeidon.deco.revertable`
decorator) can be undone and redone. If using :mod:`aeidon` in a context where
reverting actions is never needed, greater flexibility can be achieved by
accessing the subtitles directly (via :attr:`aeidon.Project.subtitles`).

:var CONFIG_HOME_DIR: Path to the user's local configuration directory
:var DATA_DIR: Path to the global data directory
:var DATA_HOME_DIR: Path to the user's local data directory
:var LOCALE_DIR: Path to the global locale directory
:var RE_ANY_TAG: Regular expression for markup tags of any format

:var align_methods: Enumerations for subtitle align methods
:var documents: Enumerations for document types
:var formats: Enumerations for subtitle file format types
:var framerates: Enumerations for framerate types
:var modes: Enumerations for position unit types
:var newlines: Enumerations for newline character types
:var players: Enumerations for video player application types
:var registers: Enumerations for action action reversion register types
"""

import re
import sys

__version__ = "1.8"

RUNNING_SPHINX = (sys.argv[0].endswith("autogen.py") or
                  sys.argv[0].endswith("sphinx-build"))

RE_ANY_TAG = re.compile(r"(^[/\\_]+|<.*?>|\{.*?\})")

try:
    import gi
    gi.require_version("Gspell", "1")
except Exception:
    pass

from aeidon.paths import * # noqa
from aeidon.position import * # noqa
from aeidon import deco # noqa
from aeidon import i18n # noqa
from aeidon import util # noqa
from aeidon import temp # noqa
from aeidon.delegate import * # noqa
from aeidon.singleton import * # noqa
from aeidon.mutables import * # noqa
from aeidon.observable import * # noqa
from aeidon.errors import * # noqa
from aeidon.enum import * # noqa
from aeidon.enums import * # noqa
from aeidon import encodings # noqa
from aeidon import languages # noqa
from aeidon import countries # noqa
from aeidon import locales # noqa
from aeidon import scripts # noqa
from aeidon.metadata import * # noqa
from aeidon.calculator import * # noqa
from aeidon.finder import * # noqa
from aeidon.parser import * # noqa
from aeidon.liner import * # noqa
from aeidon import containers # noqa
from aeidon.subtitle import * # noqa
from aeidon.file import * # noqa
from aeidon import files # noqa
from aeidon.markup import * # noqa
from aeidon import markups # noqa
from aeidon.markupconv import * # noqa
from aeidon.pattern import * # noqa
from aeidon.patternman import * # noqa
from aeidon.clipboard import * # noqa
from aeidon.revertable import * # noqa
from aeidon.spell import * # noqa
from aeidon import agents # noqa
from aeidon.project import * # noqa
from aeidon.unittest import * # noqa
