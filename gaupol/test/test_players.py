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
import sys


class TestModule(gaupol.TestCase):

    def teardown_method(self, method):

        del sys.modules["gaupol.players"]
        reload(gaupol)

    def test_attributes__unix(self):

        platform = sys.platform
        sys.platform = "linux2"
        del sys.modules["gaupol.players"]
        reload(gaupol)
        for player in gaupol.players:
            assert hasattr(player, "command")
            assert hasattr(player, "label")
        sys.platform = platform

    def test_attributes__windows(self):

        platform = sys.platform
        sys.platform = "win32"
        del sys.modules["gaupol.players"]
        reload(gaupol)
        for player in gaupol.players:
            assert hasattr(player, "command")
            assert hasattr(player, "label")
        sys.platform = platform

    def test_items(self):

        assert hasattr(gaupol.players, "MPLAYER")
        assert hasattr(gaupol.players, "VLC")
