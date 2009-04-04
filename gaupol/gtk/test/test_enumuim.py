# Copyright (C) 2009 Osmo Salomaa
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

import gaupol.gtk


class TestModule(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()

    def test_field_actions(self):

        for field in gaupol.gtk.fields:
            name = gaupol.gtk.field_actions[field]
            assert self.application.get_action(name) is not None

    def test_framerate_actions(self):

        for framerate in gaupol.framerates:
            name = gaupol.gtk.framerate_actions[framerate]
            assert self.application.get_action(name) is not None

    def test_mode_actions(self):

        for mode in gaupol.modes:
            name = gaupol.gtk.mode_actions[mode]
            assert self.application.get_action(name) is not None
