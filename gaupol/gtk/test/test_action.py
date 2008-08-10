# Copyright (C) 2005-2008 Osmo Salomaa
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


class TestAction(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.action = gaupol.gtk.Action("test")
        self.action.accelerator = "X"
        self.action.widgets = ("notebook",)
        self.application = gaupol.gtk.Application()
        self.application.on_test_activate = lambda *args: None
        self.action.finalize(self.application)

    def test_set_sensitive(self):

        self.action.set_sensitive(False)
        self.action.set_sensitive(True)

    def test_update_sensitivity(self):

        self.action.update_sensitivity(self.application, None)


class TestMenuAction(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.action = gaupol.gtk.MenuAction("test")
        self.action.widgets = ("notebook",)
        self.application = gaupol.gtk.Application()
        self.application.on_test_activate = lambda *args: None
        self.action.finalize(self.application)


class TestToggleAction(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.action = gaupol.gtk.ToggleAction("test")
        self.action.widgets = ("notebook",)
        self.application = gaupol.gtk.Application()
        self.application.on_test_toggled = lambda *args: None
        self.action.finalize(self.application)


class TestTopMenuAction(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.action = gaupol.gtk.TopMenuAction("test")
        self.action.widgets = ("notebook",)
        self.application = gaupol.gtk.Application()
        self.action.finalize(self.application)


class TestRadioAction(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.action = gaupol.gtk.RadioAction("test")
        self.action.widgets = ("notebook",)
        self.action.group = self.action.__class__.__name__
        self.application = gaupol.gtk.Application()
        self.application.on_test_changed = lambda *args: None
        self.action.finalize(self.application)
