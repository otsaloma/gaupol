# -*- coding: utf-8-unix -*-

# Copyright (C) 2005-2008,2010 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Simple subtitle data editing actions for :class:`gaupol.Application`."""

import aeidon
import gaupol
_ = aeidon.i18n._

from gi.repository import Gtk


class ClearTextsAction(gaupol.Action):

    """Clear the selected texts."""

    def __init__(self):
        """Initialize a :class:`ClearTextsAction` object."""
        gaupol.Action.__init__(self, "clear_texts")
        self.props.label = _("Cl_ear")
        self.props.stock_id = Gtk.STOCK_CLEAR
        self.props.tooltip = _("Clear the selected texts")
        self.accelerator = "C"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        aeidon.util.affirm(col is not None)
        aeidon.util.affirm(page.view.is_text_column(col))


class CopyTextsAction(gaupol.Action):

    """Copy the selected texts to the clipboard."""

    def __init__(self):
        """Initialize a :class:`CopyTextsAction` object."""
        gaupol.Action.__init__(self, "copy_texts")
        self.props.label = _("_Copy")
        self.props.stock_id = Gtk.STOCK_COPY
        self.props.tooltip = _("Copy the selected texts to the clipboard")
        self.accelerator = "<Control>C"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        aeidon.util.affirm(col is not None)
        aeidon.util.affirm(page.view.is_text_column(col))


class CutTextsAction(gaupol.Action):

    """Cut the selected texts to the clipboard."""

    def __init__(self):
        """Initialize a :class:`CutTextsAction` object."""
        gaupol.Action.__init__(self, "cut_texts")
        self.props.label = _("Cu_t")
        self.props.stock_id = Gtk.STOCK_CUT
        self.props.tooltip = _("Cut the selected texts to the clipboard")
        self.accelerator = "<Control>X"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        aeidon.util.affirm(col is not None)
        aeidon.util.affirm(page.view.is_text_column(col))


class EditPreferencesAction(gaupol.Action):

    """Configure Gaupol."""

    def __init__(self):
        """Initialize an :class:`EditPreferencesAction` object."""
        gaupol.Action.__init__(self, "edit_preferences")
        self.props.label = _("_Preferences")
        self.props.stock_id = Gtk.STOCK_PREFERENCES
        self.props.tooltip = _("Configure Gaupol")
        self.action_group = "main-safe"


class EditNextValueAction(gaupol.Action):

    """Edit the focused column of the next subtitle."""

    def __init__(self):
        """Initialize an :class:`EditNextValueAction` object."""
        gaupol.Action.__init__(self, "edit_next_value")
        self.props.label = _("Edit _Next Cell")
        self.props.short_label = _("Next")
        self.props.stock_id = Gtk.STOCK_EDIT
        self.props.tooltip = _("Edit the focused column of the next subtitle")
        self.accelerator = "space"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        row, col = page.view.get_focus()
        aeidon.util.affirm(not None in (row, col))
        aeidon.util.affirm(row < len(page.project.subtitles) - 1)
        column = page.view.get_column(col)
        renderer = column.get_cells()[0]
        mode = renderer.props.mode
        aeidon.util.affirm(mode == Gtk.CellRendererMode.EDITABLE)


class EditValueAction(gaupol.Action):

    """Edit the focused cell."""

    def __init__(self):
        """Initialize an :class:`EditValueAction` object."""
        gaupol.Action.__init__(self, "edit_value")
        self.props.is_important = True
        self.props.label = _("_Edit Cell")
        self.props.short_label = _("Edit")
        self.props.stock_id = Gtk.STOCK_EDIT
        self.props.tooltip = _("Edit the focused cell")
        self.accelerator = "Return"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        row, col = page.view.get_focus()
        aeidon.util.affirm(not None in (row, col))
        column = page.view.get_column(col)
        renderer = column.get_cells()[0]
        mode = renderer.props.mode
        aeidon.util.affirm(mode == Gtk.CellRendererMode.EDITABLE)


class ExtendSelectionToBeginningAction(gaupol.Action):

    """Extend the selection up to the first subtitle."""

    def __init__(self):
        """Initialize an :class:`ExtendSelectionToBeginningAction` object."""
        gaupol.Action.__init__(self, "extend_selection_to_beginning")
        self.props.label = _("Extend To _Beginning")
        self.props.tooltip = _("Extend the current selection "
                               "up to the first subtitle")

        self.accelerator = "<Shift><Control>Home"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(page.view.get_selected_rows())


class ExtendSelectionToEndAction(gaupol.Action):

    """Extend the selection up to the last subtitle."""

    def __init__(self):
        """Initialize an :class:`ExtendSelectionToEndAction` object."""
        gaupol.Action.__init__(self, "extend_selection_to_end")
        self.props.label = _("Extend To _End")
        self.props.tooltip = _("Extend the current selection "
                               "up to the last subtitle")

        self.accelerator = "<Shift><Control>End"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(page.view.get_selected_rows())


