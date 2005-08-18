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


"""Editing of text data."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.constants import POSITION
from gaupol.gui.colcons import *
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.delegates.durmanager import DURAction
from gaupol.gui.dialogs.question import PasteFitQuestionDialog


class TextEditAction(DURAction):

    """Base class for text-editing actions."""

    def __init__(self, project):

        self.project = project

        self._col = project.get_focus()[1]
        self._rows = project.get_selected_rows()

        # Save original texts.
        texts = project.data.texts
        data_col = project.get_data_column(self._col)
        self._orig_texts = [texts[row][data_col] for row in self._rows]

        self.documents = [project.get_document_type(self._col)]

    def undo(self):
        """Undo text-editing."""

        texts = self.project.data.texts
        model = self.project.tree_view.get_model()
        data_col = self.project.get_data_column(self._col)

        for i in range(len(self._rows)):
            row = self._rows[i]
            text = self._orig_texts[i]
            model[row][self._col] = text
            texts[row][ data_col] = text


class CaseChangeAction(TextEditAction):

    """Action to change text case."""

    def __init__(self, project, method):
        """
        Initialize a CaseChangeAction object.
        
        method: "capitalize", "upper", "lower", "title" or "swapcase"
        """
        TextEditAction.__init__(self, project)

        self._method  = method

        data_col = project.get_data_column(self._col)
        first = self._rows[ 0] + 1
        last  = self._rows[-1] + 1
        subs  = (first, last)

        descriptions = (
            (
                _('Changing case of text of subtitle %d')        % first,
                _('Changing case of translation of subtitle %d') % first
            ), (
                _('Changing case of text of subtitles %d, ... , %d') % subs,
                _('Changing case of translation of subtitles %d, ... , %d') \
                % subs
            )
        )
        self.description = descriptions[min(last - first, 1)][data_col]

    def do(self):
        """Change case."""

        model    = self.project.tree_view.get_model()
        data     = self.project.data
        texts    = self.project.data.texts
        col      = self._col
        data_col = self.project.get_data_column(col)

        data.change_case(self._rows, data_col, self._method)
        
        for row in self._rows:
            model[row][col] = texts[row][data_col]


class ClearAction(TextEditAction):

    """Action to clear text."""

    def __init__(self, project):

        TextEditAction.__init__(self, project)

        data_col = project.get_data_column(self._col)
        first = self._rows[ 0] + 1
        last  = self._rows[-1] + 1
        subs  = (first, last)

        descriptions = (
            (
                _('Clearing text of subtitle %d')        % first,
                _('Clearing translation of subtitle %d') % first
            ), (
                _('Clearing text of subtitles %d, ... , %d')        % subs,
                _('Clearing translation of subtitles %d, ... , %d') % subs
            )
        )
        self.description = descriptions[min(last - first, 1)][data_col]

    def do(self):
        """Clear text."""

        model    = self.project.tree_view.get_model()
        texts    = self.project.data.texts
        col      = self._col
        data_col = self.project.get_data_column(col)
        
        for row in self._rows:
            texts[row][data_col] = u''
            model[row][     col] = u''


class CutAction(ClearAction):

    """Action to clear text after text has been copied to clipboard."""

    def __init__(self, project):

        ClearAction.__init__(self, project)

        data_col = project.get_data_column(self._col)
        first = self._rows[ 0] + 1
        last  = self._rows[-1] + 1
        subs  = (first, last)

        descriptions = (
            (
                _('Cutting text of subtitle %d')        % first,
                _('Cutting translation of subtitle %d') % first
            ), (
                _('Cutting text of subtitles %d, ... , %d')        % subs,
                _('Cutting translation of subtitles %d, ... , %d') % subs
            )
        )
        self.description = descriptions[min(last - first, 1)][data_col]


class DialogLineAction(TextEditAction):

    """Action to toggle dialog lines on text."""

    def __init__(self, project):

        TextEditAction.__init__(self, project)

        data_col = project.get_data_column(self._col)
        first = self._rows[ 0] + 1
        last  = self._rows[-1] + 1
        subs  = (first, last)

        descriptions = (
            (
                _('Toggling dialog lines on text of subtitle %d')        \
                % first,
                _('Toggling dialog lines on translation of subtitle %d') \
                % first
            ), (
                _('Toggling dialog lines on text of subtitles %d, ... , %d') \
                % subs,
                _('Toggling dialog lines on translation of subtitles %d, ... , %d') \
                % subs
            )
        )
        self.description = descriptions[min(last - first, 1)][data_col]

    def do(self):
        """Toggle dialog lines."""

        model    = self.project.tree_view.get_model()
        data     = self.project.data
        texts    = self.project.data.texts
        col      = self._col
        data_col = self.project.get_data_column(col)

        data.toggle_dialog_lines(self._rows, data_col)
        
        for row in self._rows:
            model[row][col] = texts[row][data_col]


class ItalicAction(TextEditAction):

    """Action to toggle text italicization."""

    def __init__(self, project):

        TextEditAction.__init__(self, project)

        data_col = project.get_data_column(self._col)
        first = self._rows[ 0] + 1
        last  = self._rows[-1] + 1
        subs  = (first, last)

        descriptions = (
            (
                _('Toggling italicization of text of subtitle %d')        \
                % first,
                _('Toggling italicization of translation of subtitle %d') \
                % first
            ), (
                _('Toggling italicization of text of subtitles %d, ... , %d') \
                % subs,
                _('Toggling italicization of translation of subtitles %d, ... , %d') \
                % subs
            )
        )
        self.description = descriptions[min(last - first, 1)][data_col]

    def do(self):
        """Toggle italicization."""

        model    = self.project.tree_view.get_model()
        data     = self.project.data
        texts    = self.project.data.texts
        col      = self._col
        data_col = self.project.get_data_column(col)

        data.toggle_italicization(self._rows, data_col)
        
        for row in self._rows:
            model[row][col] = texts[row][data_col]


class PasteAction(DURAction):

    """Action to paste texts from clipboard."""

    def __init__(self, project, texts):

        self.project = project

        self._col = project.get_focus()[1]
        self._start_row = project.get_selected_rows()[0]

        # Texts from clipboard.
        self._new_texts = texts

        data_col = project.get_data_column(self._col)
        texts = self.project.data.texts
        self._orig_texts = []
        
        # Save original texts. Skipped rows have None elements.
        for i in range(len(self._new_texts)):
        
            if self._new_texts[i] is None:
                self._orig_texts.append(None)
                continue
            
            row = self._start_row + i
            self._orig_texts.append(texts[row][data_col])


        self.documents = [project.get_document_type(self._col)]

        data_col = project.get_data_column(self._col)
        first = self._start_row + 1
        last  = self._start_row + len(self._new_texts)
        subs  = (first, last)

        descriptions = (
            (
                _('Pasting to text of subtitle %d')                   % first,
                _('Pasting to translation of subtitle %d')            % first
            ), (
                _('Pasting to text of subtitles %d, ... , %d')        % subs,
                _('Pasting to translation of subtitles %d, ... , %d') % subs
            )
        )
        self.description = descriptions[min(last - first, 1)][data_col]

    def do(self):
        """Paste texts from clipboard."""

        model    = self.project.tree_view.get_model()
        data     = self.project.data
        texts    = self.project.data.texts
        col      = self._col
        data_col = self.project.get_data_column(self._col)

        # Unselect all subtitles.
        selection = self.project.tree_view.get_selection()
        selection.unselect_all()

        for i in range(len(self._new_texts)):
        
            if self._new_texts[i] is None:
                continue
            
            row = self._start_row + i
            text = self._new_texts[i]
            
            # Set data.
            data.set_text(row, data_col, text)
            model[row][col] = text
            
            # Selected row where pasted.
            selection.select_path(row)

    def undo(self):
        """Restore original texts."""

        model    = self.project.tree_view.get_model()
        data     = self.project.data
        texts    = self.project.data.texts
        col      = self._col
        data_col = self.project.get_data_column(self._col)

        for i in range(len(self._orig_texts)):
        
            if self._orig_texts[i] is None:
                continue
            
            row = self._start_row + i
            text = self._orig_texts[i]
            
            # Set data.
            data.set_text(row, data_col, text)
            model[row][col] = text


class TextEditor(Delegate):

    """Editing of text data."""

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
        
        project = self.get_current_project()
        model = project.tree_view.get_model()
        selected_rows = project.get_selected_rows()
        col = project.get_focus()[1]
        texts = []
        
        # Add selected texts to list and None for unselected elements.
        for row in range(selected_rows[0], selected_rows[-1] + 1):
            if row in selected_rows:
                texts.append(model[row][col])
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

    def on_dialog_activated(self, *args):
        """Toggle dialog lines on selected text cells."""
        
        project = self.get_current_project()
        action = DialogLineAction(project)
        self.do_action(project, action)
        
    def on_italic_activated(self, *args):
        """Italicize selected text cells."""

        project = self.get_current_project()
        action = ItalicAction(project)
        self.do_action(project, action)
        
    def on_lower_activated(self, *args):
        """Change case to lower in selected text cells."""

        self._change_case('lower')

    def on_paste_activated(self, *args):
        """Paste the clipboard contents."""

        project = self.get_current_project()
        model = project.tree_view.get_model()
        start_row = project.get_selected_rows()[0]

        rows_room    = len(model) - start_row
        rows_needed  = len(self.clipboard.data)
        rows_lacking = rows_needed - rows_room
        
        if rows_lacking > 0:
        
            dialog = PasteFitQuestionDialog(self.window, rows_lacking)
            response = dialog.run()
            dialog.destroy()

            # User chose not to add new subtitles.
            if response != gtk.RESPONSE_YES:
                return
            
            # Select the very last row to insert new rows at correct location.
            selection = project.tree_view.get_selection()
            selection.unselect_all()
            selection.select_path(len(model) - 1)
            
            # Insert needed amount of rows.
            self.insert_subtitles(POSITION.BELOW, rows_lacking)

            # Restore first row of selection to paste at correct location.
            selection.unselect_all()
            selection.select_path(start_row)

        action = PasteAction(project, self.clipboard.data)
        self.do_action(project, action)

    def on_sentence_activated(self, *args):
        """Change case to sentence in selected text cells."""

        self._change_case('capitalize')
        
    def on_title_activated(self, *args):
        """Change case to title in selected text cells."""

        self._change_case('title')
        
    def on_upper_activated(self, *args):
        """Change case to upper in selected text cells."""

        self._change_case('upper')
