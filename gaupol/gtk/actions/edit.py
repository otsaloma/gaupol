# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Simple subtitle data editing actions."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._


class ClearTextsAction(gaupol.gtk.Action):

    """Clear the selected texts."""

    def __init__(self):
        """Initialize a ClearTextsAction object."""

        gaupol.gtk.Action.__init__(self, "clear_texts")
        self.props.label = _("Cl_ear")
        self.props.stock_id = gtk.STOCK_CLEAR
        self.props.tooltip = _("Clear the selected texts")
        self.accelerator = "C"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        gaupol.util.affirm(page.view.is_text_column(col))


class CopyTextsAction(gaupol.gtk.Action):

    """Copy the selected texts to the clipboard."""

    def __init__(self):
        """Initialize a CopyTextsAction object."""

        gaupol.gtk.Action.__init__(self, "copy_texts")
        self.props.label = _("_Copy")
        self.props.stock_id = gtk.STOCK_COPY
        self.props.tooltip = _("Copy the selected texts to the clipboard")
        self.accelerator = "<Control>C"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        gaupol.util.affirm(page.view.is_text_column(col))


class CutTextsAction(gaupol.gtk.Action):

    """Cut the selected texts to the clipboard."""

    def __init__(self):
        """Initialize a CutTextsAction object."""

        gaupol.gtk.Action.__init__(self, "cut_texts")
        self.props.label = _("Cu_t")
        self.props.stock_id = gtk.STOCK_CUT
        self.props.tooltip = _("Cut the selected texts to the clipboard")
        self.accelerator = "<Control>X"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        gaupol.util.affirm(page.view.is_text_column(col))


class EditPreferencesAction(gaupol.gtk.Action):

    """Configure Gaupol."""

    def __init__(self):
        """Initialize an EditPreferencesAction object."""

        gaupol.gtk.Action.__init__(self, "edit_preferences")
        self.props.label = _("_Preferences")
        self.props.stock_id = gtk.STOCK_PREFERENCES
        self.props.tooltip = _("Configure Gaupol")
        self.action_group = "main-safe"


class EditNextValueAction(gaupol.gtk.Action):

    """Edit the focused column of the next subtitle."""

    def __init__(self):
        """Initialize an EditNextValueAction object."""

        gaupol.gtk.Action.__init__(self, "edit_next_value")
        self.props.label = _("Edit _Next Cell")
        self.props.short_label = _("Next")
        self.props.stock_id = gtk.STOCK_EDIT
        self.props.tooltip = _("Edit the focused column of the next subtitle")
        self.accelerator = "space"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        row, col = page.view.get_focus()
        gaupol.util.affirm(not None in (row, col))
        gaupol.util.affirm(row < len(page.project.subtitles) - 1)
        column = page.view.get_column(col)
        renderer = column.get_cell_renderers()[0]
        mode = renderer.props.mode
        gaupol.util.affirm(mode == gtk.CELL_RENDERER_MODE_EDITABLE)


class EditValueAction(gaupol.gtk.Action):

    """Edit the focused cell."""

    def __init__(self):
        """Initialize an EditValueAction object."""

        gaupol.gtk.Action.__init__(self, "edit_value")
        self.props.is_important = True
        self.props.label = _("_Edit Cell")
        self.props.short_label = _("Edit")
        self.props.stock_id = gtk.STOCK_EDIT
        self.props.tooltip = _("Edit the focused cell")
        self.accelerator = "Return"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        row, col = page.view.get_focus()
        gaupol.util.affirm(not None in (row, col))
        column = page.view.get_column(col)
        renderer = column.get_cell_renderers()[0]
        mode = renderer.props.mode
        gaupol.util.affirm(mode == gtk.CELL_RENDERER_MODE_EDITABLE)


class ExtendSelectionToBeginningAction(gaupol.gtk.Action):

    """Extend the selection up to the first subtitle."""

    def __init__(self):
        """Initialize an ExtendSelectionToBeginningAction object."""

        gaupol.gtk.Action.__init__(self, "extend_selection_to_beginning")
        self.props.label = _("Extend To _Beginning")
        tip = _("Extend the current selection up to the first subtitle")
        self.props.tooltip = tip
        self.accelerator = "<Shift><Control>Home"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.subtitles)
        gaupol.util.affirm(page.view.get_selected_rows())


class ExtendSelectionToEndAction(gaupol.gtk.Action):

    """Extend the selection up to the last subtitle."""

    def __init__(self):
        """Initialize an ExtendSelectionToEndAction object."""

        gaupol.gtk.Action.__init__(self, "extend_selection_to_end")
        self.props.label = _("Extend To _End")
        tip = _("Extend the current selection up to the last subtitle")
        self.props.tooltip = tip
        self.accelerator = "<Shift><Control>End"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.subtitles)
        gaupol.util.affirm(page.view.get_selected_rows())


