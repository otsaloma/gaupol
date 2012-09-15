# -*- coding: utf-8 -*-

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
import os

from gi.repository import Gtk


class TestCloseAgent(gaupol.TestCase):

    def run__confirm_close_main(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.delegate._confirm_close_main(page)

    def run__confirm_close_translation(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.delegate._confirm_close_translation(page)

    def setup_method(self, method):
        self.application = self.new_application()
        self.delegate = self.application.close.__self__

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__on_close_all_projects_activate(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.NO
        self.application.get_action("close_all_projects").activate()
        self.application.open_main(self.new_subrip_file())
        self.application.open_main(self.new_subrip_file())
        for page in self.application.pages:
            page.project.remove_subtitles((0,))
        self.application.get_action("close_all_projects").activate()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__on_close_project_activate(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.NO
        self.application.get_action("close_project").activate()
        self.application.open_main(self.new_subrip_file())
        self.application.pages[-1].project.remove_subtitles((0,))
        self.application.get_action("close_project").activate()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__on_page_close_request(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.NO
        self.application.pages[-1].emit("close-request")
        self.application.open_main(self.new_subrip_file())
        self.application.pages[-1].project.remove_subtitles((0,))
        self.application.pages[-1].emit("close-request")

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__on_quit_activate(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.CANCEL
        for page in self.application.pages:
            page.project.remove_subtitles((0,))
        self.application.get_action("quit").activate()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__on_window_delete_event(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.CANCEL
        for page in self.application.pages:
            page.project.remove_subtitles((0,))
        self.application.window.emit("delete-event", None)

    def test__save_window_geometry(self):
        self.delegate._save_window_geometry()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.silent(gaupol.Default)
    def test_close__both_changed(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.CANCEL
        self.application.pages[-1].project.remove_subtitles((0,))
        self.application.close(self.application.pages[-1], confirm=True)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.silent(gaupol.Default)
    def test_close__main_changed__discard(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.NO
        doc = aeidon.documents.MAIN
        self.application.pages[-1].project.clear_texts((0,), doc)
        self.application.close(self.application.pages[-1], confirm=True)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.silent(gaupol.Default)
    def test_close__main_changed__save(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.YES
        doc = aeidon.documents.MAIN
        self.application.pages[-1].project.clear_texts((0,), doc)
        self.application.close(self.application.pages[-1], confirm=True)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.silent(gaupol.Default)
    def test_close__main_removed(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.CANCEL
        page = self.application.get_current_page()
        os.remove(page.project.main_file.path)
        self.application.close(page, confirm=True)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.silent(gaupol.Default)
    def test_close__translation_changed__discard(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.NO
        doc = aeidon.documents.TRAN
        self.application.pages[-1].project.clear_texts((0,), doc)
        self.application.close(self.application.pages[-1], confirm=True)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.silent(gaupol.Default)
    def test_close__translation_changed__save(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.YES
        doc = aeidon.documents.TRAN
        self.application.pages[-1].project.clear_texts((0,), doc)
        self.application.close(self.application.pages[-1], confirm=True)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.silent(gaupol.Default)
    def test_close__translation_removed(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.CANCEL
        page = self.application.get_current_page()
        os.remove(page.project.tran_file.path)
        self.application.close(page, confirm=True)

    @aeidon.deco.silent(gaupol.Default)
    def test_close__unchanged__confirm(self):
        self.application.close(self.application.pages[-1], confirm=True)

    @aeidon.deco.silent(gaupol.Default)
    def test_close__unchanged__no_confirm(self):
        self.application.close(self.application.pages[-1], confirm=False)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.silent(gaupol.Default)
    def test_close_all__multiple_changed(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.NO
        self.application.open_main(self.new_subrip_file())
        self.application.open_main(self.new_subrip_file())
        for page in self.application.pages:
            page.project.remove_subtitles((0,))
        self.application.close_all()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    @aeidon.deco.silent(gaupol.Default)
    def test_close_all__single_changed(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.NO
        self.application.pages[-1].project.remove_subtitles((0,))
        self.application.close_all()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test_quit__default(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.CANCEL
        for page in self.application.pages:
            page.project.remove_subtitles((0,))
        self.assert_raises(gaupol.Default, self.application.quit)
