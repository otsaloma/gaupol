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

import gaupol.gtk
_ = gaupol.i18n._


class ActivateNextProjectAction(gaupol.gtk.Action):

    """Activate the project in the next tab."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "activate_next_project")
        self.props.label = _("_Next")
        self.props.tooltip = _("Activate the project in the next tab")
        self.accelerator = "<Control>Page_Down"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        index = application.pages.index(page) + 1
        gaupol.util.affirm(index in range(len(application.pages)))


class ActivatePreviousProjectAction(gaupol.gtk.Action):

    """Activate the project in the previous tab."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "activate_previous_project")
        self.props.label = _("_Previous")
        self.props.tooltip = _("Activate the project in the previous tab")
        self.accelerator = "<Control>Page_Up"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(application.pages.index(page) > 0)


class MoveTabLeftAction(gaupol.gtk.Action):

    """Move the current tab to the left."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "move_tab_left")
        self.props.label = _("Move Tab _Left")
        self.props.tooltip = _("Move the current tab to the left")
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(application.pages.index(page) > 0)


class MoveTabRightAction(gaupol.gtk.Action):

    """Move the current tab to the right."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "move_tab_right")
        self.props.label = _("Move Tab _Right")
        self.props.tooltip = _("Move the current tab to the right")
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        index = application.pages.index(page) + 1
        gaupol.util.affirm(index in range(len(application.pages)))


class ShowColumnsMenuAction(gaupol.gtk.MenuAction):

    """Show the columns view menu."""
    def __init__(self):

        gaupol.gtk.MenuAction.__init__(self, "show_columns_menu")
        self.props.label = _("_Columns")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class ShowFramerate24Action(gaupol.gtk.RadioAction):

    """Change the framerate to 24 fps."""

    def __init__(self):

        gaupol.gtk.RadioAction.__init__(self, "show_framerate_24")
        framerate = gaupol.gtk.conf.editor.framerate
        self.props.active = (framerate == gaupol.framerates.FPS_24)
        self.props.label = _("2_4 fps")
        tooltip = _("Calculate nonnative units with framerate 24 fps")
        self.props.tooltip = tooltip
        self.props.value = gaupol.framerates.FPS_24
        self.action_group = "main-unsafe"
        self.framerate = gaupol.framerates.FPS_24
        self.group = "ShowFramerate24Action"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.main_file is not None)


class ShowFramerate25Action(gaupol.gtk.RadioAction):

    """Change the framerate to 25 fps."""

    def __init__(self):

        gaupol.gtk.RadioAction.__init__(self, "show_framerate_25")
        framerate = gaupol.gtk.conf.editor.framerate
        self.props.active = (framerate == gaupol.framerates.FPS_25)
        self.props.label = _("2_5 fps")
        tooltip = _("Calculate nonnative units with framerate 25 fps")
        self.props.tooltip = tooltip
        self.props.value = gaupol.framerates.FPS_25
        self.action_group = "main-unsafe"
        self.framerate = gaupol.framerates.FPS_25
        self.group = "ShowFramerate24Action"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.main_file is not None)


class ShowFramerate30Action(gaupol.gtk.RadioAction):

    """Change the framerate to 30 fps."""

    def __init__(self):

        gaupol.gtk.RadioAction.__init__(self, "show_framerate_30")
        framerate = gaupol.gtk.conf.editor.framerate
        self.props.active = (framerate == gaupol.framerates.FPS_30)
        self.props.label = _("_30 fps")
        tooltip = _("Calculate nonnative units with framerate 30 fps")
        self.props.tooltip = tooltip
        self.props.value = gaupol.framerates.FPS_30
        self.action_group = "main-unsafe"
        self.framerate = gaupol.framerates.FPS_30
        self.group = "ShowFramerate24Action"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.main_file is not None)


class ShowFramerateMenuAction(gaupol.gtk.MenuAction):

    """Show the framerate view menu."""

    def __init__(self):

        gaupol.gtk.MenuAction.__init__(self, "show_framerate_menu")
        self.props.label = _("F_ramerate")
        self.action_group = "main-unsafe"
        self.widgets = ("framerate_combo",)

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.main_file is not None)


