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


import os

from gaupol.gtk.app                 import Application
from gaupol.gtk.icons               import *
from gaupol.gtk.delegate.spellcheck import SpellCheckDelegate
from gaupol.gtk.dialog.spellcheck   import _SPELL_CHECK_DIR
from gaupol.gtk.util                import conf
from gaupol.test                    import Test


class TestSpellCheckDelegate(Test):

    def setup_method(self, method):

        self.app = Application()
        self.app.open_main_files([self.get_subrip_path()])
        self.delegate = SpellCheckDelegate(self.app)

        conf.spell_check.main_lang = 'en_CA'
        conf.spell_check.tran_lang = 'en_CA'
        conf.spell_check.cols = [MTXT, TTXT]

        self.repl_path = os.path.join(_SPELL_CHECK_DIR, 'en_CA.repl')
        self.dict_path = os.path.join(_SPELL_CHECK_DIR, 'en_CA.dict')
        if not os.path.isfile(self.repl_path):
            self.files.append(self.repl_path)
        if not os.path.isfile(self.dict_path):
            self.files.append(self.dict_path)

    def teardown_method(self, method):

        self.app._window.destroy()

    def test_on_page_checked(self):

        page = self.app.get_current_page()
        rows = [[1, 2], [0]]
        texts = [['a', 'b'], ['c']]
        self.delegate._on_page_checked(None, page, rows, texts)

    def test_on_page_selected(self):

        page = self.app.get_current_page()
        self.delegate._on_page_selected(None, page)

    def test_actions(self):

        self.app.on_check_spelling_activate()
        self.app.on_configure_spell_check_activate()
