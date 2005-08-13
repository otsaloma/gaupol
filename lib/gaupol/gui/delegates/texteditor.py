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


"""Editor of text data."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.gui.constants import NO, SHOW, HIDE, DURN, TEXT, TRAN
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.delegates.durmanager import DURAction
from gaupol.gui.dialogs.error import PasteFitErrorDialog


class TextEditAction(DURAction):

    """Base class for text-editing actions."""

    def __init__(self, project):

        self.project         = project
        self.sel_data_rows   = project.get_selected_data_rows()
        self.focus_store_col = project.get_store_focus()[1]

        texts = project.data.texts
        data_col = self.focus_store_col - 4
        self.orig_texts = [texts[i][data_col] for i in self.sel_data_rows]

        documents = ['main'] * 5 + ['translation']
        self.document = documents[self.focus_store_col]

    def undo(self):
        """Undo text-editing."""

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


class CaseChangeAction(TextEditAction):

    """Action to change text case."""

    def __init__(self, project, method):
        """
        Initialize a CaseChangeAction object.
        
        method: "capitalize", "upper", "lower", "title" or "swapcase"
        """
        TextEditAction.__init__(self, project)

        self.method  = method

        descriptions = [
            None, None, None, None,
            _('Changing text case'),
            _('Changing translation case')
        ]
        self.description = descriptions[self.focus_store_col]

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


class ClearAction(TextEditAction):

    """Action to clear text."""

    def __init__(self, project):

        TextEditAction.__init__(self, project)

        descriptions = [
            None, None, None, None,
            _('Clearing text case'),
            _('Clearing translation case')
        ]
        self.description = descriptions[self.focus_store_col]

    def do(self):
        """Clear text."""

        store     = self.project.tree_view.get_model()
        data      = self.project.data
        texts     = self.project.data.texts
        data_col  = self.focus_store_col - 4
        store_col = self.focus_store_col

        for i in range(len(self.sel_data_rows)):
        
            data_row = self.sel_data_rows[i]
            store_row = self.project.get_store_row(data_row)
            data.clear_text(data_row, data_col)
            store[store_row][store_col] = texts[data_row][data_col]


class CutAction(ClearAction):

    """Action to clear text after text has been copied to clipboard."""

    def __init__(self, project):

        ClearAction.__init__(self, project)

        descriptions = [
            None, None, None, None,
            _('Cutting text'),
            _('Cutting translation')
        ]
        self.description = descriptions[self.focus_store_col]


class DialogLineAction(TextEditAction):

    """Action to toggle dialog lines on text."""

    def __init__(self, project):

        TextEditAction.__init__(self, project)

        descriptions = [
            None, None, None, None,
            _('Toggling text dialog lines'),
            _('Toggling translation dialog lines')
        ]
        self.description = descriptions[self.focus_store_col]

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


class ItalicAction(TextEditAction):

    """Action to toggle text italicization."""

    def __init__(self, project):

        TextEditAction.__init__(self, project)

        descriptions = [
            None, None, None, None,
            _('Toggling text italicization'),
            _('Toggling translation italicization')
        ]
        self.description = descriptions[self.focus_store_col]

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


class PasteAction(DURAction):

    """Action to paste text cells."""

    def __init__(self, project, texts):

        self.project         = project
        self.sel_data_rows   = project.get_selected_data_rows()
        self.focus_store_col = project.get_store_focus()[1]

        documents = ['main'] * 5 + ['translation']
        self.document = documents[self.focus_store_col]

        descriptions = [
            None, None, None, None,
            _('Pasting text'),
            _('Pasting translation')
        ]
        self.description = descriptions[self.focus_store_col]

        self.new_texts = texts

        start_row = self.sel_data_rows[0]
        data_col  = self.focus_store_col - 4
        texts     = self.project.data.texts

        self.orig_texts = []
        for i in range(len(self.new_texts)):
        
            if self.new_texts[i] is None:
                self.orig_texts.append(None)
                continue
            
            data_row = start_row + i
            self.orig_texts.append(texts[data_row][data_col])

    def do(self):
        """Clear text."""

        store     = self.project.tree_view.get_model()
        data      = self.project.data
        texts     = self.project.data.texts
        data_col  = self.focus_store_col - 4
        store_col = self.focus_store_col

        start_row = self.sel_data_rows[0]

        selection = self.project.tree_view.get_selection()
        selection.unselect_all()

        for i in range(len(self.new_texts)):
        
            if self.new_texts[i] is None:
                continue
            
            data_row = start_row + i
            store_row = self.project.get_store_row(data_row)
            data.set_text(data_row, data_col, self.new_texts[i])
            store[store_row][store_col] = texts[data_row][data_col]
            selection.select_path(store_row)

    def undo(self):
        """Undo text-editing."""

        store     = self.project.tree_view.get_model()
        data      = self.project.data
        texts     = self.project.data.texts
        data_col  = self.focus_store_col - 4
        store_col = self.focus_store_col

        start_row = self.sel_data_rows[0]

        for i in range(len(self.orig_texts)):
        
            if self.orig_texts[i] is None:
                continue
            
            data_row = start_row + i
            store_row = self.project.get_store_row(data_row)
            data.set_text(data_row, data_col, self.orig_texts[i])
            store[store_row][store_col] = texts[data_row][data_col]


class TextEditor(Delegate):

    """Editor of text data."""

    def _change_case(self, method):
        """
        Change case of selected text cells.
        
        method: "capitalize", "upper", "lower", "title" or "swapcase"
        """
        project = self.get_current_project()
        action = CaseChangeAction(project, method)
        self.do_action(project, action)

    def _copy_selection(self):
        """Copy selected data to clipboard."""
        
        project   = self.get_current_project()
        store     = project.tree_view.get_model()
        sel_rows  = project.get_selected_store_rows()
        store_col = project.get_store_focus()[1]
        texts     = []
        
        # Add texts to list and None for unselected elements.
        for row in range(sel_rows[0], sel_rows[-1] + 1):
            if row in sel_rows:
                texts.append(store[row][store_col])
            else:
                texts.append(None)
        
        self.clipboard.set_data(texts)

    def on_clear_activated(self, *args):
        """Clear the selected text cells."""
        
        project = self.get_current_project()
        action = ClearAction(project)
        self.do_action(project, action)

    def on_copy_activated(self, *args):
        """Copy selection to the clipboard."""
        
        self._copy_selection()

    def on_cut_activated(self, *args):
        """Cut selection to the clipboard."""
        
        self._copy_selection()

        project = self.get_current_project()
        action = CutAction(project)
        self.do_action(project, action)

    def on_dialog_lines_activated(self, *args):
        """Toggle dialog lines on selected text cells."""
        
        project = self.get_current_project()
        action = DialogLineAction(project)
        self.do_action(project, action)
        
    def on_italic_style_activated(self, *args):
        """Italicize selected text cells."""

        project = self.get_current_project()
        action = ItalicAction(project)
        self.do_action(project, action)
        
    def on_lower_case_activated(self, *args):
        """Change case to lower in selected text cells."""

        self._change_case('lower')

    def on_paste_activated(self, *args):
        """Paste the clipboard contents."""

        project     = self.get_current_project()
        store       = project.tree_view.get_model()
        top_row     = project.get_selected_store_rows()[0]
        rows_room   = len(store) - top_row
        rows_needed = len(self.clipboard.get_data())
        
        if rows_needed > rows_room:
            dialog = PasteFitErrorDialog(self.window, rows_needed - rows_room)
            dialog.run()
            dialog.destroy()
            return

        action = PasteAction(project, self.clipboard.data)
        self.do_action(project, action)

    def on_sentence_case_activated(self, *args):
        """Change case to sentence in selected text cells."""

        self._change_case('capitalize')
        
    def on_title_case_activated(self, *args):
        """Change case to title in selected text cells."""

        self._change_case('title')
        
    def on_upper_case_activated(self, *args):
        """Change case to upper in selected text cells."""

        self._change_case('upper')
