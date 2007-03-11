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


"""File menu UI manager actions."""


import gtk
from gettext import gettext as _

from ._action import UIMAction


class CloseProjectAction(UIMAction):

    """Close project."""

    action_item = (
        "close_project",
        gtk.STOCK_CLOSE,
        _("_Close"),
        "<control>W",
        _("Close the current project"),)

    paths = ["/ui/menubar/file/close"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class EditHeadersAction(UIMAction):

    """Edit file headers."""

    action_item = (
        "edit_headers",
        gtk.STOCK_PROPERTIES,
        _("_Headers"),
        "<alt>Return",
        _("Edit file headers"),)

    paths = ["/ui/menubar/file/headers"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is None:
            return False
        main_file = page.project.main_file
        tran_file = page.project.tran_file
        if main_file is not None:
            if main_file.has_header:
                return True
        if tran_file is not None:
            if tran_file.has_header:
                return True
        return False


class NewProjectAction(UIMAction):

    """Create a new project."""

    action_item = (
        "new_project",
        gtk.STOCK_NEW,
        _("_New"),
        "<control>N",
        _("Create a new project"),)

    paths = ["/ui/menubar/file/new"]


class OpenMainFileAction(UIMAction):

    """Open main files."""

    action_item = (
        "open_main_file",
        gtk.STOCK_OPEN,
        _("_Open..."),
        "<control>O",
        _("Open main files"),)

    paths = ["/ui/menubar/file/open_main"]
    widgets = ["open_button"]


class OpenTranslationFileAction(UIMAction):

    """Open a translation file."""

    action_item = (
        "open_translation_file",
        None,
        _("O_pen Translation..."),
        None,
        _("Open a translation file"),)

    paths = ["/ui/menubar/file/open_translation"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            if page.project.main_file is not None:
                return True
        return False


class QuitAction(UIMAction):

    """Quit Gaupol."""

    action_item = (
        "quit",
        gtk.STOCK_QUIT,
        _("_Quit"),
        "<control>Q",
        _("Quit Gaupol"),)

    paths = ["/ui/menubar/file/quit"]


class SaveMainDocumentAction(UIMAction):

    """Save the current main document."""

    action_item = (
        "save_main_document",
        gtk.STOCK_SAVE,
        _("_Save"),
        "<control>S",
        _("Save the current main document"),)

    paths = ["/ui/menubar/file/save_main", "/ui/main_toolbar/save_main"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class SaveMainDocumentAsAction(UIMAction):

    """Save the current main document with a different name."""

    action_item = (
        "save_main_document_as",
        gtk.STOCK_SAVE_AS,
        _("Save _As..."),
        "<shift><control>S",
        _("Save the current main document with a different name"),)

    paths = ["/ui/menubar/file/save_main_as"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class SaveTranslationDocumentAction(UIMAction):

    """Save the current translation document."""

    action_item = (
        "save_translation_document",
        None,
        _("Sa_ve Translation"),
        "<control>T",
        _("Save the current translation document"),)

    paths = ["/ui/menubar/file/save_translation"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class SaveTranslationDocumentAsAction(UIMAction):

    """Save the current translation document with a different name."""

    action_item = (
        "save_translation_document_as",
        None,
        _("Save _Translation As..."),
        "<shift><control>T",
        _("Save the current translation document with a different name"),)

    paths = ["/ui/menubar/file/save_translation_as"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class SelectVideoFileAction(UIMAction):

    """Select a video file."""

    action_item = (
        "select_video_file",
        None,
        _("Select _Video..."),
        None,
        _("Select a video file"),)

    paths = ["/ui/menubar/file/select_video"]
    widgets = ["video_button"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            if page.project.main_file is not None:
                return True
        return False


class ShowRecentMainMenuAction(UIMAction):

    """Show the recent main file menu."""

    menu_item = (
        "show_recent_main_menu",
        None,
        _("Open _Recent"),
        None,
        None,)

    paths = ["/ui/menubar/file/recent_main"]


class ShowRecentTranslationMenuAction(UIMAction):

    """Show the recent translation file menu."""

    menu_item = (
        "show_recent_translation_menu",
        None,
        _("Open R_ecent Translation"),
        None,
        None,)

    paths = ["/ui/menubar/file/recent_translation"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            if page.project.main_file is not None:
                return True
        return False
