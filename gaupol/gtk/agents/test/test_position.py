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


import gtk

from gaupol.gtk import unittest


class TestPositionAgent(unittest.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        respond = lambda *args: gtk.RESPONSE_CANCEL
        self.application.flash_dialog = respond

    def test_on_adjust_durations_activate(self):

        self.application.on_adjust_durations_activate()

    def test_on_transform_positions_activate(self):

        self.application.on_transform_positions_activate()

    def test_on_convert_framerate_activate(self):

        self.application.on_convert_framerate_activate()

    def test_on_shift_positions_activate(self):

        self.application.on_shift_positions_activate()
