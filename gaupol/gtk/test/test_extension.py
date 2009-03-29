# Copyright (C) 2008 Osmo Salomaa
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
import gtk


class PuppetExtension(gaupol.gtk.Extension):

    pass


class TestExtension(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        self.extension = PuppetExtension()
        self.conf = gaupol.gtk.conf.extensions

    def test_read_config(self):

        path = gaupol.temp.create()
        fobj = open(path, "w")
        fobj.write("[extensions]\n")
        fobj.write("[[test]]\n")
        fobj.write("x = integer(default=5)\n")
        fobj.close()
        self.extension.read_config(path)
        assert self.conf.test.x == 5
        self.conf.test.x = 6
        assert self.conf.test.x == 6
        self.extension.read_config(path)
        gaupol.temp.remove(path)

    def test_setup_method(self):

        self.extension.setup(self.application)

    def test_show_help(self):

        function = self.extension.show_help
        self.raises(NotImplementedError, function)

    def test_show_preferences_dialog(self):

        function = self.extension.show_preferences_dialog
        self.raises(NotImplementedError, function, gtk.Window())

    def test_teardown_method(self):

        self.extension.teardown(self.application)

    def test_update(self):

        page = self.application.get_current_page()
        self.extension.update(self.application, page)
