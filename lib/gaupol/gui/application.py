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

from gaupol.gui.delegates.durmanager import DURManager
from gaupol.gui.delegates.filecloser import FileCloser
from gaupol.gui.delegates.fileopener import FileOpener
from gaupol.gui.delegates.filesaver import FileSaver
from gaupol.gui.delegates.formatter import Formatter
from gaupol.gui.delegates.guibuilder import GUIBuilder
from gaupol.gui.delegates.guiupdater import GUIUpdater
from gaupol.gui.delegates.helper import Helper
from gaupol.gui.delegates.maneditor import ManualEditor
from gaupol.gui.delegates.searcher import Searcher
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

        # Widgets from the Glade XML file.
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
        self.redo_button = None
        self.undo_button = None

        # UIManager and merge IDs.
        self.uim              = None
        self.documents_uim_id = None
        self.recent_uim_id    = None
        self.undo_redo_uim_id = None

        # Tooltips.
        self.ttips_always = gtk.Tooltips()
        self.ttips_open   = gtk.Tooltips()

        # GObject timeout tag for message statusbar timed-out vanishings.
        self.msg_stbar_gobj_tag = None

        self.config.read_from_file()
        self._assign_delegations()

        self.build_gui()
        self.window.show()
        
    def _assign_delegations(self):
        """Map method names to Delegate objects."""
        
        dur_manager = DURManager(self)
        file_closer = FileCloser(self)
        file_opener = FileOpener(self)
        file_saver  = FileSaver(self)
        formatter   = Formatter(self)
        gui_builder = GUIBuilder(self)
        gui_updater = GUIUpdater(self)
        helper      = Helper(self)
        man_editor  = ManualEditor(self)
        searcher    = Searcher(self)
        viewer      = Viewer(self)

        self._delegations = {
            'add_to_recent_files'                    : file_opener,
            'build_gui'                              : gui_builder,
            'do_action'                              : dur_manager,
            'on_about_activated'                     : helper,
            'on_close_activated'                     : file_closer,
            'on_close_all_activated'                 : file_closer,
            'on_dialog_lines_activated'              : formatter,
            'on_document_toggled'                    : gui_updater,
            'on_edit_mode_toggled'                   : viewer,
            'on_files_dropped'                       : file_opener,
            'on_framerate_changed'                   : viewer,
            'on_framerate_toggled'                   : viewer,
            'on_go_to_subtitle_activated'            : searcher,
            'on_import_translation_activated'        : file_opener,
            'on_invert_case_activated'               : formatter,
            'on_italic_style_activated'              : formatter,
            'on_lower_case_activated'                : formatter,
            'on_new_activated'                       : file_opener,
            'on_next_activated'                      : gui_updater,
            'on_notebook_page_switched'              : gui_updater,
            'on_notebook_tab_close_button_clicked'   : file_closer,
            'on_open_activated'                      : file_opener,
            'on_previous_activated'                  : gui_updater,
            'on_quit_activated'                      : file_closer,
            'on_recent_file_activated'               : file_opener,
            'on_redo_activated'                      : dur_manager,
            'on_redo_button_clicked'                 : dur_manager,
            'on_redo_item_activated'                 : dur_manager,
            'on_revert_activated'                    : file_opener,
            'on_save_a_copy_activated'               : file_saver,
            'on_save_a_copy_of_translation_activated': file_saver,
            'on_save_activated'                      : file_saver,
            'on_save_all_activated'                  : file_saver,
            'on_save_as_activated'                   : file_saver,
            'on_save_translation_activated'          : file_saver,
            'on_save_translation_as_activated'       : file_saver,
            'on_sentence_case_activated'             : formatter,
            'on_statusbar_toggled'                   : viewer,
            'on_title_case_activated'                : formatter,
            'on_toolbar_toggled'                     : viewer,
            'on_tree_view_cell_edited'               : man_editor,
            'on_tree_view_cell_editing_started'      : man_editor,
            'on_tree_view_column_toggled'            : viewer,
            'on_tree_view_cursor_moved'              : gui_updater,
            'on_tree_view_headers_clicked'           : viewer,
            'on_tree_view_selection_changed'         : gui_updater,
            'on_undo_activated'                      : dur_manager,
            'on_undo_button_clicked'                 : dur_manager,
            'on_undo_item_activated'                 : dur_manager,
            'on_upper_case_activated'                : formatter,
            'on_window_delete_event'                 : file_closer,
            'on_window_state_event'                  : gui_updater,
            'open_main_files'                        : file_opener,
            'redo_action'                            : dur_manager,
            'save_main_document_as'                  : file_saver,
            'save_main_document'                     : file_saver,
            'save_translation_document_as'           : file_saver,
            'save_translation_document'              : file_saver,
            'set_menu_notify_events'                 : gui_updater,
            'set_sensitivities'                      : gui_updater,
            'set_status_message'                     : gui_updater,
            'undo_action'                            : dur_manager,
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
