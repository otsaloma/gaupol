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

"""Names and codes for locales and conversions between them.

Locale codes are of form ``aa[_BB][@Cccc]``, where ``aa`` is a language code,
``BB`` a country code and ``Cccc`` a script. See :mod:`aeidon.languages`,
:mod:`aeidon.countries` and :mod:`aeidon.scripts` for the details.
"""

import aeidon
import os
import re
_ = aeidon.i18n._


def code_to_country_require(code):
    assert re.match(r"^[a-z][a-z](_[A-Z][A-Z])?$", code)

@aeidon.deco.contractual
def code_to_country(code):
    """Convert locale `code` to localized country name or ``None``.

    Raise :exc:`KeyError` if `code` not found.
    """
    if len(code) < 5: return None
    return aeidon.countries.code_to_name(code[-2:])

def code_to_language_require(code):
    assert re.match(r"^[a-z][a-z](_[A-Z][A-Z])?$", code)

@aeidon.deco.contractual
def code_to_language(code):
    """Convert locale `code` to localized language name.

    Raise :exc:`KeyError` if `code` not found.
    """
    return aeidon.languages.code_to_name(code[:2])

def code_to_name_require(code):
    assert re.match(r"^[a-z][a-z](_[A-Z][A-Z])?$", code)

@aeidon.deco.contractual
def code_to_name(code):
    """Convert locale `code` to localized name.

    Raise :exc:`KeyError` if `code` not found.
    Return localized ``LANGUAGE (COUNTRY)``.
    """
    language = code_to_language(code)
    country = code_to_country(code)
    if country is None: return language
    return _("%(language)s (%(country)s)") % locals()

@aeidon.deco.once
def get_system_code():
    """Return the locale code preferred by system or ``None``."""
    import locale
    return locale.getdefaultlocale()[0]

@aeidon.deco.once
def get_system_modifier():
    """Return the script modifier of system or ``None``."""
    import locale
    names = ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG")
    values = list(map(os.environ.get, names))
    values = [_f for _f in values if _f]
    for value in (x for x in values if x.count("@")):
        return value[value.index("@") + 1:value.index("@") + 5]
    return None
