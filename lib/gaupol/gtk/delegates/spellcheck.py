# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Checking spelling."""


try:
    from psyco.classes import *
except ImportError:
    pass

import logging

import gtk

from gaupol.constants              import Action, Document
from gaupol.gtk.delegates          import Delegate, UIMAction
from gaupol.gtk.dialogs.language   import LanguageDialog
from gaupol.gtk.dialogs.spellcheck import SpellCheckDialog
from gaupol.gtk.error              import Cancelled
from gaupol.gtk.util               import config, gtklib


logger = logging.getLogger()


# Check if PyEnchant 1.1.3 or later is available.
enchant_available = False
try:
    import enchant
    if enchant.__version__ < '1.1.3':
        raise ImportError
    enchant_available = True
except ImportError:
    msg  = 'PyEnchant 1.1.3 or greater not found. '
    msg += 'Spell-checking not possible.'
    logger.info(msg)
except enchant.Error, detail:
    msg  = 'PyEnchant: %s. ' % detail
    msg += 'Spell-checking not possible.'
    logger.error(msg)


class ConfigureSpellCheckAction(UIMAction):

    """Configure spell-check."""

    uim_action_item = (
        'configure_spell_check',
        None,
        _('Co_nfigure Spell-check'),
        None,
        _('Set document languages and spell-check targets'),
        'on_configure_spell_check_activated'
    )

    uim_paths = ['/ui/menubar/tools/configure_spell_check']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return enchant_available


class SpellCheckAction(UIMAction):

    """Check spelling."""

    uim_action_item = (
        'check_spelling',
        gtk.STOCK_SPELL_CHECK,
        _('_Check Spelling'),
        'F7',
        _('Check for incorrect spelling'),
        'on_check_spelling_activated'
    )

    uim_paths = [
        '/ui/menubar/tools/check_spelling',
        '/ui/toolbar/check_spelling'
    ]

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False

        if not enchant_available:
            return False

        if not config.spell_check.check_main and \
           not config.spell_check.check_translation:
            return False

        if config.spell_check.check_main and \
           config.spell_check.main_language is None:
            return False

        if config.spell_check.check_translation and \
           config.spell_check.translation_language is None:
            return False

        return True


class SpellCheckDelegate(Delegate):

    """Checking spelling."""

    def _on_cell_selected(self, dialog, page, row, document):
        """Show cell."""

        page.view.set_focus(row, document + 4)
        page.view.scroll_to_row(row)

    def on_check_spelling_activated(self, *args):
        """Check for incorrent spelling."""

        # Get pages to check.
        if config.spell_check.check_all_projects:
            pages = self.pages
        else:
            pages = [self.get_current_page()]

        try:
            dialog = SpellCheckDialog(self.window, pages)
        except Cancelled:
            return

        dialog.connect('cell-selected', self._on_cell_selected)
        dialog.connect('destroyed'    , self._on_destroyed    )
        dialog.connect('page-checked' , self._on_page_checked )
        dialog.connect('page-selected', self._on_page_selected)

        dialog.show()

    def on_configure_spell_check_activated(self, *args):
        """Configure spell-check."""

        gtklib.set_cursor_busy(self.window)
        dialog = LanguageDialog(self.window)
        gtklib.set_cursor_normal(self.window)
        dialog.run()
        dialog.destroy()

    def _on_destroyed(self, dialog):
        """Delete dialog."""

        gtklib.destroy_gobject(dialog)

    def _on_page_checked(self, dialog, page, rows, texts):
        """
        Commit changes to texts.

        rows: (main text rows, translation text rows)
        texts: (main texts, translation texts)
        """
        MAIN = 0
        TRAN = 1

        if not rows[MAIN] and not rows[TRAN]:
            return

        if rows[MAIN] and rows[TRAN]:
            page.project.replace_both_texts(rows, texts)
        elif rows[MAIN]:
            page.project.replace_texts(rows[MAIN], Document.MAIN, texts[MAIN])
        elif rows[TRAN]:
            page.project.replace_texts(rows[TRAN], Document.TRAN, texts[TRAN])
        else:
            return

        desc = _('Spell-checking')
        page.project.modify_action_description(Action.DO, desc)
        self.set_sensitivities(page)

    def _on_page_selected(self, dialog, page):
        """Show page."""

        index = self.pages.index(page)
        self.notebook.set_current_page(index)
