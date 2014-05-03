# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

"""Actions that provide top-level menus for :class:`gaupol.Application`."""

import aeidon
import gaupol
_ = aeidon.i18n._


class ShowAudioMenuAction(gaupol.TopMenuAction):

    """Show the "Audio" menu."""

    def __init__(self):
        """Initialize a :class:`ShowAudioMenuAction` instance."""
        gaupol.TopMenuAction.__init__(self, "show_audio_menu")
        self.props.label = _("_Audio")
        self.action_group = "main-safe"


class ShowEditMenuAction(gaupol.TopMenuAction):

    """Show the "Edit" menu."""

    def __init__(self):
        """Initialize a :class:`ShowEditMenuAction` instance."""
        gaupol.TopMenuAction.__init__(self, "show_edit_menu")
        self.props.label = _("_Edit")
        self.action_group = "main-safe"


class ShowFileMenuAction(gaupol.TopMenuAction):

    """Show the "File" menu."""

    def __init__(self):
        """Initialize a :class:`ShowFileMenuAction` instance."""
        gaupol.TopMenuAction.__init__(self, "show_file_menu")
        self.props.label = _("_File")
        self.action_group = "main-safe"


class ShowHelpMenuAction(gaupol.TopMenuAction):

    """Show the "Help" menu."""

    def __init__(self):
        """Initialize a :class:`ShowHelpMenuAction` instance."""
        gaupol.TopMenuAction.__init__(self, "show_help_menu")
        self.props.label = _("_Help")
        self.action_group = "main-safe"


class ShowProjectsMenuAction(gaupol.TopMenuAction):

    """Show the "Projects" menu."""

    def __init__(self):
        """Initialize a :class:`ShowProjectsMenuAction` instance."""
        gaupol.TopMenuAction.__init__(self, "show_projects_menu")
        self.props.label = _("_Projects")
        self.action_group = "main-safe"


class ShowTextMenuAction(gaupol.TopMenuAction):

    """Show the "Text" menu."""

    def __init__(self):
        """Initialize a :class:`ShowTextMenuAction` instance."""
        gaupol.TopMenuAction.__init__(self, "show_text_menu")
        self.props.label = _("_Text")
        self.action_group = "main-safe"


class ShowToolsMenuAction(gaupol.TopMenuAction):

    """Show the "Tools" menu."""

    def __init__(self):
        """Initialize a :class:`ShowToolsMenuAction` instance."""
        gaupol.TopMenuAction.__init__(self, "show_tools_menu")
        self.props.label = _("T_ools")
        self.action_group = "main-safe"


class ShowVideoMenuAction(gaupol.TopMenuAction):

    """Show the "Video" menu."""

    def __init__(self):
        """Initialize a :class:`ShowVideoMenuAction` instance."""
        gaupol.TopMenuAction.__init__(self, "show_video_menu")
        self.props.label = _("Vi_deo")
        self.action_group = "main-safe"


class ShowViewMenuAction(gaupol.TopMenuAction):

    """Show the "View" menu."""

    def __init__(self):
        """Initialize a :class:`ShowViewMenuAction` instance."""
        gaupol.TopMenuAction.__init__(self, "show_view_menu")
        self.props.label = _("_View")
        self.action_group = "main-safe"


__all__ = tuple(x for x in dir() if x.endswith("Action"))
