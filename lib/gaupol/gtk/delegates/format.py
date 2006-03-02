# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Formatting text."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _

import gtk

from gaupol.gtk.colconstants import *
from gaupol.gtk.delegates    import Delegate, UIMAction


class FormatAction(UIMAction):

    """Base class for text formatting actions."""

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False

        selection = bool(page.view.get_selected_rows())
        focus = page.view.get_focus()[1] in (MTXT, TTXT)
        return bool(selection and focus)


class CaseChangeActionMenu(FormatAction):

    """Changing case."""

    uim_menu_item = (
        'show_case_menu',
        None,
        _('_Case')
    )

    uim_paths = ['/ui/menubar/format/case']


class CaseLowerAction(FormatAction):

    """Changing to lower case."""

    uim_action_item = (
        'use_lower_case',
        None,
        _('_Lower'),
        '<control>L',
        _('Change the selected texts to lower case'),
        'on_use_lower_case_activated'
    )

    uim_paths = ['/ui/menubar/format/case/lower']


class CaseSentenceAction(FormatAction):

    """Changing to sentence case."""

    uim_action_item = (
        'use_sentence_case',
        None,
        _('_Sentence'),
        '<control>E',
        _('Change the selected texts to Sentence case'),
        'on_use_sentence_case_activated'
    )

    uim_paths = ['/ui/menubar/format/case/sentence']


class CaseTitleAction(FormatAction):

    """Changing to title case."""

    uim_action_item = (
        'use_title_case',
        None,
        _('_Title'),
        '<control>Y',
        _('Change the selected texts to Title Case'),
        'on_use_title_case_activated'
    )

    uim_paths = ['/ui/menubar/format/case/title']


class CaseUpperAction(FormatAction):

    """Changing to upper case."""

    uim_action_item = (
        'use_upper_case',
        None,
        _('_Upper'),
        '<control>U',
        _('Change the selected texts to UPPER CASE'),
        'on_use_upper_case_activated'
    )

    uim_paths = ['/ui/menubar/format/case/upper']


class ToggleDialogLinesAction(FormatAction):

    """Toggling dialog lines."""

    uim_action_item = (
        'toggle_dialog_lines',
        None,
        _('_Dialog'),
        '<control>D',
        _('Toggle dialog lines on the selected texts'),
        'on_toggle_dialog_lines_activated'
    )

    uim_paths = ['/ui/menubar/format/dialog']


class ToggleItalicizationAction(UIMAction):

    """Toggling italicization."""

    uim_action_item = (
        'toggle_italicization',
        gtk.STOCK_ITALIC,
        _('_Italic'),
        '<control>I',
        _('Toggle italicization of the selected texts'),
        'on_toggle_italicization_activated'
    )

    uim_paths = ['/ui/menubar/format/italic']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False
        if not page.view.get_selected_rows():
            return False

        col = page.view.get_focus()[1]
        if col not in (MTXT, TTXT):
            return False
        if col == MTXT and page.project.main_file is None:
            return False
        if col == TTXT and page.project.tran_file is None:
            return False

        return True


class FormatDelegate(Delegate):

    """Formatting text."""

    def _change_case(self, method):
        """
        Change case.

        method: "title", "capitalize", "upper" or "lower"
        """
        page     = self.get_current_page()
        rows     = page.view.get_selected_rows()
        col      = page.view.get_focus()[1]
        document = page.text_column_to_document(col)

        page.project.change_case(rows, document, method)
        self.set_sensitivities(page)

    def on_toggle_dialog_lines_activated(self, *args):
        """Toggle dialog lines."""

        page     = self.get_current_page()
        rows     = page.view.get_selected_rows()
        col      = page.view.get_focus()[1]
        document = page.text_column_to_document(col)

        page.project.toggle_dialog_lines(rows, document)
        self.set_sensitivities(page)
        self.set_character_status(page)

    def on_toggle_italicization_activated(self, *args):
        """Toggle italicization."""

        page     = self.get_current_page()
        rows     = page.view.get_selected_rows()
        col      = page.view.get_focus()[1]
        document = page.text_column_to_document(col)

        page.project.toggle_italicization(rows, document)
        self.set_sensitivities(page)

    def on_use_lower_case_activated(self, *args):
        """Use lower case."""

        self._change_case('lower')

    def on_use_sentence_case_activated(self, *args):
        """Use sentence case."""

        self._change_case('capitalize')

    def on_use_title_case_activated(self, *args):
        """Use title case."""

        self._change_case('title')

    def on_use_upper_case_activated(self, *args):
        """Use upper case."""

        self._change_case('upper')


if __name__ == '__main__':

    from gaupol.gtk.application import Application
    from gaupol.test            import Test

    class TestFormatDelegate(Test):

        def __init__(self):

            Test.__init__(self)
            self.application = Application()
            self.application.open_main_files([self.get_subrip_path()])

        def destroy(self):

            self.application.window.destroy()

        def test_on_toggle_dialog_lines_activated(self):

            page = self.application.get_current_page()
            page.project.main_texts[0] = 'test\ntest'
            page.reload_all()
            page.view.set_focus(0, MTXT)

            self.application.on_toggle_dialog_lines_activated()
            assert page.project.main_texts[0] == '- test\n- test'
            page.assert_store()

            self.application.on_toggle_dialog_lines_activated()
            assert page.project.main_texts[0] == 'test\ntest'
            page.assert_store()

            self.application.undo(2)
            assert page.project.main_texts[0] == 'test\ntest'
            page.assert_store()

        def test_on_toggle_italicization_activated(self):

            page = self.application.get_current_page()
            page.project.main_texts[0] = 'test\ntest'
            page.reload_all()
            page.view.set_focus(0, MTXT)

            self.application.on_toggle_italicization_activated()
            assert page.project.main_texts[0] == '<i>test\ntest</i>'
            page.assert_store()

            self.application.on_toggle_italicization_activated()
            assert page.project.main_texts[0] == 'test\ntest'
            page.assert_store()

            self.application.undo(2)
            assert page.project.main_texts[0] == 'test\ntest'
            page.assert_store()

        def test_on_case_activated(self):

            page = self.application.get_current_page()
            page.project.main_texts[0] = 'test\ntest'
            page.reload_all()
            page.view.set_focus(0, MTXT)

            self.application.on_use_upper_case_activated()
            assert page.project.main_texts[0] == 'TEST\nTEST'
            page.assert_store()

            self.application.on_use_lower_case_activated()
            assert page.project.main_texts[0] == 'test\ntest'
            page.assert_store()

            self.application.on_use_sentence_case_activated()
            assert page.project.main_texts[0] == 'Test\ntest'
            page.assert_store()

            self.application.on_use_title_case_activated()
            assert page.project.main_texts[0] == 'Test\nTest'
            page.assert_store()

            self.application.undo(4)
            assert page.project.main_texts[0] == 'test\ntest'
            page.assert_store()

    TestFormatDelegate().run()
