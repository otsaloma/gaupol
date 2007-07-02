# Copyright (C) 2006-2007 Osmo Salomaa
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
from gaupol.gtk import unittest


class TestModule(unittest.TestCase):

    def on_conf_editor_notify_custom_font(self, obj, value):

        assert value == "Serif 12"

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
        assert gaupol.gtk.conf.general.version == gaupol.__version__
        assert gaupol.gtk.conf.editor.custom_font == ""

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
