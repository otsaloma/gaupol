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

from gaupol.gtk.errors import Default
from gaupol.gtk import unittest


class TestSaveAgent(unittest.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.save_main.im_self

       respond = lambda *args: gtk.RESPONSE_DELETE_EVENT
        self.delegate.flash_dialog = respond
        self.delegate.run_dialog = respond

    def test__show_encoding_error_dialog(self):

        self.delegate._show_encoding_error_dialog("test", "ascii")

    def test__show_io_error_dialog(self):

        self.delegate._show_io_error_dialog("test", "test")

    def test_on_save_all_documents_activate(self):

        self.application.on_save_all_documents_activate()

    def test_on_save_main_document_activate(self):

        self.application.on_save_main_document_activate()

    def test_on_save_main_document_as_activate(self):

        self.application.on_save_main_document_as_activate()

    def test_on_save_translation_document_activate(self):

        self.application.on_save_translation_document_activate()

    def test_on_save_translation_document_as_activate(self):

        self.application.on_save_translation_document_as_activate()

    def test_save_main(self):

        page = self.application.get_current_page()
        self.application.save_main(page)

    def test_save_main_as(self):

        page = self.application.get_current_page()
        function = self.application.save_main_as
        self.raises(Default, function, page)

    def test_save_translation(self):

        page = self.application.get_current_page()
        self.application.save_translation(page)

    def test_save_translation_as(self):

        page = self.application.get_current_page()
        function = self.application.save_translation_as
        self.raises(Default, function, page)
