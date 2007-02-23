# Copyright (C) 2005-2007 Osmo Salomaa
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

from gaupol import cons
from gaupol.unittest import TestCase, reversion_test


MAIN = cons.DOCUMENT.MAIN
TRAN = cons.DOCUMENT.TRAN


class TestSearchAgent(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = self.project.find_next.im_self

        for texts in (self.project.main_texts, self.project.tran_texts):
            texts[0] = \
                "God has promised you that\n" + \
                "you will go to Heaven?"
            texts[1] = \
                "So you are certain of\n" + \
                "being saved?"
            texts[2] = \
                "Be careful,\n" + \
                "it's a dangerous answer."

        rows = range(3, len(self.project.main_texts))
        self.project.remove_subtitles(rows, register=None)

    def test_find_next(self):

        cases = (
            (r"^", [MAIN], True, (
                (0, MAIN, ( 0,  0)),
                (0, MAIN, (26, 26)),
                (1, MAIN, ( 0,  0)),
                (1, MAIN, (22, 22)),
                (2, MAIN, ( 0,  0)),
                (2, MAIN, (12, 12)),
                (0, MAIN, ( 0,  0)))),
            (r"$", [MAIN, TRAN], True, (
                (0, MAIN, (25, 25)),
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
                (0, MAIN, (25, 25)))),
            (r"\n", [TRAN], True, (
                (0, TRAN, (25, 26)),
                (1, TRAN, (21, 22)),
                (2, TRAN, (11, 12)),
                (0, TRAN, (25, 26)))),
            (r" t", [MAIN], False, (
                (0, MAIN, (20, 22)),
                (0, MAIN, (37, 39)),
                StopIteration)),
            (r"l{2}", [TRAN], False, (
                (0, TRAN, (32, 34)),
                StopIteration)),
            (r"xxx", [MAIN, TRAN], False, (
                StopIteration,)))

        for pattern, docs, wrap, matches in cases:
            self.project.set_find_target(None, docs, wrap)
            self.project.set_find_regex(pattern, re.DOTALL)
            row = 0
            doc = docs[0]
            pos = None
            for match in matches:
                if match is StopIteration:
                    try:
                        self.project.find_next(row, doc, pos)
                        raise AssertionError
                    except StopIteration:
                        continue
                assert self.project.find_next(row, doc, pos) == match
                row = match[0]
                doc = match[1]
                pos = match[2][1]

    def test_find_previous(self):

        cases = (
            (r"^", [MAIN], True, (
                (2, MAIN, (12, 12)),
                (2, MAIN, ( 0,  0)),
                (1, MAIN, (22, 22)),
                (1, MAIN, ( 0,  0)),
                (0, MAIN, (26, 26)),
                (0, MAIN, ( 0,  0)),
                (2, MAIN, (12, 12)))),
            (r"$", [MAIN, TRAN], True, (
                (2, TRAN, (36, 36)),
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
                (2, TRAN, (36, 36)))),
            (r"\n", [TRAN], True, (
                (2, TRAN, (11, 12)),
                (1, TRAN, (21, 22)),
                (0, TRAN, (25, 26)),
                (2, TRAN, (11, 12)))),
            (r" t", [MAIN], False, (
                (0, MAIN, (37, 39)),
                (0, MAIN, (20, 22)),
                StopIteration)),
            (r"l{2}", [TRAN], False, (
                (0, TRAN, (32, 34)),
                StopIteration)),
            (r"xxx", [MAIN, TRAN], False, (
                StopIteration,)))

        for pattern, docs, wrap, matches in cases:
            self.project.set_find_target(None, docs, wrap)
            self.project.set_find_regex(pattern, re.DOTALL)
            row = 2
            doc = docs[-1]
            pos = None
            for match in matches:
                if match is StopIteration:
                    try:
                        self.project.find_previous(row, doc, pos)
                        raise AssertionError
                    except StopIteration:
                        continue
                assert self.project.find_previous(row, doc, pos) == match
                row = match[0]
                doc = match[1]
                pos = match[2][0]

    @reversion_test
    def test_replace_next(self):

        self.project.set_find_target(None, [MAIN])
        self.project.set_find_regex(r"\b\s")
        self.project.set_find_replacement("")
        self.project.find_next(0, MAIN, 4)
        self.project.replace()
        assert self.project.main_texts[0] == \
            "God haspromised you that\n" + \
            "you will go to Heaven?"

    @reversion_test
    def test_replace_previous(self):

        self.project.set_find_target(None, [MAIN])
        self.project.set_find_regex(r"\b\s")
        self.project.set_find_replacement("")
        self.project.find_previous(2, MAIN)
        self.project.replace()
        assert self.project.main_texts[2] == \
            "Be careful,\n" + \
            "it's a dangerousanswer."

    @reversion_test
    def test_replace_all_regex(self):

        self.project.set_find_target(None, [MAIN, TRAN])
        self.project.set_find_regex(r"$")
        self.project.set_find_replacement("--")
        self.project.replace_all()
        for texts in (self.project.main_texts, self.project.tran_texts):
            assert texts[0] == \
                "God has promised you that--\n" + \
                "you will go to Heaven?--"
            assert texts[1] == \
                "So you are certain of--\n" + \
                "being saved?--"
            assert texts[2] == \
                "Be careful,--\n" + \
                "it's a dangerous answer.--"

    @reversion_test
    def test_replace_all_string(self):

        self.project.set_find_target(None, [MAIN, TRAN])
        self.project.set_find_string("a")
        self.project.set_find_replacement("-")
        self.project.replace_all()
        for texts in (self.project.main_texts, self.project.tran_texts):
            assert texts[0] == \
                "God h-s promised you th-t\n" + \
                "you will go to He-ven?"
            assert texts[1] == \
                "So you -re cert-in of\n" + \
                "being s-ved?"
            assert texts[2] == \
                "Be c-reful,\n" + \
                "it's - d-ngerous -nswer."

    def test_set_find_regex(self):

        flags = re.DOTALL | re.MULTILINE | re.UNICODE
        self.project.set_find_regex(r"test")
        assert self.delegate._finder.pattern.pattern == r"test"
        assert self.delegate._finder.pattern.flags == flags

        self.project.set_find_regex(r"test", re.IGNORECASE)
        assert self.delegate._finder.pattern.pattern == r"test"
        assert self.delegate._finder.pattern.flags == flags | re.IGNORECASE

        try:
            self.project.set_find_regex(r"*(")
            raise AssertionError
        except re.error:
            pass

    def test_set_find_replacement(self):

        self.project.set_find_replacement("test")
        assert self.delegate._finder.replacement == "test"

    def test_set_find_string(self):

        self.project.set_find_string("")
        assert self.delegate._finder.pattern == ""
        assert self.delegate._finder.ignore_case == False

        self.project.set_find_string("test", True)
        assert self.delegate._finder.pattern == "test"
        assert self.delegate._finder.ignore_case == True

    def test_set_find_target(self):

        self.project.set_find_target()
        assert self.delegate._rows == []
        assert self.delegate._docs == [MAIN, TRAN]
        assert self.delegate._wrap == True

        self.project.set_find_target([1], [MAIN], False)
        assert self.delegate._rows == [1]
        assert self.delegate._docs == [MAIN]
        assert self.delegate._wrap == False