class InsertSubtitlesAction(gaupol.Action):

    """Insert subtitles."""

    def __init__(self):
        """Initialize an :class:`InsertSubtitlesAction` object."""
        gaupol.Action.__init__(self, "insert_subtitles")
        self.props.label = _("_Insert Subtitles…")
        self.props.short_label = _("Insert")
        self.props.stock_id = Gtk.STOCK_ADD
        self.props.tooltip = _("Insert new subtitles")
        self.accelerator = "Insert"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        if page.project.subtitles:
            aeidon.util.affirm(page.view.get_selected_rows())


class InvertSelectionAction(gaupol.Action):

    """Invert the current selection."""

    def __init__(self):
        """Initialize an :class:`InvertSelectionAction` object."""
        gaupol.Action.__init__(self, "invert_selection")
        self.props.label = _("_Invert Selection")
        self.props.tooltip = _("Invert the current selection")
        self.accelerator = "<Control>I"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)


class MergeSubtitlesAction(gaupol.Action):

    """Merge the selected subtitles."""

    def __init__(self):
        """Initialize a :class:`MergeSubtitlesAction` object."""
        gaupol.Action.__init__(self, "merge_subtitles")
        self.props.label = _("_Merge Subtitles")
        self.props.tooltip = _("Merge the selected subtitles")
        self.accelerator = "M"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        rows = page.view.get_selected_rows()
        aeidon.util.affirm(len(rows) > 1)
        aeidon.util.affirm(list(rows) == list(range(rows[0], rows[-1] + 1)))


class PasteTextsAction(gaupol.Action):

    """Paste texts from the clipboard."""

    def __init__(self):
        """Initialize a :class:`PasteTextsAction` object."""
        gaupol.Action.__init__(self, "paste_texts")
        self.props.label = _("_Paste")
        self.props.stock_id = Gtk.STOCK_PASTE
        self.props.tooltip = _("Paste texts from the clipboard")
        self.accelerator = "<Control>V"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(not application.clipboard.is_empty())
        aeidon.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        aeidon.util.affirm(col is not None)
        aeidon.util.affirm(page.view.is_text_column(col))


class RedoActionAction(gaupol.Action):

    """Redo the last undone action."""

    __gtype_name__ = "RedoActionAction"

    def __init__(self):
        """Initialize a :class:`RedoActionAction` object."""
        gaupol.Action.__init__(self, "redo_action")
        self.props.label = _("_Redo")
        self.props.stock_id = Gtk.STOCK_REDO
        self.props.tooltip = _("Redo the last undone action")
        self.accelerator = "<Shift><Control>Z"
        self.action_group = "main-unsafe"
        # XXX:
        # self.set_tool_item_type(Gtk.MenuToolButton)

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.can_redo())


class RemoveSubtitlesAction(gaupol.Action):

    """Remove the selected subtitles."""

    def __init__(self):
        """Initialize a :class:`RemoveSubtitlesAction` object."""
        gaupol.Action.__init__(self, "remove_subtitles")
        self.props.label = _("Rem_ove Subtitles")
        self.props.short_label = _("Remove")
        self.props.stock_id = Gtk.STOCK_REMOVE
        self.props.tooltip = _("Remove the selected subtitles")
        self.accelerator = "Delete"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.view.get_selected_rows())


class SelectAllAction(gaupol.Action):

    """Select all subtitles."""

    def __init__(self):
        """Initialize a :class:`SelectAllAction` object."""
        gaupol.Action.__init__(self, "select_all")
        self.props.label = _("Select _All")
        self.props.stock_id = Gtk.STOCK_SELECT_ALL
        self.props.tooltip = _("Select all subtitles")
        self.accelerator = "<Control>A"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)


class ShowSelectionMenuAction(gaupol.MenuAction):

    """Show the selection menu."""

    def __init__(self):
        """Initialize a :class:`ShowSelectionMenuAction` object."""
        gaupol.MenuAction.__init__(self, "show_selection_menu")
        self.props.label = _("Sele_ction")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)


class SplitSubtitleAction(gaupol.Action):

    """Split the selected subtitle."""

    def __init__(self):
        """Initialize a :class:`SplitSubtitleAction` object."""
        gaupol.Action.__init__(self, "split_subtitle")
        self.props.label = _("_Split Subtitle")
        self.props.tooltip = _("Split the selected subtitle")
        self.accelerator = "S"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(len(page.view.get_selected_rows()) == 1)


class UndoActionAction(gaupol.Action):

    """Undo the last action."""

    __gtype_name__ = "UndoActionAction"

    def __init__(self):
        """Initialize an :class:`UndoActionAction` object."""
        gaupol.Action.__init__(self, "undo_action")
        self.props.is_important = True
        self.props.label = _("_Undo")
        self.props.stock_id = Gtk.STOCK_UNDO
        self.props.tooltip = _("Undo the last action")
        self.accelerator = "<Control>Z"
        self.action_group = "main-unsafe"
        # XXX:
        # self.set_tool_item_type(Gtk.MenuToolButton)

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.can_undo())


__all__ = tuple([x for x in dir() if x.endswith("Action")])
