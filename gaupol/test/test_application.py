# -*- coding: utf-8 -*-

# Copyright (C) 2026 Osmo Salomaa
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import aeidon
import gaupol


class TestApplication(gaupol.TestCase):

    def test_custom_framerates(self):
        gaupol.conf.editor.custom_framerates = [48.0]
        self.application = self.new_application()
        framerate = aeidon.framerates.FPS_48_000
        assert framerate.value == 48.0
        action = self.application.get_action("set-framerate")
        action.activate(str(framerate))
        page = self.application.get_current_page()
        assert page.project.framerate == framerate
        delattr(aeidon.framerates, "FPS_48_000")
