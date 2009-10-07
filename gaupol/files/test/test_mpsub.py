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


class TestMPsubTime(gaupol.TestCase):

    name = "mpsub-time"

    def setup_method(self, method):

        format = gaupol.formats.MPSUB
        path = self.new_temp_file(format, self.name)
        self.file = gaupol.files.new(format, path, "ascii")

    def test_copy_from(self):

        self.file.set_header("FORMAT=25.00")
        path = self.new_temp_file(self.file.format, self.name)
        new_file = gaupol.files.new(self.file.format, path, "ascii")
        new_file.copy_from(self.file)
        assert new_file.header == self.file.header
        assert new_file.framerate == self.file.framerate
        assert new_file.mode == self.file.mode

    def test_read(self):

        assert self.file.read()
        assert self.file.header
        assert self.file.mode in gaupol.modes
        if self.file.framerate is not None:
            assert self.file.framerate in gaupol.framerates

    def test_set_header(self):

        self.file.set_header("FORMAT=TIME")
        assert self.file.mode == gaupol.modes.TIME
        assert self.file.framerate == gaupol.framerates.NONE
        self.file.set_header("FORMAT=29.97")
        assert self.file.mode == gaupol.modes.FRAME
        assert self.file.framerate == gaupol.framerates.FPS_30
        function = self.file.set_header
        self.raises(ValueError, function, "FORMAT=NONE")

    def test_write(self):

        subtitles = self.file.read()
        doc = gaupol.documents.MAIN
        self.file.write(subtitles, doc)
        text = open(self.file.path, "r").read().strip()
        reference = self.get_sample_text(self.file.format, self.name)
        assert text == reference


class TestMPsubFrame(TestMPsubTime):

    name = "mpsub-frame"
