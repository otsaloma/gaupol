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
import time


class TestPreviewAgent(gaupol.TestCase):

    def run__show_encoding_error_dialog(self):
        self.delegate._show_encoding_error_dialog()

    def run__show_io_error_dialog(self):
        self.delegate._show_io_error_dialog("test")

    def run__show_process_error_dialog(self):
        self.delegate._show_process_error_dialog("test")

    def setup_method(self, method):
        gaupol.conf.preview.custom_command = "echo $SUBFILE"
        gaupol.conf.preview.use_custom_command = True
        self.application = self.new_application()
        page = self.application.get_current_page()
        page.project.video_path = self.new_subrip_file()
        self.delegate = self.application.preview.__self__

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__show_encoding_error_dialog(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        self.delegate._show_encoding_error_dialog()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__show_io_error_dialog(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        self.delegate._show_io_error_dialog("test")

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__show_process_error_dialog(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        self.delegate._show_process_error_dialog("test")

    def test_on_preview_activate__main(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("preview").activate()

    def test_on_preview_activate__translation(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.TRAN_TEXT)
        self.application.get_action("preview").activate()

    def test_preview__main(self):
        page = self.application.get_current_page()
        doc = aeidon.documents.MAIN
        self.application.preview(page, 13, doc)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test_preview__process_error(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        gaupol.conf.preview.custom_command = "xxxxx"
        page = self.application.get_current_page()
        doc = aeidon.documents.MAIN
        self.application.preview(page, 13, doc)
        time.sleep(1)
        gaupol.util.iterate_main()

    def test_preview__translation(self):
        page = self.application.get_current_page()
        doc = aeidon.documents.TRAN
        self.application.preview(page, 13, doc)

    def test_preview__unicode_error(self):
        page = self.application.get_current_page()
        doc = aeidon.documents.MAIN
        page.project.set_text(0, doc, "\303\266")
        page.project.main_file.encoding = "ascii"
        self.application.preview(page, 13, doc)

    def test_preview_changes(self):
        page = self.application.get_current_page()
        subtitles = [x.copy() for x in page.project.subtitles]
        framerate = page.project.framerate
        self.application.preview_changes(page,
                                         3,
                                         aeidon.documents.TRAN,
                                         page.project.remove_subtitles,
                                         ((0, 1, 2),))

        assert page.project.subtitles == subtitles
        assert page.project.framerate == framerate
