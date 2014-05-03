# -*- coding: utf-8 -*-

# Copyright (C) 2009 Osmo Salomaa
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

import aeidon
import gaupol


class TestModule(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()

    def test_field_actions(self):
        for field in gaupol.fields:
            name = gaupol.field_actions[field]
            action = self.application.get_action(name)
            assert action is not None

    def test_framerate_actions(self):
        for framerate in aeidon.framerates:
            name = gaupol.framerate_actions[framerate]
            action = self.application.get_action(name)
            assert action is not None

    def test_mode_actions(self):
        for mode in (aeidon.modes.TIME, aeidon.modes.FRAME):
            name = gaupol.mode_actions[mode]
            action = self.application.get_action(name)
            assert action is not None
