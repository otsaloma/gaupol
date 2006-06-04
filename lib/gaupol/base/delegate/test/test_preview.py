# Copyright (C) 2005-2006 Osmo Salomaa
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

from gaupol.base                  import cons
from gaupol.base.delegate.preview import PreviewDelegate
from gaupol.test                  import Test


class TestPreviewDelegate(Test):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = PreviewDelegate(self.project)

    def test_get_subtitle_path(self):

        value = self.delegate._get_subtitle_path(cons.Document.MAIN)
        assert value == (self.project.main_file.path, False)

        self.project.clear_texts([0], cons.Document.MAIN)
        value = self.delegate._get_subtitle_path(cons.Document.MAIN)
        assert value[0] != self.project.main_file.path
        assert value[1] is True
        self.files.append(value[0])

    def test_get_temp_file_path(self):

        path = self.project.get_temp_file_path(cons.Document.MAIN)
        assert os.path.isfile(path)
        self.files.append(path)

        path = self.project.get_temp_file_path(cons.Document.TRAN)
        assert os.path.isfile(path)
        self.files.append(path)

    def test_guess_video_path(self):

        assert self.project.guess_video_path() is None
