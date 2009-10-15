# Copyright (C) 2007-2009 Osmo Salomaa
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

"""Names and ISO 15924 codes for scripts and conversions between them."""

import aeidon
import os
import re

_scripts = {}


def _init_scripts():
    """Initialize the dictionary mapping codes to scripts."""
    import xml.etree.ElementTree as ET
    path = os.path.join(aeidon.DATA_DIR, "iso-codes", "iso_15924.xml")
    for element in ET.parse(path).findall("iso_15924_entry"):
        code = element.get("alpha_4_code")
        name = element.get("name")
        if code and name:
            _scripts[code] = name

def code_to_name_require(code):
    assert re.match(r"^[A-Z][a-z]{3}$", code)

@aeidon.deco.contractual
def code_to_name(code):
    """Convert ISO 15924 `code` to localized script name.

    Raise :exc:`KeyError` if code not found.
    """
    return aeidon.i18n.dgettext("iso_15924", _scripts[code])

def is_valid_require(code):
    assert re.match(r"^[A-Z][a-z]{3}$", code)

@aeidon.deco.contractual
def is_valid(code):
    """Return ``True`` if `code` is a valid ISO 15924 script code."""
    return (code in _scripts)


_init_scripts()
