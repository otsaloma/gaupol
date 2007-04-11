# Copyright (C) 2006-2007 Osmo Salomaa
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


import re

from gaupol.unittest import TestCase
from .. import scriptlib


class TestModule(TestCase):

    def test_get_capitalize_after(self):

        assert scriptlib._CAP_AFTERS
        for script, name, pattern in scriptlib._CAP_AFTERS:
            value = scriptlib.get_capitalize_after(script)
            re.compile(value)

    def test_get_clause_separator(self):

        assert scriptlib._CLAUSE_SEPS
        for script, name, pattern in scriptlib._CLAUSE_SEPS:
            value = scriptlib.get_clause_separator(script)
            re.compile(value)

    def test_get_dialogue_separator(self):

        assert scriptlib._DIALOGUE_SEPS
        for script, name, pattern in scriptlib._DIALOGUE_SEPS:
            value = scriptlib.get_dialogue_separator(script)
            re.compile(value)
