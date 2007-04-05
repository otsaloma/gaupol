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


from gettext import gettext as _

from gaupol.gtk import conf, const
from ._action import UIMAction


class ActivateNextProjectAction(UIMAction):

    """Activate the project in the next tab."""

    action_item = (
        "activate_next_project",
        None,
        _("_Next"),
        "<control>Page_Down",
        _("Activate the project in the next tab"),)

    paths = ["/ui/menubar/projects/next"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            index = application.pages.index(page) + 1
            return (index in range(len(application.pages)))
        return False


class ActivatePreviousProjectAction(UIMAction):

    """Activate the project in the previous tab."""

    action_item = (
        "activate_previous_project",
        None,
        _("_Previous"),
        "<control>Page_Up",
        _("Activate the project in the previous tab"),)

    paths = ["/ui/menubar/projects/previous"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            return (application.pages.index(page) > 0)
        return False


class MoveTabLeftAction(UIMAction):

    """Move the current tab to the left."""

    action_item = (
        "move_tab_left",
        None,
        _("Move Tab _Left"),
        None,
        _("Move the current tab to the left"),)

    paths = ["/ui/menubar/projects/move_tab_left"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            return (application.pages.index(page) > 0)
        return False


class MoveTabRightAction(UIMAction):

    """Move the current tab to the right."""

    action_item = (
        "move_tab_right",
        None,
        _("Move Tab _Right"),
        None,
        _("Move the current tab to the right"),)

    paths = ["/ui/menubar/projects/move_tab_right"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            index = application.pages.index(page) + 1
            return (index in range(len(application.pages)))
        return False


class ShowColumnsMenuAction(UIMAction):

    """Show the columns view menu."""

    menu_item = (
        "show_columns_menu",
        None,
        _("_Columns"),
        None,
        None,)

    paths = ["/ui/menubar/view/columns"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            return (page.project.main_file is not None)
        return False


class ShowFramerate23976Action(UIMAction):

    """Change the framerate with which unnative units are calculated."""

    radio_items = (
        [("show_framerate_23_976",
          None,
          _("2_3.976 fps"),
          None,
          _("Calculate unnative units with framerate 23.976 fps"),
          0,),
         ("show_framerate_25",
          None,
          _("2_5 fps"),
          None,
          _("Calculate unnative units with framerate 25 fps"),
          1,),
         ("show_framerate_29_97",
          None,
          _("2_9.97 fps"),
          None,
          _("Calculate unnative units with framerate 29.97 fps"),
          2,),],
        conf.editor.framerate,)

    paths = const.FRAMERATE.uim_paths
    widgets = ["framerate_combo"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            return (page.project.main_file is not None)
        return False


class ShowFramerateMenuAction(UIMAction):

    """Show the framerate view menu."""

    menu_item = (
        "show_framerate_menu",
        None,
        _("_Framerate"),
        None,
        None,)

    paths = ["/ui/menubar/view/framerate"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            return (page.project.main_file is not None)
        return False


class ShowTimesAction(UIMAction):

    """Change the units in which postions are shown."""

    radio_items = (
        [("show_times",
          None,
          _("T_imes"),
          "R",
          _("Show positions as times"),
          0,),
         ("show_frames",
          None,
          _("F_rames"),
          "<shift>R",
          _("Show positions as frames"),
          1,),],
          conf.editor.mode,)

    paths = const.MODE.uim_paths

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class ToggleDurationColumnAction(UIMAction):

    """Show or hide the "Duration" column."""

    toggle_item = (
        "toggle_duration_column",
        None,
        _("_Duration"),
        None,
        _('Show or hide the "Duration" column'),
        const.COLUMN.DURN in conf.editor.visible_cols,)

    # pylint: disable-msg=E1101
    paths = [const.COLUMN.DURN.uim_path]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class ToggleHideColumnAction(UIMAction):

    """Show or hide the "Hide" column."""

    toggle_item = (
        "toggle_hide_column",
        None,
        _("_Hide"),
        None,
        _('Show or hide the "Hide" column'),
        const.COLUMN.HIDE in conf.editor.visible_cols,)

    # pylint: disable-msg=E1101
    paths = [const.COLUMN.HIDE.uim_path]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class ToggleMainTextColumnAction(UIMAction):

    """Show or hide the "Main Text" column."""

    toggle_item = (
        "toggle_main_text_column",
        None,
        _("_Main Text"),
        None,
        _('Show or hide the "Main Text" column'),
        const.COLUMN.MTXT in conf.editor.visible_cols,)

    # pylint: disable-msg=E1101
    paths = [const.COLUMN.MTXT.uim_path]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class ToggleMainToolbarAction(UIMAction):

    """Show or hide the main toolbar."""

    toggle_item = (
        "toggle_main_toolbar",
        None,
        _("_Main Toolbar"),
        None,
        _("Show or hide the main toolbar"),
        conf.application_window.show_main_toolbar,)

    paths = ["/ui/menubar/view/main_toolbar"]


class ToggleNumberColumnAction(UIMAction):

    """Show or hide the 'No.' column."""

    toggle_item = (
        "toggle_number_column",
        None,
        _("_No."),
        None,
        _('Show or hide the "No." column'),
        const.COLUMN.NO in conf.editor.visible_cols,)

    # pylint: disable-msg=E1101
    paths = [const.COLUMN.NO.uim_path]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class ToggleOutputWindowAction(UIMAction):

    """Show or hide the output window."""

    toggle_item = (
        "toggle_output_window",
        None,
        _("_Output Window"),
        None,
        _("Show or hide the output window"),
        conf.output_window.show,)

    paths = ["/ui/menubar/view/output_window"]


class ToggleShowColumnAction(UIMAction):

    """Show or hide the 'Show' column."""

    toggle_item = (
        "toggle_show_column",
        None,
        _("_Show"),
        None,
        _('Show or hide the "Show" column'),
        const.COLUMN.SHOW in conf.editor.visible_cols,)

    # pylint: disable-msg=E1101
    paths = [const.COLUMN.SHOW.uim_path]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class ToggleStatusbarAction(UIMAction):

    """Show or hide the statusbar."""

    toggle_item = (
        "toggle_statusbar",
        None,
        _("_Statusbar"),
        None,
        _("Show or hide the statusbar"),
        conf.application_window.show_statusbar,)

    paths = ["/ui/menubar/view/statusbar"]


class ToggleTranslationTextColumnAction(UIMAction):

    """Show or hide the 'Translation Text' column."""

    toggle_item = (
        "toggle_translation_text_column",
        None,
        _("_Translation Text"),
        None,
        _('Show or hide the "Translation Text" column'),
        const.COLUMN.TTXT in conf.editor.visible_cols,)

    # pylint: disable-msg=E1101
    paths = [const.COLUMN.TTXT.uim_path]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class ToggleVideoToolbarAction(UIMAction):

    """Show or hide the video toolbar."""

    toggle_item = (
        "toggle_video_toolbar",
        None,
        _("_Video Toolbar"),
        None,
        _("Show or hide the video toolbar"),
        conf.application_window.show_video_toolbar,)

    paths = ["/ui/menubar/view/video_toolbar"]
