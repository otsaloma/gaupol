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

from .test_subfile import TestSubtitleFile
from .. import mpsub


class TestMPsub(TestSubtitleFile):

    def setup_method(self, method):

        path = self.get_subrip_path()
        self.file = mpsub.MPsub(path, "ascii")

    def test_set_header(self):

        self.file.set_header("FORMAT=TIME\n")
        assert self.file.mode == gaupol.MODE.TIME
        self.file.set_header("FORMAT=23.98\n")
        assert self.file.mode == gaupol.MODE.FRAME
        self.raises(ValueError, self.file.set_header, "")
