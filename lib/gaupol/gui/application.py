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


"""Gaupol main user interface."""


import logging
import os
import sys

try:
    from psyco.classes import *
except ImportError:
    pass

import gtk
import gtk.glade

from gaupol.gui.delegates.filecloser import FileCloser
from gaupol.gui.delegates.fileopener import FileOpener
from gaupol.gui.delegates.filesaver import FileSaver
from gaupol.gui.delegates.guibuilder import GUIBuilder
from gaupol.gui.delegates.guiupdater import GUIUpdater
from gaupol.gui.delegates.helper import Helper
from gaupol.gui.delegates.viewer import Viewer
from gaupol.gui.util.config import Config
from gaupol.paths import GLADE_DIR


logger = logging.getLogger()


GLADE_XML_PATH   = os.path.join(GLADE_DIR , 'main-window.glade')


class Application(object):

    """
    Gaupol main user interface.
    
    This is the master class for gaupol gui. All methods are outsourced to
    delegates.
    """
    
    def __init__(self):

        try:
            glade_xml = gtk.glade.XML(GLADE_XML_PATH)
        except RuntimeError:
            logger.critical('Failed to import Glade XML file "%s".' \
                            % GLADE_XML_PATH) 
            sys.exit()

        self.projects     = []
        self.counter      = 0
        self.config       = Config()
        self._delegations = None

        # Widgets from Glade XML file.
        self.main_vbox  = glade_xml.get_widget('main_vbox')
        self.msg_stbar  = glade_xml.get_widget('message_statusbar')
        self.notebook   = glade_xml.get_widget('notebook')
        self.orig_stbar = glade_xml.get_widget('original_text_statusbar')
        self.stbar_hbox = glade_xml.get_widget('statusbar_hbox')
        self.tran_stbar = glade_xml.get_widget('translation_text_statusbar')
        self.window     = glade_xml.get_widget('window')

        # Widgets to be manually created.
        self.fr_cmbox    = None
        self.open_button = None

        # UIManager and merge IDs.
        self.uim           = None
        self.recent_uim_id = None

        # Tooltips.
        self.ttips_always = gtk.Tooltips()
        self.ttips_open   = gtk.Tooltips()

        # GObject timeout tag for message statusbar timed-out vanishings.
        self.msg_stbar_gobj_tag = None

        self.config.read_from_file()
        self._assign_delegations()

        self.build_window()
        self.build_menubar_and_toolbar()
        self.build_notebook()
        self.build_statusbar()

        self.refresh_recent_file_menus()
        self.set_menu_tooltips('main')
        self.set_menu_tooltips('recent')

        self.set_sensitivities_and_visiblities()

        self.notebook.set_property('has-focus', True)

        self.window.show()
        
    def _assign_delegations(self):
        """Map method names to Delegate objects."""
        
        file_closer = FileCloser(self)
        file_opener = FileOpener(self)
        file_saver  = FileSaver(self)
        gui_builder = GUIBuilder(self)
        gui_updater = GUIUpdater(self)
        helper      = Helper(self)
        viewer      = Viewer(self)

        self._delegations = {
            'add_to_recent_files'                    : gui_updater,
            'build_menubar_and_toolbar'              : gui_builder,
            'build_notebook'                         : gui_builder,
            'build_statusbar'                        : gui_builder,
            'build_window'                           : gui_builder,
            'on_about_activated'                     : helper,
            'on_close_activated'                     : file_closer,
            'on_close_all_activated'                 : file_closer,
            'on_document_toggled'                    : gui_updater,
            'on_edit_mode_toggled'                   : viewer,
            'on_files_dropped'                       : file_opener,
            'on_framerate_changed'                   : viewer,
            'on_framerate_toggled'                   : viewer,
            'on_import_translation_activated'        : file_opener,
            'on_new_activated'                       : file_opener,
            'on_next_activated'                      : gui_updater,
            'on_notebook_page_switched'              : gui_updater,
            'on_notebook_tab_close_button_clicked'   : file_closer,
            'on_open_activated'                      : file_opener,
            'on_previous_activated'                  : gui_updater,
            'on_quit_activated'                      : file_closer,
            'on_recent_file_activated'               : file_opener,
            'on_report_a_bug_activated'              : helper,
            'on_revert_activated'                    : file_opener,
            'on_save_a_copy_activated'               : file_saver,
            'on_save_a_copy_of_translation_activated': file_saver,
            'on_save_activated'                      : file_saver,
            'on_save_all_activated'                  : file_saver,
            'on_save_as_activated'                   : file_saver,
            'on_save_translation_activated'          : file_saver,
            'on_save_translation_as_activated'       : file_saver,
            'on_statusbar_toggled'                   : viewer,
            'on_toolbar_toggled'                     : viewer,
            'on_tree_view_column_toggled'            : viewer,
            'on_tree_view_headers_clicked'           : viewer,
            'on_window_delete_event'                 : file_closer,
            'on_window_state_event'                  : gui_updater,
            'open_main_files'                        : file_opener,
            'refresh_documents_menu'                 : gui_updater,
            'refresh_recent_file_menus'              : gui_updater,
            'save_main_document_as'                  : file_saver,
            'save_main_document'                     : file_saver,
            'save_translation_document_as'           : file_saver,
            'save_translation_document'              : file_saver,
            'set_menu_tooltips'                      : gui_updater,
            'set_sensitivities_and_visiblities'      : gui_updater,
            'set_status_message'                     : gui_updater,
        }

    def __getattr__(self, name):
        """Delegate method calls to Delegate objects."""
        
        return self._delegations[name].__getattribute__(name)

    def get_current_project(self):
        """
        Get currently active project.
        
        Return Project or None.
        """
        try:
            return self.projects[self.notebook.get_current_page()]
        except IndexError:
            return None
