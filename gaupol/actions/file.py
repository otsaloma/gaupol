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

"""File and project actions for :class:`gaupol.Application`."""

import aeidon
import gaupol
_ = aeidon.i18n._


class AppendFileAction(gaupol.Action):

    """Append subtitles from file to the current project."""

    def __init__(self):
        """Initialize an :class:`AppendFileAction` instance."""
        gaupol.Action.__init__(self, "append_file")
        self.set_label(_("_Append File…"))
        self.set_tooltip(_("Append subtitles from file to the current project"))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(len(page.project.subtitles) > 0)


class CloseAllProjectsAction(gaupol.Action):

    """Close all open projects."""

    def __init__(self):
        """Initialize a :class:`CloseAllProjectsAction` instance."""
        gaupol.Action.__init__(self, "close_all_projects")
        self.set_icon_name("window-close")
        self.set_label(_("_Close All"))
        self.set_tooltip( _("Close all open projects"))
        self.accelerator = "<Shift><Control>W"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.pages)


class CloseProjectAction(gaupol.Action):

    """Close project."""

    def __init__(self):
        """Initialize a :class:`CloseProjectAction` instance."""
        gaupol.Action.__init__(self, "close_project")
        self.set_icon_name("window-close")
        self.set_label(_("_Close"))
        self.set_tooltip(_("Close the current project"))
        self.accelerator = "<Control>W"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class NewProjectAction(gaupol.Action):

    """Create a new project."""

    def __init__(self):
        """Initialize a :class:`NewProjectAction` instance."""
        gaupol.Action.__init__(self, "new_project")
        self.set_icon_name("document-new")
        self.set_label(_("_New"))
        self.set_tooltip(_("Create a new project"))
        self.accelerator = "<Control>N"
        self.action_group = "main-safe"


class OpenMainFilesAction(gaupol.Action):

    """Open main files."""

    __gtype_name__ = "OpenMainFilesAction"

    def __init__(self):
        """Initialize an :class:`OpenMainFilesAction` instance."""
        gaupol.Action.__init__(self, "open_main_files")
        self.set_icon_name("document-open")
        self.set_is_important(True)
        self.set_label(_("_Open…"))
        self.set_short_label(_("Open"))
        self.set_tooltip(_("Open main files"))
        self.accelerator = "<Control>O"
        self.action_group = "main-safe"


class OpenMainFilesRecentAction(gaupol.RecentAction):

    """Open main files."""

    group = "gaupol-main"

    def __init__(self):
        """Initialize an :class:`OpenMainFilesRecentAction` instance."""
        gaupol.RecentAction.__init__(self, "open_main_files_recent")
        self.set_icon_name("document-open")
        self.set_is_important(True)
        self.set_label(_("_Open…"))
        self.set_short_label(_("Open"))
        self.set_tooltip(_("Open main files"))
        self.action_group = "main-safe"


class OpenRecentMainFileAction(gaupol.RecentAction):

    """Show the recent main file menu."""

    group = "gaupol-main"

    def __init__(self):
        """Initialize a :class:`OpenRecentMainFileAction` instance."""
        gaupol.RecentAction.__init__(self, "open_recent_main_file")
        self.set_is_important(True)
        self.set_label(_("Open _Recent"))
        self.action_group = "main-safe"


class OpenRecentTranslationFileAction(gaupol.RecentAction):

    """Show the recent translation file menu."""

    group = "gaupol-translation"

    def __init__(self):
        """Initialize a :class:`OpenRecentTranslationFileAction` instance."""
        gaupol.RecentAction.__init__(self, "open_recent_translation_file")
        self.set_is_important(False)
        self.set_label(_("Open R_ecent Translation"))
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class OpenTranslationFileAction(gaupol.Action):

    """Open a translation file."""

    def __init__(self):
        """Initialize an :class:`OpenTranslationFileAction` instance."""
        gaupol.Action.__init__(self, "open_translation_file")
        self.set_icon_name("document-open")
        self.set_label(_("Open _Translation…"))
        self.set_short_label(_("Open Translation"))
        self.set_tooltip(_("Open a translation file"))
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class QuitAction(gaupol.Action):

    """Quit Gaupol."""

    def __init__(self):
        """Initialize a :class:`QuitAction` instance."""
        gaupol.Action.__init__(self, "quit")
        self.set_icon_name("application-exit")
        self.set_label(_("_Quit"))
        self.set_tooltip(_("Quit Gaupol"))
        self.accelerator = "<Control>Q"
        self.action_group = "main-safe"


