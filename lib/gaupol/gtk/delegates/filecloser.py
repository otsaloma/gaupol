# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Closing documents and quitting application."""

try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.dialogs.multiclose import MultiCloseWarningDialog
from gaupol.gui.dialogs.warning import CloseMainWarningDialog
from gaupol.gui.dialogs.warning import CloseTranslationWarningDialog
from gaupol.gui.project import Project
from gaupol.gui.util import gui


class FileCloser(Delegate):

    """Closing documents and quitting application."""

    def _close_all_projects(self):
        """
        Close all projects after asking for confirmation.
        
        Return: False if cancelled, otherwise True
        """
        unsaved_count = 0

        # Get amount of unsaved documents.
        for project in self.projects:

            if project.main_changed:
                unsaved_project = project
                unsaved_count += 1

            if project.tran_active and project.tran_changed:
                unsaved_project = project
                unsaved_count += 1

            if unsaved_count > 1:
                break

        # Confirm closing single unsaved document.
        if unsaved_count == 1:
            success = self._close_project(unsaved_project)
            if not success:
                return False

        # Confirm closing multiple unsaved documents.
        elif unsaved_count > 1:
            success = self._confirm_closing_multiple_documents(self.projects)
            if not success:
                return False

        self.projects = []
        
        while self.notebook.get_current_page() > -1:
            self.notebook.remove_page(0)

        return True

    def _close_project(self, project):
        """
        Close project after asking for confirmation.
        
        Return: False if cancelled, otherwise True
        """
        confirm_main = project.main_changed
        confirm_tran =  project.tran_active and project.tran_changed

        # Main document close dialog.
        if confirm_main and not confirm_tran:

            basename = project.get_main_basename()
            dialog = CloseMainWarningDialog(self.window, basename)
            response = dialog.run()
            dialog.destroy()
            
            # Cancel or dialog close button clicked.
            if response != gtk.RESPONSE_YES and response != gtk.RESPONSE_NO:
                return False
            
            # Save clicked.
            elif response == gtk.RESPONSE_YES:
                success = self.save_main_document(project)
                if not success:
                    return False
        
        # Translation document close dialog.
        elif not confirm_main and confirm_tran:
        
            basename = project.get_translation_basename()
            dialog = CloseTranslationWarningDialog(self.window, basename)
            response = dialog.run()
            dialog.destroy()
            
            # Cancel or dialog close button clicked.
            if response != gtk.RESPONSE_YES and response != gtk.RESPONSE_NO:
                return False

            # Save clicked.
            elif response == gtk.RESPONSE_YES:
                success = self.save_translation_document(project)
                if not success:
                    return False

        # Multidocument close dialog.
        elif confirm_main and confirm_tran:
            success = self._confirm_closing_multiple_documents([project])
            if not success:
                return False
        
        notebook_index = self.notebook.get_current_page()
        project_index  = self.projects.index(project)

        # Notebook widget does not seem to be able to handle post page-close
        # page-switching smoothly. So, as a workaround, we'll switch to next
        # page if we're closing the current page.
        if notebook_index == project_index:
            self.notebook.next_page()
        
        self.projects.remove(project)
        self.notebook.remove_page(project_index)

        return True

    def _confirm_closing_multiple_documents(self, projects):
        """
        Confirm closing projects.
        
        Return: False is cancelled, otherwise True
        """
        dialog = MultiCloseWarningDialog(self.window, projects)
        response = dialog.run()

        # "Cancel" or dialog close button clicked.
        if response != gtk.RESPONSE_YES and response != gtk.RESPONSE_NO:
            dialog.destroy()
            return False

        # "Close Without Saving" clicked.
        elif response == gtk.RESPONSE_NO:
            dialog.destroy()
            return True
            
        # "Save" clicked.
        main_projects = dialog.get_main_projects_to_save()
        tran_projects = dialog.get_translation_projects_to_save()
        dialog.destroy()

        gui.set_cursor_busy(self.window)

        for project in main_projects:
            self.save_main_document(project)

        for project in tran_projects:
            self.save_translation_document(project)

        gui.set_cursor_normal(self.window)

        return True

    def on_close_activated(self, *args):
        """Close project after asking for confirmation."""
        
        project = self.get_current_project()
        self.on_notebook_tab_close_button_clicked(project)

    def on_close_all_activated(self, *args):
        """Close all currently open projects after asking for confirmation."""
        
        success = self._close_all_projects()
        
        if success:
            self.set_sensitivities()

    def on_notebook_tab_close_button_clicked(self, project):
        """Close project after asking for confirmation."""

        success = self._close_project(project)

        if success:
            self.set_sensitivities()

    def on_quit_activated(self, *args):
        """Quit application after asking for confirmation."""

        success = self._close_all_projects()
        if not success:
            return

        if not self.config.getboolean('application_window', 'maximized'):

            size = self.window.get_size()
            self.config.setlistint('application_window', 'size', size)

            position = self.window.get_position()
            self.config.setlistint('application_window', 'position', position)

        self.config.write_to_file()

        gtk.main_quit()

    def on_window_delete_event(self, *args):
        """Quit application after asking for confirmation."""
        
        self.on_quit_activated()

        # Return True to stop other handlers.
        return True
