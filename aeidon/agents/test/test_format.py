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


class TestFormatAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()

    def test_add_dialogue_dashes(self):
        self.project.subtitles[0].main_text = (
            "- You have cut your beard?\n"
            "- Yes, don't you like it?")
        self.project.subtitles[1].main_text = (
            "It was the only beautiful thing you had.\n"
            "Now you seem a different person.")
        self.project.add_dialogue_dashes((0, 1), MAIN)
        assert self.project.subtitles[0].main_text == (
            "- You have cut your beard?\n"
            "- Yes, don't you like it?")
        assert self.project.subtitles[1].main_text == (
            "- It was the only beautiful thing you had.\n"
            "- Now you seem a different person.")

    def test_change_case__dialogue(self):
        self.project.subtitles[0].main_text = (
            "- mrs. pavinato?\n"
            "- yes, what do you want?")
        self.project.change_case((0,), MAIN, "title")
        assert self.project.subtitles[0].main_text == (
            "- Mrs. Pavinato?\n"
            "- Yes, What Do You Want?")

    def test_change_case__italic(self):
        self.project.subtitles[0].main_text = (
            "<i>mrs. pavinato?</i>\n"
            "<i>yes, what do you want?</i>")
        self.project.change_case((0,), MAIN, "capitalize")
        assert self.project.subtitles[0].main_text == (
            "<i>Mrs. pavinato?</i>\n"
            "<i>yes, what do you want?</i>")

    def test_change_case__plain(self):
        self.project.subtitles[0].main_text = (
            "mrs. pavinato?\n"
            "yes, what do you want?")
        self.project.change_case((0,), MAIN, "upper")
        assert self.project.subtitles[0].main_text == (
            "MRS. PAVINATO?\n"
            "YES, WHAT DO YOU WANT?")

    def test_italicize(self):
        self.project.subtitles[0].main_text = (
            "<i>I am no thief, I am an officer\n"
            "and a university student.</i>")
        self.project.subtitles[1].main_text = (
            "I look like this because\n"
            "I'm hunted for by the Germans.")
        self.project.italicize((0, 1), MAIN)
        assert self.project.subtitles[0].main_text == (
            "<i>I am no thief, I am an officer\n"
            "and a university student.</i>")
        assert self.project.subtitles[1].main_text == (
            "<i>I look like this because\n"
            "I'm hunted for by the Germans.</i>")

    def test_remove_dialogue_dashes__all(self):
        self.project.subtitles[0].main_text = (
            "- You have cut your beard?\n"
            "- Yes, don't you like it?")
        self.project.subtitles[1].main_text = (
            "- It was the only beautiful thing you had.\n"
            "- Now you seem a different person.")
        self.project.remove_dialogue_dashes((0, 1), MAIN)
        assert self.project.subtitles[0].main_text == (
            "You have cut your beard?\n"
            "Yes, don't you like it?")
        assert self.project.subtitles[1].main_text == (
            "It was the only beautiful thing you had.\n"
            "Now you seem a different person.")

    def test_remove_dialogue_dashes__some(self):
        self.project.subtitles[0].main_text = (
            "- You have cut your beard?\n"
            "- Yes, don't you like it?")
        self.project.subtitles[1].main_text = (
            "It was the only beautiful thing you had.\n"
            "Now you seem a different person.")
        self.project.remove_dialogue_dashes((0, 1), MAIN)
        assert self.project.subtitles[0].main_text == (
            "You have cut your beard?\n"
            "Yes, don't you like it?")
        assert self.project.subtitles[1].main_text == (
            "It was the only beautiful thing you had.\n"
            "Now you seem a different person.")

    def test_toggle_dialogue_dashes__all(self):
        self.project.subtitles[0].main_text = (
            "- You have cut your beard?\n"
            "- Yes, don't you like it?")
        self.project.subtitles[1].main_text = (
            "- It was the only beautiful thing you had.\n"
            "- Now you seem a different person.")
        self.project.toggle_dialogue_dashes((0, 1), MAIN)
        assert self.project.subtitles[0].main_text == (
            "You have cut your beard?\n"
            "Yes, don't you like it?")
        assert self.project.subtitles[1].main_text == (
            "It was the only beautiful thing you had.\n"
            "Now you seem a different person.")

    def test_toggle_dialogue_dashes__none(self):
        self.project.subtitles[0].main_text = (
            "You have cut your beard?\n"
            "Yes, don't you like it?")
        self.project.subtitles[1].main_text = (
            "It was the only beautiful thing you had.\n"
            "Now you seem a different person.")
        self.project.toggle_dialogue_dashes((0, 1), MAIN)
        assert self.project.subtitles[0].main_text == (
            "- You have cut your beard?\n"
            "- Yes, don't you like it?")
        assert self.project.subtitles[1].main_text == (
            "- It was the only beautiful thing you had.\n"
            "- Now you seem a different person.")

    def test_toggle_dialogue_dashes__some(self):
        self.project.subtitles[0].main_text = (
            "- You have cut your beard?\n"
            "- Yes, don't you like it?")
        self.project.subtitles[1].main_text = (
            "It was the only beautiful thing you had.\n"
            "Now you seem a different person.")
        self.project.toggle_dialogue_dashes((0, 1), MAIN)
        assert self.project.subtitles[0].main_text == (
            "- You have cut your beard?\n"
            "- Yes, don't you like it?")
        assert self.project.subtitles[1].main_text == (
            "- It was the only beautiful thing you had.\n"
            "- Now you seem a different person.")

    def test_toggle_italicization__all(self):
        self.project.subtitles[0].main_text = (
            "<b><i>I am no thief, I am an officer\n"
            "and a university student.</i></b>")
        self.project.subtitles[1].main_text = (
            "<i><b>I look like this because\n"
            "I'm hunted for by the Germans.</b></i>")
        self.project.toggle_italicization((0, 1), MAIN)
        assert self.project.subtitles[0].main_text == (
            "<b>I am no thief, I am an officer\n"
            "and a university student.</b>")
        assert self.project.subtitles[1].main_text == (
            "<b>I look like this because\n"
            "I'm hunted for by the Germans.</b>")

    def test_toggle_italicization__none(self):
        self.project.subtitles[0].main_text = (
            "I am no thief, I am an officer\n"
            "and a university student.")
        self.project.subtitles[1].main_text = (
            "I look like this because\n"
            "I'm hunted for by the Germans.")
        self.project.toggle_italicization((0, 1), MAIN)
        assert self.project.subtitles[0].main_text == (
            "<i>I am no thief, I am an officer\n"
            "and a university student.</i>")
        assert self.project.subtitles[1].main_text == (
            "<i>I look like this because\n"
            "I'm hunted for by the Germans.</i>")

    def test_toggle_italicization__some(self):
        self.project.subtitles[0].main_text = (
            "<i>I am no thief, I am an officer\n"
            "and a university student.</i>")
        self.project.subtitles[1].main_text = (
            "I look like this because\n"
            "I'm hunted for by the Germans.")
        self.project.toggle_italicization((0, 1), MAIN)
        assert self.project.subtitles[0].main_text == (
            "<i>I am no thief, I am an officer\n"
            "and a university student.</i>")
        assert self.project.subtitles[1].main_text == (
            "<i>I look like this because\n"
            "I'm hunted for by the Germans.</i>")

    def test_unitalicize(self):
        self.project.subtitles[0].main_text = (
            "<i>I am no thief, I am an officer\n"
            "and a university student.</i>")
        self.project.subtitles[1].main_text = (
            "I look like this because\n"
            "I'm hunted for by the Germans.")
        self.project.unitalicize((0, 1), MAIN)
        assert self.project.subtitles[0].main_text == (
            "I am no thief, I am an officer\n"
            "and a university student.")
        assert self.project.subtitles[1].main_text == (
            "I look like this because\n"
            "I'm hunted for by the Germans.")