class SaveAllDocumentsAction(gaupol.Action):

    """Save all open documents."""

    def __init__(self):
        """Initialize a :class:`SaveAllDocumentsAction` instance."""
        gaupol.Action.__init__(self, "save_all_documents")
        self.set_icon_name("document-save")
        self.set_label(_("_Save All"))
        self.set_tooltip(_("Save all open documents"))
        self.accelerator = "<Shift><Control>L"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.pages)


class SaveAllDocumentsAsAction(gaupol.Action):

    """Save all open documents with different properties."""

    def __init__(self):
        """Initialize a :class:`SaveAllDocumentsAsAction` instance."""
        gaupol.Action.__init__(self, "save_all_documents_as")
        self.set_icon_name("document-save")
        self.set_label(_("Save _All As…"))
        self.set_tooltip(_("Save all open documents with different properties"))
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm([x for x in application.pages
                            if x.project.main_file is not None])


class SaveMainDocumentAction(gaupol.Action):

    """Save the current main document."""

    def __init__(self):
        """Initialize a :class:`SaveMainDocumentAction` instance."""
        gaupol.Action.__init__(self, "save_main_document")
        self.set_icon_name("document-save")
        self.set_is_important(True)
        self.set_label(_("_Save"))
        self.set_tooltip(_("Save the current main document"))
        self.accelerator = "<Control>S"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class SaveMainDocumentAsAction(gaupol.Action):

    """Save the current main document with a different name."""

    def __init__(self):
        """Initialize a :class:`SaveMainDocumentAsAction` instance."""
        gaupol.Action.__init__(self, "save_main_document_as")
        self.set_icon_name("document-save-as")
        self.set_label(_("Save _As…"))
        self.set_short_label(_("Save As"))
        self.set_tooltip(_("Save the current main document with a different name"))
        self.accelerator = "<Shift><Control>S"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class SaveTranslationDocumentAction(gaupol.Action):

    """Save the current translation document."""

    def __init__(self):
        """Initialize a :class:`SaveTranslationDocumentAction` instance."""
        gaupol.Action.__init__(self, "save_translation_document")
        self.set_icon_name("document-save")
        self.set_label(_("Save Trans_lation"))
        self.set_tooltip(_("Save the current translation document"))
        self.accelerator = "<Control>T"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class SaveTranslationDocumentAsAction(gaupol.Action):

    """Save the current translation document with a different name."""

    def __init__(self):
        """Initialize a :class:`SaveTranslationDocumentAsAction` instance."""
        gaupol.Action.__init__(self, "save_translation_document_as")
        self.set_icon_name("document-save-as")
        self.set_label(_("Save Translat_ion As…"))
        self.set_short_label(_("Save Translation As"))
        self.set_tooltip(_("Save the current translation document with a different name"))
        self.accelerator = "<Shift><Control>T"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class SelectVideoFileAction(gaupol.Action):

    """Select a video file."""

    def __init__(self):
        """Initialize a :class:`SelectVideoFileAction` instance."""
        gaupol.Action.__init__(self, "select_video_file")
        self.set_label(_("Select _Video…"))
        self.set_tooltip(_("Select a video file"))
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class SplitProjectAction(gaupol.Action):

    """Split the current project in two."""

    def __init__(self):
        """Initialize a :class:`SplitProjectAction` instance."""
        gaupol.Action.__init__(self, "split_project")
        self.set_label(_("Spli_t Project…"))
        self.set_tooltip(_("Split the current project in two"))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(len(page.project.subtitles) > 1)


__all__ = tuple(x for x in dir() if x.endswith("Action"))
