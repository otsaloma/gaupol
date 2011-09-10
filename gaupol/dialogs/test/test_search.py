# Copyright (C) 2006-2008,2010 Osmo Salomaa
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
import gtk


class TestSearchDialog(gaupol.TestCase):

    def run__dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def run__show_regex_error_dialog_pattern(self):
        self.dialog._show_regex_error_dialog_pattern("test")

    def run__show_regex_error_dialog_replacement(self):
        self.dialog._show_regex_error_dialog_replacement("test")

    def setup_method(self, method):
        gaupol.conf.search.max_history = 2
        gaupol.conf.editor.use_custom_font = True
        gaupol.conf.editor.custom_font = "sans"
        self.application = self.new_application()
        self.dialog = gaupol.SearchDialog(self.application)
        self.dialog.show()

    def test__on_all_radio_toggled(self):
        self.dialog._current_radio.set_active(True)
        self.dialog._all_radio.set_active(True)
        self.dialog._current_radio.set_active(True)

    def test__on_application_page_changed(self):
        # Ensure that editing obsolete data is not possible.
        # http://bugzilla.gnome.org/show_bug.cgi?id=572676
        self.dialog._pattern_entry.set_text("a")
        next(self.dialog)
        page = self.application.get_current_page()
        page.project.remove_subtitles((self.dialog._match_row,))
        assert not self.dialog._text_view.props.sensitive
        assert not self.dialog._replace_button.props.sensitive

    def test__on_ignore_case_check_toggled(self):
        self.dialog._ignore_case_check.set_active(True)
        self.dialog._ignore_case_check.set_active(False)
        self.dialog._ignore_case_check.set_active(True)

    def test__on_next_button_clicked(self):
        self.dialog._pattern_entry.set_text("a")
        self.dialog._next_button.emit("clicked")

    def test__on_main_check_toggled(self):
        self.dialog._main_check.set_active(True)
        self.dialog._tran_check.set_active(True)
        self.dialog._main_check.set_active(True)

    def test__on_pattern_entry_changed(self):
        self.dialog._pattern_entry.set_text("a")
        self.dialog._pattern_entry.set_text("")

    def test__on_previous_button_clicked(self):
        self.dialog._pattern_entry.set_text("a")
        self.dialog._previous_button.emit("clicked")

    def test__on_regex_check_toggled(self):
        self.dialog._regex_check.set_active(True)
        self.dialog._regex_check.set_active(False)
        self.dialog._regex_check.set_active(True)

    def test__on_replace_all_button_clicked(self):
        self.dialog._pattern_entry.set_text("e")
        self.dialog._replacement_entry.set_text("x")
        self.dialog._replace_all_button.emit("clicked")

    def test__on_replace_button_clicked(self):
        self.dialog._pattern_entry.set_text("a")
        self.dialog._replacement_entry.set_text("x")
        self.dialog._next_button.emit("clicked")
        self.dialog._replace_button.emit("clicked")

    def test__on_response(self):
        self.dialog.response(gtk.RESPONSE_HELP)

    def test__on_show(self):
        self.dialog.show()
        self.dialog.hide()
        self.dialog.show()

    def test__on_text_view_focus_out_event(self):
        self.dialog._pattern_entry.set_text("a")
        self.dialog._next_button.emit("clicked")
        gaupol.util.iterate_main()
        self.dialog._next_button.emit("clicked")
        gaupol.util.iterate_main()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__set_pattern__re_error(self):
        gaupol.util.flash_dialog = lambda *args: gtk.RESPONSE_OK
        self.dialog._regex_check.set_active(True)
        self.dialog._pattern_entry.set_text("*")
        next(self.dialog)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__show_regex_error_dialog_pattern(self):
        gaupol.util.flash_dialog = lambda *args: gtk.RESPONSE_OK
        self.dialog._show_regex_error_dialog_pattern("test")

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__show_regex_error_dialog_replacement(self):
        gaupol.util.flash_dialog = lambda *args: gtk.RESPONSE_OK
        self.dialog._show_regex_error_dialog_replacement("test")

    def test_next(self):
        self.dialog._regex_check.set_active(True)
        for char in "aeiouy":
            self.dialog._pattern_entry.set_text(char)
            next(self.dialog)
            next(self.dialog)

    def test_next__not_found(self):
        self.dialog._regex_check.set_active(True)
        self.dialog._pattern_entry.set_text("xxx")
        next(self.dialog)
        self.dialog._all_radio.set_active(True)
        self.application.open_main(self.new_subrip_file())
        next(self.dialog)

    def test_previous(self):
        self.dialog._regex_check.set_active(True)
        for char in "aeiouy":
            self.dialog._pattern_entry.set_text(char)
            self.dialog.previous()
            self.dialog.previous()

    def test_previous__not_found(self):
        self.dialog._regex_check.set_active(True)
        self.dialog._pattern_entry.set_text("xxx")
        self.dialog.previous()
        self.dialog._all_radio.set_active(True)
        self.application.open_main(self.new_subrip_file())
        self.dialog.previous()

    def test_replace(self):
        self.dialog._regex_check.set_active(True)
        for char in "aeiouy":
            self.dialog._pattern_entry.set_text(char)
            self.dialog._replacement_entry.set_text(char)
            next(self.dialog)
            self.dialog.replace()
            self.dialog.replace()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test_replace__re_error(self):
        gaupol.util.flash_dialog = lambda *args: gtk.RESPONSE_OK
        self.dialog._regex_check.set_active(True)
        self.dialog._pattern_entry.set_text(" ")
        self.dialog._replacement_entry.set_text("\\1")
        next(self.dialog)
        self.dialog.replace()

    def test_replace_all(self):
        self.dialog._regex_check.set_active(True)
        self.dialog._pattern_entry.set_text("^")
        self.dialog._replacement_entry.set_text("-")
        self.dialog.replace_all()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test_replace_all__re_error(self):
        gaupol.util.flash_dialog = lambda *args: gtk.RESPONSE_OK
        self.dialog._regex_check.set_active(True)
        self.dialog._pattern_entry.set_text("^")
        self.dialog._replacement_entry.set_text("\\1")
        self.dialog.replace_all()
