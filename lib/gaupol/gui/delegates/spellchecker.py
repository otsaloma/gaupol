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


import gc

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.constants import TYPE
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.delegates.durmanager import DURAction
from gaupol.gui.dialogs.language import LanguageDialog
from gaupol.gui.spellcheck import SpellCheckWindow
from gaupol.gui.util import gui


class SpellCheckAction(DURAction):

    """Action for spell-checking."""

    def __init__(self, project, orig_texts, new_texts, check_text, check_tran):

        self.project = project
        
        self._orig_texts = orig_texts
        self._new_texts  = new_texts
        
        self.documents = []
        self.description = _('Spell-checking')

        if check_text:
            self.documents.append(TYPE.MAIN)
        
        if check_tran:
            self.documents.append(TYPE.TRAN)

    def redo(self):
        """Restore spell-checked texts."""
        
        self.project.data.texts = self._new_texts[:]
        self.project.reload_all_data()
        
    def undo(self):
        """Restore original texts."""
        
        #print 'undoing'
        self.project.data.texts = self._orig_texts[:]
        #print self._orig_texts[:][3][0]
        #print self.project.data.texts[:][3][0]
        self.project.reload_all_data()


class SpellChecker(Delegate):

    """Spell-checking documents."""
    
    def on_check_spelling_activated(self, *args):
        """Start spell-checking document(s)."""
        
        projects = [self.get_current_project()]
        if self.config.get('spell_check', 'check_all_documents'):
            projects = self.projects
            
        check_text = self.config.getboolean('spell_check', 'check_text'       )
        check_tran = self.config.getboolean('spell_check', 'check_translation')
            
        text_lang = self.config.get('spell_check', 'text_language'       )
        tran_lang = self.config.get('spell_check', 'translation_language')
        
        orig_texts = []
        new_texts  = []
        
        for project in projects:
            from copy import deepcopy
            # TODO:
            # Why the heck do we need deepcopy!?
            # Why not [:], list() or copy()
            # Because the texts list is nested!
            # TODO: always deepcopy for nested lists!?
            lista = deepcopy(project.data.texts)
            orig_texts.append(lista)
        
        def on_cell_selected(window, project, row, col):
            """Move focus to cell and scroll to it."""
            
            tree_view = project.tree_view
            tree_view_column = tree_view.get_column(col)
            tree_view.set_cursor(row, tree_view_column)
            tree_view.scroll_to_cell(row, tree_view_column, True, 0.5, 0.5)

        def on_checking_done(window):
            """Save spell-checked texts."""

            print orig_texts[0][3][0]
            
            for project in projects:
                new_texts.append(project.data.texts[:])
                
            for i in range(len(projects)):
                action = SpellCheckAction(
                    projects[i], orig_texts[i], new_texts[i],
                    check_text, check_tran
                )
                self.register_action(action)

            del window
            gc.collect()

        def on_project_selected(window, project):
            """Change to the page in the notebook that holds project."""

            index = self.projects.index(project)
            self.notebook.set_current_page(index)

        window = SpellCheckWindow(
            self.window, projects, check_text, check_tran,
            text_lang, tran_lang
        )
        
        window.connect('cell-selected'   , on_cell_selected   )
        window.connect('checking-done'   , on_checking_done   )
        window.connect('project-selected', on_project_selected)

    def on_set_language_and_target_activated(self, *args):
        """Select language and target for spell-checking."""
        
        gui.set_cursor_busy(self.window)
        dialog = LanguageDialog(self.window)
        
        settings = [
            (dialog.set_check_all_documents , 'check_all_documents' ),
            (dialog.set_check_text          , 'check_text'          ),
            (dialog.set_check_translation   , 'check_translation'   ),
            (dialog.set_text_language       , 'text_language'       ),
            (dialog.set_translation_language, 'translation_language'),
        ]
        
        # Set boolean values to dialog.
        for method, setting in settings[:3]:
            method(self.config.getboolean('spell_check', setting))
            
        # Set string values to dialog.
        for method, setting in settings[3:]:
            method(self.config.get('spell_check', setting))
            
        gui.set_cursor_normal(self.window)
        dialog.run()
        
        settings = [
            (dialog.get_check_all_documents , 'check_all_documents' ),
            (dialog.get_check_text          , 'check_text'          ),
            (dialog.get_check_translation   , 'check_translation'   ),
            (dialog.get_text_language       , 'text_language'       ),
            (dialog.get_translation_language, 'translation_language'),
        ]
        
        # Save boolean values.
        for method, setting in settings[:3]:
            self.config.setboolean('spell_check', setting, method())
            
        # Save string values.
        for method, setting in settings[3:]:
            value = method()
            if value is not None:
                self.config.set('spell_check', setting, value)
            
        dialog.destroy()
