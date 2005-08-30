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


"""Spell-checking documents."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.dialogs.language import LanguageDialog


class SpellChecker(Delegate):

    """Spell-checking documents."""
    
    def on_check_spelling_activated(self, *args):
        """Start spell-checking document(s)."""
        
        pass
        
    def on_set_language_and_target_activated(self, *args):
        """Select language and target for spell-checking."""
        
        dialog = LanguageDialog(self.window)
        
        settings = [
            (dialog.set_check_all_documents , 'check_all_documents' ),
            (dialog.set_check_text          , 'check_text'          ),
            (dialog.set_check_translation   , 'check_translation'   ),
            (dialog.set_text_language       , 'text_language'       ),
            (dialog.set_translation_language, 'translation_language'),
        ]
        
        # Set boolean values.
        for method, setting in settings[:3]:
            method(self.config.getboolean('spell_check', setting))
            
        # Set string values.
        for method, setting in settings[3:]:
            method(self.config.get('spell_check', setting))
        
        dialog.run()
        
        # Get new boolean values.
        value = dialog.get_check_all_documents()
        self.config.setboolean('spell_check', 'check_all_documents', value)
        value = dialog.get_check_text()
        self.config.setboolean('spell_check', 'check_text', value)
        value = dialog.get_check_translation()
        self.config.setboolean('spell_check', 'check_translation', value)
        
        # Get new text language.
        lang = dialog.get_text_language()
        if lang is not None:
            self.config.set('spell_check', 'text_language', lang)
        
        # Get new translation language.
        lang = dialog.get_translation_language()
        if lang is not None:
            self.config.set('spell_check', 'translation_language', lang)
            
        dialog.destroy()
