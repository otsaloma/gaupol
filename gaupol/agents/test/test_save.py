# Copyright (C) 2005-2008 Osmo Salomaa
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

import functools
import gaupol
import gtk
import os


class TestSaveAgent(gaupol.TestCase):

    def run__show_encoding_error_dialog(self):

        flash_dialog = gaupol.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_encoding_error_dialog("test", "ascii")

    def run__show_io_error_dialog(self):

        flash_dialog = gaupol.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_io_error_dialog("test", "test")

    def setup_method(self, method):

        self.application = self.new_application()
        self.delegate = self.application.save_main_document.im_self
        respond = lambda *args: gtk.RESPONSE_OK
        self.delegate.flash_dialog = respond
        self.delegate.run_dialog = respond
        get_filename = lambda *args: self.new_subrip_file()
        gaupol.SaveDialog.get_filename = get_filename

    def test__show_encoding_error_dialog(self):

        self.delegate._show_encoding_error_dialog("test", "ascii")

    def test__show_io_error_dialog(self):

        self.delegate._show_io_error_dialog("test", "test")

    def test_on_save_all_documents_activate(self):

        self.application.open_main_file(self.new_subrip_file())
        self.application.open_main_file(self.new_subrip_file())
        self.application.get_action("save_all_documents").activate()

    def test_on_save_main_document_activate(self):

        self.application.get_action("save_main_document").activate()

    def test_on_save_main_document_as_activate(self):

        self.application.get_action("save_main_document_as").activate()

    def test_on_save_translation_document_activate(self):

        self.application.get_action("save_translation_document").activate()

    def test_on_save_translation_document_as_activate(self):

        self.application.get_action("save_translation_document_as").activate()

    def test_save_main_document(self):

        page = self.application.get_current_page()
        self.application.save_main_document(page)

    def test_save_main_document__io_error(self):

        page = self.application.get_current_page()
        os.chmod(page.project.main_file.path, 0000)
        function = self.application.save_main_document
        self.raises(gaupol.Default, function, page)
        os.chmod(page.project.main_file.path, 0777)

    def test_save_main_document__unicode_error(self):

        page = self.application.get_current_page()
        page.project.main_file.encoding = "ascii"
        doc = aeidon.documents.MAIN
        page.project.set_text(0, doc, "\303\266")
        function = self.application.save_main_document
        self.raises(gaupol.Default, function, page)

    def test_save_main_document__untitled(self):

        self.application.get_action("new_project").activate()
        page = self.application.get_current_page()
        self.delegate.run_dialog = lambda *args: gtk.RESPONSE_CANCEL
        function = self.application.save_main_document
        self.raises(gaupol.Default, function, page)
        self.delegate.run_dialog = lambda *args: gtk.RESPONSE_OK
        self.application.save_main_document(page)

    def test_save_main_document_as(self):

        page = self.application.get_current_page()
        self.delegate.run_dialog = lambda *args: gtk.RESPONSE_CANCEL
        function = self.application.save_main_document_as
        self.raises(gaupol.Default, function, page)
        self.delegate.run_dialog = lambda *args: gtk.RESPONSE_OK
        self.application.save_main_document_as(page)

    def test_save_translation_document(self):

        page = self.application.get_current_page()
        self.application.save_translation_document(page)

    def test_save_translation_document__untitled(self):

        self.application.open_main_file(self.new_subrip_file())
        page = self.application.get_current_page()
        self.delegate.run_dialog = lambda *args: gtk.RESPONSE_CANCEL
        function = self.application.save_translation_document
        self.raises(gaupol.Default, function, page)
        self.delegate.run_dialog = lambda *args: gtk.RESPONSE_OK
        self.application.save_translation_document(page)

    def test_save_translation_document_as(self):

        page = self.application.get_current_page()
        self.delegate.run_dialog = lambda *args: gtk.RESPONSE_CANCEL
        function = self.application.save_translation_document_as
        self.raises(gaupol.Default, function, page)
        self.delegate.run_dialog = lambda *args: gtk.RESPONSE_OK
        self.application.save_translation_document_as(page)
