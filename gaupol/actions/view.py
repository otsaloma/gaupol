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

"""View menu UI manager actions."""

import gaupol
_ = aeidon.i18n._


class ActivateNextProjectAction(gaupol.Action):

    """Activate the project in the next tab."""

    def __init__(self):
        """Initialize an ActivateNextProjectAction object."""

        gaupol.Action.__init__(self, "activate_next_project")
        self.props.label = _("_Next")
        self.props.tooltip = _("Activate the project in the next tab")
        self.accelerator = "<Control>Page_Down"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)
        index = application.pages.index(page) + 1
        aeidon.util.affirm(index in range(len(application.pages)))


class ActivatePreviousProjectAction(gaupol.Action):

    """Activate the project in the previous tab."""

    def __init__(self):
        """Initialize an ActivatePreviousProjectAction object."""

        gaupol.Action.__init__(self, "activate_previous_project")
        self.props.label = _("_Previous")
        self.props.tooltip = _("Activate the project in the previous tab")
        self.accelerator = "<Control>Page_Up"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.pages.index(page) > 0)


class MoveTabLeftAction(gaupol.Action):

    """Move the current tab to the left."""

    def __init__(self):
        """Initialize a MoveTabLeftAction object."""

        gaupol.Action.__init__(self, "move_tab_left")
        self.props.label = _("Move Tab _Left")
        self.props.tooltip = _("Move the current tab to the left")
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.pages.index(page) > 0)


class MoveTabRightAction(gaupol.Action):

    """Move the current tab to the right."""

    def __init__(self):
        """Initialize a MoveTabRightAction object."""

        gaupol.Action.__init__(self, "move_tab_right")
        self.props.label = _("Move Tab _Right")
        self.props.tooltip = _("Move the current tab to the right")
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)
        index = application.pages.index(page) + 1
        aeidon.util.affirm(index in range(len(application.pages)))


class ShowColumnsMenuAction(gaupol.MenuAction):

    """Show the columns view menu."""
    def __init__(self):
        """Initialize a ShowColumnsMenuAction object."""

        gaupol.MenuAction.__init__(self, "show_columns_menu")
        self.props.label = _("_Columns")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)


class ShowFramerate24Action(gaupol.RadioAction):

    """Change the framerate to 24 fps."""

    def __init__(self):
        """Initialize a ShowFramerate24Action object."""

        gaupol.RadioAction.__init__(self, "show_framerate_24")
        framerate = gaupol.conf.editor.framerate
        self.props.active = (framerate == aeidon.framerates.FPS_24)
        self.props.label = _("2_4 fps")
        tooltip = _("Calculate nonnative units with framerate 24 fps")
        self.props.tooltip = tooltip
        self.props.value = aeidon.framerates.FPS_24
        self.action_group = "main-unsafe"
        self.framerate = aeidon.framerates.FPS_24
        self.group = "ShowFramerate24Action"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class ShowFramerate25Action(gaupol.RadioAction):

    """Change the framerate to 25 fps."""

    def __init__(self):
        """Initialize a ShowFramerate25Action object."""

        gaupol.RadioAction.__init__(self, "show_framerate_25")
        framerate = gaupol.conf.editor.framerate
        self.props.active = (framerate == aeidon.framerates.FPS_25)
        self.props.label = _("2_5 fps")
        tooltip = _("Calculate nonnative units with framerate 25 fps")
        self.props.tooltip = tooltip
        self.props.value = aeidon.framerates.FPS_25
        self.action_group = "main-unsafe"
        self.framerate = aeidon.framerates.FPS_25
        self.group = "ShowFramerate24Action"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class ShowFramerate30Action(gaupol.RadioAction):

    """Change the framerate to 30 fps."""

    def __init__(self):
        """Initialize a ShowFramerate30Action object."""

        gaupol.RadioAction.__init__(self, "show_framerate_30")
        framerate = gaupol.conf.editor.framerate
        self.props.active = (framerate == aeidon.framerates.FPS_30)
        self.props.label = _("_30 fps")
        tooltip = _("Calculate nonnative units with framerate 30 fps")
        self.props.tooltip = tooltip
        self.props.value = aeidon.framerates.FPS_30
        self.action_group = "main-unsafe"
        self.framerate = aeidon.framerates.FPS_30
        self.group = "ShowFramerate24Action"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class ShowFramerateMenuAction(gaupol.MenuAction):

    """Show the framerate view menu."""

    def __init__(self):
        """Initialize a ShowFramerateMenuAction object."""

        gaupol.MenuAction.__init__(self, "show_framerate_menu")
        self.props.label = _("F_ramerate")
        self.action_group = "main-unsafe"
        self.widgets = ("framerate_combo",)

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class ShowFramesAction(gaupol.RadioAction):

    """Show positions as frames."""

    def __init__(self):
        """Initialize a ShowFramesAction object."""

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
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)


class ShowTimesAction(gaupol.RadioAction):

    """Show positions as times."""

    def __init__(self):
        """Initialize a ShowTimesAction object."""

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
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)


