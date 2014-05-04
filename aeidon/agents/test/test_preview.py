# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import aeidon
import os


class TestPreviewAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()
        self.delegate = self.project.preview.__self__

    def test_find_video__avi(self):
        video_path = aeidon.temp.create(".avi")
        sub_path = video_path.replace(".avi", ".srt")
        file = aeidon.files.new(aeidon.formats.SUBRIP,
                                sub_path,
                                "ascii")

        self.project.save_main(file)
        self.project.find_video()
        assert self.project.video_path == video_path
        os.remove(sub_path)

    def test_find_video__none(self):
        self.project.find_video()
        assert self.project.video_path is None

    def test_preview__encoding(self):
        doc = aeidon.documents.MAIN
        self.project.video_path = self.new_subrip_file()
        self.project.preview("00:00:00.000", doc, "echo", 0, "utf_8")
        assert os.path.isfile(self.project.get_file(doc).path)

    def test_preview__main(self):
        doc = aeidon.documents.MAIN
        self.project.video_path = self.new_subrip_file()
        self.project.preview("00:00:00.000", doc, "echo", 0)
        assert os.path.isfile(self.project.get_file(doc).path)

    def test_preview__translation(self):
        doc = aeidon.documents.TRAN
        self.project.video_path = self.new_subrip_file()
        self.project.preview("00:00:00.000", doc, "echo", 0)
        assert os.path.isfile(self.project.get_file(doc).path)
