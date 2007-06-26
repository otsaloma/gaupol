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


import functools
import gaupol.gtk
import gtk

from gaupol.gtk import unittest


class TestCloseAgent(unittest.TestCase):

    def run__confirm_and_close_page_main(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        page = self.application.get_current_page()
        page.project.remove_subtitles([0])
        self.delegate._confirm_and_close_page_main(page)

    def run__confirm_and_close_page_translation(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        page = self.application.get_current_page()
        page.project.remove_subtitles([0])
        self.delegate._confirm_and_close_page_translation(page)

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.close_page.im_self
        respond = lambda *args: gtk.RESPONSE_DELETE_EVENT
        self.delegate.flash_dialog = respond
        self.delegate.run_dialog = respond

    def test__save_window_geometry(self):

        self.delegate._save_window_geometry()

    def test_close_page(self):

        self.application.open_main_file(self.get_subrip_path())
        self.application.open_translation_file(self.get_microdvd_path())
        self.application.close_page(self.application.pages[-1], False)

        self.application.open_main_file(self.get_subrip_path())
        self.application.open_translation_file(self.get_microdvd_path())
        self.application.close_page(self.application.pages[-1], True)

        self.application.open_main_file(self.get_subrip_path())
        self.application.open_translation_file(self.get_microdvd_path())
        self.application.pages[-1].project.remove_subtitles([0])
        self.application.close_page(self.application.pages[-1], True)

        doc = gaupol.gtk.DOCUMENT.MAIN
        self.application.open_main_file(self.get_subrip_path())
        self.application.open_translation_file(self.get_microdvd_path())
        self.application.pages[-1].project.clear_texts([0], doc)
        self.application.close_page(self.application.pages[-1], True)

        doc = gaupol.gtk.DOCUMENT.TRAN
        self.application.open_main_file(self.get_subrip_path())
        self.application.open_translation_file(self.get_microdvd_path())
        self.application.pages[-1].project.clear_texts([0], doc)
        self.application.close_page(self.application.pages[-1], True)

    def test_on_close_all_projects_activate(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles([0])
        self.application.on_close_all_projects_activate()
        self.application.open_main_file(self.get_subrip_path())
        self.application.on_close_all_projects_activate()

    def test_on_close_project_activate(self):

        self.application.on_close_project_activate()

    def test_on_page_close_request(self):

        page = self.application.get_current_page()
        self.application.on_page_close_request(page)