class ShowFramesAction(gaupol.gtk.RadioAction):

    """Show positions as frames."""

    def __init__(self):

        gaupol.gtk.RadioAction.__init__(self, "show_frames")
        mode = gaupol.gtk.conf.editor.mode
        self.props.active = (mode == gaupol.modes.FRAME)
        self.props.label = _("_Frames")
        self.props.tooltip = _("Show positions as frames")
        self.props.value = gaupol.modes.FRAME
        self.accelerator = "<Shift>T"
        self.action_group = "main-unsafe"
        self.group = "ShowTimesAction"
        self.mode = gaupol.modes.FRAME

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class ShowTimesAction(gaupol.gtk.RadioAction):

    """Show positions as times."""

    def __init__(self):

        gaupol.gtk.RadioAction.__init__(self, "show_times")
        mode = gaupol.gtk.conf.editor.mode
        self.props.active = (mode == gaupol.modes.TIME)
        self.props.label = _("_Times")
        self.props.tooltip = _("Show positions as times")
        self.props.value = gaupol.modes.TIME
        self.accelerator = "T"
        self.action_group = "main-unsafe"
        self.group = "ShowTimesAction"
        self.mode = gaupol.modes.TIME

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class ToggleDurationColumnAction(gaupol.gtk.ToggleAction):

    """Show or hide the 'Duration' column."""

    def __init__(self):

        gaupol.gtk.ToggleAction.__init__(self, "toggle_duration_column")
        fields = gaupol.gtk.conf.editor.visible_fields
        self.props.active = gaupol.gtk.fields.DURATION in fields
        self.props.label = _("_Duration")
        self.props.tooltip = _('Show or hide the "Duration" column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class ToggleEndColumnAction(gaupol.gtk.ToggleAction):

    """Show or hide the 'End' column."""

    def __init__(self):

        gaupol.gtk.ToggleAction.__init__(self, "toggle_end_column")
        fields = gaupol.gtk.conf.editor.visible_fields
        self.props.active = gaupol.gtk.fields.END in fields
        self.props.label = _("_End")
        self.props.tooltip = _('Show or hide the "End" column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class ToggleMainTextColumnAction(gaupol.gtk.ToggleAction):

    """Show or hide the 'Main Text' column."""

    def __init__(self):

        gaupol.gtk.ToggleAction.__init__(self, "toggle_main_text_column")
        fields = gaupol.gtk.conf.editor.visible_fields
        self.props.active = gaupol.gtk.fields.MAIN_TEXT in fields
        self.props.label = _("_Main Text")
        self.props.tooltip = _('Show or hide the "Main Text" column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class ToggleMainToolbarAction(gaupol.gtk.ToggleAction):

    """Show or hide the main toolbar."""

    def __init__(self):

        gaupol.gtk.ToggleAction.__init__(self, "toggle_main_toolbar")
        show = gaupol.gtk.conf.application_window.show_main_toolbar
        self.props.active = show
        self.props.label = _("_Main Toolbar")
        self.props.tooltip = _("Show or hide the main toolbar")
        self.action_group = "main-safe"


class ToggleNumberColumnAction(gaupol.gtk.ToggleAction):

    """Show or hide the 'No.' column."""

    def __init__(self):

        gaupol.gtk.ToggleAction.__init__(self, "toggle_number_column")
        fields = gaupol.gtk.conf.editor.visible_fields
        self.props.active = gaupol.gtk.fields.NUMBER in fields
        self.props.label = _("_No.")
        self.props.tooltip = _('Show or hide the "No." column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class ToggleOutputWindowAction(gaupol.gtk.ToggleAction):

    """Show or hide the output window."""

    def __init__(self):

        gaupol.gtk.ToggleAction.__init__(self, "toggle_output_window")
        self.props.active = gaupol.gtk.conf.output_window.show
        self.props.label = _("_Output Window")
        self.props.tooltip = _("Show or hide the output window")
        self.action_group = "main-safe"


class ToggleStartColumnAction(gaupol.gtk.ToggleAction):

    """Show or hide the 'Start' column."""

    def __init__(self):

        gaupol.gtk.ToggleAction.__init__(self, "toggle_start_column")
        fields = gaupol.gtk.conf.editor.visible_fields
        self.props.active = gaupol.gtk.fields.START in fields
        self.props.label = _("_Start")
        self.props.tooltip = _('Show or hide the "Start" column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class ToggleStatusbarAction(gaupol.gtk.ToggleAction):

    """Show or hide the statusbar."""

    def __init__(self):

        gaupol.gtk.ToggleAction.__init__(self, "toggle_statusbar")
        self.props.active = gaupol.gtk.conf.application_window.show_statusbar
        self.props.label = _("_Statusbar")
        self.props.tooltip = _("Show or hide the statusbar")
        self.action_group = "main-safe"


class ToggleTranslationTextColumnAction(gaupol.gtk.ToggleAction):

    """Show or hide the 'Translation Text' column."""

    def __init__(self):

        name = "toggle_translation_text_column"
        gaupol.gtk.ToggleAction.__init__(self, name)
        fields = gaupol.gtk.conf.editor.visible_fields
        self.props.active = gaupol.gtk.fields.TRAN_TEXT in fields
        self.props.label = _("_Translation Text")
        self.props.tooltip = _('Show or hide the "Translation Text" column')
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class ToggleVideoToolbarAction(gaupol.gtk.ToggleAction):

    """Show or hide the video toolbar."""

    def __init__(self):

        gaupol.gtk.ToggleAction.__init__(self, "toggle_video_toolbar")
        show = gaupol.gtk.conf.application_window.show_video_toolbar
        self.props.active = show
        self.props.label = _("_Video Toolbar")
        self.props.tooltip = _("Show or hide the video toolbar")
        self.action_group = "main-safe"


__all__ = gaupol.util.get_all(dir(), r"Action$")
