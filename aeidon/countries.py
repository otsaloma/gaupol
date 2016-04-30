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

"""Names and ISO 3166 codes for countries and conversions between them."""

import aeidon
import os

from aeidon.i18n import d_

_countries = {}


def _init_countries():
    """Initialize the dictionary mapping codes to names."""
    import xml.etree.ElementTree as ET
    path = "/usr/share/xml/iso-codes/iso_3166.xml"
    if not os.path.isfile(path):
        # Prefer files part of the iso-codes installation,
        # use bundled copy as fallback.
        path = os.path.join(aeidon.DATA_DIR, "iso-codes", "iso_3166.xml")
    for element in ET.parse(path).findall("iso_3166_entry"):
        code = element.get("alpha_2_code", None)
        name = element.get("name", None)
        if not code or not name: continue
        _countries[code] = name

def code_to_name(code):
    """Convert ISO 3166 `code` to localized country name."""
    if not _countries:
        _init_countries()
    with aeidon.util.silent(LookupError):
        return d_("iso_3166", _countries[code])
    return code

def is_valid(code):
    """Return ``True`` if `code` is a valid ISO 3166 country code."""
    if not _countries:
        _init_countries()
    return code in _countries
