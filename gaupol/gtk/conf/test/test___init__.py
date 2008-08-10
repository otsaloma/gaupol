# Copyright (C) 2006-2008 Osmo Salomaa
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

import gaupol.gtk


class TestModule(gaupol.gtk.TestCase):

    def on_conf_editor_notify_custom_font(self, obj, value):

        assert value == "Serif 12"

    def test__handle_transitions(self):

        path = self.get_subrip_path()
        fobj = open(path, "w")
        fobj.write("[general]\n")
        fobj.write("version = 0.7\n")
        fobj.write("[debug]\n")
        fobj.write("editor = ed\n")
        fobj.close()
        gaupol.gtk.conf.config_file = path
        gaupol.gtk.conf.read()
        assert gaupol.gtk.conf.debug.editor != "ed"
        gaupol.gtk.conf.config_file = None

    def test_connect(self):

        gaupol.gtk.conf.connect(self, "editor", "custom_font")
        gaupol.gtk.conf.editor.custom_font = "Serif 12"
        gaupol.gtk.conf.disconnect(self, "editor", "custom_font")

    def test_disconnect(self):

        gaupol.gtk.conf.connect(self, "editor", "custom_font")
        gaupol.gtk.conf.disconnect(self, "editor", "custom_font")
        gaupol.gtk.conf.editor.custom_font = "Sans 24"

    def test_read(self):

        gaupol.gtk.conf.read()
        assert hasattr(gaupol.gtk.conf, "editor")

    def test_read_defaults(self):

        gaupol.gtk.conf.read_defaults()

    def test_restore_defaults(self):

        gaupol.gtk.conf.editor.custom_font = "Serif"
        gaupol.gtk.conf.restore_defaults()
        assert gaupol.gtk.conf.editor.custom_font == ""

    def test_write(self):

        gaupol.gtk.conf.read()
        gaupol.gtk.conf.config_file = self.get_subrip_path()
        gaupol.gtk.conf.write()
        gaupol.gtk.conf.read()
