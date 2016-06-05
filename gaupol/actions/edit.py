# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Simple subtitle data editing actions for :class:`gaupol.Application`."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import Gtk


class EditPreferencesAction(gaupol.Action):

    """Configure Gaupol."""

    def __init__(self):
        """Initialize an :class:`EditPreferencesAction` instance."""
        gaupol.Action.__init__(self, "edit_preferences")
        self.set_icon_name("preferences-desktop")
        self.set_label(_("_Preferences"))
        self.set_tooltip(_("Configure Gaupol"))
        self.action_group = "main-safe"


class EditNextValueAction(gaupol.Action):

    """Edit the focused column of the next subtitle."""

    def __init__(self):
        """Initialize an :class:`EditNextValueAction` instance."""
        gaupol.Action.__init__(self, "edit_next_value")
        self.set_label(_("Edit _Next Cell"))
        self.set_tooltip(_("Edit the focused column of the next subtitle"))
        self.accelerator = "space"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        row, col = page.view.get_focus()
        aeidon.util.affirm(not None in (row, col))
        aeidon.util.affirm(row < len(page.project.subtitles) - 1)
        column = page.view.get_column(col)
        renderer = column.get_cells()[0]
        aeidon.util.affirm(renderer.props.mode ==
                           Gtk.CellRendererMode.EDITABLE)


class EditValueAction(gaupol.Action):

    """Edit the focused cell."""

    def __init__(self):
        """Initialize an :class:`EditValueAction` instance."""
        gaupol.Action.__init__(self, "edit_value")
        self.set_icon_name("insert-text")
        self.set_is_important(True)
        self.set_label(_("_Edit Cell"))
        self.set_tooltip(_("Edit the focused cell"))
        self.accelerator = "Return"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        row, col = page.view.get_focus()
        aeidon.util.affirm(not None in (row, col))
        column = page.view.get_column(col)
        renderer = column.get_cells()[0]
        aeidon.util.affirm(renderer.props.mode ==
                           Gtk.CellRendererMode.EDITABLE)


class EndEarlierAction(gaupol.Action):

    """End the selected subtitle earlier."""

    def __init__(self):
        """Initialize a :class:`EndEarlierAction` instance."""
        gaupol.Action.__init__(self, "end_earlier")
        self.set_label(_("E_nd Earlier"))
        self.set_tooltip(_("End the selected subtitle earlier"))
        self.accelerator = "E"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(len(selected_rows) == 1)


class EndLaterAction(gaupol.Action):

    """End the selected subtitle later."""

    def __init__(self):
        """Initialize a :class:`EndLaterAction` instance."""
        gaupol.Action.__init__(self, "end_later")
        self.set_label(_("En_d Later"))
        self.set_tooltip(_("End the selected subtitle later"))
        self.accelerator = "R"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(len(selected_rows) == 1)


class ExtendSelectionToBeginningAction(gaupol.Action):

    """Extend the selection up to the first subtitle."""

    def __init__(self):
        """Initialize an :class:`ExtendSelectionToBeginningAction` instance."""
        gaupol.Action.__init__(self, "extend_selection_to_beginning")
        self.set_label(_("Extend To _Beginning"))
        self.set_tooltip(_("Extend the current selection up to the first subtitle"))
        self.accelerator = "<Shift><Control>Home"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(selected_rows)


class ExtendSelectionToEndAction(gaupol.Action):

    """Extend the selection up to the last subtitle."""

    def __init__(self):
        """Initialize an :class:`ExtendSelectionToEndAction` instance."""
        gaupol.Action.__init__(self, "extend_selection_to_end")
        self.set_label(_("Extend To _End"))
        self.set_tooltip(_("Extend the current selection up to the last subtitle"))
        self.accelerator = "<Shift><Control>End"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(selected_rows)


class InsertSubtitleAtVideoPositionAction(gaupol.Action):

    """Insert a new subtitle at video position."""

    def __init__(self):
        """Initialize an :class:`InsertSubtitleAtVideoPositionAction` instance."""
        gaupol.Action.__init__(self, "insert_subtitle_at_video_position")
        self.set_icon_name("list-add")
        self.set_label(_("Inser_t Subtitle At Video Position"))
        self.set_tooltip(_("Insert a new subtitle at video position"))
        self.accelerator = "J"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.player is not None)


class InsertSubtitlesAction(gaupol.Action):

    """Insert subtitles."""

    def __init__(self):
        """Initialize an :class:`InsertSubtitlesAction` instance."""
        gaupol.Action.__init__(self, "insert_subtitles")
        self.set_icon_name("list-add")
        self.set_label(_("_Insert Subtitles…"))
        self.set_short_label(_("Insert"))
        self.set_tooltip(_("Insert new subtitles"))
        self.accelerator = "I"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        if page.project.subtitles:
            aeidon.util.affirm(selected_rows)


class InvertSelectionAction(gaupol.Action):

    """Invert the current selection."""

    def __init__(self):
        """Initialize an :class:`InvertSelectionAction` instance."""
        gaupol.Action.__init__(self, "invert_selection")
        self.set_label(_("_Invert Selection"))
        self.set_tooltip(_("Invert the current selection"))
        self.accelerator = "<Control>I"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)


