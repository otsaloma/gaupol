# Copyright (C) 2005-2007 Osmo Salomaa
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

import gtk

from gaupol.gtk import unittest
from .. import message


class _TestMessageDialog(unittest.TestCase):

    def run(self):

        # pylint: disable-msg=E1101
        self.dialog.run()
        self.dialog.destroy()

    def test___init__(self):

        pass


class TestErrorDialog(_TestMessageDialog):

    def setup_method(self, method):

        self.dialog = message.ErrorDialog(gtk.Window(), "test", "test")
        self.dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)


class TestInfoDialog(_TestMessageDialog):

    def setup_method(self, method):

        self.dialog = message.InfoDialog(gtk.Window(), "test", "test")
        self.dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)


class TestQuestionDialog(_TestMessageDialog):

    def setup_method(self, method):

        self.dialog = message.QuestionDialog(gtk.Window(), "test", "test")
        self.dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)


class TestWarningDialog(_TestMessageDialog):

    def setup_method(self, method):

        self.dialog = message.WarningDialog(gtk.Window(), "test", "test")
        self.dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
