# -*- coding: utf-8 -*-

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

"""View menu UI manager actions for :class:`gaupol.Application`."""

import aeidon
import gaupol
_ = aeidon.i18n._


class ActivateNextProjectAction(gaupol.Action):

    """Activate the project in the next tab."""

    def __init__(self):
        """Initialize an :class:`ActivateNextProjectAction` object."""
        gaupol.Action.__init__(self, "activate_next_project")
        self.props.label = _("_Next")
        self.props.tooltip = _("Activate the project in the next tab")
        self.accelerator = "<Control>Page_Down"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        index = application.pages.index(page) + 1
        aeidon.util.affirm(index in range(len(application.pages)))


class ActivatePreviousProjectAction(gaupol.Action):

    """Activate the project in the previous tab."""

    def __init__(self):
        """Initialize an :class:`ActivatePreviousProjectAction` object."""
        gaupol.Action.__init__(self, "activate_previous_project")
        self.props.label = _("_Previous")
        self.props.tooltip = _("Activate the project in the previous tab")
        self.accelerator = "<Control>Page_Up"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.pages.index(page) > 0)


class MoveTabLeftAction(gaupol.Action):

    """Move the current tab to the left."""

    def __init__(self):
        """Initialize a :class:`MoveTabLeftAction` object."""
        gaupol.Action.__init__(self, "move_tab_left")
        self.props.label = _("Move Tab _Left")
        self.props.tooltip = _("Move the current tab to the left")
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.pages.index(page) > 0)


class MoveTabRightAction(gaupol.Action):

    """Move the current tab to the right."""

    def __init__(self):
        """Initialize a :class:`MoveTabRightAction` object."""
        gaupol.Action.__init__(self, "move_tab_right")
        self.props.label = _("Move Tab _Right")
        self.props.tooltip = _("Move the current tab to the right")
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        index = application.pages.index(page) + 1
        aeidon.util.affirm(index in range(len(application.pages)))


