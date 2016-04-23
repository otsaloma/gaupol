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

"""View menu UI manager actions for :class:`gaupol.Application`."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import Gtk


class ActivateNextProjectAction(gaupol.Action):

    """Activate the project in the next tab."""

    def __init__(self):
        """Initialize an :class:`ActivateNextProjectAction` instance."""
        gaupol.Action.__init__(self, "activate_next_project")
        self.set_label(_("_Next"))
        self.set_tooltip(_("Activate the project in the next tab"))
        self.accelerator = "<Control>Page_Down"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        index = application.pages.index(page) + 1
        aeidon.util.affirm(index in range(len(application.pages)))


class ActivatePreviousProjectAction(gaupol.Action):

    """Activate the project in the previous tab."""

    def __init__(self):
        """Initialize an :class:`ActivatePreviousProjectAction` instance."""
        gaupol.Action.__init__(self, "activate_previous_project")
        self.set_label(_("_Previous"))
        self.set_tooltip(_("Activate the project in the previous tab"))
        self.accelerator = "<Control>Page_Up"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.pages.index(page) > 0)


class MoveTabLeftAction(gaupol.Action):

    """Move the current tab to the left."""

    def __init__(self):
        """Initialize a :class:`MoveTabLeftAction` instance."""
        gaupol.Action.__init__(self, "move_tab_left")
        self.set_label(_("Move Tab _Left"))
        self.set_tooltip(_("Move the current tab to the left"))
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.pages.index(page) > 0)


class MoveTabRightAction(gaupol.Action):

    """Move the current tab to the right."""

    def __init__(self):
        """Initialize a :class:`MoveTabRightAction` instance."""
        gaupol.Action.__init__(self, "move_tab_right")
        self.set_label(_("Move Tab _Right"))
        self.set_tooltip(_("Move the current tab to the right"))
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        index = application.pages.index(page) + 1
        aeidon.util.affirm(index in range(len(application.pages)))


class ShowColumnsMenuAction(gaupol.MenuAction):

    """Show the "Columns" menu."""
    def __init__(self):
        """Initialize a :class:`ShowColumnsMenuAction` instance."""
        gaupol.MenuAction.__init__(self, "show_columns_menu")
        self.set_label(_("_Columns"))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ShowFramerate23976Action(gaupol.RadioAction):

    """Calculate nonnative units with a framerate of 23.976 fps."""

    def __init__(self):
        """Initialize a :class:`ShowFramerate23976Action` instance."""
        gaupol.RadioAction.__init__(self, "show_framerate_23_976")
        framerate = gaupol.conf.editor.framerate
        self.set_active(framerate == aeidon.framerates.FPS_23_976)
        self.set_label(_("2_3.976 fps"))
        self.set_tooltip(_("Calculate nonnative units with a framerate of 23.976 fps"))
        self.props.value = aeidon.framerates.FPS_23_976
        self.action_group = "main-unsafe"
        self.framerate = aeidon.framerates.FPS_23_976
        self.group = "ShowFramerate23976Action"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class ShowFramerate24000Action(gaupol.RadioAction):

    """Calculate nonnative units with a framerate of 24.000 fps."""

    def __init__(self):
        """Initialize a :class:`ShowFramerate24000Action` instance."""
        gaupol.RadioAction.__init__(self, "show_framerate_24_000")
        framerate = gaupol.conf.editor.framerate
        self.set_active(framerate == aeidon.framerates.FPS_24_000)
        self.set_label(_("2_4.000 fps"))
        self.set_tooltip(_("Calculate nonnative units with a framerate of 24.000 fps"))
        self.props.value = aeidon.framerates.FPS_24_000
        self.action_group = "main-unsafe"
        self.framerate = aeidon.framerates.FPS_24_000
        self.group = "ShowFramerate23976Action"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class ShowFramerate25000Action(gaupol.RadioAction):

    """Calculate nonnative units with a framerate of 25.000 fps."""

    def __init__(self):
        """Initialize a :class:`ShowFramerate25000Action` instance."""
        gaupol.RadioAction.__init__(self, "show_framerate_25_000")
        framerate = gaupol.conf.editor.framerate
        self.set_active(framerate == aeidon.framerates.FPS_25_000)
        self.set_label(_("2_5.000 fps"))
        self.set_tooltip(_("Calculate nonnative units with a framerate of 25.000 fps"))
        self.props.value = aeidon.framerates.FPS_25_000
        self.action_group = "main-unsafe"
        self.framerate = aeidon.framerates.FPS_25_000
        self.group = "ShowFramerate23976Action"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class ShowFramerate29970Action(gaupol.RadioAction):

    """Calculate nonnative units with a framerate of 29.970 fps."""

    def __init__(self):
        """Initialize a :class:`ShowFramerate30Action` instance."""
        gaupol.RadioAction.__init__(self, "show_framerate_29_970")
        framerate = gaupol.conf.editor.framerate
        self.set_active(framerate == aeidon.framerates.FPS_29_970)
        self.set_label(_("2_9.970 fps"))
        self.set_tooltip(_("Calculate nonnative units with a framerate of 29.970 fps"))
        self.props.value = aeidon.framerates.FPS_29_970
        self.action_group = "main-unsafe"
        self.framerate = aeidon.framerates.FPS_29_970
        self.group = "ShowFramerate23976Action"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class ShowFramerateMenuAction(gaupol.MenuAction):

    """Show the "Framerate" menu."""

    def __init__(self):
        """Initialize a :class:`ShowFramerateMenuAction` instance."""
        gaupol.MenuAction.__init__(self, "show_framerate_menu")
        self.set_label(_("F_ramerate"))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class ShowFramesAction(gaupol.RadioAction):

    """Show positions as frames."""

    def __init__(self):
        """Initialize a :class:`ShowFramesAction` instance."""
        gaupol.RadioAction.__init__(self, "show_frames")
        self.set_active(gaupol.conf.editor.mode == aeidon.modes.FRAME)
        self.set_label(_("_Frames"))
        self.set_tooltip(_("Show positions as frames"))
        self.props.value = aeidon.modes.FRAME
        self.accelerator = "<Shift>T"
        self.action_group = "main-unsafe"
        self.group = "ShowTimesAction"
        self.mode = aeidon.modes.FRAME

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ShowLayoutMenuAction(gaupol.MenuAction):

    """Show the "Layout" menu."""

    def __init__(self):
        """Initialize a :class:`ShowLayoutMenuAction` instance."""
        gaupol.MenuAction.__init__(self, "show_layout_menu")
        self.set_label(_("_Layout"))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)


class ShowTimesAction(gaupol.RadioAction):

    """Show positions as times."""

    def __init__(self):
        """Initialize a :class:`ShowTimesAction` instance."""
        gaupol.RadioAction.__init__(self, "show_times")
        self.set_active(gaupol.conf.editor.mode == aeidon.modes.TIME)
        self.set_label(_("_Times"))
        self.set_tooltip(_("Show positions as times"))
        self.props.value = aeidon.modes.TIME
        self.accelerator = "T"
        self.action_group = "main-unsafe"
        self.group = "ShowTimesAction"
        self.mode = aeidon.modes.TIME

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ToggleDurationColumnAction(gaupol.ToggleAction):

    """Show or hide the duration column."""

    def __init__(self):
        """Initialize a :class:`ToggleDurationColumnAction` instance."""
        gaupol.ToggleAction.__init__(self, "toggle_duration_column")
        fields = gaupol.conf.editor.visible_fields
        self.set_active(gaupol.fields.DURATION in fields)
        self.set_label(_("_Duration"))
        self.set_tooltip(_('Show or hide the duration column'))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ToggleEndColumnAction(gaupol.ToggleAction):

    """Show or hide the end column."""

    def __init__(self):
        """Initialize a :class:`ToggleEndColumnAction` instance."""
        gaupol.ToggleAction.__init__(self, "toggle_end_column")
        fields = gaupol.conf.editor.visible_fields
        self.set_active(gaupol.fields.END in fields)
        self.set_label(_("_End"))
        self.set_tooltip(_('Show or hide the end column'))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ToggleMainTextColumnAction(gaupol.ToggleAction):

    """Show or hide the main text column."""

    def __init__(self):
        """Initialize a :class:`ToggleMainTextColumnAction` instance."""
        gaupol.ToggleAction.__init__(self, "toggle_main_text_column")
        fields = gaupol.conf.editor.visible_fields
        self.set_active(gaupol.fields.MAIN_TEXT in fields)
        self.set_label(_("_Text"))
        self.set_tooltip(_('Show or hide the text column'))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ToggleMainToolbarAction(gaupol.ToggleAction):

    """Show or hide the main toolbar."""

    def __init__(self):
        """Initialize a :class:`ToggleMainToolbarAction` instance."""
        gaupol.ToggleAction.__init__(self, "toggle_main_toolbar")
        show = gaupol.conf.application_window.show_main_toolbar
        self.set_active(show)
        self.set_label(_("Tool_bar"))
        self.set_tooltip(_("Show or hide the toolbar"))
        self.action_group = "main-safe"


class ToggleNumberColumnAction(gaupol.ToggleAction):

    """Show or hide the number column."""

    def __init__(self):
        """Initialize a :class:`ToggleNumberColumnAction` instance."""
        gaupol.ToggleAction.__init__(self, "toggle_number_column")
        fields = gaupol.conf.editor.visible_fields
        self.set_active(gaupol.fields.NUMBER in fields)
        self.set_label(_("_No."))
        self.set_tooltip(_('Show or hide the number column'))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class TogglePlayerAction(gaupol.ToggleAction):

    """Show or hide the video player."""

    __gtype_name__ = "TogglePlayerAction"

    def __init__(self):
        """Initialize a :class:`TogglePlayerAction` instance."""
        gaupol.ToggleAction.__init__(self, "toggle_player")
        self.set_active(False)
        self.set_label(_("_Video Player"))
        self.set_icon_name("video")
        self.set_tooltip(_("Show or hide the video player"))
        self.action_group = "main-safe"
        self.tool_item_type = Gtk.ToggleToolButton

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)


class ToggleStartColumnAction(gaupol.ToggleAction):

    """Show or hide the start column."""

    def __init__(self):
        """Initialize a :class:`ToggleStartColumnAction` instance."""
        gaupol.ToggleAction.__init__(self, "toggle_start_column")
        fields = gaupol.conf.editor.visible_fields
        self.set_active(gaupol.fields.START in fields)
        self.set_label(_("_Start"))
        self.set_tooltip(_('Show or hide the start column'))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ToggleTranslationTextColumnAction(gaupol.ToggleAction):

    """Show or hide the translation text column."""

    def __init__(self):
        """Initialize a :class:`ToggleTranslationTextColumnAction` instance."""
        name = "toggle_translation_text_column"
        gaupol.ToggleAction.__init__(self, name)
        fields = gaupol.conf.editor.visible_fields
        self.set_active(gaupol.fields.TRAN_TEXT in fields)
        self.set_label(_("T_ranslation"))
        self.set_tooltip(_('Show or hide the translation column'))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class UseHorizontalLayoutAction(gaupol.RadioAction):

    """Split window horizontally."""

    def __init__(self):
        """Initialize a :class:`UseHorizontalLayoutAction` instance."""
        gaupol.RadioAction.__init__(self, "use_horizontal_layout")
        layout = gaupol.conf.application_window.layout
        self.set_active((layout == gaupol.orientation.HORIZONTAL))
        self.set_label(_("_Horizontal"))
        self.set_tooltip(_("Split window horizontally"))
        self.props.value = gaupol.orientation.HORIZONTAL
        self.action_group = "main-unsafe"
        self.group = "UseHorizontalLayoutAction"
        self.orientation = gaupol.orientation.HORIZONTAL

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)


class UseVerticalLayoutAction(gaupol.RadioAction):

    """Split window vertically."""

    def __init__(self):
        """Initialize a :class:`UseVerticalLayoutAction` instance."""
        gaupol.RadioAction.__init__(self, "use_vertical_layout")
        layout = gaupol.conf.application_window.layout
        self.set_active((layout == gaupol.orientation.VERTICAL))
        self.set_label(_("_Vertical"))
        self.set_tooltip(_("Split window vertically"))
        self.props.value = gaupol.orientation.VERTICAL
        self.action_group = "main-unsafe"
        self.group = "UseHorizontalLayoutAction"
        self.orientation = gaupol.orientation.VERTICAL

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)


__all__ = tuple(x for x in dir() if x.endswith("Action"))
