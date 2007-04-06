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


import gtk

from gaupol.gtk import const
from gaupol.gtk.errors import Default
from gaupol.gtk.unittest import TestCase


class TestOpenAgent(TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.open_main_files.im_self

        def respond(*args):
            return gtk.RESPONSE_DELETE_EVENT
        self.delegate.flash_dialog = respond
        self.delegate.run_dialog = respond

    def test__get_encodings(self):

        encodings = self.delegate._get_encodings()
        assert encodings
        for encoding in encodings:
            assert isinstance(encoding, basestring)

        encodings = self.delegate._get_encodings("johab")
        assert encodings[0] == "johab"

    def test__get_file_open(self):

        path = self.get_subrip_path()
        assert not self.delegate._get_file_open(path)
        self.application.open_main_files([path])
        assert self.delegate._get_file_open(path)

    def test__show_encoding_error_dialog(self):

        self.delegate._show_encoding_error_dialog("test")

    def test__show_format_error_dialog(self):

        self.delegate._show_format_error_dialog("test")

    def test__show_io_error_dialog(self):

        self.delegate._show_io_error_dialog("test", "test")

    def test__show_size_warning_dialog(self):

        function = self.delegate._show_size_warning_dialog
        self.raises(Default, function, "test", 10)

    def test__show_sort_warning_dialog(self):

        function = self.delegate._show_sort_warning_dialog
        self.raises(Default, function, "test", 10)

    def test__show_ssa_warning_dialog(self):

        function = self.delegate._show_ssa_warning_dialog
        self.raises(Default, function)

    def test__show_translation_warning_dialog(self):

        function = self.delegate._show_translation_warning_dialog
        page = self.application.pages[0]
        self.raises(Default, function, page)

    def test_add_new_page(self):

        self.application.add_new_page(self.get_page())

    def test_add_to_recent_files(self):

        path = self.get_subrip_path()
        self.delegate.add_to_recent_files(path, const.DOCUMENT.MAIN)
        self.delegate.add_to_recent_files(path, const.DOCUMENT.TRAN)

    def test_connect_to_view_signals(self):

        view = self.application.pages[0].view
        self.application.connect_to_view_signals(view)

    def test_on_append_file_activate(self):

        self.application.on_append_file_activate()

    def test_on_new_project_activate(self):

        self.application.on_new_project_activate()

    def test_on_open_button_clicked(self):

        self.application.on_open_button_clicked()

    def test_on_open_main_file_activate(self):

        self.application.on_open_main_file_activate()

    def test_on_open_translation_file_activate(self):

        self.application.on_open_translation_file_activate()

    def test_on_recent_main_menu_item_activated(self):

        menu = self.application.open_button.get_menu()
        if menu.get_children():
            item = menu.get_children()[0]
            menu.activate_item(item, True)

    def test_on_recent_translation_menu_item_activated(self):

        path = "/ui/menubar/file/recent_translation"
        menu = self.application.uim.get_widget(path).get_submenu()
        if menu.get_children():
            item = menu.get_children()[0]
            menu.activate_item(item, True)

    def test_on_select_video_file_activate(self):

        self.application.on_select_video_file_activate()

    def test_on_split_project_activate(self):

        responder = iter((gtk.RESPONSE_OK, gtk.RESPONSE_CANCEL))
        def flash_dialog(dialog):
            return responder.next()
        self.delegate.flash_dialog = flash_dialog
        self.application.pages[0].view.select_rows([3])
        self.application.on_split_project_activate()
        self.application.on_split_project_activate()

    def test_on_video_button_clicked(self):

        self.application.on_video_button_clicked()

    def test_open_main_files(self):

        paths = [self.get_subrip_path(), self.get_microdvd_path()]
        self.application.open_main_files(paths)
        self.application.open_main_files(paths, "ascii")

    def test_open_translation_file(self):

        path = self.get_subrip_path()
        self.application.open_translation_file(path)
        self.application.open_translation_file(path, "ascii")
