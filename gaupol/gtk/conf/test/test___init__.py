# Copyright (C) 2005-2007 Osmo Salomaa
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


from gaupol.gtk import conf
from gaupol.gtk.unittest import TestCase


class TestModule(TestCase):

    def on_conf_editor_notify_font(self, *args):

        pass

    def test_attributes(self):

        assert hasattr(conf, "CONFIG_FILE")
        assert isinstance(conf.SPEC_FILE, basestring)

        editor = conf.debug.editor
        conf.debug.editor = "ed"
        assert conf.debug.editor == "ed"
        conf.debug.editor = editor

    def test_connect(self):

        conf.connect(self, "editor", "font")
        conf.editor.font = "Serif 12"

    def test_read(self):

        conf.read()

    def test_write(self):

        conf.CONFIG_FILE = self.get_subrip_path()
        conf.write()
