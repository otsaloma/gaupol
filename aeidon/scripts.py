# -*- coding: utf-8 -*-

# Copyright (C) 2007 Osmo Salomaa
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

"""Names and ISO 15924 codes for scripts and conversions between them."""

import aeidon
import json
import os

from aeidon.i18n import d_

_scripts = {}


def _init_scripts():
    """Initialize the dictionary mapping codes to names."""
    # Prefer globally installed, fall back on possibly bundled.
    path = "/usr/share/iso-codes/json/iso_15924.json"
    if os.path.isfile(path):
        return _init_scripts_json(path)
    path = os.path.join(aeidon.DATA_DIR, "iso-codes", "iso_15924.json")
    if os.path.isfile(path):
        return _init_scripts_json(path)

def _init_scripts_json(path):
    """Initialize the dictionary mapping codes to names."""
    with open(path, "r", encoding="utf_8") as f:
        iso = json.load(f)
    for script in iso["15924"]:
        code = script.get("alpha_4", None)
        name = script.get("name", None)
        if not code or not name: continue
        _scripts[code] = name

def code_to_name(code):
    """Convert ISO 15924 `code` to localized script name."""
    if not _scripts:
        _init_scripts()
    with aeidon.util.silent(LookupError):
        return d_("iso_15924", _scripts[code])
    return code

def is_valid(code):
    """Return ``True`` if `code` is a valid ISO 15924 script code."""
    if not _scripts:
        _init_scripts()
    return code in _scripts
