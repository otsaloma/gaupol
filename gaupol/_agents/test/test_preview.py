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


import os

from gaupol import const
from gaupol.unittest import TestCase


class TestPreviewAgent(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = self.project.preview.im_self

    def test__get_subtitle_path(self):

        # pylint: disable-msg=E1101
        path, is_temp = self.delegate._get_subtitle_path(const.DOCUMENT.MAIN)
        assert path == self.project.main_file.path
        assert not is_temp

        self.project.clear_texts([0], const.DOCUMENT.TRAN)
        path, is_temp = self.delegate._get_subtitle_path(const.DOCUMENT.TRAN)
        assert path != self.project.main_file.path
        assert os.path.isfile(path)
        assert is_temp
        self.files.add(path)

    def test__on_notify_main_file(self):

        self.delegate._on_notify_main_file()

    def test_get_temp_file_path(self):

        path = self.project.get_temp_file_path(const.DOCUMENT.MAIN)
        assert os.path.isfile(path)
        self.files.add(path)

        path = self.project.get_temp_file_path(const.DOCUMENT.TRAN)
        assert os.path.isfile(path)
        self.files.add(path)

    def test_guess_video_path(self):

        assert self.project.guess_video_path() is None
