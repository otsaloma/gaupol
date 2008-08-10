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

import gaupol
import os


class TestPreviewAgent(gaupol.TestCase):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = self.project.preview.im_self

    def test__get_subtitle_path__main(self):

        doc = gaupol.documents.MAIN
        value = self.delegate._get_subtitle_path(doc)
        assert value == self.project.main_file.path
        self.project.clear_texts((0,), doc)
        value = self.delegate._get_subtitle_path(doc)
        assert value != self.project.main_file.path

    def test__get_subtitle_path__translation(self):

        doc = gaupol.documents.TRAN
        value = self.delegate._get_subtitle_path(doc)
        assert value == self.project.tran_file.path
        self.project.clear_texts((0,), doc)
        value = self.delegate._get_subtitle_path(doc)
        assert value != self.project.tran_file.path

    def test__on_notify_main_file(self):

        self.delegate._on_notify_main_file()

    def test_get_temp_file_path(self):

        get_temp_file_path = self.project.get_temp_file_path
        path = get_temp_file_path(gaupol.documents.MAIN)
        path = get_temp_file_path(gaupol.documents.TRAN)

    def test_guess_video_path(self):

        self.project.guess_video_path()
        assert self.project.video_path is None
        video_path = gaupol.temp.create(".avi")
        sub_path = video_path.replace(".avi", ".srt")
        format = gaupol.formats.SUBRIP
        newline = gaupol.newlines.UNIX
        props = (sub_path, format, "ascii", newline)
        self.project.save_main(props)
        self.project.guess_video_path()
        assert self.project.video_path == video_path
        gaupol.temp.remove(video_path)
        os.remove(sub_path)

    def test_preview(self):

        doc = gaupol.documents.MAIN
        self.project.video_path = self.get_subrip_path()
        self.project.preview("00:00:00.000", doc, "echo", 0)
        assert os.path.isfile(self.project.get_file(doc).path)
        path = self.get_subrip_path()
        self.project.preview("00:00:00.000", doc, "echo", 0, path)
        assert os.path.isfile(self.project.get_file(doc).path)
        self.project.clear_texts((0,), gaupol.documents.MAIN)
        self.project.preview("00:00:00.000", doc, "echo", 0)
        assert os.path.isfile(self.project.get_file(doc).path)
