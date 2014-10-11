# -*- coding: utf-8 -*-

# Copyright (C) 2013 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Loading and interacting with audio."""

import aeidon


class AudioAgent(aeidon.Delegate):

    """Loading and interacting with audio."""

    @aeidon.deco.export
    def _on_volume_down_activate(self, *args):
        """Decrease volume."""
        self.player.volume = self.player.volume - 0.05
        self.volume_button.set_value(self.player.volume)
        self.update_gui()

    @aeidon.deco.export
    def _on_volume_up_activate(self, *args):
        """Increase volume."""
        self.player.volume = self.player.volume + 0.05
        self.volume_button.set_value(self.player.volume)
        self.update_gui()
