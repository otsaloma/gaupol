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
import sys


class TestModule(aeidon.TestCase):

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_attributes__unix(self):
        sys.platform = "linux2"
        reload(aeidon)
        for player in aeidon.players:
            assert hasattr(player, "command")
            assert hasattr(player, "command_utf_8")
            assert hasattr(player, "label")

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_attributes__windows(self):
        sys.platform = "win32"
        reload(aeidon)
        for player in aeidon.players:
            assert hasattr(player, "command")
            assert hasattr(player, "command_utf_8")
            assert hasattr(player, "label")

    def test_items(self):
        assert hasattr(aeidon.players, "MPLAYER")
        assert hasattr(aeidon.players, "VLC")
