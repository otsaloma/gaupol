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

import aeidon


class TestPatternManager(aeidon.TestCase):

    def setup_method(self, method):
        self.manager = aeidon.PatternManager("common-error")

    def test_get_countries(self):
        countries = self.manager.get_countries("Latn", "en")
        assert "US" in countries

    def test_get_languages(self):
        languages = self.manager.get_languages("Latn")
        assert "en" in languages

    def test_get_patterns(self):
        assert self.manager.get_patterns("Latn")
        assert self.manager.get_patterns("Latn", "en")
        assert self.manager.get_patterns("Latn", "en", "US")

    def test_get_patterns__policy_replace(self):
        self.manager = aeidon.PatternManager("line-break")
        assert self.manager.get_patterns("Latn", "en")

    def test_get_scripts(self):
        scripts = self.manager.get_scripts()
        assert "Latn" in scripts

    @aeidon.deco.monkey_patch(aeidon, "CONFIG_HOME_DIR")
    def test_save_config(self):
        aeidon.CONFIG_HOME_DIR = aeidon.temp.create_directory()
        self.manager.save_config("Latn")
        self.manager._read_patterns()
