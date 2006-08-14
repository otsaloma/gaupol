# Copyright (C) 2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""
Script specific regular expression patterns.

Module variables:

    CAPITALIZE_AFTERS: Tuple of tuples: script name, pattern, flags

"""


from gettext import gettext as _
import re


CAPITALIZE_AFTERS = (
    (_('Latin'), r'([^\.]\w\.|\?|\!)(\s|$)', re.DOTALL),
)


def get_capitalize_after(script):
    """
    Get regular expression to capitalize after for script.

    Return pattern, flags.
    """
    for entry in CAPITALIZE_AFTERS:
        if entry[0] == script:
            return entry[1], entry[2]
    raise ValueError
