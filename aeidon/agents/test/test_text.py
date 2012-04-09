# -*- coding: utf-8-unix -*-

# Copyright (C) 2007-2009 Osmo Salomaa
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

import aeidon


class TestTextAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()

    def test_break_lines(self):
        # XXX: Give penalties once we have definitions.
        for subtitle in self.project.subtitles:
            subtitle.main_text = subtitle.main_text.replace(" ", "\n")
        self.project.break_lines(self.project.get_all_indices(),
                                 aeidon.documents.MAIN,
                                 patterns=[],
                                 length_func=len,
                                 max_length=44,
                                 max_lines=2)

        for subtitle in self.project.subtitles:
            assert subtitle.main_text.count("\n") <= 2

    def test_capitalize(self):
        for subtitle in self.project.subtitles:
            subtitle.main_text = "test. test i."
        manager = aeidon.PatternManager("capitalization")
        self.project.capitalize(self.project.get_all_indices(),
                                aeidon.documents.MAIN,
                                manager.get_patterns("Latn", "en"))

        for subtitle in self.project.subtitles:
            assert subtitle.main_text == "Test. Test I."

    def test_correct_common_errors(self):
        self.project.subtitles[0].main_text = "''Test''"
        self.project.subtitles[1].main_text = "123o456o789"
        manager = aeidon.PatternManager("common-error")
        self.project.correct_common_errors(self.project.get_all_indices(),
                                           aeidon.documents.MAIN,
                                           manager.get_patterns("Latn"))

        assert self.project.subtitles[0].main_text == '"Test"'
        assert self.project.subtitles[1].main_text == "12304560789"

    def test_remove_hearing_impaired(self):
        orig_length = len(self.project.subtitles)
        self.project.subtitles[0].main_text = "[Boo] Test."
        self.project.subtitles[1].main_text = "[Boo]"
        manager = aeidon.PatternManager("hearing-impaired")
        patterns = manager.get_patterns("Latn")
        for pattern in patterns:
            pattern.enabled = True
        self.project.remove_hearing_impaired(self.project.get_all_indices(),
                                             aeidon.documents.MAIN,
                                             patterns)

        assert self.project.subtitles[0].main_text == "Test."
        assert len(self.project.subtitles) == orig_length - 1

    def test_spell_check_join_words(self):
        for subtitle in self.project.subtitles:
            subtitle.main_text = subtitle.main_text.replace("a", " a")
            subtitle.main_text = subtitle.main_text.replace("e", "e ")
        self.project.spell_check_join_words(indices=None,
                                            doc=aeidon.documents.MAIN,
                                            language="en")

    def test_spell_check_join_words__enchant_error(self):
        import enchant
        self.assert_raises(enchant.Error,
                           self.project.spell_check_join_words,
                           indices=None,
                           doc=aeidon.documents.MAIN,
                           language="xx")

    def test_spell_check_split_words(self):
        for subtitle in self.project.subtitles:
            subtitle.main_text = subtitle.main_text.replace("s ", "s")
            subtitle.main_text = subtitle.main_text.replace("y ", "y")
        self.project.spell_check_split_words(indices=None,
                                             doc=aeidon.documents.MAIN,
                                             language="en")

    def test_spell_check_split_words__enchant_error(self):
        import enchant
        self.assert_raises(enchant.Error,
                           self.project.spell_check_split_words,
                           indices=None,
                           doc=aeidon.documents.MAIN,
                           language="xx")
