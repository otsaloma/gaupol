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
import os

from gaupol.gtk.icons             import *
from gaupol.gtk.dialog.spellcheck import SpellCheckDialog
from gaupol.gtk.dialog.spellcheck import _ErrorDialog
from gaupol.gtk.dialog.spellcheck import _SPELL_CHECK_DIR
from gaupol.gtk.page              import Page
from gaupol.gtk.util              import conf, gtklib
from gaupol.test                  import Test


class TestErrorDialog(Test):

    def test_run(self):

        gtklib.run(_ErrorDialog(gtk.Window(), 'fr_FR', 'test'))


class TestSpellCheckDialog(Test):

    def setup_method(self, method):

        conf.spell_check.main_lang = 'en_CA'
        conf.spell_check.tran_lang = 'en_CA'
        conf.spell_check.cols = [MTXT, TTXT]

        self.repl_path = os.path.join(_SPELL_CHECK_DIR, 'en_CA.repl')
        self.dict_path = os.path.join(_SPELL_CHECK_DIR, 'en_CA.dict')
        if not os.path.isfile(self.repl_path):
            self.files.append(self.repl_path)
        if not os.path.isfile(self.dict_path):
            self.files.append(self.dict_path)

        pages = [Page(), Page()]
        for page in pages:
            page.project = self.get_project()
            for i, text in enumerate(page.project.main_texts):
                page.project.main_texts[i] = text.replace('a', 'x')
            for i, text in enumerate(page.project.main_texts):
                page.project.main_texts[i] = text.replace('i', 'z')
            page.reload_all()
        self.dialog = SpellCheckDialog(gtk.Window(), pages)
        self.dialog._set_page(self.dialog._pages[0])
        self.dialog._row = -1
        self.dialog._set_next_text()
        self.dialog._dialog.show()
        self.dialog._advance()

    def teardown_method(self, method):

        Test.teardown_method(self, method)
        self.dialog._dialog.destroy()

    def test_signals(self):

        self.dialog._add_button.emit('clicked')
        self.dialog._add_lower_button.emit('clicked')
        self.dialog._check_button.emit('clicked')
        self.dialog._edit_button.emit('clicked')
        self.dialog._ignore_all_button.emit('clicked')
        self.dialog._ignore_button.emit('clicked')
        self.dialog._join_back_button.emit('clicked')
        self.dialog._join_forward_button.emit('clicked')
        self.dialog._replace_all_button.emit('clicked')
        self.dialog._replace_button.emit('clicked')

    def test_store_replacement(self):

        self.dialog._store_replacement('test', 'rest')

    def test_run(self):

        gtklib.run(self.dialog)
