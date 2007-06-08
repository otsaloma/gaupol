# Copyright (C) 2005-2007 Osmo Salomaa
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


"""Simple subtitle data editing actions."""


import gaupol.gtk
import gtk
_ = gaupol.i18n._

from .action import Action


_TEXT_COLUMNS = (gaupol.gtk.COLUMN.MAIN_TEXT, gaupol.gtk.COLUMN.TRAN_TEXT)


class ClearTextsAction(Action):

    """Clear the selected texts."""

    def __init__(self):

        Action.__init__(self, "clear_texts")
        self.props.label = _("Cl_ear")
        self.props.stock_id = gtk.STOCK_CLEAR
        self.props.tooltip = _("Clear the selected texts")
        self.accelerator = "C"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.view.get_selected_rows()
        assert page.view.get_focus()[1] in _TEXT_COLUMNS


class CopyTextsAction(Action):

    """Copy the selected texts to the clipboard."""

    def __init__(self):

        Action.__init__(self, "copy_texts")
        self.props.label = _("_Copy")
        self.props.stock_id = gtk.STOCK_COPY
        self.props.tooltip = _("Copy the selected texts to the clipboard")
        self.accelerator = "<Control>C"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.view.get_selected_rows()
        assert page.view.get_focus()[1] in _TEXT_COLUMNS


class CutTextsAction(Action):

    """Cut the selected texts to the clipboard."""

    def __init__(self):

        Action.__init__(self, "cut_texts")
        self.props.label = _("Cu_t")
        self.props.stock_id = gtk.STOCK_CUT
        self.props.tooltip = _("Cut the selected texts to the clipboard")
        self.accelerator = "<Control>X"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.view.get_selected_rows()
        assert page.view.get_focus()[1] in _TEXT_COLUMNS


class EditPreferencesAction(Action):

    """Configure Gaupol."""

    def __init__(self):

        Action.__init__(self, "edit_preferences")
        self.props.label = _("_Preferences")
        self.props.stock_id = gtk.STOCK_PREFERENCES
        self.props.tooltip = _("Configure Gaupol")


class EditNextValueAction(Action):

    """Edit the focused column of the next subtitle."""

    def __init__(self):

        Action.__init__(self, "edit_next_value")
        self.props.label = _("Edit _Next Cell")
        self.props.short_label = _("Next")
        self.props.stock_id = gtk.STOCK_EDIT
        self.props.tooltip = _("Edit the focused column of the next subtitle")
        self.accelerator = "space"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        row, col = page.view.get_focus()
        assert not None in (row, col)
        assert row < len(page.project.times) - 1
        assert col != gaupol.gtk.COLUMN.NUMBER


class EditValueAction(Action):

    """Edit the focused cell."""

    def __init__(self):

        Action.__init__(self, "edit_value")
        self.props.is_important = True
        self.props.label = _("_Edit Cell")
        self.props.short_label = _("Edit")
        self.props.stock_id = gtk.STOCK_EDIT
        self.props.tooltip = _("Edit the focused cell")
        self.accelerator = "Return"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        row, col = page.view.get_focus()
        assert not None in (row, col)
        assert col != gaupol.gtk.COLUMN.NUMBER


class InsertSubtitlesAction(Action):

    """Insert subtitles."""

    def __init__(self):

        Action.__init__(self, "insert_subtitles")
        self.props.label = _("_Insert Subtitles\342\200\246")
        self.props.short_label = _("Insert")
        self.props.stock_id = gtk.STOCK_ADD
        self.props.tooltip = _("Insert subtitles")
        self.accelerator = "Insert"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        if page.project.subtitles:
            assert page.view.get_selected_rows()


class InvertSelectionAction(Action):

    """Invert the current selection."""

    def __init__(self):

        Action.__init__(self, "invert_selection")
        self.props.label = _("In_vert Selection")
        self.props.tooltip = _("Invert the current selection")
        self.accelerator = "<Control>I"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.project.subtitles


class MergeSubtitlesAction(Action):

    """Merge the selected subtitles."""

    def __init__(self):

        Action.__init__(self, "merge_subtitles")
        self.props.label = _("_Merge Subtitles")
        self.props.tooltip = _("Merge the selected subtitles")
        self.accelerator = "M"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        rows = page.view.get_selected_rows()
        assert len(rows) > 1
        assert rows == range(rows[0], rows[-1] + 1)


class PasteTextsAction(Action):

    """Paste texts from the clipboard."""

    def __init__(self):

        Action.__init__(self, "paste_texts")
        self.props.label = _("_Paste")
        self.props.stock_id = gtk.STOCK_PASTE
        self.props.tooltip = _("Paste texts from the clipboard")
        self.accelerator = "<Control>V"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert not application.clipboard.is_empty()
        assert page.view.get_selected_rows()
        assert page.view.get_focus()[1] in _TEXT_COLUMNS


class RedoActionAction(Action):

    """Redo the last undone action."""

    __gtype_name__ = "RedoActionAction"

    def __init__(self):

        Action.__init__(self, "redo_action")
        self.props.label = _("_Redo")
        self.props.stock_id = gtk.STOCK_REDO
        self.props.tooltip = _("Redo the last undone action")
        self.accelerator = "<Shift><Control>Z"
        self.set_tool_item_type(gtk.MenuToolButton)

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.project.can_redo()


class RemoveSubtitlesAction(Action):

    """Remove the selected subtitles."""

    def __init__(self):

        Action.__init__(self, "remove_subtitles")
        self.props.label = _("Rem_ove Subtitles")
        self.props.short_label = _("Remove")
        self.props.stock_id = gtk.STOCK_REMOVE
        self.props.tooltip = _("Remove the selected subtitles")
        self.accelerator = "Delete"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.view.get_selected_rows()


class SelectAllAction(Action):

    """Select all subtitles."""

    def __init__(self):

        Action.__init__(self, "select_all")
        self.props.label = _("Select _All")
        self.props.stock_id = gtk.STOCK_SELECT_ALL
        self.props.tooltip = _("Select all subtitles")
        self.accelerator = "<Control>A"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.project.subtitles


class SplitSubtitleAction(Action):

    """Split the selected subtitle."""

    def __init__(self):

        Action.__init__(self, "split_subtitle")
        self.props.label = _("_Split Subtitle")
        self.props.tooltip = _("Split the selected subtitle")
        self.accelerator = "S"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert len(page.view.get_selected_rows()) == 1


class UndoActionAction(Action):

    """Undo the last action."""

    __gtype_name__ = "UndoActionAction"

    def __init__(self):

        Action.__init__(self, "undo_action")
        self.props.is_important = True
        self.props.label = _("_Undo")
        self.props.stock_id = gtk.STOCK_UNDO
        self.props.tooltip = _("Undo the last action")
        self.accelerator = "<Control>Z"
        self.set_tool_item_type(gtk.MenuToolButton)

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.project.can_undo()
