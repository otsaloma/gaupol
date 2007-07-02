# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.


import gaupol
import os

from gaupol import unittest


class TestPreviewAgent(unittest.TestCase):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = self.project.preview.im_self

    def test__get_subtitle_path(self):

        value = self.delegate._get_subtitle_path(gaupol.DOCUMENT.MAIN)
        assert value == self.project.main_file.path
        self.project.clear_texts([0], gaupol.DOCUMENT.MAIN)
        value = self.delegate._get_subtitle_path(gaupol.DOCUMENT.MAIN)
        assert value != self.project.main_file.path
        self.files.add(value)

    def test__on_notify_main_file(self):

        self.delegate._on_notify_main_file()

    def test_get_temp_file_path(self):

        method = self.project.get_temp_file_path
        path = method(gaupol.DOCUMENT.MAIN)
        self.files.add(path)
        path = method(gaupol.DOCUMENT.TRAN)
        self.files.add(path)

    def test_guess_video_path(self):

        self.project.guess_video_path()

    def test_preview(self):

        doc = gaupol.DOCUMENT.MAIN
        self.project.video_path = self.get_subrip_path()
        self.project.preview("00:00:00.000", doc, "echo", 0)
        assert os.path.isfile(self.project.get_file(doc).path)
        path = self.get_subrip_path()
        self.project.preview("00:00:00.000", doc, "echo", 0, path)
        assert os.path.isfile(self.project.get_file(doc).path)
        self.project.clear_texts([0], gaupol.DOCUMENT.MAIN)
        self.project.preview("00:00:00.000", doc, "echo", 0)
        assert os.path.isfile(self.project.get_file(doc).path)
