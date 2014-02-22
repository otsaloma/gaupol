# -*- coding: utf-8 -*-

# Copyright (C) 2007-2008,2010,2012 Osmo Salomaa
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
import gaupol

from gi.repository import Gtk

from gaupol.assistants import CapitalizationPage
from gaupol.assistants import CommonErrorPage
from gaupol.assistants import ConfirmationPage
from gaupol.assistants import HearingImpairedPage
from gaupol.assistants import IntroductionPage
from gaupol.assistants import JoinSplitWordsPage
from gaupol.assistants import LineBreakOptionsPage
from gaupol.assistants import LineBreakPage
from gaupol.assistants import ProgressPage


class TestTextAssistantPage(gaupol.TestCase):

    def setup_method(self, method):
        self.page = gaupol.TextAssistantPage(Gtk.Window())


class _TestBuilderPage(gaupol.TestCase):

    def run__page(self):
        self.window.add(self.page)
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.set_default_size(600, 400)
        self.window.show_all()
        Gtk.main()


class TestIntroductionPage(_TestBuilderPage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.show_all()
        self.page = IntroductionPage(self.window)
        self.test_populate_tree_view()

    def test__on_columns_combo_changed(self):
        self.page._columns_combo.set_active(0)
        self.page._columns_combo.set_active(1)

    def test__on_subtitles_combo_changed(self):
        self.page._subtitles_combo.set_active(0)
        self.page._subtitles_combo.set_active(1)
        self.page._subtitles_combo.set_active(2)

    def test__on_tree_view_cell_toggled(self):
        store = self.page._tree_view.get_model()
        column = self.page._tree_view.get_column(0)
        renderer = column.get_cells()[0]
        for i in range(len(store)):
            renderer.emit("toggled", i)
            renderer.emit("toggled", i)
            renderer.emit("toggled", i)

    def test_get_field__main(self):
        self.page._columns_combo.set_active(0)
        field = self.page.get_field()
        assert field == gaupol.fields.MAIN_TEXT

    def test_get_field__tran(self):
        self.page._columns_combo.set_active(1)
        field = self.page.get_field()
        assert field == gaupol.fields.TRAN_TEXT

    def test_get_selected_pages(self):
        self.page.get_selected_pages()

    def test_get_target__all(self):
        self.page._subtitles_combo.set_active(2)
        target = self.page.get_target()
        assert target == gaupol.targets.ALL

    def test_get_target__current(self):
        self.page._subtitles_combo.set_active(1)
        target = self.page.get_target()
        assert target == gaupol.targets.CURRENT

    def test_get_target__selected(self):
        self.page._subtitles_combo.set_active(0)
        target = self.page.get_target()
        assert target == gaupol.targets.SELECTED

    def test_populate_tree_view(self):
        self.page.populate_tree_view((CapitalizationPage(Gtk.Window()),
                                      CommonErrorPage(Gtk.Window())))


class _TestLocalePage(_TestBuilderPage):

    def test__on_country_combo_changed(self):
        store = self.page._country_combo.get_model()
        for i in range(len(store)):
            if store[i][0] != gaupol.COMBO_SEPARATOR:
                self.page._country_combo.set_active(i)

    def test__on_language_combo_changed(self):
        store = self.page._language_combo.get_model()
        for i in range(len(store)):
            if store[i][0] != gaupol.COMBO_SEPARATOR:
                self.page._language_combo.set_active(i)

    def test__on_script_combo_changed(self):
        store = self.page._script_combo.get_model()
        for i in range(len(store)):
            if store[i][0] != gaupol.COMBO_SEPARATOR:
                self.page._script_combo.set_active(i)

    def test__on_tree_view_cell_toggled(self):
        store = self.page._tree_view.get_model()
        column = self.page._tree_view.get_column(0)
        renderer = column.get_cells()[0]
        for i in range(len(store)):
            renderer.emit("toggled", i)
            renderer.emit("toggled", i)
            renderer.emit("toggled", i)

    def test__populate_tree_view(self):
        self.page._populate_tree_view()

    def test_correct_texts(self):
        self.page.correct_texts(self.new_project(),
                                None,
                                aeidon.documents.MAIN)


class TestCapitalizationPage(_TestLocalePage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.show_all()
        self.page = CapitalizationPage(self.window)


class TestCommonErrorPage(_TestLocalePage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.show_all()
        self.page = CommonErrorPage(self.window)

    def test__on_human_check_toggled(self):
        self.page._human_check.set_active(True)
        self.page._human_check.set_active(False)
        self.page._human_check.set_active(True)

    def test__on_ocr_check_toggled(self):
        self.page._ocr_check.set_active(True)
        self.page._ocr_check.set_active(False)
        self.page._ocr_check.set_active(True)


class TestHearingImpairedPage(_TestLocalePage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.show_all()
        self.page = HearingImpairedPage(self.window)


class TestJoinSplitWordsPage(_TestBuilderPage):

    def run__show_error_dialog(self):
        self.page._show_error_dialog("test")

    def setup_method(self, method):
        self.project = self.new_project()
        self.window = Gtk.Window()
        self.window.show_all()
        self.page = JoinSplitWordsPage(self.window)

    def test_on_join_check_toggled(self):
        self.page._join_check.set_active(True)
        self.page._join_check.set_active(False)
        self.page._join_check.set_active(True)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__on_language_button_clicked(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        self.page._language_button.clicked()

    def test_on_split_check_toggled(self):
        self.page._split_check.set_active(True)
        self.page._split_check.set_active(False)
        self.page._split_check.set_active(True)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__show_error_dialog(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        self.page._show_error_dialog("test")

    def test_correct_texts(self):
        self.page.correct_texts(self.project,
                                None,
                                aeidon.documents.MAIN)


class TestLineBreakPage(_TestLocalePage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.show_all()
        self.page = LineBreakPage(self.window)

    def test_correct_texts__no_skip(self):
        gaupol.conf.line_break.use_skip_max_length = False
        gaupol.conf.line_break.use_skip_max_lines = False
        return self.test_correct_texts()

    def test_correct_texts__skip(self):
        gaupol.conf.line_break.use_skip_max_length = True
        gaupol.conf.line_break.use_skip_max_lines = True
        return self.test_correct_texts()


class TestLineBreakOptionsPage(_TestBuilderPage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.show_all()
        self.page = LineBreakOptionsPage(self.window)

    def test__on_max_length_spin_value_changed(self):
        self.page._max_length_spin.spin(Gtk.SpinType.STEP_FORWARD, 1)
        self.page._max_length_spin.spin(Gtk.SpinType.STEP_BACKWARD, 1)

    def test__on_max_lines_spin_value_changed(self):
        self.page._max_lines_spin.spin(Gtk.SpinType.STEP_FORWARD, 1)
        self.page._max_lines_spin.spin(Gtk.SpinType.STEP_BACKWARD, 1)

    def test__on_max_skip_length_spin_value_changed(self):
        self.page._max_skip_length_spin.spin(Gtk.SpinType.STEP_FORWARD, 1)
        self.page._max_skip_length_spin.spin(Gtk.SpinType.STEP_BACKWARD, 1)

    def test__on_max_skip_lines_spin_value_changed(self):
        self.page._max_skip_lines_spin.spin(Gtk.SpinType.STEP_FORWARD, 1)
        self.page._max_skip_lines_spin.spin(Gtk.SpinType.STEP_BACKWARD, 1)

    def test__on_skip_length_check_toggled(self):
        self.page._skip_length_check.set_active(True)
        self.page._skip_length_check.set_active(False)
        self.page._skip_length_check.set_active(True)

    def test__on_skip_lines_check_toggled(self):
        self.page._skip_lines_check.set_active(True)
        self.page._skip_lines_check.set_active(False)
        self.page._skip_lines_check.set_active(True)

    def test__on_skip_unit_combo_changed(self):
        for unit in gaupol.length_units:
            self.page._skip_unit_combo.set_active(unit)

    def test__on_unit_combo_changed(self):
        for unit in gaupol.length_units:
            self.page._unit_combo.set_active(unit)


class TestProgressPage(_TestBuilderPage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.show_all()
        self.page = ProgressPage(self.window)
        self.page.reset(100)

    def test_bump_progress(self):
        self.page.bump_progress()

    def test_reset(self):
        self.page.reset(100)

    def test_set_progress(self):
        self.page.set_progress(33, 100)
        self.page.set_progress(66, 100)

    def test_set_project_name(self):
        self.page.set_project_name("Test")

    def test_set_task_name(self):
        self.page.set_task_name("Test")


class TestConfirmationPage(_TestBuilderPage):

    def setup_method(self, method):
        self.window = Gtk.Window()
        self.window.show_all()
        self.page = ConfirmationPage(self.window)
        self.page.application = self.new_application()
        self.page.doc = aeidon.documents.MAIN
        gaupol.conf.preview.use_custom_command = True
        gaupol.conf.preview.custom_command = "echo"
        page = self.page.application.get_current_page()
        page.project.video_path = self.new_subrip_file()
        self.test_populate_tree_view()

    def test__on_mark_all_button_clicked(self):
        self.page._mark_all_button.emit("clicked")
        self.page._mark_all_button.emit("clicked")

    def test__on_preview_button_clicked(self):
        selection = self.page._tree_view.get_selection()
        selection.select_path(0)
        self.page._preview_button.emit("clicked")

    def test__on_remove_check_toggled(self):
        self.page._remove_check.set_active(True)
        self.page._remove_check.set_active(False)
        self.page._remove_check.set_active(True)

    def test__on_tree_view_cell_edited(self):
        store = self.page._tree_view.get_model()
        column = self.page._tree_view.get_column(2)
        renderer = column.get_cells()[0]
        for i in range(len(store)):
            renderer.emit("edited", i, "test")
            renderer.emit("edited", i, "test")
            renderer.emit("edited", i, "test")

    def test__on_tree_view_cell_toggled(self):
        store = self.page._tree_view.get_model()
        column = self.page._tree_view.get_column(0)
        renderer = column.get_cells()[0]
        for i in range(len(store)):
            renderer.emit("toggled", i)
            renderer.emit("toggled", i)
            renderer.emit("toggled", i)

    def test__on_tree_view_selection_changed(self):
        selection = self.page._tree_view.get_selection()
        store = self.page._tree_view.get_model()
        for i in range(len(store)):
            selection.select_path(i)

    def test__on_unmark_all_button_clicked(self):
        self.page._unmark_all_button.emit("clicked")
        self.page._unmark_all_button.emit("clicked")

    def test_get_confirmed_changes(self):
        self.page.get_confirmed_changes()

    def test_populate_tree_view(self):
        page = self.page.application.get_current_page()
        changes = [(page, i, x.main_text, x.tran_text) for i, x in
                   enumerate(page.project.subtitles)]

        self.page.populate_tree_view(changes)


class TestTextAssistant(gaupol.TestCase):

    def run__assistant(self):
        self.assistant.show()
        for signal in ("delete-event", "apply", "cancel"):
            self.assistant.connect(signal, Gtk.main_quit)
        Gtk.main()

    def setup_method(self, method):
        gaupol.conf.editor.use_custom_font = True
        gaupol.conf.editor.custom_font = "monospace"
        gaupol.conf.line_break.max_length = 10
        gaupol.conf.line_break.use_skip_max_length = False
        gaupol.conf.line_break.use_skip_max_lines = False
        gaupol.conf.text_assistant.pages = ["common-error"]
        self.application = self.new_application()
        self.assistant = gaupol.TextAssistant(self.application.window,
                                              self.application)

        self.assistant.show()

    def test__on_apply(self):
        count = self.assistant.get_n_pages()
        indices = list(range(count))
        # Remove progress page, which is automatically switched
        # to the confirmation page once done with all.
        indices.remove(count-2)
        for index in indices:
            self.assistant.set_current_page(index)
        page = self.assistant._confirmation_page
        store = page._tree_view.get_model()
        column = page._tree_view.get_column(2)
        renderer = column.get_cells()[0]
        for i in range(0, len(store), 2):
            renderer.emit("edited", i, "")
        self.assistant.emit("apply")

    def test__on_cancel(self):
        self.assistant.emit("cancel")

    def test__on_close(self):
        self.assistant.emit("close")
