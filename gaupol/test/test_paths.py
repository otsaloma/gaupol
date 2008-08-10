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
import sys


class TestModule(gaupol.TestCase):

    def teardown_method(self, method):

        reload(gaupol.paths)
        reload(gaupol)

    def test_attributes__py2exe(self):

        sys.frozen = True
        reload(gaupol.paths)
        reload(gaupol)
        assert hasattr(gaupol, "DATA_DIR")
        assert hasattr(gaupol, "LOCALE_DIR")
        assert hasattr(gaupol, "PROFILE_DIR")
        del sys.frozen

    def test_attributes__source(self):

        reload(gaupol.paths)
        reload(gaupol)
        assert os.path.isdir(gaupol.DATA_DIR)
        assert hasattr(gaupol, "LOCALE_DIR")
        assert hasattr(gaupol, "PROFILE_DIR")

    def test_attributes__unix(self):

        platform = sys.platform
        sys.platform = "linux2"
        reload(gaupol.paths)
        reload(gaupol)
        assert hasattr(gaupol, "PROFILE_DIR")
        sys.platform = platform

    def test_attributes__windows(self):

        platform = sys.platform
        sys.platform = "win32"
        reload(gaupol.paths)
        reload(gaupol)
        assert hasattr(gaupol, "PROFILE_DIR")
        sys.platform = platform
