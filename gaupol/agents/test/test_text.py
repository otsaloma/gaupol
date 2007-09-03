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

from gaupol import unittest


class TestTextAgent(unittest.TestCase):

    def setup_method(self, method):

        self.project = self.get_project()

    def test_break_lines(self):

        for subtitle in self.project.subtitles:
            subtitle.main_text = subtitle.main_text.replace(" ", "\n")
        doc = gaupol.DOCUMENT.MAIN
        manager = gaupol.PatternManager("common-error")
        patterns = manager.get_patterns("Latn")
        self.project.break_lines(None, doc, patterns, len, 44, 2, 1, True)
        for subtitle in self.project.subtitles:
            assert subtitle.main_text.count("\n") <= 2

    def test_correct_common_errors(self):

        self.project.subtitles[0].main_text = "''Test''"
        doc = gaupol.DOCUMENT.MAIN
        manager = gaupol.PatternManager("common-error")
        patterns = manager.get_patterns("Latn")
        self.project.correct_common_errors(None, doc, patterns)
        assert self.project.subtitles[0].main_text == '"Test"'

    def test_remove_hearing_impaired(self):

        orig_length = len(self.project.subtitles)
        self.project.subtitles[0].main_text = "[Boo] Test."
        self.project.subtitles[1].main_text = "[Boo]"
        doc = gaupol.DOCUMENT.MAIN
        manager = gaupol.PatternManager("hearing-impaired")
        patterns = manager.get_patterns("Latn")
        self.project.remove_hearing_impaired(None, doc, patterns)
        assert self.project.subtitles[0].main_text == "Test."
        assert len(self.project.subtitles) == orig_length - 1
