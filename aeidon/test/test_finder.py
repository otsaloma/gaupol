# Copyright (C) 2005-2007,2009 Osmo Salomaa
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
import re


class TestFinder(aeidon.TestCase):

    text = ("One only risks it, because\n"
            "one's survival depends on it.")

    def assert_find_cases(self, cases, regex, next):
        advance = (self.finder.__next__ if next else self.finder.previous)
        for pattern, matches in cases:
            self.finder.set_text(self.text, next)
            if regex:
                self.finder.set_regex(pattern)
            else: # String pattern.
                self.finder.pattern = pattern
            for match in matches:
                assert advance() == match
                assert self.finder.pos == match[next]
            self.assert_raises(StopIteration, advance)

    def assert_replace_all_cases(self, cases, regex):
        for pattern, replacement, count, text in cases:
            self.finder.set_text(self.text)
            if regex:
                self.finder.set_regex(pattern)
            else: # String pattern.
                self.finder.pattern = pattern
            self.finder.replacement = replacement
            assert self.finder.replace_all() == count
            assert self.finder.text == text

    def setup_method(self, method):
        self.finder = aeidon.Finder()

    def test_next__regex(self):
        cases = ((r"a", (
                    (22, 23),
                    (39, 40),)),
                 (r"it", (
                    (15, 17),
                    (53, 55),)),
                 (r"^", (
                    ( 0,  0),
                    (27, 27),)),
                 (r"\A", (
                    ( 0,  0),)),
                 (r"$", (
                    (26, 26),
                    (56, 56),)),
                 (r"\Z", (
                    (56, 56),)),
                 (r"\b", (
                    ( 0,  0),
                    ( 3,  3),
                    ( 4,  4),
                    ( 8,  8),
                    ( 9,  9),
                    (14, 14),
                    (15, 15),
                    (17, 17),
                    (19, 19),
                    (26, 26),
                    (27, 27),
                    (30, 30),
                    (31, 31),
                    (32, 32),
                    (33, 33),
                    (41, 41),
                    (42, 42),
                    (49, 49),
                    (50, 50),
                    (52, 52),
                    (53, 53),
                    (55, 55),)),
                 (r"\s", (
                    ( 3,  4),
                    ( 8,  9),
                    (14, 15),
                    (18, 19),
                    (26, 27),
                    (32, 33),
                    (41, 42),
                    (49, 50),
                    (52, 53),)),
                 (r"\w+", (
                    ( 0,  3),
                    ( 4,  8),
                    ( 9, 14),
                    (15, 17),
                    (19, 26),
                    (27, 30),
                    (31, 32),
                    (33, 41),
                    (42, 49),
                    (50, 52),
                    (53, 55),)),
                 (r"\W{2}", (
                    (17, 19),)))

        self.assert_find_cases(cases, True, True)

    def test_next__regex_ignore_case(self):
        cases = ((r"O" , (
                    ( 0,  1),
                    ( 4,  5),
                    (27, 28),
                    (50, 51),)),
                 (r"D", (
                    (42, 43),
                    (47, 48),)))

        self.finder.ignore_case = True
        self.assert_find_cases(cases, True, True)

    def test_next__string(self):
        cases = (("a" , (
                    (22, 23),
                    (39, 40),)),
                 ("it", (
                    (15, 17),
                    (53, 55),)),
                 ("O" , (
                    ( 0,  1),)),
                 (" ", (
                    ( 3,  4),
                    ( 8,  9),
                    (14, 15),
                    (18, 19),
                    (32, 33),
                    (41, 42),
                    (49, 50),
                    (52, 53),)),
                 ("\n", (
                    (26, 27),)),
                 ("." , (
                    (55, 56),)))

        self.assert_find_cases(cases, False, True)

    def test_next__string_ignore_case(self):
        cases = (("o" , (
                    ( 0,  1),
                    ( 4,  5),
                    (27, 28),
                    (50, 51),)),
                 ("k", (
                    (12, 13),)))

        self.finder.ignore_case = True
        self.assert_find_cases(cases, False, True)

    def test_previous__regex(self):
        cases = ((r"a" , (
                    (39, 40),
                    (22, 23),)),
                 (r"it", (
                    (53, 55),
                    (15, 17),)),
                 (r"^", (
                    (27, 27),
                    ( 0,  0),)),
                 (r"\A", (
                    ( 0,  0),)),
                 (r"$", (
                    (56, 56),
                    (26, 26),)),
                 (r"\Z", (
                    (56, 56),)),
                 (r"\b", (
                    (55, 55),
                    (53, 53),
                    (52, 52),
                    (50, 50),
                    (49, 49),
                    (42, 42),
                    (41, 41),
                    (33, 33),
                    (32, 32),
                    (31, 31),
                    (30, 30),
                    (27, 27),
                    (26, 26),
                    (19, 19),
                    (17, 17),
                    (15, 15),
                    (14, 14),
                    ( 9,  9),
                    ( 8,  8),
                    ( 4,  4),
                    ( 3,  3),
                    ( 0,  0),)),
                 (r"\s", (
                    (52, 53),
                    (49, 50),
                    (41, 42),
                    (32, 33),
                    (26, 27),
                    (18, 19),
                    (14, 15),
                    ( 8,  9),
                    ( 3,  4),)),
                 (r"\w+", (
                    (53, 55),
                    (50, 52),
                    (42, 49),
                    (33, 41),
                    (31, 32),
                    (27, 30),
                    (19, 26),
                    (15, 17),
                    ( 9, 14),
                    ( 4,  8),
                    ( 0,  3),)),
                 (r"\W{2}", (
                    (17, 19),)))

        self.assert_find_cases(cases, True, False)

    def test_previous__regex_ignore_case(self):
        cases = ((r"O" , (
                    (50, 51),
                    (27, 28),
                    ( 4,  5),
                    ( 0,  1),)),
                 (r"D", (
                    (47, 48),
                    (42, 43),)))

        self.finder.ignore_case = True
        self.assert_find_cases(cases, True, False)

    def test_previous__string(self):
        cases = (("a" , (
                    (39, 40),
                    (22, 23),)),
                 ("it", (
                    (53, 55),
                    (15, 17),)),
                 ("O" , (
                    (0, 1),)),
                 (" ", (
                    (52, 53),
                    (49, 50),
                    (41, 42),
                    (32, 33),
                    (18, 19),
                    (14, 15),
                    ( 8,  9),
                    ( 3,  4),)),
                 ("\n", (
                    (26, 27),)),
                 ("." , (
                    (55, 56),)))

        self.assert_find_cases(cases, False, False)

    def test_previous__string_ignore_case(self):
        cases = (("o" , (
                    (50, 51),
                    (27, 28),
                    ( 4,  5),
                    ( 0,  1),)),
                 ("k", (
                    (12, 13),)))

        self.finder.ignore_case = True
        self.assert_find_cases(cases, False, False)

    def test_replace__equal_length_next(self):
        self.finder.set_text(self.text)
        self.finder.pattern = "ne"
        self.finder.replacement = "--"
        next(self.finder)
        self.finder.replace()
        assert self.finder.text == (
            "O-- only risks it, because\n"
            "one's survival depends on it.")
        assert self.finder.pos == 3
        next(self.finder)
        self.finder.replace()
        assert self.finder.text == (
            "O-- only risks it, because\n"
            "o--'s survival depends on it.")
        assert self.finder.pos == 30
        self.assert_raises(StopIteration, self.finder.__next__)

    def test_replace__equal_length_previous(self):
        self.finder.set_text(self.text, False)
        self.finder.pattern = "ne"
        self.finder.replacement = "--"
        self.finder.previous()
        self.finder.replace(False)
        assert self.finder.text == (
            "One only risks it, because\n"
            "o--'s survival depends on it.")
        assert self.finder.pos == 28
        self.finder.previous()
        self.finder.replace(False)
        assert self.finder.text == (
            "O-- only risks it, because\n"
            "o--'s survival depends on it.")
        assert self.finder.pos == 1
        self.assert_raises(StopIteration, self.finder.previous)

    def test_replace__lengthen_regex_dollar_next(self):
        self.finder.set_text(self.text)
        self.finder.set_regex(r"$")
        self.finder.replacement = "--"
        next(self.finder)
        self.finder.replace()
        assert self.finder.text == (
            "One only risks it, because--\n"
            "one's survival depends on it.")
        assert self.finder.pos == 28
        next(self.finder)
        self.finder.replace()
        assert self.finder.text == (
            "One only risks it, because--\n"
            "one's survival depends on it.--")
        assert self.finder.pos == 60
        self.assert_raises(StopIteration, self.finder.__next__)

    def test_replace__lengthen_regex_dollar_previous(self):
        self.finder.set_text(self.text, False)
        self.finder.set_regex(r"$")
        self.finder.replacement = "--"
        self.finder.previous()
        self.finder.replace(False)
        assert self.finder.text == (
            "One only risks it, because\n"
            "one's survival depends on it.--")
        assert self.finder.pos == 56
        self.finder.previous()
        self.finder.replace(False)
        assert self.finder.text == (
            "One only risks it, because--\n"
            "one's survival depends on it.--")
        assert self.finder.pos == 26
        self.assert_raises(StopIteration, self.finder.previous)

    def test_replace__lengthen_regex_hat_next(self):
        self.finder.set_text(self.text)
        self.finder.set_regex(r"^")
        self.finder.replacement = "--"
        next(self.finder)
        self.finder.replace()
        assert self.finder.text == (
            "--One only risks it, because\n"
            "one's survival depends on it.")
        assert self.finder.pos == 2
        next(self.finder)
        self.finder.replace()
        assert self.finder.text == (
            "--One only risks it, because\n"
            "--one's survival depends on it.")
        assert self.finder.pos == 31
        self.assert_raises(StopIteration, self.finder.__next__)

    def test_replace__lengthen_regex_hat_previous(self):
        self.finder.set_text(self.text, False)
        self.finder.set_regex(r"^")
        self.finder.replacement = "--"
        self.finder.previous()
        self.finder.replace(False)
        assert self.finder.text == (
            "One only risks it, because\n"
            "--one's survival depends on it.")
        assert self.finder.pos == 27
        self.finder.previous()
        self.finder.replace(False)
        assert self.finder.text == (
            "--One only risks it, because\n"
            "--one's survival depends on it.")
        assert self.finder.pos == 0
        self.assert_raises(StopIteration, self.finder.previous)

    def test_replace__lengthen_string_match_next(self):
        self.finder.set_text(self.text)
        self.finder.pattern = "v"
        self.finder.replacement = "vv"
        next(self.finder)
        self.finder.replace()
        assert self.finder.text == (
            "One only risks it, because\n"
            "one's survvival depends on it.")
        assert self.finder.pos == 38
        next(self.finder)
        self.finder.replace()
        assert self.finder.text == (
            "One only risks it, because\n"
            "one's survvivval depends on it.")
        assert self.finder.pos == 41
        self.assert_raises(StopIteration, self.finder.__next__)

    def test_replace__lengthen_string_match_previous(self):
        self.finder.set_text(self.text, False)
        self.finder.pattern = "v"
        self.finder.replacement = "vv"
        self.finder.previous()
        self.finder.replace(False)
        assert self.finder.text == (
            "One only risks it, because\n"
            "one's survivval depends on it.")
        assert self.finder.pos == 38
        self.finder.previous()
        self.finder.replace(False)
        assert self.finder.text == (
            "One only risks it, because\n"
            "one's survvivval depends on it.")
        assert self.finder.pos == 36
        self.assert_raises(StopIteration, self.finder.previous)

    def test_replace__shorten_regex_next(self):
        self.finder.set_text(self.text)
        self.finder.set_regex(r"[.,]")
        self.finder.replacement = ""
        next(self.finder)
        self.finder.replace()
        assert self.finder.text == (
            "One only risks it because\n"
            "one's survival depends on it.")
        assert self.finder.pos == 17
        next(self.finder)
        self.finder.replace()
        assert self.finder.text == (
            "One only risks it because\n"
            "one's survival depends on it")
        assert self.finder.pos == 54
        self.assert_raises(StopIteration, self.finder.__next__)

    def test_replace__shorten_regex_previous(self):
        self.finder.set_text(self.text, False)
        self.finder.set_regex(r"[.,]")
        self.finder.replacement = ""
        self.finder.previous()
        self.finder.replace(False)
        assert self.finder.text == (
            "One only risks it, because\n"
            "one's survival depends on it")
        assert self.finder.pos == 55
        self.finder.previous()
        self.finder.replace(False)
        assert self.finder.text == (
            "One only risks it because\n"
            "one's survival depends on it")
        assert self.finder.pos == 17
        self.assert_raises(StopIteration, self.finder.previous)

    def test_replace_all__regex(self):
        cases = ((r"e", r"-", 6,
                  ("On- only risks it, b-caus-\n"
                   "on-'s survival d-p-nds on it.")),
                 (r"\b", r"-", 22,
                  ("-One- -only- -risks- -it-, -because-\n"
                   "-one-'-s- -survival- -depends- -on- -it-.")),
                 (r"\s", r"", 9,
                  ("Oneonlyrisksit,because"
                   "one'ssurvivaldependsonit.")),
                 (r"^", r"-", 2,
                  ("-One only risks it, because\n"
                   "-one's survival depends on it.")),
                 (r"\A", r"-", 1,
                  ("-One only risks it, because\n"
                   "one's survival depends on it.")),
                 (r"$", r"-", 2,
                  ("One only risks it, because-\n"
                   "one's survival depends on it.-")),
                 (r"\Z", r"-", 1,
                  ("One only risks it, because\n"
                   "one's survival depends on it.-")),
                 (r"\W", r"-", 12,
                  ("One-only-risks-it--because-"
                   "one-s-survival-depends-on-it-")),
                 (r".", r"-" , 56, "-" *  56),
                 (r".", r"..", 56, "." * 112),)

        self.assert_replace_all_cases(cases, True)

    def test_replace_all__string(self):
        cases = (("i", "-", 4,
                  ("One only r-sks -t, because\n"
                   "one's surv-val depends on -t.")),
                 (" ", "-", 8,
                  ("One-only-risks-it,-because\n"
                   "one's-survival-depends-on-it.")),
                 ("o", "oo", 3,
                  ("One oonly risks it, because\n"
                   "oone's survival depends oon it.")),
                 ("e", "" , 6,
                  ("On only risks it, bcaus\n"
                   "on's survival dpnds on it.")),
                 ("n", "n", 5,
                  ("One only risks it, because\n"
                   "one's survival depends on it.")))

        self.assert_replace_all_cases(cases, False)

    def test_set_regex(self):
        # pylint: disable=E1103
        flags = re.DOTALL | re.MULTILINE | re.UNICODE
        self.finder.set_regex("test")
        assert self.finder.pattern.pattern == "test"
        assert self.finder.pattern.flags == flags

    def test_set_regex__ignore_case(self):
        # pylint: disable=E1103
        flags = re.DOTALL | re.MULTILINE | re.UNICODE
        self.finder.set_regex("test", re.IGNORECASE)
        assert self.finder.pattern.pattern == "test"
        assert self.finder.pattern.flags == flags | re.IGNORECASE

    def test_set_text__next(self):
        self.finder.set_text("test")
        assert self.finder.text == "test"
        assert self.finder.match_span is None
        assert self.finder.pos == 0

    def test_set_text__previous(self):
        self.finder.set_text("test", False)
        assert self.finder.text == "test"
        assert self.finder.match_span is None
        assert self.finder.pos == 4
