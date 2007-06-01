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


"""View menu UI manager actions."""


from gaupol.gtk import conf, const
from gaupol.i18n import _
from .action import Action, RadioAction, ToggleAction


class ActivateNextProjectAction(Action):

    """Activate the project in the next tab."""

    def __init__(self):

        Action.__init__(self, "activate_next_project")
        self.props.label = _("_Next")
        self.props.tooltip = _("Activate the project in the next tab")
        self.accelerator = "<Control>Page_Down"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        index = application.pages.index(page) + 1
        assert index in range(len(application.pages))


class ActivatePreviousProjectAction(Action):

    """Activate the project in the previous tab."""

    def __init__(self):

        Action.__init__(self, "activate_previous_project")
        self.props.label = _("_Previous")
        self.props.tooltip = _("Activate the project in the previous tab")
        self.accelerator = "<Control>Page_Up"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert application.pages.index(page) > 0


class MoveTabLeftAction(Action):

    """Move the current tab to the left."""

    def __init__(self):

        Action.__init__(self, "move_tab_left")
        self.props.label = _("Move Tab _Left")
        self.props.tooltip = _("Move the current tab to the left")

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert application.pages.index(page) > 0


class MoveTabRightAction(Action):

    """Move the current tab to the right."""

    def __init__(self):

        Action.__init__(self, "move_tab_right")
        self.props.label = _("Move Tab _Right")
        self.props.tooltip = _("Move the current tab to the right")

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        index = application.pages.index(page) + 1
        assert index in range(len(application.pages))


class ShowColumnsMenuAction(Action):

    """Show the columns view menu."""
    def __init__(self):

        Action.__init__(self, "show_columns_menu")
        self.props.label = _("_Columns")

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None


class ShowFramerate24Action(RadioAction):

    """Change the framerate to 24 fps."""

    def __init__(self):

        RadioAction.__init__(self, "show_framerate_24")
        self.props.active = (conf.editor.framerate == const.FRAMERATE.P24)
        self.props.label = _("2_4 fps")
        tooltip = _("Calculate unnative units with framerate 24 fps")
        self.props.tooltip = tooltip
        self.props.value = const.FRAMERATE.P24
        self.group = "ShowFramerate24Action"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.project.main_file is not None


class ShowFramerate25Action(RadioAction):

    """Change the framerate to 25 fps."""

    def __init__(self):

        RadioAction.__init__(self, "show_framerate_25")
        self.props.active = (conf.editor.framerate == const.FRAMERATE.P25)
        self.props.label = _("2_5 fps")
        tooltip = _("Calculate unnative units with framerate 25 fps")
        self.props.tooltip = tooltip
        self.props.value = const.FRAMERATE.P25
        self.group = "ShowFramerate24Action"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.project.main_file is not None


class ShowFramerate30Action(RadioAction):

    """Change the framerate to 30 fps."""

    def __init__(self):

        RadioAction.__init__(self, "show_framerate_30")
        self.props.active = (conf.editor.framerate == const.FRAMERATE.P30)
        self.props.label = _("_30 fps")
        tooltip = _("Calculate unnative units with framerate 30 fps")
        self.props.tooltip = tooltip
        self.props.value = const.FRAMERATE.P30
        self.group = "ShowFramerate24Action"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.project.main_file is not None


class ShowFramerateMenuAction(Action):

    """Show the framerate view menu."""

    def __init__(self):

        Action.__init__(self, "show_framerate_menu")
        self.props.label = _("F_ramerate")
        self.widgets = ["framerate_combo"]

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.project.main_file is not None


class ShowFramesAction(RadioAction):

    """Show positions as frames."""

    def __init__(self):

        RadioAction.__init__(self, "show_frames")
        self.props.active = (conf.editor.mode == const.MODE.FRAME)
        self.props.label = _("_Frames")
        self.props.tooltip = _("Show positions as frames")
        self.props.value = const.MODE.FRAME
        self.accelerator = "<Shift>T"
        self.group = "ShowTimesAction"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None