class ShowColumnsMenuAction(gaupol.MenuAction):

    """Show the "Columns" menu."""
    def __init__(self):
        """Initialize a :class:`ShowColumnsMenuAction` object."""
        gaupol.MenuAction.__init__(self, "show_columns_menu")
        self.props.label = _("_Columns")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ShowFramerate23976Action(gaupol.RadioAction):

    """Calculate nonnative units with a framerate of 23.976 fps."""

    def __init__(self):
        """Initialize a :class:`ShowFramerate23976Action` object."""
        gaupol.RadioAction.__init__(self, "show_framerate_23_976")
        framerate = gaupol.conf.editor.framerate
        self.props.active = (framerate == aeidon.framerates.FPS_23_976)
        self.props.label = _("2_3.976 fps")
        self.props.tooltip = _("Calculate nonnative units "
                               "with a framerate of 23.976 fps")

        self.props.value = aeidon.framerates.FPS_23_976
        self.action_group = "main-unsafe"
        self.framerate = aeidon.framerates.FPS_23_976
        self.group = "ShowFramerate23976Action"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class ShowFramerate24000Action(gaupol.RadioAction):

    """Calculate nonnative units with a framerate of 24.000 fps."""

    def __init__(self):
        """Initialize a :class:`ShowFramerate24000Action` object."""
        gaupol.RadioAction.__init__(self, "show_framerate_24_000")
        framerate = gaupol.conf.editor.framerate
        self.props.active = (framerate == aeidon.framerates.FPS_24_000)
        self.props.label = _("2_4.000 fps")
        self.props.tooltip = _("Calculate nonnative units "
                               "with a framerate of 24.000 fps")

        self.props.value = aeidon.framerates.FPS_24_000
        self.action_group = "main-unsafe"
        self.framerate = aeidon.framerates.FPS_24_000
        self.group = "ShowFramerate23976Action"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class ShowFramerate25000Action(gaupol.RadioAction):

    """Calculate nonnative units with a framerate of 25.000 fps."""

    def __init__(self):
        """Initialize a :class:`ShowFramerate25000Action` object."""
        gaupol.RadioAction.__init__(self, "show_framerate_25_000")
        framerate = gaupol.conf.editor.framerate
        self.props.active = (framerate == aeidon.framerates.FPS_25_000)
        self.props.label = _("2_5.000 fps")
        self.props.tooltip = _("Calculate nonnative units "
                               "with a framerate of 25.000 fps")

        self.props.value = aeidon.framerates.FPS_25_000
        self.action_group = "main-unsafe"
        self.framerate = aeidon.framerates.FPS_25_000
        self.group = "ShowFramerate23976Action"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class ShowFramerate29970Action(gaupol.RadioAction):

    """Calculate nonnative units with a framerate of 29.970 fps."""

    def __init__(self):
        """Initialize a :class:`ShowFramerate30Action` object."""
        gaupol.RadioAction.__init__(self, "show_framerate_29_970")
        framerate = gaupol.conf.editor.framerate
        self.props.active = (framerate == aeidon.framerates.FPS_29_970)
        self.props.label = _("2_9.970 fps")
        self.props.tooltip = _("Calculate nonnative units "
                               "with a framerate of 29.970 fps")

        self.props.value = aeidon.framerates.FPS_29_970
        self.action_group = "main-unsafe"
        self.framerate = aeidon.framerates.FPS_29_970
        self.group = "ShowFramerate23976Action"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class ShowFramerateMenuAction(gaupol.MenuAction):

    """Show the "Framerate" menu."""

    def __init__(self):
        """Initialize a :class:`ShowFramerateMenuAction` object."""
        gaupol.MenuAction.__init__(self, "show_framerate_menu")
        self.props.label = _("F_ramerate")
        self.action_group = "main-unsafe"
        self.widgets = ("framerate_combo",)

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class ShowFramesAction(gaupol.RadioAction):

    """Show positions as frames."""

    def __init__(self):
        """Initialize a :class:`ShowFramesAction` object."""
        gaupol.RadioAction.__init__(self, "show_frames")
        mode = gaupol.conf.editor.mode
        self.props.active = (mode == aeidon.modes.FRAME)
        self.props.label = _("_Frames")
        self.props.tooltip = _("Show positions as frames")
        self.props.value = aeidon.modes.FRAME
        self.accelerator = "<Shift>T"
        self.action_group = "main-unsafe"
        self.group = "ShowTimesAction"
        self.mode = aeidon.modes.FRAME

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ShowTimesAction(gaupol.RadioAction):

    """Show positions as times."""

    def __init__(self):
        """Initialize a :class:`ShowTimesAction` object."""
        gaupol.RadioAction.__init__(self, "show_times")
        mode = gaupol.conf.editor.mode
        self.props.active = (mode == aeidon.modes.TIME)
        self.props.label = _("_Times")
        self.props.tooltip = _("Show positions as times")
        self.props.value = aeidon.modes.TIME
        self.accelerator = "T"
        self.action_group = "main-unsafe"
        self.group = "ShowTimesAction"
        self.mode = aeidon.modes.TIME

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ToggleDurationColumnAction(gaupol.ToggleAction):

    """Show or hide the duration column."""

    def __init__(self):
        """Initialize a :class:`ToggleDurationColumnAction` object."""
        gaupol.ToggleAction.__init__(self, "toggle_duration_column")
        fields = gaupol.conf.editor.visible_fields
        self.props.active = gaupol.fields.DURATION in fields
        self.props.label = _("_Duration")
        self.props.tooltip = _('Show or hide the duration column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ToggleEndColumnAction(gaupol.ToggleAction):

    """Show or hide the end column."""

    def __init__(self):
        """Initialize a :class:`ToggleEndColumnAction` object."""
        gaupol.ToggleAction.__init__(self, "toggle_end_column")
        fields = gaupol.conf.editor.visible_fields
        self.props.active = gaupol.fields.END in fields
        self.props.label = _("_End")
        self.props.tooltip = _('Show or hide the end column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ToggleMainTextColumnAction(gaupol.ToggleAction):

    """Show or hide the main text column."""

    def __init__(self):
        """Initialize a :class:`ToggleMainTextColumnAction` object."""
        gaupol.ToggleAction.__init__(self, "toggle_main_text_column")
        fields = gaupol.conf.editor.visible_fields
        self.props.active = gaupol.fields.MAIN_TEXT in fields
        self.props.label = _("_Main Text")
        self.props.tooltip = _('Show or hide the main text column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ToggleMainToolbarAction(gaupol.ToggleAction):

    """Show or hide the main toolbar."""

    def __init__(self):
        """Initialize a :class:`ToggleMainToolbarAction` object."""
        gaupol.ToggleAction.__init__(self, "toggle_main_toolbar")
        show = gaupol.conf.application_window.show_main_toolbar
        self.props.active = show
        self.props.label = _("_Main Toolbar")
        self.props.tooltip = _("Show or hide the main toolbar")
        self.action_group = "main-safe"


class ToggleNumberColumnAction(gaupol.ToggleAction):

    """Show or hide the number column."""

    def __init__(self):
        """Initialize a :class:`ToggleNumberColumnAction` object."""
        gaupol.ToggleAction.__init__(self, "toggle_number_column")
        fields = gaupol.conf.editor.visible_fields
        self.props.active = gaupol.fields.NUMBER in fields
        self.props.label = _("_No.")
        self.props.tooltip = _('Show or hide the number column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ToggleOutputWindowAction(gaupol.ToggleAction):

    """Show or hide the output window."""

    def __init__(self):
        """Initialize a :class:`ToggleOutputWindowAction` object."""
        gaupol.ToggleAction.__init__(self, "toggle_output_window")
        self.props.active = gaupol.conf.output_window.show
        self.props.label = _("_Output Window")
        self.props.tooltip = _("Show or hide the output window")
        self.action_group = "main-safe"


class ToggleStartColumnAction(gaupol.ToggleAction):

    """Show or hide the start column."""

    def __init__(self):
        """Initialize a :class:`ToggleStartColumnAction` object."""
        gaupol.ToggleAction.__init__(self, "toggle_start_column")
        fields = gaupol.conf.editor.visible_fields
        self.props.active = gaupol.fields.START in fields
        self.props.label = _("_Start")
        self.props.tooltip = _('Show or hide the start column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ToggleStatusbarAction(gaupol.ToggleAction):

    """Show or hide the statusbar."""

    def __init__(self):
        """Initialize a :class:`ToggleStatusbarAction` object."""
        gaupol.ToggleAction.__init__(self, "toggle_statusbar")
        self.props.active = gaupol.conf.application_window.show_statusbar
        self.props.label = _("_Statusbar")
        self.props.tooltip = _("Show or hide the statusbar")
        self.action_group = "main-safe"


class ToggleTranslationTextColumnAction(gaupol.ToggleAction):

    """Show or hide the translation text column."""

    def __init__(self):
        """Initialize a :class:`ToggleTranslationTextColumnAction` object."""
        name = "toggle_translation_text_column"
        gaupol.ToggleAction.__init__(self, name)
        fields = gaupol.conf.editor.visible_fields
        self.props.active = gaupol.fields.TRAN_TEXT in fields
        self.props.label = _("_Translation Text")
        self.props.tooltip = _('Show or hide the translation text column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ToggleVideoToolbarAction(gaupol.ToggleAction):

    """Show or hide the video toolbar."""

    def __init__(self):
        """Initialize a :class:`ToggleVideoToolbarAction` object."""
        gaupol.ToggleAction.__init__(self, "toggle_video_toolbar")
        show = gaupol.conf.application_window.show_video_toolbar
        self.props.active = show
        self.props.label = _("_Video Toolbar")
        self.props.tooltip = _("Show or hide the video toolbar")
        self.action_group = "main-safe"


__all__ = tuple(x for x in dir() if x.endswith("Action"))
