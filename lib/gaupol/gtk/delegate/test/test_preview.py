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

from gaupol.gtk.app              import Application
from gaupol.gtk.delegate.preview import PreviewDelegate
from gaupol.gtk.delegate.preview import _IOErrorDialog
from gaupol.gtk.delegate.preview import _UnicodeErrorDialog
from gaupol.gtk.util             import gtklib
from gaupol.test                 import Test


class TestIOErrorDialog(Test):

    def test_run(self):

        gtklib.run(_IOErrorDialog(gtk.Window(), 'test'))


class TestUnicodeErrorDialog(Test):

    def test_run(self):

        gtklib.run(_UnicodeErrorDialog(gtk.Window()))


class TestPreviewDelegate(Test):

    def setup_method(self, method):

        self.app = Application()
        self.delegate = PreviewDelegate(self.app)

    def teardown_method(self, method):

        Test.teardown_method(self, method)
        self.app._window.destroy()

    def test_post_process(self):

        data = ('test', self.get_subrip_path(), self.get_subrip_path())
        self.delegate._post_process(333, 0, data)

        data = ('test', self.get_subrip_path(), self.get_subrip_path())
        self.delegate._post_process(333, 1, data)
