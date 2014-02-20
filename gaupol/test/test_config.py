# -*- coding: utf-8 -*-

# Copyright (C) 2010 Osmo Salomaa
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

import aeidon
import gaupol
import os
import shutil


class TestConfigurationStore(gaupol.TestCase):

    def setup_method(self, method):
        self.conf = gaupol.ConfigurationStore()
        self.directory = aeidon.temp.create_directory()
        self.conf.path = os.path.join(self.directory, "test")

    def teardown_method(self, method):
        shutil.rmtree(self.directory)

    def test_connect_notify(self):
        class PuppetObserver:
            def _on_conf_editor_notify_undo_limit(self, obj, value):
                assert value == 99
        puppet = PuppetObserver()
        self.conf.connect_notify("editor", "undo_limit", puppet)
        self.conf.editor.undo_limit = 99

    def test_disconnect_notify(self):
        class PuppetObserver:
            def _on_conf_editor_notify_undo_limit(self, obj, value):
                assert value == 99
        puppet = PuppetObserver()
        self.conf.connect_notify("editor", "undo_limit", puppet)
        self.conf.editor.undo_limit = 99
        self.conf.disconnect_notify("editor", "undo_limit", puppet)
        self.conf.editor.undo_limit = 100

    def test_query_default(self):
        assert not self.conf.query_default("application_window", "maximized")
        self.conf.application_window.maximized = True
        assert not self.conf.query_default("application_window", "maximized")

    def test_read_from_file(self):
        self.conf.write_to_file()
        self.conf.restore_defaults()
        self.conf.read_from_file()

    def test_register_extension(self):
        self.conf.register_extension("test",
                                     {"x": 1, "mode": aeidon.modes.TIME},
                                     {"mode": aeidon.modes})

        assert self.conf.extensions.test.x == 1
        assert self.conf.extensions.test.mode == aeidon.modes.TIME

    def test_restore_defaults(self):
        size = list(self.conf.application_window.size)
        self.conf.application_window.size = [99, 99]
        self.conf.restore_defaults()
        assert self.conf.application_window.size == size

    def test_write_to_file(self):
        self.conf.write_to_file()
        self.conf.restore_defaults()
        self.conf.read_from_file()

    def test_write_to_file__io_error(self):
        os.chmod(self.directory, 0o000)
        self.assert_raises(IOError, self.conf.write_to_file)
        os.chmod(self.directory, 0o777)
