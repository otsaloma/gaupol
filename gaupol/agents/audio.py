# -*- coding: utf-8 -*-

# Copyright (C) 2013 Osmo Salomaa
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

"""Loading and interacting with audio."""

import aeidon

class AudioAgent(aeidon.Delegate):

    """Loading and interacting with audio."""

    @aeidon.deco.export
    def _on_volume_down_activate(self, *args):
        """Decrease volume."""
        volume = self.player.volume
        self.player.volume = volume - 0.05
        self.update_gui()

    @aeidon.deco.export
    def _on_volume_up_activate(self, *args):
        """Increase volume."""
        volume = self.player.volume
        self.player.volume = volume + 0.05
        self.update_gui()
