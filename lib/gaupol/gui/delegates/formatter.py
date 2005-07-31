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


"""Formatter to change text style."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.gui.constants import NO, SHOW, HIDE, DURN, ORIG, TRAN
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.delegates.durmanager import DURAction

class FormatAction(DURAction):

    """Base class for formatting actions."""

    def __init__(self, project):

        self.project         = project
        self.sel_data_rows   = project.get_selected_data_rows()
        self.focus_store_col = project.get_store_focus()[1]

        texts = project.data.texts
        col   = self.focus_store_col - 4
        self.orig_texts = [texts[i][col] for i in self.sel_data_rows]

        if self.focus_store_col == TRAN:
            self.document    = 'translation'
        else:
            self.document    = 'main'

    def undo(self):
        """Undo formatting."""

        texts     = self.project.data.texts
        store     = self.project.tree_view.get_model()
        data_col  = self.focus_store_col - 4
        store_col = self.focus_store_col

        for i in range(len(self.sel_data_rows)):

            data_row  = self.sel_data_rows[i]
            store_row = self.project.get_store_row(data_row)
            text      = self.orig_texts[i]

            store[store_row][store_col] = text
            texts[data_row][data_col]   = text


class CaseChangeAction(FormatAction):

    """Action to change text case."""

    def __init__(self, project, method):
        """
        Initialize a CaseChangeAction object.
        
        method: "capitalize", "upper", "lower", "title" or "swapcase"
        """
        FormatAction.__init__(self, project)

        self.method  = method

        if self.focus_store_col == TRAN:
            self.description = _('Changing translation case')
        else:
            self.description = _('Changing text case')

    def do(self):
        """Change case."""

        store     = self.project.tree_view.get_model()
        data      = self.project.data
        data_col  = self.focus_store_col - 4
        store_col = self.focus_store_col

        texts = data.change_case(self.sel_data_rows, data_col, self.method)
        
        for i in range(len(self.sel_data_rows)):
        
            store_row = self.project.get_store_row(self.sel_data_rows[i])
            store[store_row][store_col] = texts[i]


class DialogLineAction(FormatAction):

    """Action to toggle dialog lines on text."""

    def __init__(self, project):

        FormatAction.__init__(self, project)

        if self.focus_store_col == TRAN:
            self.description = _('Toggling translation dialog lines')
        else:
            self.description = _('Toggling text dialog lines')

    def do(self):
        """Toggle dialog lines."""

        store     = self.project.tree_view.get_model()
        data      = self.project.data
        data_col  = self.focus_store_col - 4
        store_col = self.focus_store_col

        texts = data.toggle_dialog_lines(self.sel_data_rows, data_col)
        
        for i in range(len(self.sel_data_rows)):
        
            store_row = self.project.get_store_row(self.sel_data_rows[i])
            store[store_row][store_col] = texts[i]


class ItalicAction(FormatAction):

    """Action to toggle text italicization."""

    def __init__(self, project):

        FormatAction.__init__(self, project)

        if self.focus_store_col == TRAN:
            self.description = _('Toggling translation italicization')
        else:
            self.description = _('Toggling text italicization')

    def do(self):
        """Toggle italicization."""

        store     = self.project.tree_view.get_model()
        data      = self.project.data
        data_col  = self.focus_store_col - 4
        store_col = self.focus_store_col

        texts = data.toggle_italicization(self.sel_data_rows, data_col)
        
        for i in range(len(self.sel_data_rows)):
        
            store_row = self.project.get_store_row(self.sel_data_rows[i])
            store[store_row][store_col] = texts[i]


class Formatter(Delegate):

    """Formatter to change text style."""

    def _change_case(self, method):
        """
        Change case of selected text cells.
        
        method: "capitalize", "upper", "lower", "title" or "swapcase"
        """
        project = self.get_current_project()
        action = CaseChangeAction(project, method)
        self.do_action(project, action)

    def on_dialog_lines_activated(self, *args):
        """Toggle dialog lines on selected text cells."""
        
        project = self.get_current_project()
        action = DialogLineAction(project)
        self.do_action(project, action)

    def on_invert_case_activated(self, *args):
        """Invert case of selected text cells."""

        self._change_case('swapcase')
        
    def on_italic_style_activated(self, *args):
        """Italicize selected text cells."""

        project = self.get_current_project()
        action = ItalicAction(project)
        self.do_action(project, action)
        
    def on_lower_case_activated(self, *args):
        """Change case to lower in selected text cells."""

        self._change_case('lower')

    def on_sentence_case_activated(self, *args):
        """Change case to sentence in selected text cells."""

        self._change_case('capitalize')
        
    def on_title_case_activated(self, *args):
        """Change case to title in selected text cells."""

        self._change_case('title')
        
    def on_upper_case_activated(self, *args):
        """Change case to upper in selected text cells."""

        self._change_case('upper')
