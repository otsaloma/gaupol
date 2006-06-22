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


"""Checking spelling."""


from gettext import gettext as _

import gtk

from gaupol.gtk                   import cons
from gaupol.gtk.colcons           import *
from gaupol.gtk.delegate          import Delegate, UIMAction
from gaupol.gtk.dialog.language   import LanguageDialog
from gaupol.gtk.dialog.spellcheck import SpellCheckDialog
from gaupol.gtk.error             import Default
from gaupol.gtk.util              import config, gtklib


_ENCHANT_AVAILABLE = False
try:
    import enchant
    if enchant.__version__ < '1.1.3':
        raise ImportError
    _ENCHANT_AVAILABLE = True
except ImportError:
    print 'PyEnchant 1.1.3 or greater not found. Spell-checking not possible.'
except enchant.Error, message:
    print 'PyEnchant error: %s. Spell-checking not possible.' % message


class CheckSpellingAction(UIMAction):

    """Check spelling."""

    action_item = (
        'check_spelling',
        gtk.STOCK_SPELL_CHECK,
        _('_Check Spelling'),
        'F7',
        _('Check for incorrect spelling'),
        'on_check_spelling_activate'
    )

    paths = [
        '/ui/menubar/tools/check_spelling',
        '/ui/main_toolbar/check_spelling'
    ]

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        if not _ENCHANT_AVAILABLE:
            return False

        if not config.spell_check.cols:
            return False
        if MTXT in config.spell_check.cols:
            if not config.spell_check.main_lang:
                return False
        if TTXT in config.spell_check.cols:
            if not config.spell_check.tran_lang:
                return False

        return True


class ConfigureSpellCheckAction(UIMAction):

    """Configure spell-check."""

    action_item = (
        'configure_spell_check',
        None,
        _('Co_nfigure Spell-check...'),
        None,
        _('Set languages and spell-check targets'),
        'on_configure_spell_check_activate'
    )

    paths = ['/ui/menubar/tools/configure_spell_check']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return _ENCHANT_AVAILABLE


class SpellCheckDelegate(Delegate):

    """Checking spelling."""

    def _on_page_checked(self, dialog, page, rows, texts):
        """Commit changes to texts."""

        if not rows[0] and not rows[1]:
            return

        page.project.replace_both_texts(rows, texts)
        page.project.set_action_description(
            cons.Action.DO, _('Spell-checking'))

    def _on_page_selected(self, dialog, page):
        """Select page."""

        index = self.pages.index(page)
        self._notebook.set_current_page(index)

    def on_check_spelling_activate(self, *args):
        """Check spelling."""

        pages = self.get_target_pages(config.spell_check.target)
        try:
            dialog = SpellCheckDialog(self._window, pages)
        except Default:
            return
        dialog.connect('page-checked' , self._on_page_checked )
        dialog.connect('page-selected', self._on_page_selected)
        gtklib.run(dialog)

    def on_configure_spell_check_activate(self, *args):
        """Configure spell-check."""

        gtklib.set_cursor_busy(self._window)
        dialog = LanguageDialog(self._window)
        gtklib.set_cursor_normal(self._window)
        gtklib.run(dialog)

        page = self.get_current_page()
        self.set_sensitivities(page)
