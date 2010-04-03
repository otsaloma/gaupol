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


class TestPreviewAgent(gaupol.TestCase):

    def run__show_encoding_error_dialog(self):

        flash_dialog = gaupol.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_encoding_error_dialog()

    def run__show_io_error_dialog(self):

        flash_dialog = gaupol.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_io_error_dialog("test")

    def run__show_process_error_dialog(self):

        flash_dialog = gaupol.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_process_error_dialog("test")

    def setup_method(self, method):

        gaupol.conf.preview.custom_command = "echo $SUBFILE"
        gaupol.conf.preview.use_custom_command = True
        self.application = self.new_application()
        page = self.application.get_current_page()
        page.project.video_path = self.new_subrip_file()
        self.delegate = self.application.preview.im_self
        respond = lambda *args: gtk.RESPONSE_DELETE_EVENT
        self.delegate.flash_dialog = respond

    def test__show_encoding_error_dialog(self):

        self.delegate._show_encoding_error_dialog()

    def test__show_io_error_dialog(self):

        self.delegate._show_io_error_dialog("test")

    def test__show_process_error_dialog(self):

        self.delegate._show_process_error_dialog("test")

    def test_on_preview_activate(self):

        page = self.application.get_current_page()
        self.application.get_action("preview").activate()
        for col in filter(page.view.is_text_column, page.view.columns):
            page.view.set_focus(0, col)
            self.application.get_action("preview").activate()
            page.view.select_rows((0, 1, 2))
            self.application.get_action("preview").activate()

    def test_preview(self):

        page = self.application.get_current_page()
        time = page.project.subtitles[3].start_time
        for doc in aeidon.documents:
            self.application.preview(page, time, doc)
            path = self.new_subrip_file()
            self.application.preview(page, time, doc, path)

    def test_preview__io_error(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        real_create = aeidon.temp.create
        temp_paths = []
        def create_temp(*args):
            path = real_create(*args)
            os.chmod(path, 0000)
            temp_paths.append(path)
            return path
        aeidon.temp.create = create_temp
        time = page.project.subtitles[0].start_time
        doc = aeidon.documents.MAIN
        self.application.preview(page, time, doc)
        for path in temp_paths:
            os.chmod(path, 0777)
        aeidon.temp.create = real_create

    def test_preview__return_non_zero(self):

        gaupol.conf.preview.custom_command = "/x/y/z.xyz"
        page = self.application.get_current_page()
        time = page.project.subtitles[0].start_time
        doc = aeidon.documents.MAIN
        self.application.preview(page, time, doc)

    def test_preview__unicode_error(self):

        page = self.application.get_current_page()
        time = page.project.subtitles[0].start_time
        doc = aeidon.documents.MAIN
        page.project.set_text(0, doc, "\303\266")
        page.project.main_file.encoding = "ascii"
        self.application.preview(page, time, doc)

    def test_preview_changes(self):

        page = self.application.get_current_page()
        subtitles = [x.copy() for x in page.project.subtitles]
        framerate = page.project.framerate
        doc = aeidon.documents.TRAN
        method = page.project.set_text
        args = (2, doc, "testing...")
        self.application.preview_changes(page, 2, doc, method, args)
        assert page.project.subtitles == subtitles
        assert page.project.framerate == framerate
