# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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

MAIN = aeidon.documents.MAIN
TRAN = aeidon.documents.TRAN


class TestSearchAgent(aeidon.TestCase):

    ######### 0000000000111111111122222222223333333333444444444
    ######### 0123456789012345678901234567890123456789012345678
    texts = ("God has promised you that\nyou will go to Heaven?",
             "So you are certain of\nbeing saved?",
             "Be careful,\nit's a dangerous answer.")

    def setup_method(self, method):
        self.project = self.new_project()
        for i, text in enumerate(self.texts):
            self.project.subtitles[i].main_text = text
            self.project.subtitles[i].tran_text = text
        indices = list(range(3, len(self.project.subtitles)))
        self.project.remove_subtitles(indices, register=None)

    def test_find_next(self):
        matches = iter(((0, MAIN, ( 0,  0)),
                        (0, MAIN, (26, 26)),
                        (1, MAIN, ( 0,  0)),
                        (1, MAIN, (22, 22)),
                        (2, MAIN, ( 0,  0)),
                        (2, MAIN, (12, 12)),
                        StopIteration))

        self.project.set_search_target(None, (MAIN,), wrap=False)
        self.project.set_search_regex(r"^")
        index, doc, pos = None, MAIN, None
        while True:
            try:
                index, doc, span = self.project.find_next(index, doc, pos)
                assert (index, doc, span) == next(matches)
                pos = span[1]
            except StopIteration:
                assert next(matches) is StopIteration
                break

    def test_find_previous(self):
        matches = iter(((1, MAIN, ( 3,  6)),
                        (0, MAIN, (26, 29)),
                        (0, MAIN, (17, 20)),
                        StopIteration))

        self.project.set_search_target(None, (MAIN,), wrap=False)
        self.project.set_search_string("you", ignore_case=False)
        index, doc, pos = None, MAIN, None
        while True:
            try:
                index, doc, span = self.project.find_previous(index, doc, pos)
                assert (index, doc, span) == next(matches)
                pos = span[0]
            except StopIteration:
                assert next(matches) is StopIteration
                break

    @aeidon.deco.reversion_test
    def test_replace(self):
        self.project.set_search_target(None, (MAIN,))
        self.project.set_search_regex(r"\b\s")
        self.project.set_search_replacement("")
        self.project.find_next(index=0, doc=MAIN, pos=4)
        self.project.replace()
        text = self.project.subtitles[0].main_text
        assert text == "God haspromised you that\nyou will go to Heaven?"

    @aeidon.deco.reversion_test
    def test_replace_all(self):
        self.project.set_search_target(None, (MAIN, TRAN))
        self.project.set_search_regex(r"$")
        self.project.set_search_replacement("--")
        self.project.replace_all()
        texts = ("God has promised you that--\nyou will go to Heaven?--",
                 "So you are certain of--\nbeing saved?--",
                 "Be careful,--\nit's a dangerous answer.--")

        for i, text in enumerate(texts):
            assert self.project.subtitles[i].main_text == text
            assert self.project.subtitles[i].tran_text == text
