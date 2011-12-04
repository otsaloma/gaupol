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


class TestMPsubTime(aeidon.TestCase):

    format = aeidon.formats.MPSUB
    name = "mpsub-time"

    def setup_method(self, method):
        path = self.new_temp_file(self.format, self.name)
        self.file = aeidon.files.new(self.format, path, "ascii")

    def test_copy_from(self):
        self.file.set_header("FORMAT=25.00")
        path = self.new_temp_file(self.format, self.name)
        new_file = aeidon.files.new(self.format, path, "ascii")
        new_file.copy_from(self.file)
        assert new_file.header == self.file.header
        assert new_file.framerate == self.file.framerate
        assert new_file.mode == self.file.mode

    def test_read(self):
        assert self.file.read()
        assert self.file.header
        assert self.file.mode in aeidon.modes
        if self.file.framerate is not None:
            assert self.file.framerate in aeidon.framerates

    def test_set_header__frame(self):
        self.file.set_header("FORMAT=29.97")
        assert self.file.mode == aeidon.modes.FRAME
        assert self.file.framerate == aeidon.framerates.FPS_29_970

    def test_set_header__time(self):
        self.file.set_header("FORMAT=TIME")
        assert self.file.mode == aeidon.modes.TIME
        assert self.file.framerate == aeidon.framerates.NONE

    def test_set_header__value_error(self):
        self.assert_raises(ValueError,
                           self.file.set_header,
                           "FORMAT=NONE")

    def test_write(self):
        self.file.write(self.file.read(), aeidon.documents.MAIN)
        text = open(self.file.path, "r").read().strip()
        reference = self.get_sample_text(self.format, self.name)
        assert text == reference


class TestMPsubFrame(TestMPsubTime):

    name = "mpsub-frame"