class ShowTimesAction(RadioAction):

    """Show positions as times."""

    def __init__(self):

        RadioAction.__init__(self, "show_times")
        self.props.active = (conf.editor.mode == const.MODE.TIME)
        self.props.label = _("_Times")
        self.props.tooltip = _("Show positions as times")
        self.props.value = const.MODE.TIME
        self.accelerator = "T"
        self.group = "ShowTimesAction"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None


class ToggleDurationColumnAction(ToggleAction):

    """Show or hide the "Duration" column."""

    def __init__(self):

        ToggleAction.__init__(self, "toggle_duration_column")
        self.props.active = const.COLUMN.DURN in conf.editor.visible_cols
        self.props.label = _("_Duration")
        self.props.tooltip = _('Show or hide the "Duration" column')

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None


class ToggleEndColumnAction(ToggleAction):

    """Show or hide the "End" column."""

    def __init__(self):

        ToggleAction.__init__(self, "toggle_end_column")
        self.props.active = const.COLUMN.END in conf.editor.visible_cols
        self.props.label = _("_End")
        self.props.tooltip = _('Show or hide the "End" column')

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None


class ToggleMainTextColumnAction(ToggleAction):

    """Show or hide the "Main Text" column."""

    def __init__(self):

        ToggleAction.__init__(self, "toggle_main_text_column")
        self.props.active = const.COLUMN.MTXT in conf.editor.visible_cols
        self.props.label = _("_Main Text")
        self.props.tooltip = _('Show or hide the "Main Text" column')

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None


class ToggleMainToolbarAction(ToggleAction):

    """Show or hide the main toolbar."""

    def __init__(self):

        ToggleAction.__init__(self, "toggle_main_toolbar")
        self.props.active = conf.application_window.show_main_toolbar
        self.props.label = _("_Main Toolbar")
        self.props.tooltip = _("Show or hide the main toolbar")


class ToggleNumberColumnAction(ToggleAction):

    """Show or hide the 'No.' column."""

    def __init__(self):

        ToggleAction.__init__(self, "toggle_number_column")
        self.props.active = const.COLUMN.NO in conf.editor.visible_cols
        self.props.label = _("_No.")
        self.props.tooltip = _('Show or hide the "No." column')

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None


class ToggleOutputWindowAction(ToggleAction):

    """Show or hide the output window."""

    def __init__(self):

        ToggleAction.__init__(self, "toggle_output_window")
        self.props.active = conf.output_window.show
        self.props.label = _("_Output Window")
        self.props.tooltip = _("Show or hide the output window")


class ToggleStartColumnAction(ToggleAction):

    """Show or hide the 'Start' column."""

    def __init__(self):

        ToggleAction.__init__(self, "toggle_start_column")
        self.props.active = const.COLUMN.START in conf.editor.visible_cols
        self.props.label = _("_Start")
        self.props.tooltip = _('Show or hide the "Start" column')

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None


class ToggleStatusbarAction(ToggleAction):

    """Show or hide the statusbar."""

    def __init__(self):

        ToggleAction.__init__(self, "toggle_statusbar")
        self.props.active = conf.application_window.show_statusbar
        self.props.label = _("_Statusbar")
        self.props.tooltip = _("Show or hide the statusbar")


class ToggleTranslationTextColumnAction(ToggleAction):

    """Show or hide the 'Translation Text' column."""

    def __init__(self):

        ToggleAction.__init__(self, "toggle_translation_text_column")
        self.props.active = const.COLUMN.TTXT in conf.editor.visible_cols
        self.props.label = _("_Translation Text")
        self.props.tooltip = _('Show or hide the "Translation Text" column')

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None


class ToggleVideoToolbarAction(ToggleAction):

    """Show or hide the video toolbar."""

    def __init__(self):

        ToggleAction.__init__(self, "toggle_video_toolbar")
        self.props.active = conf.application_window.show_video_toolbar
        self.props.label = _("_Video Toolbar")
        self.props.tooltip = _("Show or hide the video toolbar")
