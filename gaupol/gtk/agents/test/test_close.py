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
import gaupol.gtk
import gtk
import os


class TestCloseAgent(gaupol.gtk.TestCase):

    def run__confirm_and_close_page_main(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.delegate._confirm_and_close_page_main(page)

    def run__confirm_and_close_page_translation(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.delegate._confirm_and_close_page_translation(page)

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.close_page.im_self
        respond = lambda *args: gtk.RESPONSE_DELETE_EVENT
        self.delegate.flash_dialog = respond

    def test__save_window_geometry(self):

        self.delegate._save_window_geometry()

    @gaupol.deco.silent(gaupol.gtk.Default)
    def test_close_page__both_changed(self):

        self.application.open_main_file(self.get_subrip_path())
        self.application.open_translation_file(self.get_microdvd_path())
        self.application.pages[-1].project.remove_subtitles((0,))
        self.application.close_page(self.application.pages[-1], True)

    @gaupol.deco.silent(gaupol.gtk.Default)
    def test_close_page__main_changed__discard(self):

        respond = lambda *args: gtk.RESPONSE_NO
        self.delegate.flash_dialog = respond
        doc = gaupol.documents.MAIN
        self.application.open_main_file(self.get_subrip_path())
        self.application.open_translation_file(self.get_microdvd_path())
        self.application.pages[-1].project.clear_texts((0,), doc)
        self.application.close_page(self.application.pages[-1], True)

    @gaupol.deco.silent(gaupol.gtk.Default)
    def test_close_page__main_changed__save(self):

        respond = lambda *args: gtk.RESPONSE_YES
        self.delegate.flash_dialog = respond
        doc = gaupol.documents.MAIN
        self.application.open_main_file(self.get_subrip_path())
        self.application.open_translation_file(self.get_microdvd_path())
        self.application.pages[-1].project.clear_texts((0,), doc)
        self.application.close_page(self.application.pages[-1], True)

    @gaupol.deco.silent(gaupol.gtk.Default)
    def test_close_page__main_removed(self):

        page = self.application.get_current_page()
        os.remove(page.project.main_file.path)
        self.application.close_page(page, True)

    @gaupol.deco.silent(gaupol.gtk.Default)
    def test_close_page__translation_changed__discard(self):

        respond = lambda *args: gtk.RESPONSE_NO
        self.delegate.flash_dialog = respond
        doc = gaupol.documents.TRAN
        self.application.open_main_file(self.get_subrip_path())
        self.application.open_translation_file(self.get_microdvd_path())
        self.application.pages[-1].project.clear_texts((0,), doc)
        self.application.close_page(self.application.pages[-1], True)

    @gaupol.deco.silent(gaupol.gtk.Default)
    def test_close_page__translation_changed__save(self):

        respond = lambda *args: gtk.RESPONSE_YES
        self.delegate.flash_dialog = respond
        doc = gaupol.documents.TRAN
        self.application.open_main_file(self.get_subrip_path())
        self.application.open_translation_file(self.get_microdvd_path())
        self.application.pages[-1].project.clear_texts((0,), doc)
        self.application.close_page(self.application.pages[-1], True)

    @gaupol.deco.silent(gaupol.gtk.Default)
    def test_close_page__translation_removed(self):

        page = self.application.get_current_page()
        os.remove(page.project.tran_file.path)
        self.application.close_page(page, True)

    @gaupol.deco.silent(gaupol.gtk.Default)
    def test_close_page__unchanged__confirm(self):

        self.application.open_main_file(self.get_subrip_path())
        self.application.open_translation_file(self.get_microdvd_path())
        self.application.close_page(self.application.pages[-1], True)

    @gaupol.deco.silent(gaupol.gtk.Default)
    def test_close_page__unchanged__no_confirm(self):

        self.application.open_main_file(self.get_subrip_path())
        self.application.open_translation_file(self.get_microdvd_path())
        self.application.close_page(self.application.pages[-1], False)

    def test_on_close_all_projects_activate(self):

        self.application.get_action("close_all_projects").activate()
        self.application.open_main_file(self.get_subrip_path())
        self.application.open_main_file(self.get_subrip_path())
        for page in self.application.pages:
            page.project.remove_subtitles((0,))
        self.application.get_action("close_all_projects").activate()

    def test_on_close_project_activate(self):

        self.application.get_action("close_project").activate()
        self.application.open_main_file(self.get_subrip_path())
        self.application.pages[-1].project.remove_subtitles((0,))
        self.application.get_action("close_project").activate()

    def test_on_page_close_request(self):

        self.application.pages[-1].emit("close-request")
        self.application.open_main_file(self.get_subrip_path())
        self.application.pages[-1].project.remove_subtitles((0,))
        self.application.pages[-1].emit("close-request")

    def test_on_quit_activate(self):

        for page in self.application.pages:
            page.project.remove_subtitles((0,))
        self.application.get_action("quit").activate()

    def test_on_window_delete_event(self):

        for page in self.application.pages:
            page.project.remove_subtitles((0,))
        self.application.window.emit("delete-event", None)
