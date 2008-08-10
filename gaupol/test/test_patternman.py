# Copyright (C) 2007-2008 Osmo Salomaa
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

import gaupol
import tempfile


class TestPatternManager(gaupol.TestCase):

    def setup_method(self, method):

        self.manager = gaupol.PatternManager("hearing-impaired")

    def test_get_countries(self):

        self.manager.get_countries("Latn", "en")

    def test_get_languages(self):

        assert self.manager.get_languages("Latn")

    def test_get_patterns(self):

        assert self.manager.get_patterns("Latn")
        assert self.manager.get_patterns("Latn", "en")
        assert self.manager.get_patterns("Latn", "en", "GB")

    def test_get_patterns__policy_replace(self):

        self.manager = gaupol.PatternManager("line-break")
        assert self.manager.get_patterns("Latn", "en")

    def test_get_scripts(self):

        self.manager = gaupol.PatternManager("common-error")
        assert self.manager.get_scripts()

    def test_save_config(self):

        directory = gaupol.PROFILE_DIR
        gaupol.PROFILE_DIR = tempfile.gettempdir()
        self.manager.save_config("Latn")
        self.manager._read_patterns()
        gaupol.PROFILE_DIR = directory
