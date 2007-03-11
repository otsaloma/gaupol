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


import gtk
from gettext import gettext as _

from gaupol.gtk.index import *
from ._action import UIMAction


class ClearTextsAction(UIMAction):

    """Clear the selected texts."""

    action_item = (
        "clear_texts",
        gtk.STOCK_CLEAR,
        _("C_lear"),
        "C",
        _("Clear the selected texts"),)

    paths = ["/ui/menubar/text/clear"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            selection = bool(page.view.get_selected_rows())
            focus = page.view.get_focus()[1] in (MTXT, TTXT)
            return bool(selection and focus)
        return False


class CopyTextsAction(UIMAction):

    """Copy the selected texts to the clipboard."""

    action_item = (
        "copy_texts",
        gtk.STOCK_COPY,
        _("_Copy"),
        "<control>C",
        _("Copy the selected texts to the clipboard"),)

    paths = ["/ui/menubar/text/copy"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            selection = bool(page.view.get_selected_rows())
            focus = page.view.get_focus()[1] in (MTXT, TTXT)
            return bool(selection and focus)
        return False


class CutTextsAction(UIMAction):

    """Cut the selected texts to the clipboard."""

    action_item = (
        "cut_texts",
        gtk.STOCK_CUT,
        _("Cu_t"),
        "<control>X",
        _("Cut the selected texts to the clipboard"),)

    paths = ["/ui/menubar/text/cut"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            selection = bool(page.view.get_selected_rows())
            focus = page.view.get_focus()[1] in (MTXT, TTXT)
            return bool(selection and focus)
        return False


class EditPreferencesAction(UIMAction):

    """Configure Gaupol."""

    action_item = (
        "edit_preferences",
        gtk.STOCK_PREFERENCES,
        _("Pre_ferences"),
        None,
        _("Configure Gaupol"),)

    paths = ["/ui/menubar/edit/preferences"]


class EditNextValueAction(UIMAction):

    """Edit the focused column of the next subtitle."""

    action_item = (
        "edit_next_value",
        None,
        _("Edit _Next Cell"),
        "space",
        _("Edit the focused column of the next subtitle"),)

    paths = ["/ui/menubar/edit/edit_next"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            row, col = page.view.get_focus()
            if None in (row, col):
                return False
            if row == len(page.project.times) - 1:
                return False
            return (col != NO)
        return False


class EditValueAction(UIMAction):

    """Edit the focused cell."""

    action_item = (
        "edit_value",
        gtk.STOCK_EDIT,
        _("_Edit Cell"),
        "Return",
        _("Edit the focused cell"),)

    paths = ["/ui/menubar/edit/edit", "/ui/view_popup/edit"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            row, col = page.view.get_focus()
            if None in (row, col):
                return False
            return (col != NO)
        return False


class InsertSubtitlesAction(UIMAction):

    """Insert blank subtitles."""

    action_item = (
        "insert_subtitles",
        gtk.STOCK_ADD,
        _("_Insert Subtitles..."),
        "Insert",
        _("Insert blank subtitles"),)

    paths = [
        "/ui/menubar/edit/insert",
        "/ui/main_toolbar/insert",
        "/ui/view_popup/insert"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            if page.view.get_selected_rows():
                return True
            if not page.project.times:
                return True
        return False


class InvertSelectionAction(UIMAction):

    """Invert the current selection."""

    action_item = (
        "invert_selection",
        None,
        _("In_vert Selection"),
        "<shift><control>A",
        _("Invert the current selection"),)

    paths = ["/ui/menubar/edit/invert_selection"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            return bool(page.project.times)
        return False


class MergeSubtitlesAction(UIMAction):

    """Merge the selected subtitles."""

    action_item = (
        "merge_subtitles",
        None,
        _("_Merge Subtitles"),
        "M",
        _("Merge the selected subtitles"),)

    paths = ["/ui/menubar/edit/merge", "/ui/view_popup/merge"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            rows = page.view.get_selected_rows()
            if (len(rows) > 1) and (rows[-1] == rows[0] + len(rows) - 1):
                return True
        return False


class PasteTextsAction(UIMAction):

    """Paste texts from the clipboard."""

    action_item = (
        "paste_texts",
        gtk.STOCK_PASTE,
        _("_Paste"),
        "<control>V",
        _("Paste texts from the clipboard"),)

    paths = ["/ui/menubar/text/paste"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if (page is not None) and application.clipboard.data:
            selection = bool(page.view.get_selected_rows())
            focus = (page.view.get_focus()[1] in (MTXT, TTXT))
            return bool(selection and focus)
        return False


class RedoActionAction(UIMAction):

    """Redo the last undone action."""

    action_item = (
        "redo_action",
        gtk.STOCK_REDO,
        _("_Redo"),
        "<shift><control>Z",
        _("Redo the last undone action"),)

    paths = ["/ui/menubar/edit/redo"]
    widgets = ["redo_button"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            return page.project.can_redo()
        return False


class RemoveSubtitlesAction(UIMAction):

    """Remove the selected subtitles."""

    action_item = (
        "remove_subtitles",
        gtk.STOCK_REMOVE,
        _("Rem_ove Subtitles"),
        "Delete",
        _("Remove the selected subtitles"),)

    paths = [
        "/ui/menubar/edit/remove",
        "/ui/main_toolbar/remove",
        "/ui/view_popup/remove"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            return bool(page.view.get_selected_rows())
        return False


class SelectAllAction(UIMAction):

    """Select all subtitles."""

    action_item = (
        "select_all",
        None,
        _("Select _All"),
        "<control>A",
        _("Select all subtitles"),)

    paths = ["/ui/menubar/edit/select_all"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            return bool(page.project.times)
        return False


class SplitSubtitlesAction(UIMAction):

    """Split the selected subtitle."""

    action_item = (
        "split_subtitle",
        None,
        _("_Split Subtitle"),
        "S",
        _("Split the selected subtitle"),)

    paths = ["/ui/menubar/edit/split", "/ui/view_popup/split"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            return (len(page.view.get_selected_rows()) == 1)
        return False


class UndoActionAction(UIMAction):

    """Undo the last action."""

    action_item = (
        "undo_action",
        gtk.STOCK_UNDO,
        _("_Undo"),
        "<control>Z",
        _("Undo the last action"),)

    paths = ["/ui/menubar/edit/undo"]
    widgets = ["undo_button"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            return page.project.can_undo()
        return False
