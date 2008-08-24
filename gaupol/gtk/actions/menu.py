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

"""Actions that provide top-level menus."""

import gaupol
_ = gaupol.i18n._


class ShowEditMenuAction(gaupol.gtk.TopMenuAction):

    """Show the 'Edit' menu."""

    def __init__(self):

        gaupol.gtk.TopMenuAction.__init__(self, "show_edit_menu")
        self.props.label = _("_Edit")


class ShowFileMenuAction(gaupol.gtk.TopMenuAction):

    """Show the 'File' menu."""

    def __init__(self):

        gaupol.gtk.TopMenuAction.__init__(self, "show_file_menu")
        self.props.label = _("_File")


class ShowHelpMenuAction(gaupol.gtk.TopMenuAction):

    """Show the 'Help' menu."""

    def __init__(self):

        gaupol.gtk.TopMenuAction.__init__(self, "show_help_menu")
        self.props.label = _("_Help")


class ShowProjectsMenuAction(gaupol.gtk.TopMenuAction):

    """Show the 'Projects' menu."""

    def __init__(self):

        gaupol.gtk.TopMenuAction.__init__(self, "show_projects_menu")
        self.props.label = _("_Projects")


class ShowTextMenuAction(gaupol.gtk.TopMenuAction):

    """Show the 'Text' menu."""

    def __init__(self):

        gaupol.gtk.TopMenuAction.__init__(self, "show_text_menu")
        self.props.label = _("_Text")


class ShowToolsMenuAction(gaupol.gtk.TopMenuAction):

    """Show the 'Tools' menu."""

    def __init__(self):

        gaupol.gtk.TopMenuAction.__init__(self, "show_tools_menu")
        self.props.label = _("T_ools")


class ShowViewMenuAction(gaupol.gtk.TopMenuAction):

    """Show the 'View' menu."""

    def __init__(self):

        gaupol.gtk.TopMenuAction.__init__(self, "show_view_menu")
        self.props.label = _("_View")


__all__ = gaupol.util.get_all(dir(), r"Action$")
