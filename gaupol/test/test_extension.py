# Copyright (C) 2008,2010 Osmo Salomaa
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
from gi.repository import Gtk


class TestExtension(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()
        class PuppetExtension(gaupol.Extension): pass
        self.extension = PuppetExtension()

    def test_setup_method(self):
        self.extension.setup(self.application)

    def test_show_help(self):
        self.assert_raises(NotImplementedError,
                    self.extension.show_help)

    def test_show_preferences_dialog(self):
        self.assert_raises(NotImplementedError,
                    self.extension.show_preferences_dialog,
                    Gtk.Window())

    def test_teardown_method(self):
        self.extension.teardown(self.application)

    def test_update(self):
        self.extension.update(self.application,
                              self.application.get_current_page())
