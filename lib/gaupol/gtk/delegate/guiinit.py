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


"""Initialization of application window."""


from gettext import gettext as _
import os

import gobject
import gtk
import pango

from gaupol.base.paths   import DATA_DIR
from gaupol.gtk          import cons
from gaupol.gtk.delegate import Delegate, UIMActions
from gaupol.gtk.output   import OutputWindow
from gaupol.gtk.util     import config, gtklib


_GAUPOL_ICON = os.path.join(DATA_DIR, 'icons', 'gaupol.png' )
_MENUBAR_XML = os.path.join(DATA_DIR, 'ui'   , 'menubar.xml')
_POPUPS_XML  = os.path.join(DATA_DIR, 'ui'   , 'popups.xml' )
_TOOLBAR_XML = os.path.join(DATA_DIR, 'ui'   , 'toolbar.xml')


class GUIInitDelegate(Delegate):

    """Initialization of application window."""

    def _init_main_toolbar(self):
        """Initialize main toolbar."""

        self._init_toolbuttons()
        toolbar = self._uim.get_widget('/ui/main_toolbar')
        toolbar.set_show_arrow(True)
        toolbar.insert(self._open_button, 0)
        toolbar.insert(gtk.SeparatorToolItem(), 2)
        toolbar.insert(self._undo_button, 3)
        toolbar.insert(self._redo_button, 4)

    def _init_notebook(self):
        """Initialize notebook."""

        self._notebook = gtk.Notebook()
        self._notebook.set_scrollable(True)
        self._notebook.popup_enable()
        self._notebook.drag_dest_set(
            gtk.DEST_DEFAULT_ALL, [('text/uri-list', 0, 0)],
            gtk.gdk.ACTION_DEFAULT|gtk.gdk.ACTION_COPY|gtk.gdk.ACTION_MOVE| \
            gtk.gdk.ACTION_LINK|gtk.gdk.ACTION_PRIVATE|gtk.gdk.ACTION_ASK
        )

        gtklib.connect(self, '_notebook', 'switch-page'       , False)
        gtklib.connect(self, '_notebook', 'drag-data-received', False)

    def _init_output_window(self):
        """Initialize output window."""

        self._output_window = OutputWindow()
        if config.output_window.show:
            self._output_window.show()

        gtklib.connect(self, '_output_window', 'closed', False)

    def _init_statusbar(self):
        """Initialize statusbar."""

        self._msg_statusbar  = gtk.Statusbar()
        self._main_statusbar = gtk.Statusbar()
        self._tran_statusbar = gtk.Statusbar()
        self._main_statusbar.set_size_request(60, -1)
        self._tran_statusbar.set_size_request(60, -1)

        msg_event_box  = gtk.EventBox()
        main_event_box = gtk.EventBox()
        tran_event_box = gtk.EventBox()
        msg_event_box.add(self._msg_statusbar)
        main_event_box.add(self._main_statusbar)
        tran_event_box.add(self._tran_statusbar)

        self._tooltips.set_tip(
            main_event_box,
            _('Amount of characters in the main text of the selected '
              'subtitle')
        )
        self._tooltips.set_tip(
            tran_event_box,
            _('Amount of characters in the translation text of the selected '
              'subtitle')
        )

        hbox = gtk.HBox()
        hbox.pack_start(msg_event_box , True , True , 0)
        hbox.pack_start(main_event_box, False, False, 0)
        hbox.pack_start(tran_event_box, False, False, 0)

        return hbox

    def _init_toolbuttons(self):
        """Initialize toolbar buttons."""

        self._open_button = gtk.MenuToolButton(gtk.STOCK_OPEN)
        self._open_button.set_label(_('Open'))
        self._open_button.set_is_important(True)
        self._open_button.set_menu(gtk.Menu())
        self._open_button.set_tooltip(
            self._static_tooltips, _('Open main files'))
        self._open_button.set_arrow_tooltip(
            self._static_tooltips, _('Open a recently used main file'))

        gtklib.connect(self, '_open_button', 'clicked'  , False)
        gtklib.connect(self, '_open_button', 'show-menu', False)

        self._undo_button = gtk.MenuToolButton(gtk.STOCK_UNDO)
        self._undo_button.set_label(_('Undo'))
        self._undo_button.set_is_important(True)
        self._undo_button.set_menu(gtk.Menu())
        self._undo_button.set_tooltip(
            self._tooltips, _('Undo the last action'))
        self._undo_button.set_arrow_tooltip(
            self._tooltips, _('Undo several actions'))

        gtklib.connect(self, '_undo_button', 'clicked'  , False)
        gtklib.connect(self, '_undo_button', 'show-menu', False)

        self._redo_button = gtk.MenuToolButton(gtk.STOCK_REDO)
        self._redo_button.set_label(_('Redo'))
        self._redo_button.set_is_important(False)
        self._redo_button.set_menu(gtk.Menu())
        self._redo_button.set_tooltip(
            self._tooltips, _('Redo the last undone action'))
        self._redo_button.set_arrow_tooltip(
            self._tooltips, _('Redo several undone actions'))

        gtklib.connect(self, '_redo_button', 'clicked'  , False)
        gtklib.connect(self, '_redo_button', 'show-menu', False)

    def _init_ui_manager(self):
        """Initialize UI manager."""

        self._uim = gtk.UIManager()

        menu_items = [
            ('show_file_menu'    , None, _('_File')    ),
            ('show_edit_menu'    , None, _('_Edit')    ),
            ('show_view_menu'    , None, _('_View')    ),
            ('show_format_menu'  , None, _('F_ormat')  ),
            ('show_search_menu'  , None, _('_Search')  ),
            ('show_tools_menu'   , None, _('_Tools')   ),
            ('show_projects_menu', None, _('_Projects')),
            ('show_help_menu'    , None, _('_Help')    ),
        ]

        action_group = gtk.ActionGroup('main')
        action_group.add_actions(menu_items, None)
        for cls in UIMActions.classes:
            if cls.menu_item is not None:
                action_group.add_actions([cls.menu_item], None)
            if cls.action_item is not None:
                item = list(cls.action_item)
                item[5] = getattr(self, item[5])
                action_group.add_actions([tuple(item)], None)
            if cls.toggle_item is not None:
                item = list(cls.toggle_item)
                item[5] = getattr(self, item[5])
                item[6] = cls.get_toggle_value()
                action_group.add_toggle_actions([tuple(item)], None)
            if cls.radio_items is not None:
                action_group.add_radio_actions(
                    cls.radio_items[0],
                    cls.get_radio_index(),
                    getattr(self, cls.radio_items[2])
                )

        self._uim.insert_action_group(action_group ,  0)
        self._uim.insert_action_group(gtk.ActionGroup('recent') , -1)
        self._uim.insert_action_group(gtk.ActionGroup('projects'), -1)

        self._uim.add_ui_from_file(_MENUBAR_XML)
        self._uim.add_ui_from_file(_TOOLBAR_XML)
        self._uim.add_ui_from_file(_POPUPS_XML)

        action = self._uim.get_action('/ui/menubar/file')
        action.connect('activate', self.on_show_file_menu_activate)
        action = self._uim.get_action('/ui/menubar/projects')
        action.connect('activate', self.on_show_projects_menu_activate)

        self._window.add_accel_group(self._uim.get_accel_group())

    def _init_video_toolbar(self):
        """Initialize video toolbar."""

        toolbar = gtk.Toolbar()
        toolbar.set_show_arrow(True)

        label = gtk.Label(_('Video file:'))
        tool_item = gtk.ToolItem()
        tool_item.set_border_width(4)
        tool_item.add(label)
        toolbar.insert(tool_item, -1)

        hbox = gtk.HBox(False, 4)
        image = gtk.image_new_from_stock(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
        hbox.pack_start(image, False, False)
        self._video_label = gtk.Label()
        self._video_label.props.xalign = 0
        self._video_label.set_ellipsize(pango.ELLIPSIZE_MIDDLE)
        hbox.pack_start(self._video_label, True, True)
        hbox.pack_start(gtk.VSeparator(), False, False)
        image = gtk.image_new_from_stock(gtk.STOCK_OPEN, gtk.ICON_SIZE_MENU)
        hbox.pack_start(image, False, False)

        self._video_button = gtk.Button()
        self._video_button.add(hbox)
        self._video_button.drag_dest_set(
            gtk.DEST_DEFAULT_ALL, [('text/uri-list', 0, 0)],
            gtk.gdk.ACTION_DEFAULT|gtk.gdk.ACTION_COPY|gtk.gdk.ACTION_MOVE| \
            gtk.gdk.ACTION_LINK|gtk.gdk.ACTION_PRIVATE|gtk.gdk.ACTION_ASK
        )
        gtklib.connect(self, '_video_button', 'clicked'           , False)
        gtklib.connect(self, '_video_button', 'drag-data-received', False)

        tool_item = gtk.ToolItem()
        tool_item.set_border_width(4)
        tool_item.set_expand(True)
        tool_item.add(self._video_button)
        toolbar.insert(tool_item, -1)

        label = gtk.Label(_('Framerate:'))
        tool_item = gtk.ToolItem()
        tool_item.set_border_width(4)
        tool_item.add(label)
        toolbar.insert(tool_item, -1)

        self._framerate_combo = gtk.combo_box_new_text()
        for i in range(len(cons.Framerate.display_names)):
            self._framerate_combo.insert_text(
                i, cons.Framerate.display_names[i])
        self._framerate_combo.set_active(config.editor.framerate)
        gtklib.connect(self, '_framerate_combo', 'changed', False)

        tool_item = gtk.ToolItem()
        tool_item.set_border_width(4)
        tool_item.add(self._framerate_combo)
        toolbar.insert(tool_item, -1)

        return toolbar

    def _init_window(self):
        """Initialize window."""

        self._window = gtk.Window()
        self._window.resize(*config.application_window.size)
        self._window.move(*config.application_window.position)
        if config.application_window.maximized:
            self._window.maximize()

        icon_theme = gtk.icon_theme_get_default()
        if icon_theme.has_icon('gaupol'):
            self._window.set_icon_name('gaupol')
            gtk.window_set_default_icon_name('gaupol')
        if self._window.get_icon is None:
            try:
                gtk.window_set_default_icon_from_file(_GAUPOL_ICON)
            except gobject.GError:
                print 'Failed to load icon file "%s".' % _GAUPOL_ICON

        gtklib.connect(self, '_window', 'delete-event'      , False)
        gtklib.connect(self, '_window', 'window-state-event', False)

    def init_gui(self):
        """Initialize application window."""

        self._init_window()
        self._init_ui_manager()
        self._init_main_toolbar()
        self._init_notebook()
        video_toolbar = self._init_video_toolbar()
        statusbar = self._init_statusbar()
        self._init_output_window()

        menubar = self._uim.get_widget('/ui/menubar')
        main_toolbar = self._uim.get_widget('/ui/main_toolbar')

        vbox = gtk.VBox()
        self._window.add(vbox)
        vbox.pack_start(menubar       , False, False, 0)
        vbox.pack_start(main_toolbar  , False, False, 0)
        vbox.pack_start(self._notebook, True , True,  0)
        vbox.pack_start(video_toolbar , False, False, 0)
        vbox.pack_start(statusbar     , False, False, 0)

        vbox.show_all()
        if not config.application_window.show_main_toolbar:
            main_toolbar.hide()
        if not config.application_window.show_video_toolbar:
            video_toolbar.hide()
        if not config.application_window.show_statusbar:
            statusbar.hide()

        self.set_menu_notify_events('main')
        self.set_sensitivities()
        self._notebook.grab_focus()
        self._window.show()
