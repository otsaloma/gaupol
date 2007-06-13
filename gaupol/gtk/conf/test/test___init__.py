# Copyright (C) 2006-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


import gaupol.gtk
from gaupol.gtk import unittest


class TestModule(unittest.TestCase):

    def on_conf_editor_notify_font(self, obj, value):

        assert value == "Serif 12"

    def test_connect(self):

        gaupol.gtk.conf.connect(self, "editor", "font")
        gaupol.gtk.conf.editor.font = "Serif 12"
        gaupol.gtk.conf.disconnect(self, "editor", "font")

    def test_disconnect(self):

        gaupol.gtk.conf.connect(self, "editor", "font")
        gaupol.gtk.conf.disconnect(self, "editor", "font")
        gaupol.gtk.conf.editor.font = "Sans 24"

    def test_read(self):

        gaupol.gtk.conf.read()
        assert gaupol.gtk.conf.general.version == gaupol.__version__
        assert gaupol.gtk.conf.editor.font == ""

    def test_write(self):

        gaupol.gtk.conf.read()
        gaupol.gtk.conf.config_file = self.get_subrip_path()
        gaupol.gtk.conf.write()
        gaupol.gtk.conf.read()
