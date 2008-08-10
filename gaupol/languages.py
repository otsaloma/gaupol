# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Names and ISO 639 codes for languages and conversions between them."""

import gaupol
import os
import re

_languages = {}


def _init_languages():
    """Initialize the dictionary mapping codes to languages."""

    import xml.etree.ElementTree as ET
    path = os.path.join(gaupol.DATA_DIR, "codes", "iso_639.xml")
    for element in ET.parse(path).findall("iso_639_entry"):
        code = element.get("iso_639_1_code")
        name = element.get("name")
        if not all((code, name)): continue
        _languages[code] = name

def code_to_name_require(code):
    assert re.match(r"^[a-z][a-z]$", code)

@gaupol.deco.contractual
def code_to_name(code):
    """Convert ISO 639 code to localized language name.

    Raise KeyError if code not found.
    """
    return gaupol.i18n.dgettext("iso_639", _languages[code])

def is_valid_require(code):
    assert re.match(r"^[a-z][a-z]$", code)

@gaupol.deco.contractual
def is_valid(code):
    """Return True if code is a valid ISO 639 language code."""

    return (code in _languages)

_init_languages()
