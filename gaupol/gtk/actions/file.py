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

"""File and project actions."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._


class AppendFileAction(gaupol.gtk.Action):

    """Append subtitles from file to the current project."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "append_file")
        self.props.label = _("_Append File\342\200\246")
        self.props.stock_id = gtk.STOCK_ADD
        tooltip = _("Append subtitles from file to the current project")
        self.props.tooltip = tooltip

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class CloseAllProjectsAction(gaupol.gtk.Action):

    """Close all open projects."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "close_all_projects")
        self.props.label = _("_Close All")
        self.props.stock_id = gtk.STOCK_CLOSE
        self.props.tooltip =  _("Close all open projects")
        self.accelerator = "<Shift><Control>W"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(application.pages)


class CloseProjectAction(gaupol.gtk.Action):

    """Close project."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "close_project")
        self.props.label = _("_Close")
        self.props.stock_id = gtk.STOCK_CLOSE
        self.props.tooltip = _("Close the current project")
        self.accelerator = "<Control>W"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class EditHeadersAction(gaupol.gtk.Action):

    """Edit file headers."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "edit_headers")
        self.props.label = _("_Headers")
        self.props.stock_id = gtk.STOCK_PROPERTIES
        self.props.tooltip = _("Edit file headers")
        self.accelerator = "<Alt>Return"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        has_header_found = False
        if page.project.main_file is not None:
            if page.project.main_file.format.has_header:
                has_header_found = True
        if page.project.tran_file is not None:
            if page.project.tran_file.format.has_header:
                has_header_found = True
        gaupol.util.affirm(has_header_found)


class NewProjectAction(gaupol.gtk.Action):

    """Create a new project."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "new_project")
        self.props.label = _("_New")
        self.props.stock_id = gtk.STOCK_NEW
        self.props.tooltip = _("Create a new project")
        self.accelerator = "<Control>N"


class OpenMainFilesAction(gaupol.gtk.Action):

    """Open main files."""

    __gtype_name__ = "OpenMainFilesAction"

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "open_main_files")
        self.props.is_important = True
        self.props.label = _("_Open\342\200\246")
        self.props.short_label = _("Open")
        self.props.stock_id = gtk.STOCK_OPEN
        self.props.tooltip = _("Open main files")
        self.accelerator = "<Control>O"
        self.set_tool_item_type(gtk.MenuToolButton)


class OpenTranslationFileAction(gaupol.gtk.Action):

    """Open a translation file."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "open_translation_file")
        self.props.label = _("Open _Translation\342\200\246")
        self.props.short_label = _("Open Translation")
        self.props.stock_id = gtk.STOCK_OPEN
        self.props.tooltip = _("Open a translation file")

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.main_file is not None)


class QuitAction(gaupol.gtk.Action):

    """Quit Gaupol."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "quit")
        self.props.label = _("_Quit")
        self.props.stock_id = gtk.STOCK_QUIT
        self.props.tooltip = _("Quit Gaupol")
        self.accelerator = "<Control>Q"


class SaveAllDocumentsAction(gaupol.gtk.Action):

    """Save all open documents."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "save_all_documents")
        self.props.label = _("_Save All")
        self.props.stock_id = gtk.STOCK_SAVE
        self.props.tooltip = _("Save all open documents")
        self.accelerator = "<Shift><Control>L"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(application.pages)


class SaveMainDocumentAction(gaupol.gtk.Action):

    """Save the current main document."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "save_main_document")
        self.props.is_important = True
        self.props.label = _("_Save")
        self.props.stock_id = gtk.STOCK_SAVE
        self.props.tooltip = _("Save the current main document")
        self.accelerator = "<Control>S"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class SaveMainDocumentAsAction(gaupol.gtk.Action):

    """Save the current main document with a different name."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "save_main_document_as")
        self.props.label = _("Save _As\342\200\246")
        self.props.short_label = _("Save As")
        self.props.stock_id = gtk.STOCK_SAVE_AS
        tooltip = _("Save the current main document with a different name")
        self.props.tooltip = tooltip
        self.accelerator = "<Shift><Control>S"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class SaveTranslationDocumentAction(gaupol.gtk.Action):

    """Save the current translation document."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "save_translation_document")
        self.props.label = _("Save Trans_lation")
        self.props.stock_id = gtk.STOCK_SAVE
        self.props.tooltip = _("Save the current translation document")
        self.accelerator = "<Control>T"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class SaveTranslationDocumentAsAction(gaupol.gtk.Action):

    """Save the current translation document with a different name."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "save_translation_document_as")
        self.props.label = _("Save Translat_ion As\342\200\246")
        self.props.short_label = _("Save Translation As")
        self.props.stock_id = gtk.STOCK_SAVE_AS
        tip = _("Save the current translation document with a different name")
        self.props.tooltip = tip
        self.accelerator = "<Shift><Control>T"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class SelectVideoFileAction(gaupol.gtk.Action):

    """Select a video file."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "select_video_file")
        self.props.label = _("Select _Video\342\200\246")
        self.props.short_label = _("Video")
        self.props.stock_id = gtk.STOCK_FILE
        self.props.tooltip = _("Select a video file")
        self.widgets = ("video_button",)

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.main_file is not None)


class ShowRecentMainMenuAction(gaupol.gtk.Action):

    """Show the recent main file menu."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "show_recent_main_menu")
        self.props.label = _("Open _Recent")


class ShowRecentTranslationMenuAction(gaupol.gtk.Action):

    """Show the recent translation file menu."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "show_recent_translation_menu")
        self.props.label = _("Open R_ecent Translation")

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class SplitProjectAction(gaupol.gtk.Action):

    """Split the current project in two."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "split_project")
        self.props.label = _("Spli_t Project\342\200\246")
        self.props.tooltip = _("Split the current project in two")

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(len(page.project.subtitles) > 1)


__all__ = gaupol.util.get_all(dir(), r"Action$")
