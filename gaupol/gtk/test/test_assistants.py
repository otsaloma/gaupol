# Copyright (C) 2007-2008 Osmo Salomaa
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

import gaupol.gtk
import gtk

# pylint: disable-msg=F0401
from ..assistants import _CapitalizationPage
from ..assistants import _CommonErrorPage
from ..assistants import _ConfirmationPage
from ..assistants import _HearingImpairedPage
from ..assistants import _IntroductionPage
from ..assistants import _LineBreakPage
from ..assistants import _LineBreakOptionsPage
from ..assistants import _ProgressPage


class TestTextAssistantPage(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.page = gaupol.gtk.TextAssistantPage()


class _Test_GladePage(gaupol.gtk.TestCase):

    # pylint: disable-msg=E1101

    def run__page(self):

        window = gtk.Window()
        window.add(self.page)
        window.connect("delete-event", gtk.main_quit)
        window.set_default_size(500, 400)
        window.show_all()
        gtk.main()


class Test_IntroductionPage(_Test_GladePage):

    def setup_method(self, method):

        self.page = _IntroductionPage()
        self.test_populate_tree_view()

    def test__on_all_radio_toggled(self):

        self.page._all_radio.set_active(True)
        self.page._current_radio.set_active(True)
        self.page._selected_radio.set_active(True)

    def test__on_main_radio_toggled(self):

        self.page._main_radio.set_active(True)
        self.page._tran_radio.set_active(True)
        self.page._main_radio.set_active(True)

    def test__on_tree_view_cell_toggled(self):

        store = self.page._tree_view.get_model()
        column = self.page._tree_view.get_column(0)
        renderer = column.get_cell_renderers()[0]
        for i in range(len(store)):
            renderer.emit("toggled", i)
            renderer.emit("toggled", i)
            renderer.emit("toggled", i)

    def test_get_field(self):

        self.page._main_radio.set_active(True)
        field = self.page.get_field()
        assert field == gaupol.gtk.fields.MAIN_TEXT
        self.page._tran_radio.set_active(True)
        field = self.page.get_field()
        assert field == gaupol.gtk.fields.TRAN_TEXT

    def test_get_selected_pages(self):

        self.page.get_selected_pages()

    def test_get_target(self):

        self.page._all_radio.set_active(True)
        target = self.page.get_target()
        assert target == gaupol.gtk.targets.ALL
        self.page._current_radio.set_active(True)
        target = self.page.get_target()
        assert target == gaupol.gtk.targets.CURRENT
        self.page._selected_radio.set_active(True)
        target = self.page.get_target()
        assert target == gaupol.gtk.targets.SELECTED

    def test_populate_tree_view(self):

        pages = (_CapitalizationPage(), _CommonErrorPage())
        self.page.populate_tree_view(pages)


class _Test_LocalePage(_Test_GladePage):

    # pylint: disable-msg=E1101

    def test__get_country(self):

        self.page._country_combo.set_active(0)
        self.page._get_country()

    def test__get_language(self):

        self.page._language_combo.set_active(0)
        self.page._get_language()

    def test__get_script(self):

        self.page._script_combo.set_active(0)
        self.page._get_script()

    def test__on_country_combo_changed(self):

        store = self.page._country_combo.get_model()
        for i in range(len(store)):
            if store[i][0] != gaupol.gtk.COMBO_SEPARATOR:
                self.page._country_combo.set_active(i)

    def test__on_language_combo_changed(self):

        store = self.page._language_combo.get_model()
        for i in range(len(store)):
            if store[i][0] != gaupol.gtk.COMBO_SEPARATOR:
                self.page._language_combo.set_active(i)

    def test__on_script_combo_changed(self):

        store = self.page._script_combo.get_model()
        for i in range(len(store)):
            if store[i][0] != gaupol.gtk.COMBO_SEPARATOR:
                self.page._script_combo.set_active(i)

    def test__on_tree_view_cell_toggled(self):

        store = self.page._tree_view.get_model()
        column = self.page._tree_view.get_column(0)
        renderer = column.get_cell_renderers()[0]
        for i in range(len(store)):
            renderer.emit("toggled", i)
            renderer.emit("toggled", i)
            renderer.emit("toggled", i)

    def test__populate_tree_view(self):

        self.page._populate_tree_view()

    def test_correct_texts(self):

        project = self.get_project()
        doc = gaupol.documents.MAIN
        self.page.correct_texts(project, None, doc)


class Test_CapitalizationPage(_Test_LocalePage):

    def setup_method(self, method):

        self.page = _CapitalizationPage()


class Test_CommonErrorPage(_Test_LocalePage):

    def setup_method(self, method):

        self.page = _CommonErrorPage()

    def test__on_human_check_toggled(self):

        self.page._human_check.set_active(True)
        self.page._human_check.set_active(False)
        self.page._human_check.set_active(True)

    def test__on_ocr_check_toggled(self):

        self.page._ocr_check.set_active(True)
        self.page._ocr_check.set_active(False)
        self.page._ocr_check.set_active(True)


class Test_HearingImpairedPage(_Test_LocalePage):

    def setup_method(self, method):

        self.page = _HearingImpairedPage()


class Test_LineBreakPage(_Test_LocalePage):

    def setup_method(self, method):

        self.page = _LineBreakPage()

    def test__max_skip_length(self):

        gaupol.gtk.conf.line_break.skip_length = True
        assert self.page._max_skip_length < 100
        gaupol.gtk.conf.line_break.skip_length = False
        assert self.page._max_skip_length > 100

    def test__max_skip_lines(self):

        gaupol.gtk.conf.line_break.skip_lines = True
        assert self.page._max_skip_lines < 10
        gaupol.gtk.conf.line_break.skip_lines = False
        assert self.page._max_skip_lines > 10


class TestLineBreakOptionsPage(_Test_GladePage):

    def setup_method(self, method):

        self.page = _LineBreakOptionsPage()

    def test__on_max_length_spin_value_changed(self):

        self.page._max_length_spin.spin(gtk.SPIN_STEP_FORWARD)
        self.page._max_length_spin.spin(gtk.SPIN_STEP_FORWARD)

    def test__on_max_lines_spin_value_changed(self):

        self.page._max_lines_spin.spin(gtk.SPIN_STEP_FORWARD)
        self.page._max_lines_spin.spin(gtk.SPIN_STEP_FORWARD)

    def test__on_max_skip_length_spin_value_changed(self):

        self.page._max_skip_length_spin.spin(gtk.SPIN_STEP_FORWARD)
        self.page._max_skip_length_spin.spin(gtk.SPIN_STEP_FORWARD)

    def test__on_max_skip_lines_spin_value_changed(self):

        self.page._max_skip_lines_spin.spin(gtk.SPIN_STEP_FORWARD)
        self.page._max_skip_lines_spin.spin(gtk.SPIN_STEP_FORWARD)

    def test__on_skip_length_check_toggled(self):

        self.page._skip_length_check.set_active(True)
        self.page._skip_length_check.set_active(False)
        self.page._skip_length_check.set_active(True)

    def test__on_skip_lines_check_toggled(self):

        self.page._skip_lines_check.set_active(True)
        self.page._skip_lines_check.set_active(False)
        self.page._skip_lines_check.set_active(True)

    def test__on_skip_unit_combo_changed(self):

        for unit in gaupol.gtk.length_units:
            self.page._skip_unit_combo.set_active(unit)

    def test__on_unit_combo_changed(self):

        for unit in gaupol.gtk.length_units:
            self.page._skip_unit_combo.set_active(unit)


class Test_ProgressPage(_Test_GladePage):

    def setup_method(self, method):

        self.page = _ProgressPage()
        self.page.reset(100)
        self.test_set_progress()
        self.test_set_project_name()
        self.test_set_task_name()

    def test_bump_progress(self):

        self.page.bump_progress()

    def test_reset(self):

        self.page.reset(100)

    def test_set_progress(self):

        self.page.set_progress(33, 100)
        self.page.set_progress(34, 100)
        self.page.set_progress(66, 100)

    def test_set_project_name(self):

        self.page.set_project_name("Test")

    def test_set_task_name(self):

        self.page.set_task_name("Test")


class Test_ConfirmationPage(_Test_GladePage):

    def setup_method(self, method):

        self.page = _ConfirmationPage()
        self.page.application = self.get_application()
        self.page.doc = gaupol.documents.MAIN
        gaupol.gtk.conf.preview.use_custom = True
        gaupol.gtk.conf.preview.custom_command = "echo"
        page = self.page.application.get_current_page()
        page.project.video_path = self.get_subrip_path()
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
        renderer = column.get_cell_renderers()[0]
        for i in range(len(store)):
            renderer.emit("edited", i, "test")
            renderer.emit("edited", i, "test")
            renderer.emit("edited", i, "test")

    def test__on_tree_view_cell_toggled(self):

        store = self.page._tree_view.get_model()
        column = self.page._tree_view.get_column(0)
        renderer = column.get_cell_renderers()[0]
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

        changes = []
        page = self.page.application.get_current_page()
        for i in range(len(page.project.subtitles)):
            orig = page.project.subtitles[i].main_text
            new = page.project.subtitles[i].tran_text
            changes.append((page, i, orig, new))
        self.page.populate_tree_view(changes)


class TestTextAssistant(gaupol.gtk.TestCase):

    def run__assistant(self):

        self.assistant.show()
        for signal in ("delete-event", "apply", "cancel"):
            self.assistant.connect(signal, gtk.main_quit)
        gtk.main()

    def setup_method(self, method):

        gaupol.gtk.conf.editor.use_custom_font = True
        gaupol.gtk.conf.editor.custom_font = "sans"
        gaupol.gtk.conf.line_break.max_length = 10
        gaupol.gtk.conf.line_break.skip_length = False
        gaupol.gtk.conf.line_break.skip_lines = False
        gaupol.gtk.conf.text_assistant.pages = ["line-break"]
        self.application = self.get_application()
        args = (self.application.window, self.application)
        self.assistant = gaupol.gtk.TextAssistant(*args)
        self.assistant.show()

    def test__on_apply(self):

        count = self.assistant.get_n_pages()
        function = self.assistant.set_current_page
        for i in range(count):
            self.assistant.set_current_page(i)
        page = self.assistant._confirmation_page
        store = page._tree_view.get_model()
        column = page._tree_view.get_column(2)
        renderer = column.get_cell_renderers()[0]
        for i in range(0, len(store), 2):
            renderer.emit("edited", i, "")
        self.assistant.emit("apply")

    def test__on_cancel(self):

        self.assistant.emit("cancel")

    def test__on_close(self):

        self.assistant.emit("close")
