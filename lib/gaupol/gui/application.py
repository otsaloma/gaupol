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


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.gui.delegates.celleditor import CellEditor
from gaupol.gui.delegates.durmanager import DURManager
from gaupol.gui.delegates.filecloser import FileCloser
from gaupol.gui.delegates.fileopener import FileOpener
from gaupol.gui.delegates.filesaver import FileSaver
from gaupol.gui.delegates.guibuilder import GUIBuilder
from gaupol.gui.delegates.guiupdater import GUIUpdater
from gaupol.gui.delegates.helper import Helper
from gaupol.gui.delegates.prefeditor import PreferenceEditor
from gaupol.gui.delegates.roweditor import RowEditor
from gaupol.gui.delegates.searcher import Searcher
from gaupol.gui.delegates.texteditor import TextEditor
from gaupol.gui.delegates.viewer import Viewer
from gaupol.gui.util.clipboard import Clipboard
from gaupol.gui.util.config import Config
from gaupol.gui.util import gui


class Application(object):

    """
    Gaupol main user interface.
    
    This is the main class for gaupol gui. All methods are outsourced to
    delegates.
    """
    
    def __init__(self):

        self.projects = []
        self.counter  = 0
        self.config   = Config()

        glade_xml  = gui.get_glade_xml('main-window.glade')
        get_widget = glade_xml.get_widget

        # Widgets from the Glade XML file.
        self.window            = get_widget('window')
        self.notebook          = get_widget('notebook')
        self.message_statusbar = get_widget('message_statusbar')
        self.text_statusbar    = get_widget('text_statusbar')
        self.tran_statusbar    = get_widget('translation_statusbar')

        # Widgets to be manually created.
        self.framerate_combo_box = None
        self.open_button         = None
        self.redo_button         = None
        self.undo_button         = None

        # UIManager and merge IDs.
        self.uim                 = None
        self.documents_uim_id    = None
        self.recent_files_uim_id = None
        self.undo_redo_uim_id    = None

        # Tooltips, which are enabled when a document is open.
        self.tooltips = gtk.Tooltips()

        # Internal clipboard.
        self.clipboard = Clipboard()

        # GObject timeout tag for message statusbar.
        self.message_tag = None

        self._delegations = None
        self._assign_delegations()
        
        self.config.read_from_file()
        self.build_gui()
        self.window.show()
        
    def _assign_delegations(self):
        """Map method names to Delegate objects."""
        
        cell_editor       = CellEditor(self)
        dur_manager       = DURManager(self)
        file_closer       = FileCloser(self)
        file_opener       = FileOpener(self)
        file_saver        = FileSaver(self)
        gui_builder       = GUIBuilder(self)
        gui_updater       = GUIUpdater(self)
        helper            = Helper(self)
        preference_editor = PreferenceEditor(self)
        row_editor        = RowEditor(self)
        searcher          = Searcher(self)
        text_editor       = TextEditor(self)
        viewer            = Viewer(self)

        self._delegations = {
            'add_to_recent_files'                    : file_opener,
            'build_gui'                              : gui_builder,
            'do_action'                              : dur_manager,
            'insert_subtitles'                       : row_editor,
            'on_about_activated'                     : helper,
            'on_check_latest_version_activated'      : helper,
            'on_clear_activated'                     : text_editor,
            'on_close_activated'                     : file_closer,
            'on_close_all_activated'                 : file_closer,
            'on_copy_activated'                      : text_editor,
            'on_cut_activated'                       : text_editor,
            'on_dialog_lines_activated'              : text_editor,
            'on_document_toggled'                    : gui_updater,
            'on_edit_cell_activated'                 : cell_editor,
            'on_edit_mode_toggled'                   : viewer,
            'on_files_dropped'                       : file_opener,
            'on_framerate_changed'                   : viewer,
            'on_framerate_toggled'                   : viewer,
            'on_import_translation_activated'        : file_opener,
            'on_insert_subtitles_activated'          : row_editor,
            'on_invert_selection_activated'          : row_editor,
            'on_italic_activated'                    : text_editor,
            'on_jump_to_subtitle_activated'          : searcher,
            'on_lower_activated'                     : text_editor,
            'on_new_activated'                       : file_opener,
            'on_next_activated'                      : gui_updater,
            'on_notebook_page_switched'              : gui_updater,
            'on_notebook_tab_close_button_clicked'   : file_closer,
            'on_open_activated'                      : file_opener,
            'on_paste_activated'                     : text_editor,
            'on_preferences_activated'               : preference_editor,
            'on_previous_activated'                  : gui_updater,
            'on_quit_activated'                      : file_closer,
            'on_recent_file_activated'               : file_opener,
            'on_redo_activated'                      : dur_manager,
            'on_redo_item_activated'                 : dur_manager,
            'on_remove_subtitles_activated'          : row_editor,
            'on_report_a_bug_activated'              : helper,
            'on_revert_activated'                    : file_opener,
            'on_save_a_copy_activated'               : file_saver,
            'on_save_a_copy_of_translation_activated': file_saver,
            'on_save_activated'                      : file_saver,
            'on_save_all_activated'                  : file_saver,
            'on_save_as_activated'                   : file_saver,
            'on_save_translation_activated'          : file_saver,
            'on_save_translation_as_activated'       : file_saver,
            'on_select_all_activated'                : row_editor,
            'on_sentence_activated'                  : text_editor,
            'on_statusbar_toggled'                   : viewer,
            'on_support_activated'                   : helper,
            'on_title_activated'                     : text_editor,
            'on_toolbar_toggled'                     : viewer,
            'on_tree_view_button_press_event'        : gui_updater,
            'on_tree_view_cell_edited'               : cell_editor,
            'on_tree_view_cell_editing_started'      : cell_editor,
            'on_tree_view_column_toggled'            : viewer,
            'on_tree_view_cursor_moved'              : gui_updater,
            'on_tree_view_headers_clicked'           : viewer,
            'on_tree_view_selection_changed'         : gui_updater,
            'on_undo_activated'                      : dur_manager,
            'on_undo_item_activated'                 : dur_manager,
            'on_unselect_all_activated'              : row_editor,
            'on_upper_activated'                     : text_editor,
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
