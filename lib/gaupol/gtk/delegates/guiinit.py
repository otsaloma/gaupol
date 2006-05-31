# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Initialization of the application window and all its widgets."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _
import logging
import os

import gobject
import gtk
import pango

from gaupol.gtk.cons import *
from gaupol.gtk.delegates import Delegate, UIMActions
from gaupol.gtk.paths     import UI_DIR, ICON_DIR
from gaupol.gtk.util      import config, gtklib
from gaupol.gtk.output    import OutputWindow


logger = logging.getLogger()

MENUBAR_XML_PATH = os.path.join(UI_DIR, 'menubar.xml')
TOOLBAR_XML_PATH = os.path.join(UI_DIR, 'toolbar.xml')
POPUPS_XML_PATH  = os.path.join(UI_DIR, 'popups.xml' )
GAUPOL_ICON      = os.path.join(ICON_DIR, 'gaupol.png')


class GUIInitDelegate(Delegate):

    """Initialization of the main window and all its widgets."""

    def init_gui(self):
        """Initialize the main window and all its widgets."""

        self._init_window()
        vbox = gtk.VBox()
        self.window.add(vbox)

        # Initialize widgets.
        main_toolbar = self._init_menubar_and_main_toolbar(vbox)
        self._init_notebook(vbox)
        video_toolbar = self._init_video_toolbar(vbox)
        statusbar_hbox = self._init_statusbar(vbox)

        # Show or hide widgets.
        vbox.show_all()
        if not config.app_window.show_main_toolbar:
            main_toolbar.hide()
        if not config.app_window.show_video_toolbar:
            video_toolbar.hide()
        if not config.app_window.show_statusbar:
            statusbar_hbox.hide()

        # Initialize output window.
        self.output_window = OutputWindow()
        if config.output_window.show:
            self.output_window.show()
        self.output_window.connect('close', self.on_output_window_close)

        self.set_menu_notify_events('main')
        self.set_sensitivities()
        self.notebook.grab_focus()
        self.window.show()

    def _init_menubar_and_main_toolbar(self, vbox):
        """
        Initialize the menubar and the main_toolbar.

        Return toolbar.
        """
        self._init_ui_manager()
        menubar = self.uim.get_widget('/ui/menubar')
        toolbar = self.uim.get_widget('/ui/main_toolbar')
        toolbar.set_show_arrow(True)

        # Pack menubar and toolbar.
        vbox.pack_start(menubar, False, False, 0)
        vbox.pack_start(toolbar, False, False, 0)

        # Initialize special toolbar buttons.
        self._init_open_button()
        self._init_undo_and_redo_buttons()

        return toolbar

    def _init_notebook(self, vbox):
        """Initialize the notebook."""

        self.notebook = gtk.Notebook()
        vbox.pack_start(self.notebook, True, True, 0)
        self.notebook.set_scrollable(True)
        self.notebook.popup_enable()

        method = self.on_notebook_page_switched
        self.notebook.connect_after('switch-page', method)

        # Set drag-and-drop for file opening.
        self.notebook.drag_dest_set(
            gtk.DEST_DEFAULT_ALL,
            [('text/uri-list', 0, 0)],
            gtk.gdk.ACTION_DEFAULT|gtk.gdk.ACTION_COPY|gtk.gdk.ACTION_MOVE| \
            gtk.gdk.ACTION_LINK|gtk.gdk.ACTION_PRIVATE|gtk.gdk.ACTION_ASK
        )
        method = self.on_notebook_drag_data_received
        self.notebook.connect('drag-data-received', method)

    def _init_open_button(self):
        """Initialize the open button in the toolbar."""

        self.open_button = gtk.MenuToolButton(gtk.STOCK_OPEN)
        self.open_button.set_label(_('Open'))
        self.open_button.set_is_important(True)
        self.open_button.set_menu(gtk.Menu())

        self.open_button.connect('clicked'  , self.on_open_main_file_activated)
        self.open_button.connect('show-menu', self.on_open_button_show_menu   )

        tip = _('Open main files')
        self.open_button.set_tooltip(self.static_tooltips, tip)
        tip = _('Open a recently used main file')
        self.open_button.set_arrow_tooltip(self.static_tooltips, tip)

        toolbar = self.uim.get_widget('/ui/main_toolbar')
        toolbar.insert(self.open_button, 0)

    def _init_statusbar(self, vbox):
        """
        Initialize the statusbar.

        Return statusbar horizontal box.
        """
        hbox = gtk.HBox()
        vbox.pack_start(hbox, False, False, 0)

        message_event_box = gtk.EventBox()
        text_event_box    = gtk.EventBox()
        tran_event_box    = gtk.EventBox()

        tip = _('Amount of characters in the main text of the selected '
                'subtitle')
        self.tooltips.set_tip(text_event_box, tip)
        tip = _('Amount of characters in the translation text of the selected '
                'subtitle')
        self.tooltips.set_tip(tran_event_box, tip)

        hbox.pack_start(message_event_box, True , True , 0)
        hbox.pack_start(text_event_box   , False, False, 0)
        hbox.pack_start(tran_event_box   , False, False, 0)

        self.msg_statusbar  = gtk.Statusbar()
        self.main_statusbar = gtk.Statusbar()
        self.tran_statusbar = gtk.Statusbar()

        # Set an initial width for statusbars.
        self.main_statusbar.set_size_request(100, -1)
        self.tran_statusbar.set_size_request(100, -1)

        message_event_box.add(self.msg_statusbar)
        text_event_box.add(self.main_statusbar)
        tran_event_box.add(self.tran_statusbar)

        return hbox

    def _init_ui_manager(self):
        """Initialize the UI manager for the menubar and the toolbar."""

        self.uim = gtk.UIManager()

        # Name, Stock-icon, Label, [Accelerator, Tooltip, Callback]
        menu_items = [
            (
                'show_file_menu',
                None,
                _('_File'),
                None,
                None,
                self.on_show_file_menu_activated
            ), (
                'show_edit_menu',
                None,
                _('_Edit')
            ), (
                'show_view_menu',
                None,
                _('_View')
            ), (
                'show_format_menu',
                None,
                _('F_ormat')
            ), (
                'show_search_menu',
                None,
                _('_Search')
            ), (
                'show_tools_menu',
                None,
                _('_Tools')
            ), (
                'show_projects_menu',
                None,
                _('_Projects'),
                None,
                None,
                self.on_show_projects_menu_activated
            ), (
                'show_help_menu',
                None,
                _('_Help')
            ),
        ]

        action_group = gtk.ActionGroup('main')
        action_group.add_actions(menu_items, None)

        # Loop through all actions and add their UI manager items after
        # evaluating methods from strings to method objects and converting
        # lists into tuples.
        for cls in UIMActions.classes:

            if cls.uim_menu_item is not None:
                action_group.add_actions([cls.uim_menu_item], None)

            if cls.uim_action_item is not None:
                item = list(cls.uim_action_item)
                item[5] = getattr(self, item[5])
                action_group.add_actions([tuple(item)], None)

            if cls.uim_toggle_item is not None:
                item = list(cls.uim_toggle_item)
                item[5] = getattr(self, item[5])
                item[6] = cls.get_uim_toggle_item_value()
                action_group.add_toggle_actions([tuple(item)], None)

            if cls.uim_radio_items is not None:
                action_group.add_radio_actions(
                    cls.uim_radio_items[0],
                    cls.get_uim_radio_items_index(),
                    getattr(self, cls.uim_radio_items[2])
                )

        self.uim.insert_action_group(action_group               ,  0)
        self.uim.insert_action_group(gtk.ActionGroup('recent')  , -1)
        self.uim.insert_action_group(gtk.ActionGroup('projects'), -1)

        self.uim.add_ui_from_file(MENUBAR_XML_PATH)
        self.uim.add_ui_from_file(TOOLBAR_XML_PATH)
        self.uim.add_ui_from_file(POPUPS_XML_PATH )

        self.window.add_accel_group(self.uim.get_accel_group())

    def _init_undo_and_redo_buttons(self):
        """Initialize the undo and redo buttons in the toolbar."""

        self.undo_button = gtk.MenuToolButton(gtk.STOCK_UNDO)
        self.undo_button.set_label(_('Undo'))
        self.undo_button.set_is_important(True)
        self.undo_button.set_menu(gtk.Menu())
        self.undo_button.connect('clicked'  , self.on_undo_action_activated)
        self.undo_button.connect('show-menu', self.on_undo_button_show_menu)

        tip = _('Undo the last action')
        self.undo_button.set_tooltip(self.tooltips, tip)
        tip = _('Undo several actions')
        self.undo_button.set_arrow_tooltip(self.tooltips, tip)

        self.redo_button = gtk.MenuToolButton(gtk.STOCK_REDO)
        self.redo_button.set_label(_('Redo'))
        self.redo_button.set_is_important(False)
        self.redo_button.set_menu(gtk.Menu())
        self.redo_button.connect('clicked'  , self.on_redo_action_activated)
        self.redo_button.connect('show-menu', self.on_redo_button_show_menu)

        tip = _('Redo the last undone action')
        self.redo_button.set_tooltip(self.tooltips, tip)
        tip = _('Redo several undone actions')
        self.redo_button.set_arrow_tooltip(self.tooltips, tip)

        toolbar = self.uim.get_widget('/ui/main_toolbar')
        toolbar.insert(gtk.SeparatorToolItem(), 2)
        toolbar.insert(self.undo_button, 3)
        toolbar.insert(self.redo_button, 4)

    def _init_video_toolbar(self, vbox):
        """
        Initialize the video toolbar.

        Return toolbar.
        """
        toolbar = gtk.Toolbar()
        toolbar.set_show_arrow(True)
        vbox.pack_start(toolbar, False, False, 0)

        # Add video file label to toolbar.
        label = gtk.Label(_('Video file:'))
        tool_item = gtk.ToolItem()
        tool_item.set_border_width(4)
        tool_item.add(label)
        toolbar.insert(tool_item, -1)

        # Create video file button.
        hbox=gtk.HBox(False, 4)
        self.video_button = gtk.Button()
        self.video_button.add(hbox)
        method = self.on_select_video_file_activated
        self.video_button.connect('clicked', method)

        # Pack video file button contents.
        image = gtk.image_new_from_stock(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
        hbox.pack_start(image, False, False)
        self.video_label = gtk.Label()
        self.video_label.props.xalign = 0
        self.video_label.set_ellipsize(pango.ELLIPSIZE_MIDDLE)
        hbox.pack_start(self.video_label, True, True)
        hbox.pack_start(gtk.VSeparator(), False, False)
        image = gtk.image_new_from_stock(gtk.STOCK_OPEN, gtk.ICON_SIZE_MENU)
        hbox.pack_start(image, False, False)

        # Set drag-and-drop for video file button.
        self.video_button.drag_dest_set(
            gtk.DEST_DEFAULT_ALL,
            [('text/uri-list', 0, 0)],
            gtk.gdk.ACTION_DEFAULT|gtk.gdk.ACTION_COPY|gtk.gdk.ACTION_MOVE| \
            gtk.gdk.ACTION_LINK|gtk.gdk.ACTION_PRIVATE|gtk.gdk.ACTION_ASK
        )
        method = self.on_video_file_button_drag_data_received
        self.video_button.connect('drag-data-received', method)

        # Add video file button to toolbar.
        tool_item = gtk.ToolItem()
        tool_item.set_border_width(4)
        tool_item.set_expand(True)
        tool_item.add(self.video_button)
        toolbar.insert(tool_item, -1)

        # Add video file label to toolbar.
        label = gtk.Label(_('Framerate:'))
        tool_item = gtk.ToolItem()
        tool_item.set_border_width(4)
        tool_item.add(label)
        toolbar.insert(tool_item, -1)

        # Create framerate combo box..
        self.framerate_combo = gtk.combo_box_new_text()
        for i in range(len(Framerate.display_names)):
            self.framerate_combo.insert_text(i, Framerate.display_names[i])
        self.framerate_combo.set_active(config.editor.framerate)
        self.framerate_combo.connect('changed', self.on_framerate_changed)

        # Add framerate combo box to toolbar.
        tool_item = gtk.ToolItem()
        tool_item.set_border_width(4)
        tool_item.add(self.framerate_combo)
        toolbar.insert(tool_item, -1)

        return toolbar

    def _init_window(self):
        """Initialize the main window."""

        self.window = gtk.Window()
        self.window.resize(*config.app_window.size)
        self.window.move(*config.app_window.position)
        if config.app_window.maximized:
            self.window.maximize()

        icon_theme = gtk.icon_theme_get_default()
        if icon_theme.has_icon('gaupol'):
            self.window.set_icon_name('gaupol')
            gtk.window_set_default_icon_name('gaupol')
        else:
            try:
                gtk.window_set_default_icon_from_file(GAUPOL_ICON)
            except gobject.GError:
                logger.error('Failed to load icon file "%s".' % GAUPOL_ICON)

        self.window.connect('delete-event'      , self.on_window_delete_event)
        self.window.connect('window-state-event', self.on_window_state_event )
