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

from gaupol.gtk.app           import Application
from gaupol.gtk.delegate.help import _VersionErrorDialog
from gaupol.gtk.delegate.help import _VersionInfoDialog
from gaupol.gtk.util          import gtklib
from gaupol.test              import Test


class TestVersionCheckErrorDialog(Test):

    def test_run(self):

        gtklib.run(_VersionErrorDialog(gtk.Window(), 'test'))


class TestVersionCheckInfoDialog(Test):

    def test_run(self):

        gtklib.run(_VersionInfoDialog(gtk.Window(), '0.0.1', '0.0.1'))
        gtklib.run(_VersionInfoDialog(gtk.Window(), '0.0.1', '0.0.2'))


class TestHelpDelegate(Test):

    def setup_method(self, method):

        self.app = Application()

    def teardown_method(self, method):

        Test.teardown_method(self, method)
        self.app._window.destroy()

    def test_actions(self):

        self.app.on_check_latest_version_activate()
        self.app.on_report_a_bug_activate()
        self.app.on_view_about_dialog_activate()
