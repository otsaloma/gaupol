# Copyright (C) 2007 Osmo Salomaa
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

import gaupol
import tempfile

from gaupol import unittest
from .. import patternman


class TestPatternManager(unittest.TestCase):

    def setup_method(self, method):

        self.manager = patternman.PatternManager("hearing-impaired")

    def test_get_patterns(self):

        patterns = self.manager.get_patterns("Latn")
        assert patterns
        for pattern in patterns:
            pattern.get_name()
            pattern.get_description()

    def test_save(self):

        directory = gaupol.PROFILE_DIR
        gaupol.PROFILE_DIR = tempfile.gettempdir()
        self.manager.save("Latn")
        self.manager._read_patterns()
        gaupol.PROFILE_DIR = directory
