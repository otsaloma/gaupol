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

"""Names and ISO 639 codes for languages and conversions between them.

Module variable 'languages' maps ISO 639 two letter language codes to their
English language names. The 'code_to_name' function returns a localized
version of that language name if the 'iso-codes' gettext domain exists.
"""

import gaupol
import os
import re
import xml.etree.ElementTree as ET

languages = {}


def _init_languages():
    """Initialize the dictionary mapping codes to languages."""

    path = os.path.join(gaupol.DATA_DIR, "codes", "iso_639.xml")
    for element in ET.parse(path).findall("iso_639_entry"):
        code = element.get("iso_639_1_code")
        name = element.get("name")
        if not None in (code, name):
            languages[code] = name

def code_to_name_require(code):
    assert re.match(r"^[a-z][a-z]$", code)

@gaupol.util.contractual
def code_to_name(code):
    """Convert ISO 639 code to localized language name.

    Raise KeyError if code not found.
    """
    return gaupol.i18n.dgettext("iso_639", languages[code])

_init_languages()
