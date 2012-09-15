# -*- coding: utf-8 -*-

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

import aeidon
import gaupol


class TestAction(gaupol.TestCase):

    def setup_method(self, method):
        self.action = gaupol.Action("test")
        self.action.accelerator = "X"
        self.action.widgets = ("notebook",)
        self.application = gaupol.Application()
        self.application._on_test_activate = lambda *args: None
        self.action.finalize(self.application)

    def test_set_sensitive(self):
        self.action.set_sensitive(False)
        self.action.set_sensitive(True)

    def test_update_sensitivity(self):
        self.action.update_sensitivity(self.application, None)


class TestMenuAction(gaupol.TestCase):

    def setup_method(self, method):
        self.action = gaupol.MenuAction("test")
        self.action.widgets = ("notebook",)
        self.application = gaupol.Application()
        self.application._on_test_activate = lambda *args: None
        self.action.finalize(self.application)


class TestRecentAction(gaupol.TestCase):

    @aeidon.deco.monkey_patch(gaupol.RecentAction, "group")
    def setup_method(self, method):
        gaupol.RecentAction.group = "gaupol-main"
        self.action = gaupol.RecentAction("test")
        self.action.widgets = ("notebook",)
        self.application = gaupol.Application()
        self.application._on_test_item_activated = lambda *args: None
        self.action.finalize(self.application)


class TestToggleAction(gaupol.TestCase):

    def setup_method(self, method):
        self.action = gaupol.ToggleAction("test")
        self.action.widgets = ("notebook",)
        self.application = gaupol.Application()
        self.application._on_test_toggled = lambda *args: None
        self.action.finalize(self.application)


class TestTopMenuAction(gaupol.TestCase):

    def setup_method(self, method):
        self.action = gaupol.TopMenuAction("test")
        self.action.widgets = ("notebook",)
        self.application = gaupol.Application()
        self.action.finalize(self.application)


class TestRadioAction(gaupol.TestCase):

    def setup_method(self, method):
        self.action = gaupol.RadioAction("test")
        self.action.widgets = ("notebook",)
        self.action.group = self.action.__class__.__name__
        self.application = gaupol.Application()
        self.application._on_test_changed = lambda *args: None
        self.action.finalize(self.application)
