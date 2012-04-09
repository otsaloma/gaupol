# -*- coding: utf-8-unix -*-

# Copyright (C) 2005-2008,2010 Osmo Salomaa
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
import os


class TestOpenAgent(gaupol.TestCase):

    def run__show_encoding_error_dialog(self):
        self.delegate._show_encoding_error_dialog("test")

    def run__show_format_error_dialog(self):
        self.delegate._show_format_error_dialog("test")

    def run__show_io_error_dialog(self):
        self.delegate._show_io_error_dialog("test", "test")

    def run__show_parse_error_dialog(self):
        self.delegate._show_parse_error_dialog("test", aeidon.formats.SUBRIP)

    @aeidon.deco.silent(gaupol.Default)
    def run__show_size_warning_dialog(self):
        self.delegate._show_size_warning_dialog("test", 2)

    @aeidon.deco.silent(gaupol.Default)
    def run__show_sort_warning_dialog(self):
        self.delegate._show_sort_warning_dialog("test", 3)

    @aeidon.deco.silent(gaupol.Default)
    def run__show_translation_warning_dialog(self):
        page = self.application.get_current_page()
        self.delegate._show_translation_warning_dialog(page)

    def setup_method(self, method):
        self.application = self.new_application()
        self.delegate = self.application.open_main.__self__

    @aeidon.deco.monkey_patch(gaupol.FileDialog, "get_filenames")
    @aeidon.deco.monkey_patch(gaupol.util, "run_dialog")
    def test__on_append_file_activate(self):
        get_filenames = lambda *args: (self.new_subrip_file(),)
        gaupol.FileDialog.get_filenames = get_filenames
        gaupol.util.run_dialog = lambda *args: Gtk.ResponseType.OK
        self.application.get_action("append_file").activate()

    def test__on_new_project_activate(self):
        self.application.get_action("new_project").activate()

    @aeidon.deco.monkey_patch(gaupol.FileDialog, "get_filenames")
    @aeidon.deco.monkey_patch(gaupol.util, "run_dialog")
    def test__on_open_main_files_activate(self):
        get_filenames = lambda *args: (self.new_subrip_file(),)
        gaupol.FileDialog.get_filenames = get_filenames
        gaupol.util.run_dialog = lambda *args: Gtk.ResponseType.OK
        self.application.get_action("open_main_files").activate()

    @aeidon.deco.monkey_patch(gaupol.FileDialog, "get_filenames")
    @aeidon.deco.monkey_patch(gaupol.util, "run_dialog")
    def test__on_open_translation_file_activate(self):
        get_filenames = lambda *args: (self.new_subrip_file(),)
        gaupol.FileDialog.get_filenames = get_filenames
        gaupol.util.run_dialog = lambda *args: Gtk.ResponseType.OK
        page = self.application.get_current_page()
        self.application.get_action("open_translation_file").activate()

    @aeidon.deco.monkey_patch(gaupol.FileDialog, "get_filenames")
    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.monkey_patch(gaupol.util, "run_dialog")
    def test__on_open_translation_file_activate__changed(self):
        get_filenames = lambda *args: (self.new_subrip_file(),)
        gaupol.FileDialog.get_filenames = get_filenames
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.YES
        gaupol.util.run_dialog = lambda *args: Gtk.ResponseType.OK
        page = self.application.get_current_page()
        self.application.get_action("open_translation_file").activate()
        page.project.set_text(0, aeidon.documents.TRAN, "")
        self.application.get_action("open_translation_file").activate()

    @aeidon.deco.monkey_patch(gaupol.FileDialog, "get_filenames")
    @aeidon.deco.monkey_patch(gaupol.util, "run_dialog")
    def test__on_select_video_file_activate(self):
        get_filenames = lambda *args: (self.new_subrip_file(),)
        gaupol.FileDialog.get_filenames = get_filenames
        gaupol.util.run_dialog = lambda *args: Gtk.ResponseType.OK
        page = self.application.get_current_page()
        page.project.video_path = self.new_subrip_file()
        self.application.get_action("select_video_file").activate()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__on_split_project_activate(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        page = self.application.get_current_page()
        page.view.select_rows((3,))
        self.application.get_action("split_project").activate()

    @aeidon.deco.monkey_patch(gaupol.FileDialog, "get_filenames")
    @aeidon.deco.monkey_patch(gaupol.util, "run_dialog")
    def test__on_video_button_clicked(self):
        get_filenames = lambda *args: (self.new_subrip_file(),)
        gaupol.FileDialog.get_filenames = get_filenames
        gaupol.util.run_dialog = lambda *args: Gtk.ResponseType.OK
        self.application.video_button.emit("clicked")

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__show_encoding_error_dialog(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        self.delegate._show_encoding_error_dialog("test")

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__show_format_error_dialog(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        self.delegate._show_format_error_dialog("test")

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__show_io_error_dialog(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        self.delegate._show_io_error_dialog("test", "test")

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__show_parse_error_dialog(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        self.delegate._show_parse_error_dialog("test", aeidon.formats.SUBRIP)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.silent(gaupol.Default)
    def test__show_size_warning_dialog(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        self.delegate._show_size_warning_dialog("test", 2)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.silent(gaupol.Default)
    def test__show_sort_warning_dialog__no(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.NO
        self.delegate._show_sort_warning_dialog("test", 3)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.silent(gaupol.Default)
    def test__show_sort_warning_dialog__yes(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.YES
        self.delegate._show_sort_warning_dialog("test", 3)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.silent(gaupol.Default)
    def test__show_translation_warning_dialog__no(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.NO
        page = self.application.get_current_page()
        self.delegate._show_translation_warning_dialog(page)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.silent(gaupol.Default)
    def test__show_translation_warning_dialog__yes(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.YES
        page = self.application.get_current_page()
        self.delegate._show_translation_warning_dialog(page)

    def test_add_page(self):
        self.application.add_page(self.new_page())

    def test_add_to_recent_files__main(self):
        self.application.add_to_recent_files(self.new_subrip_file(),
                                             aeidon.formats.SUBRIP,
                                             aeidon.documents.MAIN)

    def test_add_to_recent_files__translation(self):
        self.application.add_to_recent_files(self.new_subrip_file(),
                                             aeidon.formats.SUBRIP,
                                             aeidon.documents.TRAN)

    def test_append_file(self):
        self.application.append_file(self.new_subrip_file())
        self.application.append_file(self.new_subrip_file(), "ascii")

    def test_connect_view_signals(self):
        page = self.application.get_current_page()
        self.application.connect_view_signals(page.view)

    def test_open_main(self):
        path = self.new_subrip_file()
        self.application.open_main(path)

    def test_open_main__again(self):
        path = self.new_subrip_file()
        self.application.open_main(path)
        self.application.open_main(path)

    def test_open_main__ascii(self):
        path = self.new_subrip_file()
        self.application.open_main(path, "ascii")

    def test_open_main__auto(self):
        path = self.new_subrip_file()
        self.application.open_main(path, "auto")

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test_open_main__format_error(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        path = self.new_subrip_file()
        open(path, "w").write("xxx\n")
        self.application.open_main(path)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test_open_main__io_error(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        path = self.new_subrip_file()
        os.chmod(path, 0000)
        self.application.open_main(path)
        os.chmod(path, 0o777)

    def test_open_main__multiple(self):
        self.application.open_main((self.new_subrip_file(),
                                    self.new_subrip_file(),
                                    self.new_microdvd_file(),
                                    self.new_microdvd_file()))

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test_open_main__parse_error(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.YES
        path = self.new_microdvd_file()
        fobj = open(path, "w")
        fobj.write("{10}{20}Testing...\n")
        fobj.write("{20}{30}Testing...\n")
        fobj.write("{30}{40}Testing...\n")
        fobj.write("{xx}{yy}Testing...\n")
        fobj.close()
        self.application.open_main(path)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test_open_main__sort_warning(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.YES
        path = self.new_microdvd_file()
        fobj = open(path, "w")
        fobj.write("{30}{40}Testing...\n")
        fobj.write("{40}{50}Testing...\n")
        fobj.write("{10}{20}Testing...\n")
        fobj.write("{20}{30}Testing...\n")
        fobj.close()
        self.application.open_main(path)

    def test_open_translation(self):
        path = self.new_subrip_file()
        self.application.open_translation(path)

    def test_open_translation__align_method(self):
        path = self.new_subrip_file()
        align_method = aeidon.align_methods.POSITION
        self.application.open_translation(path, align_method=align_method)
