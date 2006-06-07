# Copyright (C) 2005-2006 Osmo Salomaa
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


import gtk

from gaupol.gtk.dialog.message import ErrorDialog
from gaupol.gtk.dialog.message import InfoDialog
from gaupol.gtk.dialog.message import QuestionDialog
from gaupol.gtk.dialog.message import WarningDialog
from gaupol.test               import Test


class TestErrorDialog(Test):

    def test_init(self):

        ErrorDialog(gtk.Window(), 'test', 'test')


class TestInfoDialog(Test):

    def test_init(self):

        InfoDialog(gtk.Window(), 'test', 'test')


class TestQuestionDialog(Test):

    def test_init(self):

        QuestionDialog(gtk.Window(), 'test', 'test')


class TestWarningDialog(Test):

    def test_init(self):

        WarningDialog(gtk.Window(), 'test', 'test')
