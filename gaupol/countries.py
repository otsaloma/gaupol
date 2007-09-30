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

"""Names and ISO 3166 codes for countries and conversions between them.

Module variable 'countries' maps ISO 3166 two letter country codes to their
English language names. The 'code_to_name' function returns a localized
version of that country name if the 'iso_3166' gettext domain exists.
"""

import gaupol
import os
import re
import xml.etree.ElementTree as ET

countries = {}


def _init_countries():
    """Initialize the dictionary mapping codes to names."""

    path = os.path.join(gaupol.DATA_DIR, "codes", "iso_3166.xml")
    for element in ET.parse(path).findall("iso_3166_entry"):
        code = element.get("alpha_2_code")
        name = element.get("name")
        if not None in (code, name):
            countries[code] = name

def code_to_name_require(code):
    assert re.match(r"^[A-Z][A-Z]$", code)

@gaupol.util.contractual
def code_to_name(code):
    """Convert ISO 639 code to localized country name.

    Raise KeyError if code not found.
    """
    return gaupol.i18n.dgettext("iso_3166", countries[code])

_init_countries()
