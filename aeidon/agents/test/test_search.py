# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009 Osmo Salomaa
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
import re

MAIN = aeidon.documents.MAIN
TRAN = aeidon.documents.TRAN


class TestSearchAgent(aeidon.TestCase):

    def _test_find_next(self, pattern, docs, wrap, matches):
        self.project.set_search_target(None, docs, wrap)
        self.project.set_search_regex(pattern)
        index = None
        doc = docs[0]
        pos = None
        for match in matches:
            if match is StopIteration:
                self.assert_raises(StopIteration,
                                   self.project.find_next,
                                   index, doc, pos)

                continue
            value = self.project.find_next(index, doc, pos)
            assert value == match
            index = match[0]
            doc = match[1]
            pos = match[2][1]

    def _test_find_previous(self, pattern, docs, wrap, matches):
        self.project.set_search_target(None, docs, wrap)
        self.project.set_search_regex(pattern)
        index = None
        doc = docs[-1]
        pos = None
        for match in matches:
            if match is StopIteration:
                self.assert_raises(StopIteration,
                                   self.project.find_previous,
                                   index, doc, pos)

                continue
            value = self.project.find_previous(index, doc, pos)
            assert value == match
            index = match[0]
            doc = match[1]
            pos = match[2][0]

    def setup_method(self, method):
        self.project = self.new_project()
        self.delegate = self.project.find_next.__self__
        texts = (("God has promised you that\n"
                  "you will go to Heaven?"),
                 ("So you are certain of\n"
                  "being saved?"),
                 ("Be careful,\n"
                  "it's a dangerous answer."))

        for i, text in enumerate(texts):
            self.project.subtitles[i].main_text = text
            self.project.subtitles[i].tran_text = text
        indices = list(range(3, len(self.project.subtitles)))
        self.project.remove_subtitles(indices, register=None)

    def test_find_next__1(self):
        matches = ((0, MAIN, ( 0,  0)),
                   (0, MAIN, (26, 26)),
                   (1, MAIN, ( 0,  0)),
                   (1, MAIN, (22, 22)),
                   (2, MAIN, ( 0,  0)),
                   (2, MAIN, (12, 12)),
                   (0, MAIN, ( 0,  0)),)

        self._test_find_next(pattern=r"^",
                             docs=(MAIN,),
                             wrap=True,
                             matches=matches)

    def test_find_next__2(self):
        matches = ((0, MAIN, (25, 25)),
                   (0, MAIN, (48, 48)),
                   (1, MAIN, (21, 21)),
                   (1, MAIN, (34, 34)),
                   (2, MAIN, (11, 11)),
                   (2, MAIN, (36, 36)),
                   (0, TRAN, (25, 25)),
                   (0, TRAN, (48, 48)),
                   (1, TRAN, (21, 21)),
                   (1, TRAN, (34, 34)),
                   (2, TRAN, (11, 11)),
                   (2, TRAN, (36, 36)),
                   (0, MAIN, (25, 25)),)

        self._test_find_next(pattern=r"$",
                             docs=(MAIN, TRAN),
                             wrap=True,
                             matches=matches)

    def test_find_next__3(self):
        matches = ((0, TRAN, (25, 26)),
                   (1, TRAN, (21, 22)),
                   (2, TRAN, (11, 12)),
                   (0, TRAN, (25, 26)),)

        self._test_find_next(pattern=r"\n",
                             docs=(TRAN,),
                             wrap=True,
                             matches=matches)

    def test_find_next__4(self):
        matches = ((0, MAIN, (20, 22)),
                   (0, MAIN, (37, 39)),
                   StopIteration,)

        self._test_find_next(pattern=r" t",
                             docs=(MAIN,),
                             wrap=False,
                             matches=matches)

    def test_find_next__5(self):
        matches = ((0, TRAN, (32, 34)),
                   StopIteration,)

        self._test_find_next(pattern=r"l{2}",
                             docs=(TRAN,),
                             wrap=False,
                             matches=matches)

    def test_find_next__6(self):
        matches = (StopIteration,)
        self._test_find_next(pattern=r"xxx",
                             docs=(MAIN, TRAN),
                             wrap=False,
                             matches=matches)

    def test_find_next__7(self):
        matches = (StopIteration,)
        self._test_find_next(pattern=r"xxx",
                             docs=(MAIN, TRAN),
                             wrap=True,
                             matches=matches)

    def test_find_previous__1(self):
        matches = ((2, MAIN, (12, 12)),
                   (2, MAIN, ( 0,  0)),
                   (1, MAIN, (22, 22)),
                   (1, MAIN, ( 0,  0)),
                   (0, MAIN, (26, 26)),
                   (0, MAIN, ( 0,  0)),
                   (2, MAIN, (12, 12)),)

        self._test_find_previous(pattern=r"^",
                                 docs=(MAIN,),
                                 wrap=True,
                                 matches=matches)

    def test_find_previous__2(self):
        matches = ((2, TRAN, (36, 36)),
                   (2, TRAN, (11, 11)),
                   (1, TRAN, (34, 34)),
                   (1, TRAN, (21, 21)),
                   (0, TRAN, (48, 48)),
                   (0, TRAN, (25, 25)),
                   (2, MAIN, (36, 36)),
                   (2, MAIN, (11, 11)),
                   (1, MAIN, (34, 34)),
                   (1, MAIN, (21, 21)),
                   (0, MAIN, (48, 48)),
                   (0, MAIN, (25, 25)),
                   (2, TRAN, (36, 36)),)

        self._test_find_previous(pattern=r"$",
                                 docs=(MAIN, TRAN),
                                 wrap=True,
                                 matches=matches)

    def test_find_previous__3(self):
        matches = ((2, TRAN, (11, 12)),
                   (1, TRAN, (21, 22)),
                   (0, TRAN, (25, 26)),
                   (2, TRAN, (11, 12)),)

        self._test_find_previous(pattern=r"\n",
                                 docs=(TRAN,),
                                 wrap=True,
                                 matches=matches)

    def test_find_previous__4(self):
        matches = ((0, MAIN, (37, 39)),
                   (0, MAIN, (20, 22)),
                   StopIteration,)

        self._test_find_previous(pattern=r" t",
                                 docs=(MAIN,),
                                 wrap=False,
                                 matches=matches)

    def test_find_previous__5(self):
        matches = ((0, TRAN, (32, 34)),
                   StopIteration,)

        self._test_find_previous(pattern=r"l{2}",
                                 docs=(TRAN,),
                                 wrap=False,
                                 matches=matches)

    def test_find_previous__6(self):
        matches = (StopIteration,)
        self._test_find_previous(pattern=r"xxx",
                                 docs=(MAIN, TRAN),
                                 wrap=False,
                                 matches=matches)

    def test_find_previous__7(self):
        matches = (StopIteration,)
        self._test_find_previous(pattern=r"xxx",
                                 docs=(MAIN, TRAN),
                                 wrap=True,
                                 matches=matches)

    @aeidon.deco.reversion_test
    def test_replace(self):
        self.project.set_search_target(None, (MAIN,))
        self.project.set_search_regex(r"\b\s")
        self.project.set_search_replacement("")
        self.project.find_next(0, MAIN, 4)
        self.project.replace()
        assert self.project.subtitles[0].main_text == (
            "God haspromised you that\n"
            "you will go to Heaven?")

    @aeidon.deco.reversion_test
    def test_replace_all(self):
        self.project.set_search_target(None, (MAIN, TRAN))
        self.project.set_search_regex(r"$")
        self.project.set_search_replacement("--")
        self.project.replace_all()
        texts = (("God has promised you that--\n"
                  "you will go to Heaven?--"),
                 ("So you are certain of--\n"
                  "being saved?--"),
                 ("Be careful,--\n"
                  "it's a dangerous answer.--"))

        for i, text in enumerate(texts):
            assert self.project.subtitles[i].main_text == text
            assert self.project.subtitles[i].tran_text == text

    def test_set_search_regex(self):
        finder = self.delegate._finder
        self.project.set_search_regex(r"test")
        assert finder.pattern.pattern == r"test"
        assert finder.pattern.flags & re.DOTALL
        assert finder.pattern.flags & re.MULTILINE

    def test_set_search_regex__ignore_case(self):
        finder = self.delegate._finder
        self.project.set_search_regex(r"test", re.IGNORECASE)
        assert finder.pattern.pattern == r"test"
        assert finder.pattern.flags & re.IGNORECASE

    def test_set_search_replacement(self):
        self.project.set_search_replacement("test")
        assert self.delegate._finder.replacement == "test"

    def test_set_search_string(self):
        finder = self.delegate._finder
        self.project.set_search_string("")
        assert finder.pattern == ""
        assert finder.ignore_case == False

    def test_set_search_string__ignore_case(self):
        finder = self.delegate._finder
        self.project.set_search_string("test", True)
        assert finder.pattern == "test"
        assert finder.ignore_case == True

    def test_set_search_target(self):
        self.project.set_search_target((1,), (MAIN,), False)
        assert self.delegate._indices == (1,)
        assert self.delegate._docs == (MAIN,)
        assert self.delegate._wrap == False

    def test_set_search_target__none(self):
        self.project.set_search_target()
        assert self.delegate._indices == None
        assert self.delegate._docs == (MAIN, TRAN)
        assert self.delegate._wrap == True
