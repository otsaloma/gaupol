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
import json
import os

from aeidon.i18n import d_

_countries = {}


def _init_countries():
    """Initialize the dictionary mapping codes to names."""
    # Prefer globally installed, fall back on possibly bundled.
    path = "/usr/share/iso-codes/json/iso_3166-1.json"
    if os.path.isfile(path):
        return _init_countries_json(path)
    path = os.path.join(aeidon.DATA_DIR, "iso-codes", "iso_3166-1.json")
    if os.path.isfile(path):
        return _init_countries_json(path)

def _init_countries_json(path):
    """Initialize the dictionary mapping codes to names."""
    with open(path, "r", encoding="utf_8") as f:
        iso = json.load(f)
    for country in iso["3166-1"]:
        code = country.get("alpha_2", None)
        name = country.get("name", None)
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
