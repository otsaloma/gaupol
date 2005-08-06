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


"""Opener of existing subtitle files and creator new ones."""


import os
import urllib
import urlparse

try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.gui.constants import ORIG, TRAN
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.dialogs.error import ReadFileErrorDialog
from gaupol.gui.dialogs.error import UnicodeDecodeErrorDialog
from gaupol.gui.dialogs.error import UnknownFileFormatErrorDialog
from gaupol.gui.dialogs.filechooser import OpenDialog
from gaupol.gui.dialogs.question import RevertQuestionDialog
from gaupol.gui.dialogs.warning import ImportTranslationWarningDialog
from gaupol.gui.dialogs.warning import OpenBigFileWarningDialog
from gaupol.gui.project import Project
from gaupol.gui.util import gui
from gaupol.lib.file.determiner import UnknownFileFormatError
from gaupol.lib.util import encodings as encodings_module


class FileOpener(Delegate):

    """Opener of existing subtitle files and creator new ones."""
    
    def _add_new_project(self, project):
        """Add a new project and open a new notebook page for it."""

        self.projects.append(project)
        index = self.projects.index(project)
        self._connect_project_signals(project)

        if project.data.main_file is not None:
            self.add_to_recent_files(project.data.main_file.path)

        scroller = gtk.ScrolledWindow()
        scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroller.add(project.tree_view)
    
        self.notebook.append_page_menu(
            scroller, project.tab_widget, project.tab_menu_label
        )       
        self.notebook.show_all()
        self.notebook.set_current_page(index)

        project.reload_all_data()

    def add_to_recent_files(self, path):
        """Add path to recent file menus."""
    
        recent_files = self.config.getlist('file', 'recent_files')
        maximum = self.config.getint('file', 'maximum_recent_files')
        
        try:
            recent_files.remove(path)
        except ValueError:
            pass
        
        recent_files.insert(0, path)
        
        while len(recent_files) > maximum:
            recent_files.pop()

        self.config.setlist('file', 'recent_files', recent_files)

    def _connect_project_signals(self, project):
        """Connect gObject signals emitted by project."""
        
        signals = (
            'notebook-tab-close-button-clicked',
            'tree-view-button-press-event',
            'tree-view-cell-edited',
            'tree-view-cell-editing-started',
            'tree-view-cursor-moved',
            'tree-view-headers-clicked',
            'tree-view-selection-changed',
        )
            
        callbacks = (
            self.on_notebook_tab_close_button_clicked,
            self.on_tree_view_button_press_event,
            self.on_tree_view_cell_edited,
            self.on_tree_view_cell_editing_started,
            self.on_tree_view_cursor_moved,
            self.on_tree_view_headers_clicked,
            self.on_tree_view_selection_changed,
        )
        
        for i in range(len(signals)):
            project.connect(signals[i], callbacks[i])

    def _get_default_encoding(self):
        """
        Get default encoding to use for opening files.
        
        Default encoding is locale encoding, or if it doesn't exist or isn't
        valid, then UTF-8.
        """
        try:
            return encodings_module.get_locale_encoding()[0]
        except TypeError:
            return 'utf_8'

    def _get_main_file_open(self, path):
        """
        Make sure main file is not already open.
        
        If it is already open, select that page in the notebook.
        Return: True, if main file is open, otherwise False
        """
        for i in range(len(self.projects)):
        
            main_file = self.projects[i].data.main_file
            
            if main_file is None:
                continue
                
            if main_file.path != path:
                continue
                
            self.notebook.set_current_page(i)

            basename = self.projects[i].get_main_basename()
            message = _('Subtitle file "%s" is already open') % basename
            self.set_status_message(message)

            return True

        return False
        
    def on_files_dropped(self, notebook, context, x, y, sel_data, info, time):
        """Open drag-dropped files."""
        
        uris = sel_data.get_uris()
        paths = []

        for uri in uris:
            unquoted_uri = urllib.unquote(uri)
            path = urlparse.urlsplit(unquoted_uri)[2]
            if os.path.isfile(path):
                paths.append(path)

        self.open_main_files(paths)
        
    def on_import_translation_activated(self, *args):
        """Import a translation file with FileChooser."""

        gui.set_cursor_busy(self.window)
        project = self.get_current_project()

        # Warn if current translation is unsaved.
        if project.tran_changed:

            basename = project.get_translation_basename()
            dialog = ImportTranslationWarningDialog(self.window, basename)
            gui.set_cursor_normal(self.window)
            response = dialog.run()
            dialog.destroy()

            # "Cancel" or dialog close button clicked.
            if response != gtk.RESPONSE_NO and response != gtk.RESPONSE_YES:
                return
            
            # "Save" clicked.
            elif response == gtk.RESPONSE_YES:
                self.on_save_translation_activated()

            gui.set_cursor_busy(self.window)

        new_project = self._select_and_read_file(
            'translation', _('Import Translation'), project
        )
        if new_project is None:
            gui.set_cursor_normal(self.window)
            return

        project = new_project

        # Show the translation column.
        if not project.tree_view.get_column(TRAN).get_visible():
            name = '/ui/menubar/view/columns/translation'
            self.uim.get_action(name).activate()

        project.tran_changed = 0
        self.set_sensitivities()
        project.reload_all_data()

        basename = project.get_translation_basename()
        message = _('Imported translation file "%s"') % basename
        self.set_status_message(message)
        
        gui.set_cursor_normal(self.window)
        
    def on_new_activated(self, *args):
        """Create a new project and start with one blank subtitle."""
        
        self.counter += 1
        project = Project(self.config, self.counter)
        
        project.data.times.append(['00:00:00,000'] * 3)
        project.data.frames.append([0] * 3)
        project.data.texts.append([u''] * 2)

        self._add_new_project(project)
        self.set_status_message(_('Created a new subtitle'))

    def on_open_activated(self, *args):
        """Open a main file with FileChooser."""

        gui.set_cursor_busy(self.window)

        project = self._select_and_read_file('main', _('Open'))
        if project is None:
            gui.set_cursor_normal(self.window)
            return

        self._add_new_project(project)

        basename = project.get_main_basename()
        message = _('Opened subtitle file "%s"') % basename
        self.set_status_message(message)

        gui.set_cursor_normal(self.window)

    def on_recent_file_activated(self, action):
        """Open main file selected from recent files menu."""
        
        index = int(action.get_name().split('-')[-1])
        recent_files = self.config.getlist('file', 'recent_files')
        path = recent_files[index]
        
        self.open_main_files([path])
        
    def on_revert_activated(self, *args):
        """Revert unsaved changes to both main and translation documents."""

        project = self.get_current_project()

        main_exists = project.data.main_file is not None
        tran_exists = project.data.tran_file is not None
        
        dialog = RevertQuestionDialog(
            self.window,
            project.main_changed, project.tran_changed, 
            main_exists, tran_exists,
            project.get_main_basename(), project.get_translation_basename()
        )
        response = dialog.run()
        dialog.destroy()

        if response != gtk.RESPONSE_YES:
            return

        gui.set_cursor_busy(self.window)
            
        if main_exists and project.main_changed:
            self._read_file(
                self.window, 'main', project.data.main_file.path,
                project.data.main_file.encoding, project
            )
        if tran_exists and project.tran_changed:
            self._read_file(
                self.window, 'translation', project.data.tran_file.path,
                project.data.tran_file.encoding
            )

        project.main_changed = 0
        project.tran_changed = 0

        project.undoables = []
        project.redoables = []

        self.set_sensitivities()
        project.reload_all_data()

        gui.set_cursor_normal(self.window)

    def open_main_files(self, paths):
        """
        Open main files in paths list.

        Files are opened with the default encoding.
        """
        gui.set_cursor_busy(self.window)

        encoding = self._get_default_encoding()
        paths.sort()

        for path in paths:

            project = self._read_file(self.window, 'main', path, encoding)
            if project is None:
                continue

            # Make sure file is not already open.
            is_open = self._get_main_file_open(path)
            if is_open:
                continue

            self._add_new_project(project)
            
            basename = project.get_main_basename()
            message = _('Opened subtitle file "%s"') % basename
            self.set_status_message(message)

            # Show the new notebook page right away.
            while gtk.events_pending():
                gtk.main_iteration()

        gui.set_cursor_normal(self.window)
        
    def _select_and_read_file(self, file_type, title, project=None):
        """
        Select a file with FileChooser and read it.
        
        file_type: "main" or "translation"
        project: should be given when reading into existing project

        Return: Project or None.
        """
        open_dialog = OpenDialog(self.config, title, self.window)

        gui.set_cursor_normal(self.window)

        while True:
        
            response = open_dialog.run()

            if response != gtk.RESPONSE_OK:
                open_dialog.destroy()
                return None

            path        = open_dialog.get_filename()
            dirname     = os.path.dirname(path)
            encoding    = open_dialog.get_encoding()
            file_filter = open_dialog.get_filter().get_name()

            self.config.set('file', 'directory', dirname    )
            self.config.set('file', 'encoding' , encoding   )
            self.config.set('file', 'filter'   , file_filter)

            # Make sure file is not already open.
            if file_type == 'main':
                is_open = self._get_main_file_open(path)
                if is_open:
                    open_dialog.destroy()
                    return None

            project = self._read_file(
                open_dialog, file_type, path, encoding, project
            )
            if project is not None:
                break

        open_dialog.destroy()
        gui.set_cursor_busy(self.window)

        return project

    def _read_file(self, parent, file_type, path, encoding, project=None):
        """
        Check if a file is openable and read it if possible.
        
        file_type: "main" or "translation"
        project: should be given when reading into existing project
        
        Return: Project or None, if unsuccessful.
        """
        basename   = os.path.basename(path)
        size_bytes = os.stat(path)[6]
        size_megs  = float(size_bytes) / 1048576.0

        # Show a warning dialog if filesize is over 1 MB.
        if size_megs > 1:
            dialog = OpenBigFileWarningDialog(parent, basename, size_megs)
            response = dialog.run()
            dialog.destroy()
            if response != gtk.RESPONSE_OK:
                return None

        try:
            if file_type == 'main':
                project = project or Project(self.config)
                project.data.read_main_file(path, encoding)
            elif file_type == 'translation':
                project.data.read_translation_file(path, encoding)
            return project

        except IOError, (errno, detail):
            dialog = ReadFileErrorDialog(parent, basename, detail)
            response = dialog.run()
            dialog.destroy()
            return None

        except UnicodeError:
            enc_disp = encodings_module.get_display_name(encoding)
            dialog = UnicodeDecodeErrorDialog(parent, basename, enc_disp)
            response = dialog.run()
            dialog.destroy()
            return None
            
        except UnknownFileFormatError:
            dialog = UnknownFileFormatErrorDialog(parent, basename)
            response = dialog.run()
            dialog.destroy()
            return None        
