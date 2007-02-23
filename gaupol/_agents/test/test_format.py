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


from gaupol import cons
from gaupol.unittest import TestCase, reversion_test


class TestFormatAgent(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()

        self.project.main_texts[0] = \
            "In love? What's that?"
        self.project.main_texts[1] = \
            "<i>There's one thing I'd like</i>\n" + \
            "<i>to know, miss.</i>"
        self.project.main_texts[2] = \
            "- Yes, Mr. Johnson.\n" + \
            "- You've finished taking me"
        self.project.main_texts[3] = \
            "<i>- for an ass, or are you beginning?\n" + \
            "- Let go of me.</i>"

    @reversion_test
    def test_change_case_capitalize(self):

        self.project.change_case(range(4), cons.DOCUMENT.MAIN, "capitalize")
        assert self.project.main_texts[0] == \
            "In love? what's that?"
        assert self.project.main_texts[1] == \
            "<i>There's one thing i'd like</i>\n" + \
            "<i>to know, miss.</i>"
        assert self.project.main_texts[2] == \
            "- yes, mr. johnson.\n" + \
            "- you've finished taking me"
        assert self.project.main_texts[3] == \
            "<i>- for an ass, or are you beginning?\n" + \
            "- let go of me.</i>"

    @reversion_test
    def test_change_case_lower(self):

        self.project.change_case(range(4), cons.DOCUMENT.MAIN, "lower")
        assert self.project.main_texts[0] == \
            "in love? what's that?"
        assert self.project.main_texts[1] == \
            "<i>there's one thing i'd like</i>\n" + \
            "<i>to know, miss.</i>"
        assert self.project.main_texts[2] == \
            "- yes, mr. johnson.\n" + \
            "- you've finished taking me"
        assert self.project.main_texts[3] == \
            "<i>- for an ass, or are you beginning?\n" + \
            "- let go of me.</i>"

    @reversion_test
    def test_change_case_title(self):

        self.project.change_case(range(4), cons.DOCUMENT.MAIN, "title")
        assert self.project.main_texts[0] == \
            "In Love? What'S That?"
        assert self.project.main_texts[1] == \
            "<i>There'S One Thing I'D Like</i>\n" + \
            "<i>To Know, Miss.</i>"
        assert self.project.main_texts[2] == \
            "- Yes, Mr. Johnson.\n" + \
            "- You'Ve Finished Taking Me"
        assert self.project.main_texts[3] == \
            "<i>- For An Ass, Or Are You Beginning?\n" + \
            "- Let Go Of Me.</i>"

    @reversion_test
    def test_change_case_upper(self):

        self.project.change_case(range(4), cons.DOCUMENT.MAIN, "upper")
        assert self.project.main_texts[0] == \
            "IN LOVE? WHAT'S THAT?"
        assert self.project.main_texts[1] == \
            "<i>THERE'S ONE THING I'D LIKE</i>\n" + \
            "<i>TO KNOW, MISS.</i>"
        assert self.project.main_texts[2] == \
            "- YES, MR. JOHNSON.\n" + \
            "- YOU'VE FINISHED TAKING ME"
        assert self.project.main_texts[3] == \
            "<i>- FOR AN ASS, OR ARE YOU BEGINNING?\n" + \
            "- LET GO OF ME.</i>"

    @reversion_test
    def test_toggle_dialogue_lines_all(self):

        self.project.toggle_dialogue_lines([2, 3], cons.DOCUMENT.MAIN)
        assert self.project.main_texts[2] == \
            "Yes, Mr. Johnson.\n" + \
            "You've finished taking me"
        assert self.project.main_texts[3] == \
            "<i>for an ass, or are you beginning?\n" + \
            "Let go of me.</i>"

    @reversion_test
    def test_toggle_dialogue_lines_none(self):

        self.project.toggle_dialogue_lines([0, 1], cons.DOCUMENT.MAIN)
        assert self.project.main_texts[0] == \
            "- In love? What's that?"
        assert self.project.main_texts[1] == \
            "<i>- There's one thing I'd like</i>\n" + \
            "<i>- to know, miss.</i>"

    @reversion_test
    def test_toggle_dialogue_lines_partial(self):

        self.project.toggle_dialogue_lines([1, 2], cons.DOCUMENT.MAIN)
        assert self.project.main_texts[1] == \
            "<i>- There's one thing I'd like</i>\n" + \
            "<i>- to know, miss.</i>"
        assert self.project.main_texts[2] == \
            "- Yes, Mr. Johnson.\n" + \
            "- You've finished taking me"

    @reversion_test
    def test_toggle_italicization_all(self):

        self.project.toggle_italicization([1, 3], cons.DOCUMENT.MAIN)
        assert self.project.main_texts[1] == \
            "There's one thing I'd like\n" + \
            "to know, miss."
        assert self.project.main_texts[3] == \
            "- for an ass, or are you beginning?\n" + \
            "- Let go of me."

    @reversion_test
    def test_toggle_italicization_none(self):

        self.project.toggle_italicization([0, 2], cons.DOCUMENT.MAIN)
        assert self.project.main_texts[0] == \
            "<i>In love? What's that?</i>"
        assert self.project.main_texts[2] == \
            "<i>- Yes, Mr. Johnson.\n" + \
            "- You've finished taking me</i>"

    @reversion_test
    def test_toggle_italicization_partial(self):

        self.project.toggle_italicization([0, 1], cons.DOCUMENT.MAIN)
        assert self.project.main_texts[0] == \
            "<i>In love? What's that?</i>"
        assert self.project.main_texts[1] == \
            "<i>There's one thing I'd like\n" + \
            "to know, miss.</i>"
