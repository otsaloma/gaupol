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


"""Names and codes for locales and conversions between them.

Module variable 'locales' is a set of locale codes for which spell-check
dictionaries are known to exist.
"""

from __future__ import with_statement

import gaupol
import os
import re
_ = gaupol.i18n._

locales = set()

def _init_locales():
    """Initialize the set of locale codes."""

    path = os.path.join(gaupol.DATA_DIR, "codes", "locales.txt")
    with open(path, "r") as fobj:
        lines = [x.strip() for x in fobj.readlines()]
        for line in (x for x in lines if x):
            locales.add(line)

def code_to_country_require(code):
    assert re.match(r"^[a-z][a-z](_[A-Z][A-Z])?$", code)

@gaupol.util.contractual
@gaupol.util.asserted_return
def code_to_country(code):
    """Convert locale code to localized country name.

    Raise KeyError if code not found.
    """
    assert len(code) == 5
    return gaupol.countries.code_to_name(code[-2:])

def code_to_language_require(code):
    assert re.match(r"^[a-z][a-z](_[A-Z][A-Z])?$", code)

@gaupol.util.contractual
def code_to_language(code):
    """Convert locale code to localized language name.

    Raise KeyError if code not found.
    """
    return gaupol.languages.code_to_name(code[:2])

def code_to_name_require(code):
    assert re.match(r"^[a-z][a-z](_[A-Z][A-Z])?$", code)

@gaupol.util.contractual
def code_to_name(code):
    """Convert locale code to localized name 'Language (Country)'.

    Raise KeyError if code not found.
    """
    language = code_to_language(code)
    country = code_to_country(code)
    if country is None:
        return language
    return _("%(language)s (%(country)s)") % locals()

@gaupol.util.once
def get_system_code():
    """The locale code preferred by system or None."""

    import locale
    return locale.getdefaultlocale()[0]

@gaupol.util.once
def get_system_modifier():
    """Get the script modifier of system or None."""

    import locale
    names = ["LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"]
    values = [os.environ.get(x) for x in names]
    values = [x for x in values if x is not None]
    values = [locale.normalize(x) for x in values]
    for value in (x for x in values if x.count("@")):
        return value[value.index("@") + 1:]
    return None

_init_locales()