class InsertSubtitlesAction(gaupol.gtk.Action):

    """Insert subtitles."""

    def __init__(self):
        """Initialize an InsertSubtitlesAction object."""

        gaupol.gtk.Action.__init__(self, "insert_subtitles")
        self.props.label = _("_Insert Subtitles\342\200\246")
        self.props.short_label = _("Insert")
        self.props.stock_id = gtk.STOCK_ADD
        self.props.tooltip = _("Insert subtitles")
        self.accelerator = "Insert"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        if page.project.subtitles:
            gaupol.util.affirm(page.view.get_selected_rows())


class InvertSelectionAction(gaupol.gtk.Action):

    """Invert the current selection."""

    def __init__(self):
        """Initialize an InvertSelectionAction object."""

        gaupol.gtk.Action.__init__(self, "invert_selection")
        self.props.label = _("_Invert Selection")
        self.props.tooltip = _("Invert the current selection")
        self.accelerator = "<Control>I"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.subtitles)


class MergeSubtitlesAction(gaupol.gtk.Action):

    """Merge the selected subtitles."""

    def __init__(self):
        """Initialize a MergeSubtitlesAction object."""

        gaupol.gtk.Action.__init__(self, "merge_subtitles")
        self.props.label = _("_Merge Subtitles")
        self.props.tooltip = _("Merge the selected subtitles")
        self.accelerator = "M"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        rows = page.view.get_selected_rows()
        gaupol.util.affirm(len(rows) > 1)
        gaupol.util.affirm(list(rows) == range(rows[0], rows[-1] + 1))


class PasteTextsAction(gaupol.gtk.Action):

    """Paste texts from the clipboard."""

    def __init__(self):
        """Initialize a PasteTextsAction object."""

        gaupol.gtk.Action.__init__(self, "paste_texts")
        self.props.label = _("_Paste")
        self.props.stock_id = gtk.STOCK_PASTE
        self.props.tooltip = _("Paste texts from the clipboard")
        self.accelerator = "<Control>V"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(not application.clipboard.is_empty())
        gaupol.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        gaupol.util.affirm(page.view.is_text_column(col))


class RedoActionAction(gaupol.gtk.Action):

    """Redo the last undone action."""

    __gtype_name__ = "RedoActionAction"

    def __init__(self):
        """Initialize a RedoActionAction object."""

        gaupol.gtk.Action.__init__(self, "redo_action")
        self.props.label = _("_Redo")
        self.props.stock_id = gtk.STOCK_REDO
        self.props.tooltip = _("Redo the last undone action")
        self.accelerator = "<Shift><Control>Z"
        self.action_group = "main-unsafe"
        self.set_tool_item_type(gtk.MenuToolButton)

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.can_redo())


class RemoveSubtitlesAction(gaupol.gtk.Action):

    """Remove the selected subtitles."""

    def __init__(self):
        """Initialize a RemoveSubtitlesAction object."""

        gaupol.gtk.Action.__init__(self, "remove_subtitles")
        self.props.label = _("Rem_ove Subtitles")
        self.props.short_label = _("Remove")
        self.props.stock_id = gtk.STOCK_REMOVE
        self.props.tooltip = _("Remove the selected subtitles")
        self.accelerator = "Delete"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.view.get_selected_rows())


class SelectAllAction(gaupol.gtk.Action):

    """Select all subtitles."""

    def __init__(self):
        """Initialize a SelectAllAction object."""

        gaupol.gtk.Action.__init__(self, "select_all")
        self.props.label = _("Select _All")
        self.props.stock_id = gtk.STOCK_SELECT_ALL
        self.props.tooltip = _("Select all subtitles")
        self.accelerator = "<Control>A"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.subtitles)


class ShowSelectionMenuAction(gaupol.gtk.MenuAction):

    """Show the selection menu."""

    def __init__(self):
        """Initialize a ShowSelectionMenuAction object."""

        gaupol.gtk.MenuAction.__init__(self, "show_selection_menu")
        self.props.label = _("Sele_ction")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.subtitles)


class SplitSubtitleAction(gaupol.gtk.Action):

    """Split the selected subtitle."""

    def __init__(self):
        """Initialize a SplitSubtitleAction object."""

        gaupol.gtk.Action.__init__(self, "split_subtitle")
        self.props.label = _("_Split Subtitle")
        self.props.tooltip = _("Split the selected subtitle")
        self.accelerator = "S"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(len(page.view.get_selected_rows()) == 1)


class UndoActionAction(gaupol.gtk.Action):

    """Undo the last action."""

    __gtype_name__ = "UndoActionAction"

    def __init__(self):
        """Initialize an UndoActionAction object."""

        gaupol.gtk.Action.__init__(self, "undo_action")
        self.props.is_important = True
        self.props.label = _("_Undo")
        self.props.stock_id = gtk.STOCK_UNDO
        self.props.tooltip = _("Undo the last action")
        self.accelerator = "<Control>Z"
        self.action_group = "main-unsafe"
        self.set_tool_item_type(gtk.MenuToolButton)

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.can_undo())


__all__ = gaupol.util.get_all(dir(), r"Action$")
