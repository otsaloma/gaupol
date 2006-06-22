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


from gaupol.gtk.app   import Application
from gaupol.gtk.icons import *
from gaupol.test      import Test


class TestFormatDelegate(Test):

    def setup_method(self, method):

        self.app = Application()
        self.app.open_main_files([self.get_subrip_path()])
        page = self.app.get_current_page()
        page.view.set_focus(0, MTXT)
        page.view.select_rows([0, 1, 2, 3])

    def teardown_method(self, method):

        Test.teardown_method(self, method)
        self.app._window.destroy()

    def test_actions(self):

        self.app.on_toggle_dialog_lines_activate()
        self.app.on_toggle_dialog_lines_activate()
        self.app.on_toggle_italicization_activate()
        self.app.on_toggle_italicization_activate()
        self.app.on_use_lower_case_activate()
        self.app.on_use_lower_case_activate()
        self.app.on_use_sentence_case_activate()
        self.app.on_use_sentence_case_activate()
        self.app.on_use_title_case_activate()
        self.app.on_use_title_case_activate()
        self.app.on_use_upper_case_activate()
        self.app.on_use_upper_case_activate()