class MergeSubtitlesAction(gaupol.Action):

    """Merge the selected subtitles."""

    def __init__(self):
        """Initialize a :class:`MergeSubtitlesAction` instance."""
        gaupol.Action.__init__(self, "merge_subtitles")
        self.set_label(_("_Merge Subtitles"))
        self.set_tooltip(_("Merge the selected subtitles"))
        self.accelerator = "M"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(len(selected_rows) > 1)
        block = list(range(selected_rows[0], selected_rows[-1]+1))
        aeidon.util.affirm(list(selected_rows) == block)


class RedoActionAction(gaupol.Action):

    """Redo the last undone action."""

    __gtype_name__ = "RedoActionAction"

    def __init__(self):
        """Initialize a :class:`RedoActionAction` instance."""
        gaupol.Action.__init__(self, "redo_action")
        self.set_icon_name("edit-redo")
        self.set_label(_("_Redo"))
        self.set_tooltip(_("Redo the last undone action"))
        self.accelerator = "<Shift><Control>Z"
        self.action_group = "main-unsafe"
        self.tool_item_type = Gtk.MenuToolButton

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.can_redo())


class RemoveSubtitlesAction(gaupol.Action):

    """Remove the selected subtitles."""

    def __init__(self):
        """Initialize a :class:`RemoveSubtitlesAction` instance."""
        gaupol.Action.__init__(self, "remove_subtitles")
        self.set_icon_name("list-remove")
        self.set_label(_("Rem_ove Subtitles"))
        self.set_short_label(_("Remove"))
        self.set_tooltip(_("Remove the selected subtitles"))
        self.accelerator = "Delete"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(selected_rows)


class SelectAllAction(gaupol.Action):

    """Select all subtitles."""

    def __init__(self):
        """Initialize a :class:`SelectAllAction` instance."""
        gaupol.Action.__init__(self, "select_all")
        self.set_icon_name("edit-select-all")
        self.set_label(_("Select _All"))
        self.set_tooltip(_("Select all subtitles"))
        self.accelerator = "<Control>A"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)


class SetEndFromVideoPositionAction(gaupol.Action):

    """Set subtitle end from video position."""

    def __init__(self):
        """Initialize an :class:`SetEndFromVideoPositionAction` instance."""
        gaupol.Action.__init__(self, "set_end_from_video_position")
        self.set_label(_("Set En_d From Video Position"))
        self.set_tooltip(_("Set subtitle end from video position"))
        self.accelerator = "K"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.player is not None)
        aeidon.util.affirm(len(selected_rows) == 1)


class ShowSelectionMenuAction(gaupol.MenuAction):

    """Show the selection menu."""

    def __init__(self):
        """Initialize a :class:`ShowSelectionMenuAction` instance."""
        gaupol.MenuAction.__init__(self, "show_selection_menu")
        self.set_label(_("Sele_ction"))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)


class ShowStretchMenuAction(gaupol.MenuAction):

    """Show the stretch menu."""

    def __init__(self):
        """Initialize a :class:`ShowStretchMenuAction` instance."""
        gaupol.MenuAction.__init__(self, "show_stretch_menu")
        self.set_label(_("Stretc_h Subtitle"))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(len(selected_rows) == 1)


class SplitSubtitleAction(gaupol.Action):

    """Split the selected subtitle."""

    def __init__(self):
        """Initialize a :class:`SplitSubtitleAction` instance."""
        gaupol.Action.__init__(self, "split_subtitle")
        self.set_label(_("_Split Subtitle"))
        self.set_tooltip(_("Split the selected subtitle"))
        self.accelerator = "S"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(len(selected_rows) == 1)


class StartEarlierAction(gaupol.Action):

    """Start the selected subtitle earlier."""

    def __init__(self):
        """Initialize a :class:`StartEarlierAction` instance."""
        gaupol.Action.__init__(self, "start_earlier")
        self.set_label(_("_Start Earlier"))
        self.set_tooltip(_("Start the selected subtitle earlier"))
        self.accelerator = "Q"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(len(selected_rows) == 1)


class StartLaterAction(gaupol.Action):

    """Start the selected subtitle later."""

    def __init__(self):
        """Initialize a :class:`StartLaterAction` instance."""
        gaupol.Action.__init__(self, "start_later")
        self.set_label(_("S_tart Later"))
        self.set_tooltip(_("Start the selected subtitle later"))
        self.accelerator = "W"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(len(selected_rows) == 1)


class UndoActionAction(gaupol.Action):

    """Undo the last action."""

    __gtype_name__ = "UndoActionAction"

    def __init__(self):
        """Initialize an :class:`UndoActionAction` instance."""
        gaupol.Action.__init__(self, "undo_action")
        self.set_icon_name("edit-undo")
        self.set_is_important(True)
        self.set_label(_("_Undo"))
        self.set_tooltip(_("Undo the last action"))
        self.accelerator = "<Control>Z"
        self.action_group = "main-unsafe"
        self.tool_item_type = Gtk.MenuToolButton

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.can_undo())


__all__ = tuple(x for x in dir() if x.endswith("Action"))
