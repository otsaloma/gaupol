# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import gaupol

from gi.repository import Gtk


class _TestMessageDialog(gaupol.TestCase):

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()


class TestErrorDialog(_TestMessageDialog):

    def setup_method(self, method):
        self.dialog = gaupol.ErrorDialog(Gtk.Window(), "test", "test")
        self.dialog.add_button("_OK", Gtk.ResponseType.OK)
        self.dialog.set_default_response(Gtk.ResponseType.OK)
        self.dialog.show()


class TestInfoDialog(_TestMessageDialog):

    def setup_method(self, method):
        self.dialog = gaupol.InfoDialog(Gtk.Window(), "test", "test")
        self.dialog.add_button("_OK", Gtk.ResponseType.OK)
        self.dialog.set_default_response(Gtk.ResponseType.OK)
        self.dialog.show()


class TestQuestionDialog(_TestMessageDialog):

    def setup_method(self, method):
        self.dialog = gaupol.QuestionDialog(Gtk.Window(), "test", "test")
        self.dialog.add_button("_No", Gtk.ResponseType.NO)
        self.dialog.add_button("_Yes", Gtk.ResponseType.YES)
        self.dialog.set_default_response(Gtk.ResponseType.YES)
        self.dialog.show()


class TestWarningDialog(_TestMessageDialog):

    def setup_method(self, method):
        self.dialog = gaupol.WarningDialog(Gtk.Window(), "test", "test")
        self.dialog.add_button("_OK", Gtk.ResponseType.OK)
        self.dialog.set_default_response(Gtk.ResponseType.OK)
        self.dialog.show()
