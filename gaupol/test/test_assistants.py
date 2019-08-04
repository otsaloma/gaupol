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
import gaupol

from gi.repository import Gtk
from unittest.mock import patch

from gaupol.assistants import CapitalizationPage
from gaupol.assistants import CommonErrorPage
from gaupol.assistants import ConfirmationPage
from gaupol.assistants import HearingImpairedPage
from gaupol.assistants import IntroductionPage
from gaupol.assistants import JoinSplitWordsPage
from gaupol.assistants import LineBreakOptionsPage
from gaupol.assistants import LineBreakPage
from gaupol.assistants import ProgressPage

OK = lambda *args: Gtk.ResponseType.OK


class _TestBuilderPage(gaupol.TestCase):

    def run_page(self):
        self.window.connect("delete-event", Gtk.main_quit)
        Gtk.main()


class TestIntroductionPage(_TestBuilderPage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.set_border_width(12)
        self.window.set_default_size(800, 500)
        self.page = IntroductionPage(self.window)
        self.window.add(self.page)
        self.window.show_all()


class _TestLocalePage(_TestBuilderPage):

    def test_correct_texts(self):
        self.page.correct_texts(self.new_project(),
                                None,
                                aeidon.documents.MAIN)


class TestCapitalizationPage(_TestLocalePage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.set_border_width(12)
        self.window.set_default_size(800, 500)
        self.page = CapitalizationPage(self.window)
        self.window.add(self.page)
        self.window.show_all()


class TestCommonErrorPage(_TestLocalePage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.set_border_width(12)
        self.window.set_default_size(800, 500)
        self.page = CommonErrorPage(self.window)
        self.window.add(self.page)
        self.window.show_all()


class TestHearingImpairedPage(_TestLocalePage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.set_border_width(12)
        self.window.set_default_size(800, 500)
        self.page = HearingImpairedPage(self.window)
        self.window.add(self.page)
        self.window.show_all()


class TestJoinSplitWordsPage(_TestBuilderPage):

    def run__show_error_dialog(self):
        self.page._show_error_dialog("test")

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.set_border_width(12)
        self.window.set_default_size(800, 500)
        self.project = self.new_project()
        self.page = JoinSplitWordsPage(self.window)
        self.window.add(self.page)
        self.window.show_all()

    @patch("gaupol.util.flash_dialog", OK)
    def test_correct_texts(self):
        language = self.get_spell_check_language("en")
        gaupol.conf.spell_check.language = language
        self.page.correct_texts(self.project,
                                None,
                                aeidon.documents.MAIN)


class TestLineBreakPage(_TestLocalePage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.set_border_width(12)
        self.window.set_default_size(800, 500)
        self.page = LineBreakPage(self.window)
        self.window.add(self.page)
        self.window.show_all()


class TestLineBreakOptionsPage(_TestBuilderPage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.set_border_width(12)
        self.window.set_default_size(800, 500)
        self.page = LineBreakOptionsPage(self.window)
        self.window.add(self.page)
        self.window.show_all()


class TestProgressPage(_TestBuilderPage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.set_border_width(12)
        self.window.set_default_size(800, 500)
        self.page = ProgressPage(self.window)
        self.page.reset(100)
        self.window.add(self.page)
        self.window.show_all()


class TestConfirmationPage(_TestBuilderPage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.set_border_width(12)
        self.window.set_default_size(800, 500)
        self.page = ConfirmationPage(self.window)
        self.window.add(self.page)
        self.window.show_all()


class TestTextAssistant(gaupol.TestCase):

    def run_assistant(self):
        self.assistant.show()
        self.assistant.connect("apply", Gtk.main_quit)
        self.assistant.connect("cancel", Gtk.main_quit)
        self.assistant.connect("delete-event", Gtk.main_quit)
        Gtk.main()

    def setup_method(self, method):
        gaupol.conf.text_assistant.pages = ["common-error"]
        self.application = self.new_application()
        self.assistant = gaupol.TextAssistant(
            self.application.window, self.application)
        self.assistant.show()
