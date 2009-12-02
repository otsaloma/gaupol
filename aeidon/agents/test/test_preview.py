# Copyright (C) 2005-2009 Osmo Salomaa
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
import os


class TestPreviewAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()
        self.delegate = self.project.preview.im_self

    def test_get_temp_file_path__main(self):
        get_temp_file_path = self.project.get_temp_file_path
        path = get_temp_file_path(aeidon.documents.MAIN)
        path = get_temp_file_path(aeidon.documents.MAIN, "ascii")

    def test_get_temp_file_path__translation(self):
        get_temp_file_path = self.project.get_temp_file_path
        path = get_temp_file_path(aeidon.documents.TRAN)
        path = get_temp_file_path(aeidon.documents.TRAN, "ascii")

    def test_guess_video_path__avi(self):
        video_path = aeidon.temp.create(".avi")
        sub_path = video_path.replace(".avi", ".srt")
        self.project.save_main((sub_path,
                                aeidon.formats.SUBRIP,
                                "ascii",
                                aeidon.newlines.UNIX))

        self.project.guess_video_path()
        assert self.project.video_path == video_path
        aeidon.temp.remove(video_path)
        os.remove(sub_path)

    def test_guess_video_path__none(self):
        self.project.guess_video_path()
        assert self.project.video_path is None

    def test_preview(self):
        doc = aeidon.documents.MAIN
        self.project.video_path = self.new_subrip_file()
        self.project.preview("00:00:00.000", doc, "echo", 0)
        assert os.path.isfile(self.project.get_file(doc).path)

    def test_preview__sub_path(self):
        doc = aeidon.documents.MAIN
        path = self.new_subrip_file()
        self.project.preview("00:00:00.000", doc, "echo", 0, path, "utf_8")
        assert os.path.isfile(self.project.get_file(doc).path)

    def test_preview__temp(self):
        doc = aeidon.documents.MAIN
        self.project.clear_texts((0,), doc)
        self.project.preview("00:00:00.000", doc, "echo", 0)
        assert os.path.isfile(self.project.get_file(doc).path)
