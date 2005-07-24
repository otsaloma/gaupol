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


"""File saver to save currently open main or translation documents."""


import os

try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.gui.constants import ORIG, TRAN
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.dialogs.error import UnicodeEncodeErrorDialog
from gaupol.gui.dialogs.error import WriteFileErrorDialog
from gaupol.gui.dialogs.filechooser import SaveDialog
from gaupol.gui.dialogs.question import OverwriteFileQuestionDialog
from gaupol.gui.util import gui
from gaupol.lib.formats.all import *
from gaupol.lib.util import encodings as encodings_module


class FileSaver(Delegate):

    """File saver to save currently open main or translation documents."""

    def on_save_a_copy_activated(self, *args):
        """Save a copy of the main document."""

        project = self.get_current_project()
        
        success = self.save_a_copy_of_main_document(project)
        if not success:
            return False

        return True

    def on_save_a_copy_of_translation_activated(self, *args):
        """Save a copy of the translation document."""

        project = self.get_current_project()
        
        success = self.save_a_copy_of_translation_document(project)
        if not success:
            return False

        return True

    def on_save_activated(self, *args):
        """
        Save the main document.

        Return: success (True or False)
        """
        project = self.get_current_project()
        
        success = self.save_main_document(project)
        if not success:
            return False

        self.window.set_title(project.tab_label.get_text())
        self.set_sensitivities_and_visiblities(project)

        return True

    def on_save_all_activated(self, *args):
        """Save all subtitle and translation document."""

        for project in self.projects:
            if project.main_changed:
                self.save_main_document(project)
            if project.tran_changed:
                self.save_translation_document(project)

        project = self.get_current_project()
        self.window.set_title(project.tab_label.get_text())
        self.set_sensitivities_and_visiblities(project)

    def on_save_as_activated(self, *args):
        """
        Save the main document with FileChooser.

        Return: success (True or False)
        """
        project = self.get_current_project()
        
        success = self.save_main_document_as(project)
        if not success:
            return False

        self.window.set_title(project.tab_label.get_text())
        self.set_sensitivities_and_visiblities(project)

        return True

    def on_save_translation_activated(self, *args):
        """
        Save the translation document.

        Return: success (True or False)
        """
        project = self.get_current_project()
        
        success = self.save_translation_document(project)
        if not success:
            return False

        self.set_sensitivities_and_visiblities(project)

        return True

    def on_save_translation_as_activated(self, *args):
        """
        Save the translation file with FileChooser.

        Return: success (True or False)
        """
        project = self.get_current_project()
        
        success = self.save_translation_document_as(project)
        if not success:
            return False

        self.set_sensitivities_and_visiblities(project)

        return True

    def save_a_copy_of_main_document(self, project):
        """
        Save a copy of the main document with FileChooser.
        
        return: success (True or False)
        """
        gui.set_cursor_busy(self.window)

        path, format, encoding, newlines = \
            project.get_main_document_properties()
        untitle = _('%s (copy)') % project.get_main_corename()

        path = self._select_and_write_file(
            project, 'main', _('Save A Copy'), 
            None, untitle, format, encoding, newlines,
            False
        )
        if path is None:
            gui.set_cursor_normal(self.window)
            return False


        self.set_status_message(_('Saved a copy of subtitle file to "%s".') \
                                % path)
        gui.set_cursor_normal(self.window)
        
        return True

    def save_a_copy_of_translation_document(self, project):
        """
        Save a copy of the translation document with FileChooser.
        
        return: success (True or False)
        """
        gui.set_cursor_busy(self.window)

        path, format, encoding, newlines = \
            project.get_translation_document_properties()
        untitle = _('%s (copy)') % project.get_translation_corename()

        path = self._select_and_write_file(
            project, 'translation', _('Save A Copy Of Translation'), 
            None, untitle, format, encoding, newlines,
            False
        )
        if path is None:
            gui.set_cursor_normal(self.window)
            return False


        self.set_status_message(_('Saved a copy of translation file to "%s".') \
                                % path)
        gui.set_cursor_normal(self.window)
        
        return True

    def save_main_document(self, project):
        """
        Save the main document.

        Return: success (True or False)
        """
        gui.set_cursor_busy(self.window)

        if project.data.main_file is None:
            return self.save_main_document_as(project)

        success = self._write_file(
            project, 'main', self.window, False, True
        )
        if not success:
            gui.set_cursor_normal(self.window)
            return False
        
        project.main_changed = False
        project.set_tab_labels()
        self.refresh_documents_menu()
        
        basename = os.path.basename(project.data.main_file.path)
        self.set_status_message(_('Saved subtitle file "%s".') % basename)
        gui.set_cursor_normal(self.window)
        
        return True

    def save_main_document_as(self, project):
        """
        Save the main document with FileChooser.

        Return: success (True or False)
        """
        gui.set_cursor_busy(self.window)

        path, format, encoding, newlines = \
            project.get_main_document_properties()

        path = self._select_and_write_file(
            project, 'main', _('Save As'), 
            path, project.untitle, format, encoding, newlines,
            True
        )
        if path is None:
            gui.set_cursor_normal(self.window)
            return False

        # Reload original text column data if tags might have chaged after
        # saving in a different format.
        if format is not None:
            if format != project.data.main_file.FORMAT:
                project.reload_tree_view_data_in_columns([ORIG])

        project.main_changed = False
        project.set_tab_labels()
        self.refresh_documents_menu()
        self.add_to_recent_files(path)
        
        self.set_status_message(_('Saved subtitle file as "%s".') % path)
        gui.set_cursor_normal(self.window)
        
        return True
    
    def save_translation_document(self, project):
        """
        Save the translation document.

        Return: success (True or False)
        """
        gui.set_cursor_busy(self.window)

        if project.data.tran_file is None:
            return self.save_translation_document_as(project)

        success = self._write_file(
            project, 'translation', self.window, False, True
        )
        if not success:
            gui.set_cursor_normal(self.window)
            return False
        
        project.tran_changed = False
        project.set_tab_labels()
        self.refresh_documents_menu()
        
        basename = os.path.basename(project.data.tran_file.path)
        self.set_status_message(_('Saved translation file "%s".') % basename)
        gui.set_cursor_normal(self.window)
        
        return True

    def save_translation_document_as(self, project):
        """
        Save the translation document with FileChooser.

        Return: success (True or False)
        """
        gui.set_cursor_busy(self.window)

        path, format, encoding, newlines = \
            project.get_translation_document_properties()
        untitle = project.get_translation_corename()

        path = self._select_and_write_file(
            project, 'translation', _('Save Translation As'), 
            path, untitle, format, encoding, newlines,
            True
        )
        if path is None:
            gui.set_cursor_normal(self.window)
            return False

        # Reload translation text column data if tags might have chaged after
        # saving in a different format.
        if format is not None:
            if format != project.data.tran_file.FORMAT:
                project.reload_tree_view_data_in_columns([TRAN])

        project.tran_changed = False
        project.set_tab_labels()
        self.refresh_documents_menu()
        
        self.set_status_message(_('Saved translation file as "%s".') % path)
        gui.set_cursor_normal(self.window)
        
        return True
        
    def _select_and_write_file(
        self, project, file_type, title,
        path, untitle, format, encoding, newlines,
        keep_changes=True
    ):
        """
        Select a file with FileChooser and write it.
        
        file_type: "main" or "translation"
        Return: path or None, if unsuccessfull
        """
        save_dialog = SaveDialog(self.config, title, self.window)
        
        if path is not None:
            save_dialog.set_filename(path)
        else:
            save_dialog.set_current_name(untitle)

        save_dialog.set_format(format)
        save_dialog.set_encoding(encoding)
        save_dialog.set_newlines(newlines)
        
        gui.set_cursor_normal(self.window)

        while True:

            response = save_dialog.run()
            
            if response != gtk.RESPONSE_OK:
                save_dialog.destroy()
                return None

            path        = save_dialog.get_filename()
            dirname     = os.path.dirname(path)
            format      = save_dialog.get_format()
            encoding    = save_dialog.get_encoding()
            file_filter = save_dialog.get_filter().get_name()
            newlines    = save_dialog.get_newlines()

            extension = eval(format)(None, None).EXTENSION
            if not path.endswith(extension):
                path += extension

            self.config.set('file', 'directory', dirname    )
            self.config.set('file', 'encoding' , encoding   )
            self.config.set('file', 'filter'   , file_filter)
            self.config.set('file', 'format'   , format     )
            self.config.set('file', 'newlines' , newlines   )
            
            success = self._write_file(
                project, file_type, save_dialog,
                True, keep_changes,
                path, format, encoding, newlines,
            )
            
            if success:
                break
            
        save_dialog.destroy()
        gui.set_cursor_busy(self.window)

        return path
        
    def _write_file(
        self, project, file_type, parent,
        ask_overwrite, keep_changes=True,
        path=None, format=None, encoding=None, newlines=None,
    ):
        """
        Check if a file is writeable and write it if possible.
        
        file_type: "main" or "translation"
        Return: success (True or False)
        """
        if path is None:
            if file_type == 'main':
                path = project.data.main_file.path
            elif file_type == 'translation':
                path = project.data.tran_file.path

        basename = os.path.basename(path)

        # Ask whether to overwrite or not.
        if ask_overwrite and os.path.isfile(path):
            dialog = OverwriteFileQuestionDialog(parent, basename)
            response = dialog.run()
            dialog.destroy()
            if response != gtk.RESPONSE_YES:
                return False

        try:

            if path     is None or \
               format   is None or \
               encoding is None or \
               newlines is None :
                eval('project.data.write_%s_file' % file_type)(keep_changes)

            else:
                eval('project.data.write_%s_file' % file_type)(
                    keep_changes, path, format, encoding, newlines
                )

        except IOError, (errno, detail):
            dialog = WriteFileErrorDialog(parent, basename, detail)
            response = dialog.run()
            dialog.destroy()
            return False

        except UnicodeError:
            enc_disp = encodings_module.get_display_name(encoding)
            dialog = UnicodeEncodeErrorDialog(parent, basename, enc_disp)
            response = dialog.run()
            dialog.destroy()
            return False

        return True
