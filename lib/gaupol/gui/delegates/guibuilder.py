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


"""Building and preparing the application main window."""


import logging
import os

try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk

from gaupol.constants import FRAMERATE, MODE
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.util import gui
from gaupol.paths import UI_DIR, ICON_DIR


MENUBAR_XML_PATH = os.path.join(UI_DIR  , 'menubar.xml')
TOOLBAR_XML_PATH = os.path.join(UI_DIR  , 'toolbar.xml')
POPUPS_XML_PATH  = os.path.join(UI_DIR  , 'popups.xml' )
GAUPOL_ICON_PATH = os.path.join(ICON_DIR, 'gaupol.png' )


logger = logging.getLogger()


class GUIBuilder(Delegate):

    """Building and preparing the application main window."""

    def _build_framerate_combo_box(self):
        """Build the framerate ComboBox in the toolbar."""
        
        self.framerate_combo_box = gtk.combo_box_new_text()

        # Add entries.
        for i in range(len(FRAMERATE.NAMES)):
            entry = _('%s fps') % FRAMERATE.NAMES[i]
            self.framerate_combo_box.insert_text(i, entry)

        # Set active framerate.
        framerate_name = self.config.get('editor', 'framerate')
        framerate = FRAMERATE.NAMES.index(framerate_name)
        self.framerate_combo_box.set_active(framerate)
        
        self.framerate_combo_box.connect('changed', self.on_framerate_changed)

        # Put framerate ComboBox to an event box and enable tooltip.
        event_box = gtk.EventBox()
        event_box.add(self.framerate_combo_box)
        self.tooltips.set_tip(event_box, _('Framerate'))

        # Create a tool item for the framerate combo box.
        tool_item = gtk.ToolItem()
        tool_item.set_border_width(4)
        tool_item.add(event_box)

         # Add tool item to toolbar.
        toolbar = self.uim.get_widget('/ui/toolbar')
        toolbar.insert(gtk.SeparatorToolItem(), -1)
        toolbar.insert(tool_item, -1)

    def build_gui(self):
        """Build and prepare the entire GUI."""
    
        self._build_window()
        self._build_menubar_and_toolbar()
        self._build_notebook()
        self._build_statusbar()

        self.set_menu_notify_events('main')
        self.set_sensitivities()

        self.notebook.grab_focus()

    def _build_menubar_and_toolbar(self):
        """Build the menubar and the toolbar."""

        self._build_ui_manager()
        
        # Pack menubar and toolbar.
        menubar = self.uim.get_widget('/ui/menubar')
        toolbar = self.uim.get_widget('/ui/toolbar')
        vbox = self.window.get_child()
        vbox.pack_start(menubar, False, False, 0)
        vbox.pack_start(toolbar, False, False, 0)
        vbox.reorder_child(menubar, 0)
        vbox.reorder_child(toolbar, 1)

        self._build_open_button()
        self._build_undo_and_redo_buttons()
        self._build_framerate_combo_box()

        toolbar.show_all()

        if not self.config.getboolean('view', 'toolbar'):
            toolbar.hide()

    def _build_notebook(self):
        """Build the notebook."""

        # Glade refuses to create a notebook with 0 pages.
        self.notebook.remove_page(0)
        
        method = self.on_notebook_page_switched
        self.notebook.connect_after('switch-page', method)

        # Set drag-and-drop for file opening.
        self.notebook.drag_dest_set(
            gtk.DEST_DEFAULT_ALL, [('text/uri-list', 0, 0)],
            gtk.gdk.ACTION_DEFAULT|gtk.gdk.ACTION_COPY|gtk.gdk.ACTION_MOVE| \
            gtk.gdk.ACTION_LINK|gtk.gdk.ACTION_PRIVATE|gtk.gdk.ACTION_ASK
        )
        self.notebook.connect('drag-data-received', self.on_files_dropped)

    def _build_open_button(self):
        """Build the open button on the toolbar."""
        
        self.open_button = gtk.MenuToolButton(gtk.STOCK_OPEN)
        self.open_button.set_label(_('Open'))
        self.open_button.set_is_important(True)
        self.open_button.connect('clicked', self.on_open_activated)

        # Not self.tooltips, because the open button tooltip should always
        # be visible, whether or not a document is open.
        tooltips = gtk.Tooltips()
        
        tip = _('Open a subtitle file')
        self.open_button.set_tooltip(tooltips, tip)

        tip = _('Open a recently used subtitle file')
        self.open_button.set_arrow_tooltip(tooltips, tip)
        
        toolbar = self.uim.get_widget('/ui/toolbar')
        toolbar.insert(self.open_button, 0)

    def _build_statusbar(self):
        """Build the statusbar."""

        event_box = gui.get_event_box(self.text_statusbar)
        tip = _('Amount of characters in the text of the selected subtitle')
        self.tooltips.set_tip(event_box, tip)
        
        event_box = gui.get_event_box(self.tran_statusbar)
        tip = _('Amount of characters in the translation of the selected subtitle')
        self.tooltips.set_tip(event_box, tip)

        statusbar_hbox = gui.get_parent_widget(self.text_statusbar, gtk.HBox)

        if not self.config.getboolean('view', 'statusbar'):
            statusbar_hbox.hide()

    def _build_ui_manager(self):
        """Build menubar and toolbar actions usings UIManager."""

        self.uim = gtk.UIManager()

        menus = [
            # Name      , Stock-icon, Label
            ('file'     , None      , _('_File')     ),
            ('edit'     , None      , _('_Edit')     ),
            ('view'     , None      , _('_View')     ),
            ('columns'  , None      , _('_Columns')  ),
            ('framerate', None      , _('_Framerate')),
            ('format'   , None      , _('F_ormat')   ),
            ('case'     , None      , _('_Case')     ),
            ('search'   , None      , _('_Search')   ),
            ('documents', None      , _('_Documents')),
            ('help'     , None      , _('_Help')     ),
        ]

        action_items = [
            # Name,
            # Stock-icon,
            # Label,
            # Accelerator,
            # Tooltip,
            # Callback
            (    
                'new',
                gtk.STOCK_NEW,
                _('_New...'),
                '<control>N',
                _('Create a new subtitle document'),
                self.on_new_activated
            ), (
                'open',
                gtk.STOCK_OPEN,
                _('_Open...'),
                '<control>O',
                _('Open a subtitle file'),
                self.on_open_activated
            ), (
                'import_translation',
                None,
                _('_Import Translation...'),
                None,
                _('Import translations from a subtitle file'),
                self.on_import_translation_activated
            ), (
                'save',
                gtk.STOCK_SAVE,
                _('_Save'),
                '<control>S',
                _('Save the current subtitle file'),
                self.on_save_activated
            ), (
                'save_as',
                gtk.STOCK_SAVE_AS,
                _('Save _As...'),
                '<shift><control>S',
                _('Save the current subtitle file with a different name'),
                self.on_save_as_activated
            ), (
                'save_a_copy',
                None,
                _('Sa_ve A Copy...'),
                None,
                _('Save a copy of the current subtitle document.'),
                self.on_save_a_copy_activated
            ), (
                'save_translation',
                gtk.STOCK_SAVE,
                _('Sav_e Translation'),
                '',
                _('Save the current translation file'),
                self.on_save_translation_activated
            ), (
                'save_translation_as',
                gtk.STOCK_SAVE_AS,
                _('Save _Translation As...'),
                '',
                _('Save the current translation file with a different name'),
                self.on_save_translation_as_activated
            ), (
                'save_a_copy_of_translation',
                None,
                _('Save A Cop_y Of Translation...'),
                None,
                _('Save a copy of the current translation document'),
                self.on_save_a_copy_of_translation_activated
            ), (
                'revert',
                gtk.STOCK_REVERT_TO_SAVED,
                _('_Revert'),
                None,
                _('Revert to a saved version'),
                self.on_revert_activated
            ), (
                'close',
                gtk.STOCK_CLOSE,
                _('_Close'),
                '<control>W',
                _('Close the current subtitle file'),
                self.on_close_activated
            ), (
                'quit',
                gtk.STOCK_QUIT,
                _('_Quit'),
                '<control>Q',
                _('Quit Gaupol'),
                self.on_quit_activated
            ), (
                'undo',
                gtk.STOCK_UNDO,
                _('_Undo'),
                '<control>Z',
                _('Undo the last action'),
                self.on_undo_activated
            ), (
                'redo',
                gtk.STOCK_REDO,
                _('_Redo'),
                '<shift><control>Z',
                _('Redo the last undone action'),
                self.on_redo_activated
            ), (
                'edit_cell',
                gtk.STOCK_EDIT,
                _('_Edit'),
                'Return',
                _('Edit the focused cell'),
                self.on_edit_cell_activated
            ), (
                'cut',
                gtk.STOCK_CUT,
                _('Cu_t'),
                '<control>X',
                _('Cut the selected texts to clipboard'),
                self.on_cut_activated
            ), (
                'copy',
                gtk.STOCK_COPY,
                _('_Copy'),
                '<control>C',
                _('Copy the selected texts to clipboard'),
                self.on_copy_activated
            ), (
                'paste',
                gtk.STOCK_PASTE,
                _('_Paste'),
                '<control>V',
                _('Paste texts from clipboard'),
                self.on_paste_activated
            ), (
                'clear',
                gtk.STOCK_CLEAR,
                _('C_lear'),
                'Delete',
                _('Clear the selected texts'),
                self.on_clear_activated
            ), (
                'insert_subtitles',
                gtk.STOCK_ADD,
                _('_Insert Subtitles'),
                '<control>Insert',
                _('Insert blank subtitles'),
                self.on_insert_subtitles_activated
            ), (
                'remove_subtitles',
                gtk.STOCK_REMOVE,
                _('_Remove Subtitles'),
                '<control>Delete',
                _('Remove selected subtitles'),
                self.on_remove_subtitles_activated
            ), (
                'select_all',
                None,
                _('Select _All'),
                '<control>A',
                _('Select all subtitles'),
                self.on_select_all_activated
            ), (
                'unselect_all',
                None,
                _('Unse_lect All'),
                '<shift><control>A',
                _('Unselect all subtitles'),
                self.on_unselect_all_activated
            ), (
                'invert_selection',
                None,
                _('I_nvert Selection'),
                None,
                _('Invert the current selection'),
                self.on_invert_selection_activated
            ), (
                'preferences',
                gtk.STOCK_PREFERENCES,
                _('Pre_ferences'),
                None,
                _('Configure Gaupol'),
                self.on_preferences_activated
            ), (
                'dialog',
                None,
                _('_Dialog'),
                '<control>D',
                _('Toggle dialog lines on the selected texts'),
                self.on_dialog_activated
            ), (
                'italic',
                gtk.STOCK_ITALIC,
                _('_Italic'),
                '<control>I',
                _('Toggle the italicization of the selected texts'),
                self.on_italic_activated
            ), (
                'title',
                None,
                _('_Title'),
                '<control>L',
                _('Change the selected texts to Title Case'),
                self.on_title_activated
            ), (
                'sentence',
                None,
                _('_Sentence'),
                '<control>E',
                _('Change the selected texts to Sentence case'),
                self.on_sentence_activated
            ), (
                'upper',
                None,
                _('_Upper'),
                '<control>U',
                _('Change the selected texts to UPPER CASE'),
                self.on_upper_activated
            ), (
                'lower',
                None,
                _('_Lower'),
                '<control>R',
                _('Change the selected texts to lower case'),
                self.on_lower_activated
            ), (
                'jump_to_subtitle',
                gtk.STOCK_JUMP_TO,
                _('_Jump To Subtitle'),
                '<control>J',
                _('Jump to a specific subtitle'),
                self.on_jump_to_subtitle_activated
            ), (
                'save_all',
                gtk.STOCK_SAVE,
                _('_Save All'),
                '<shift><control>L',
                _('Save all open documents'),
                self.on_save_all_activated
            ), (
                'close_all',
                gtk.STOCK_CLOSE,
                _('_Close All'),
                '<shift><control>W',
                _('Close all open documents'),
                self.on_close_all_activated
            ), (
                'previous',
                None,
                _('_Previous'),
                '<control>Page_Up',
                _('Activate document in the previous tab'),
                self.on_previous_activated
            ), (
                'next',
                None,
                _('_Next'),
                '<control>Page_Down',
                _('Activate document in the next tab'),
                self.on_next_activated
            ), (
                'support',
                None,
                _('_Support'),
                None,
                _('Submit a support request'),
                self.on_support_activated
            ), (
                'report_a_bug',
                None,
                _('_Report A Bug'),
                None,
                _('Submit a bug report'),
                self.on_report_a_bug_activated
            ), (
                'check_latest_version',
                None,
                _('_Check Latest Version'),
                None,
                _('Check if you have the latest version'),
                self.on_check_latest_version_activated
            ), (
                'about',
                gtk.STOCK_ABOUT,
                _('_About'),
                None,
                _('Information about Gaupol'),
                self.on_about_activated
            )
        ]
        
        columns = self.config.getlist('view', 'columns')

        toggle_items = [
            # Name,
            # Stock-icon,
            # Label,
            # Accelerator,
            # Tooltip,
            # Callback
            # Value
            (
                'toolbar',
                None,
                _('_Toolbar'),
                None,
                _('Change the visibility of the toolbar'),
                self.on_toolbar_toggled,
                self.config.getboolean('view', 'toolbar')
            ), (
                'statusbar',
                None,
                _('_Statusbar'),
                None,
                _('Change the visibility of the statusbar'),
                self.on_statusbar_toggled,
                self.config.getboolean('view', 'statusbar')
            ), (
                'number',
                None,
                _('_No.'),
                None,
                _('Change the visibility of the "No." column'),
                self.on_tree_view_column_toggled,
                'number' in columns
            ), (
                'show',
                None,
                _('_Show'),
                None,
                _('Change the visibility of the "Show" column'),
                self.on_tree_view_column_toggled,
                'show' in columns
            ), (
                'hide',
                None,
                _('_Hide'),
                None,
                _('Change the visibility of the "Hide" column'),
                self.on_tree_view_column_toggled,
                'hide' in columns
            ), (
                'duration',
                None,
                _('_Duration'),
                None,
                _('Change the visibility of the "Duration" column'),
                self.on_tree_view_column_toggled,
                'duration' in columns
            ), (
                'text',
                None,
                _('_Text'),
                None,
                _('Change the visibility of the "Text" column'),
                self.on_tree_view_column_toggled,
                'text' in columns
            ), (
                'translation',
                None,
                _('T_ranslation'),
                None,
                _('Change the visibility of the "Translation" column'),
                self.on_tree_view_column_toggled,
                'translation' in columns
            )
        ]

        edit_mode_radio_items = [
            # Name,
            # Stock-Icon,
            # Label,
            # Accelerator,
            # Tooltip,
            # Index
            (
                'times',
                None,
                _('T_imes') ,
                '<control>T',
                _('Show timings as times'),
                0
            ), (
                'frames',
                None,
                _('F_rames'),
                '<control>F',
                _('Show timings as frames'),
                1
            )
        ]

        framerate_radio_items = [
            (
                '23.976',
                None,
                _('2_3.976 fps'),
                None,
                _('Calculate unnative timings with framerate 23.976 fps'),
                0
            ), (
                '25',
                None,
                _('2_5 fps'),
                None,
                _('Calculate unnative timings with framerate 25 fps'),
                1
            ), (
                '29.97',
                None,
                _('2_9.97 fps'),
                None,
                _('Calculate unnative timings with framerate 29.97 fps'),
                2
            )
        ]

        # Get edit mode.
        edit_mode_name = self.config.get('editor', 'edit_mode')
        edit_mode = MODE.NAMES.index(edit_mode_name)

        # Get framerate.
        framerate_name = self.config.get('editor', 'framerate')
        framerate = FRAMERATE.NAMES.index(framerate_name)

        # Add actions to ActionGroup.
        action_group = gtk.ActionGroup('main')
        action_group.add_actions(menus, None)
        action_group.add_actions(action_items, None)
        action_group.add_toggle_actions(toggle_items, None)

        action_group.add_radio_actions(
            edit_mode_radio_items, edit_mode, self.on_edit_mode_toggled
        )
        action_group.add_radio_actions(
            framerate_radio_items, framerate, self.on_framerate_toggled,
        )
        
        # Add ActionGroups to UIManager.
        self.uim.insert_action_group(action_group                ,  0)
        self.uim.insert_action_group(gtk.ActionGroup('recent')   , -1)
        self.uim.insert_action_group(gtk.ActionGroup('documents'), -1)
        self.uim.insert_action_group(gtk.ActionGroup('undo_redo'), -1)
        
        # Add menubar, toolbar and popup entries.
        self.uim.add_ui_from_file(MENUBAR_XML_PATH)
        self.uim.add_ui_from_file(TOOLBAR_XML_PATH)
        self.uim.add_ui_from_file(POPUPS_XML_PATH )
        
        self.window.add_accel_group(self.uim.get_accel_group())

    def _build_undo_and_redo_buttons(self):
        """Build the undo and redo buttons on the toolbar."""
        
        self.undo_button = gtk.MenuToolButton(gtk.STOCK_UNDO)
        self.undo_button.set_label(_('Undo'))
        self.undo_button.set_is_important(True)
        self.undo_button.connect('clicked', self.on_undo_activated)
        
        tip = _('Undo the last action')
        self.undo_button.set_tooltip(self.tooltips, tip)

        tip = _('Undo several actions')
        self.undo_button.set_arrow_tooltip(self.tooltips, tip)

        self.redo_button = gtk.MenuToolButton(gtk.STOCK_REDO)
        self.redo_button.set_label(_('Redo'))
        self.redo_button.set_is_important(False)
        self.redo_button.connect('clicked', self.on_redo_activated)
        
        tip = _('Redo the last undone action')
        self.redo_button.set_tooltip(self.tooltips, tip)

        tip = _('Redo several undone actions')
        self.redo_button.set_arrow_tooltip(self.tooltips, tip)
        
        # Pack buttons.
        toolbar = self.uim.get_widget('/ui/toolbar')
        toolbar.insert(gtk.SeparatorToolItem(), 2)
        toolbar.insert(self.undo_button, 3)
        toolbar.insert(self.redo_button, 4)

    def _build_window(self):
        """Build the window."""

        width, height = self.config.getlistint('main_window', 'size')
        self.window.resize(width, height)
        
        x_pos, y_pos = self.config.getlistint('main_window', 'position')
        self.window.move(x_pos, y_pos )

        if self.config.getboolean('main_window', 'maximized'):
            self.window.maximize()
        
        try:
            gtk.window_set_default_icon_from_file(GAUPOL_ICON_PATH)
        except gobject.GError:
            logger.error('Failed to load icon file "%s".' % GAUPOL_ICON_PATH)

        self.window.connect('delete_event'      , self.on_window_delete_event)
        self.window.connect('window_state_event', self.on_window_state_event )