class ToggleDurationColumnAction(gaupol.ToggleAction):

    """Show or hide the 'Duration' column."""

    def __init__(self):
        """Initialize a ToggleDurationColumnAction object."""

        gaupol.ToggleAction.__init__(self, "toggle_duration_column")
        fields = gaupol.conf.editor.visible_fields
        self.props.active = gaupol.fields.DURATION in fields
        self.props.label = _("_Duration")
        self.props.tooltip = _('Show or hide the "Duration" column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)


class ToggleEndColumnAction(gaupol.ToggleAction):

    """Show or hide the 'End' column."""

    def __init__(self):
        """Initialize a ToggleEndColumnAction object."""

        gaupol.ToggleAction.__init__(self, "toggle_end_column")
        fields = gaupol.conf.editor.visible_fields
        self.props.active = gaupol.fields.END in fields
        self.props.label = _("_End")
        self.props.tooltip = _('Show or hide the "End" column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)


class ToggleMainTextColumnAction(gaupol.ToggleAction):

    """Show or hide the 'Main Text' column."""

    def __init__(self):
        """Initialize a ToggleMainTextColumnAction object."""

        gaupol.ToggleAction.__init__(self, "toggle_main_text_column")
        fields = gaupol.conf.editor.visible_fields
        self.props.active = gaupol.fields.MAIN_TEXT in fields
        self.props.label = _("_Main Text")
        self.props.tooltip = _('Show or hide the "Main Text" column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)


class ToggleMainToolbarAction(gaupol.ToggleAction):

    """Show or hide the main toolbar."""

    def __init__(self):
        """Initialize a ToggleMainToolbarAction object."""

        gaupol.ToggleAction.__init__(self, "toggle_main_toolbar")
        show = gaupol.conf.application_window.show_main_toolbar
        self.props.active = show
        self.props.label = _("_Main Toolbar")
        self.props.tooltip = _("Show or hide the main toolbar")
        self.action_group = "main-safe"


class ToggleNumberColumnAction(gaupol.ToggleAction):

    """Show or hide the 'No.' column."""

    def __init__(self):
        """Initialize a ToggleNumberColumnAction object."""

        gaupol.ToggleAction.__init__(self, "toggle_number_column")
        fields = gaupol.conf.editor.visible_fields
        self.props.active = gaupol.fields.NUMBER in fields
        self.props.label = _("_No.")
        self.props.tooltip = _('Show or hide the "No." column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)


class ToggleOutputWindowAction(gaupol.ToggleAction):

    """Show or hide the output window."""

    def __init__(self):
        """Initialize a ToggleOutputWindowAction object."""

        gaupol.ToggleAction.__init__(self, "toggle_output_window")
        self.props.active = gaupol.conf.output_window.show
        self.props.label = _("_Output Window")
        self.props.tooltip = _("Show or hide the output window")
        self.action_group = "main-safe"


class ToggleStartColumnAction(gaupol.ToggleAction):

    """Show or hide the 'Start' column."""

    def __init__(self):
        """Initialize a ToggleStartColumnAction object."""

        gaupol.ToggleAction.__init__(self, "toggle_start_column")
        fields = gaupol.conf.editor.visible_fields
        self.props.active = gaupol.fields.START in fields
        self.props.label = _("_Start")
        self.props.tooltip = _('Show or hide the "Start" column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)


class ToggleStatusbarAction(gaupol.ToggleAction):

    """Show or hide the statusbar."""

    def __init__(self):
        """Initialize a ToggleStatusbarAction object."""

        gaupol.ToggleAction.__init__(self, "toggle_statusbar")
        self.props.active = gaupol.conf.application_window.show_statusbar
        self.props.label = _("_Statusbar")
        self.props.tooltip = _("Show or hide the statusbar")
        self.action_group = "main-safe"


class ToggleTranslationTextColumnAction(gaupol.ToggleAction):

    """Show or hide the 'Translation Text' column."""

    def __init__(self):
        """Initialize a ToggleTranslationTextColumnAction object."""

        name = "toggle_translation_text_column"
        gaupol.ToggleAction.__init__(self, name)
        fields = gaupol.conf.editor.visible_fields
        self.props.active = gaupol.fields.TRAN_TEXT in fields
        self.props.label = _("_Translation Text")
        self.props.tooltip = _('Show or hide the "Translation Text" column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        aeidon.util.affirm(page is not None)


class ToggleVideoToolbarAction(gaupol.ToggleAction):

    """Show or hide the video toolbar."""

    def __init__(self):
        """Initialize a ToggleVideoToolbarAction object."""

        gaupol.ToggleAction.__init__(self, "toggle_video_toolbar")
        show = gaupol.conf.application_window.show_video_toolbar
        self.props.active = show
        self.props.label = _("_Video Toolbar")
        self.props.tooltip = _("Show or hide the video toolbar")
        self.action_group = "main-safe"


__all__ = aeidon.util.get_all(dir(), r"Action$")
