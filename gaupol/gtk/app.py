# Copyright (C) 2005-2007 Osmo Salomaa
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


"""GTK user interface controller.

Module variables:

    _ICON_FILE:   Path to non-themed fallback icon
    _UI_XML_FILE: Path to UI manager XML layout file
"""


import os
import types
from gettext import gettext as _

import gtk
import pango

from gaupol.base import Observable
from gaupol.clipboard import Clipboard
from gaupol.gtk import conf, cons, paths, util
from gaupol.gtk._actions import *
from gaupol.gtk._actions import ACTIONS
from gaupol.gtk._agents import *
from gaupol.gtk._agents import AGENTS
from gaupol.gtk.runner import Runner
from .output import OutputWindow


_ICON_FILE = os.path.join(paths.DATA_DIR, "icons", "gaupol.png")
_UI_XML_FILE = os.path.join(paths.DATA_DIR, "ui.xml")


class Application(Observable, Runner):

    """
    GTK user interface controller.

    Instance variables:

        _delegations:    Dictionary mapping method names to Agents
        clipboard        Application-wide Clipboard
        counter:         Integer for naming unsaved projects
        framerate_combo: gtk.ComboBox
        notebook:        gtk.Notebook
        open_button:     gtk.MenuToolButton
        output_window:   OutputWindow
        pages:           List of Pages
        recent_manager:  gtk.RecentManager
        redo_button:     gtk.MenuToolButton
        static_tooltips: gtk.Tooltips, enabled always
        statusbar:       gtk.Statusbar
        tooltips:        gtk.Tooltips, enabled if a project is open
        uim:             gtk.UIManager
        undo_button:     gtk.MenuToolButton
        video_button:    gtk.Button
        video_toolbar:   gtk.Toolbar
        window:          gtk.Window
        x_clipboard:     gtk.Clipboard (X clipboard)

    Signals:

        page-added (application, page)
        page-changed (application, page)
        page-closed (application, page)
        pages-reordered (application, page, number)

    See gaupol.gtk._agents for application methods provided by agents.
    """

    _signals = [
        "page-added",
        "page-changed",
        "page-closed",
        "pages-reordered",]

    def __getattr__(self, name):

        return self._delegations[name].__getattribute__(name)

    def __init__(self):

        # pylint: disable-msg=W0231
        Observable.__init__(self)

        self._delegations    = {}
        self.clipboard       = Clipboard()
        self.counter         = 0
        self.framerate_combo = None
        self.notebook        = None
        self.open_button     = None
        self.output_window   = None
        self.pages           = []
        self.recent_manager  = gtk.recent_manager_get_default()
        self.redo_button     = None
        self.static_tooltips = gtk.Tooltips()
        self.statusbar       = None
        self.tooltips        = gtk.Tooltips()
        self.uim             = None
        self.undo_button     = None
        self.video_button    = None
        self.video_toolbar   = None
        self.window          = None
        self.x_clipboard     = gtk.Clipboard()

        self._init_delegations()
        self._init_gui()

    def _init_delegations(self):
        """Initialize the delegate mappings."""

        for agent in (eval(x)(self) for x in AGENTS):
            for attr_name in (x for x in dir(agent) if not x.startswith("_")):
                attr = getattr(agent, attr_name)
                if type(attr) is types.MethodType:
                    if attr_name in self._delegations:
                        raise ValueError
                    self._delegations[attr_name] = agent

    def _init_framerate_combo(self):
        """Intialize the framerate combo box on the video toolbar."""

        self.framerate_combo = gtk.combo_box_new_text()
        for name in cons.FRAMERATE.display_names:
            self.framerate_combo.append_text(name)
        self.framerate_combo.set_active(conf.editor.framerate)
        util.connect(self, "framerate_combo", "changed")

        tool_item = gtk.ToolItem()
        tool_item.set_border_width(4)
        tool_item.add(self.framerate_combo)
        self.video_toolbar.insert(tool_item, -1)

    def _init_framerate_label(self):
        """Intialize the framerate label on the video toolbar."""

        label = gtk.Label(_("Framerate:"))
        tool_item = gtk.ToolItem()
        tool_item.set_border_width(4)
        tool_item.add(label)
        self.video_toolbar.insert(tool_item, -1)

    def _init_gui(self):
        """Initialize the user interface."""

        vbox = gtk.VBox()
        self._init_window()
        self._init_uim()
        self._init_menubar(vbox)
        self._init_main_toolbar(vbox)
        self._init_recent_menus()
        self._init_notebook(vbox)
        self._init_video_toolbar(vbox)
        self._init_statusbar(vbox)
        self._init_output_window()
        self.window.add(vbox)

        vbox.show_all()
        if not conf.application_window.show_main_toolbar:
            self.uim.get_widget("/ui/main_toolbar").hide()
        if not conf.application_window.show_video_toolbar:
            self.video_toolbar.hide()
        if not conf.application_window.show_statusbar:
            self.statusbar.hide()

        self.set_menu_notify_events("main")
        self.update_gui()
        self.window.show()

    def _init_main_toolbar(self, vbox):
        """Initialize the main toolbar."""

        self._init_open_button()
        self._init_redo_button()
        self._init_undo_button()

        toolbar = self.uim.get_widget("/ui/main_toolbar")
        toolbar.insert(self.open_button, 0)
        toolbar.insert(gtk.SeparatorToolItem(), 2)
        toolbar.insert(self.undo_button, 3)
        toolbar.insert(self.redo_button, 4)
        path = "/ui/main_toolbar/save_main"
        self.uim.get_widget(path).set_is_important(True)

        style = conf.application_window.toolbar_style
        if style != cons.TOOLBAR_STYLE.DEFAULT:
            toolbar.set_style(style.value)
        conf.connect(self, "application_window", "toolbar_style")
        vbox.pack_start(toolbar, False, False, 0)

    def _init_menubar(self, vbox):
        """Initialize the menubar."""

        menubar = self.uim.get_widget("/ui/menubar")
        vbox.pack_start(menubar, False, False, 0)

    def _init_notebook(self, vbox):
        """Initialize the notebook."""

        self.notebook = gtk.Notebook()
        self.notebook.set_scrollable(True)
        self.notebook.drag_dest_set(
            gtk.DEST_DEFAULT_ALL,
            [("text/uri-list", 0, 0)],
            gtk.gdk.ACTION_COPY)

        util.connect(self, "notebook", "drag-data-received")
        util.connect(self, "notebook", "page-reordered")
        method = self.on_notebook_switch_page
        self.notebook.connect_after("switch-page", method)
        vbox.pack_start(self.notebook, True , True , 0)

    def _init_open_button(self):
        """Initialize the open button."""

        self.open_button = gtk.MenuToolButton(gtk.STOCK_OPEN)
        self.open_button.set_label(_("Open"))
        self.open_button.set_is_important(True)
        self.open_button.set_menu(gtk.Menu())
        self.open_button.set_tooltip(
            self.static_tooltips, _("Open main files"))
        self.open_button.set_arrow_tooltip(
            self.static_tooltips, _("Open a recently used main file"))
        util.connect(self, "open_button", "clicked")

    def _init_output_window(self):
        """Initialize output window."""

        self.output_window = OutputWindow()
        util.connect(self, "output_window", "notify::visible")
        if conf.output_window.show:
            self.output_window.show()

    def _init_recent_menus(self):
        """Initialize the recent file menus."""

        path = "/ui/menubar/file/recent_main"
        self.uim.get_widget(path).set_submenu(gtk.Menu())
        path = "/ui/menubar/file/recent_translation"
        self.uim.get_widget(path).set_submenu(gtk.Menu())
        self.open_button.set_menu(gtk.Menu())
        util.connect(self, "open_button", "show-menu")

    def _init_redo_button(self):
        """Initialize the redo button."""

        self.redo_button = gtk.MenuToolButton(gtk.STOCK_REDO)
        self.redo_button.set_label(_("Redo"))
        self.redo_button.set_is_important(False)
        self.redo_button.set_menu(gtk.Menu())
        self.redo_button.set_tooltip(
            self.tooltips, _("Redo the last undone action"))
        self.redo_button.set_arrow_tooltip(
            self.tooltips, _("Redo undone actions"))
        util.connect(self, "redo_button", "clicked")
        util.connect(self, "redo_button", "show-menu")

    def _init_statusbar(self, vbox):
        """Initialize the statusbar."""

        self.statusbar = gtk.Statusbar()
        self.statusbar.set_has_resize_grip(True)
        event_box = gtk.EventBox()
        event_box.add(self.statusbar)
        vbox.pack_start(event_box, False, False, 0)

    def _init_uim(self):
        """Initialize the UI manager."""

        self.uim = gtk.UIManager()
        action_group = gtk.ActionGroup("main")
        self._init_uim_menus(action_group)
        self._init_uim_actions(action_group)
        self.uim.insert_action_group(action_group ,  0)
        self.uim.insert_action_group(gtk.ActionGroup("recent") , -1)
        self.uim.insert_action_group(gtk.ActionGroup("projects"), -1)
        self.uim.add_ui_from_file(_UI_XML_FILE)
        self.window.add_accel_group(self.uim.get_accel_group())

        action = self.uim.get_action("/ui/menubar/projects")
        action.connect("activate", self.on_show_projects_menu_activate)

        # FIX:
        # Remove ellipses from toolitems.
        #widget = self.uim.get_widget("/ui/main_toolbar/find")
        #widget.set_label(_("Find"))
        #widget = self.uim.get_widget("/ui/main_toolbar/replace")
        #widget.set_label(_("Replace"))

    def _init_uim_actions(self, action_group):
        """Initialize the UI manager actions."""

        def get_method(name):
            name = "on_" + name.replace("-", "_") + "_activate"
            return getattr(self, name)

        for class_name in ACTIONS:
            cls = eval(class_name)
            if cls.menu_item is not None:
                item = list(cls.menu_item)
                method = util.ignore_exceptions()(get_method)(item[0])
                item.append(method)
                action_group.add_actions([tuple(item)], None)
            if cls.action_item is not None:
                item = list(cls.action_item)
                item.append(get_method(item[0]))
                action_group.add_actions([tuple(item)], None)
            if cls.toggle_item is not None:
                item = list(cls.toggle_item)
                item.insert(5, get_method(item[0]))
                action_group.add_toggle_actions([tuple(item)], None)
            if cls.radio_items is not None:
                items, value = cls.radio_items
                method = get_method(items[0][0])
                action_group.add_radio_actions(items, value, method)

    def _init_uim_menus(self, action_group):
        """Initialize the UI manager menus."""

        menu_items = [
            ("show_file_menu"    , None, _("_File")    ),
            ("show_edit_menu"    , None, _("_Edit")    ),
            ("show_view_menu"    , None, _("_View")    ),
            ("show_text_menu"    , None, _("_Text")    ),
            ("show_tools_menu"   , None, _("T_ools")   ),
            ("show_projects_menu", None, _("_Projects")),
            ("show_help_menu"    , None, _("_Help")    ),]
        action_group.add_actions(menu_items)

    def _init_undo_button(self):
        """Initialize the undo button."""

        self.undo_button = gtk.MenuToolButton(gtk.STOCK_UNDO)
        self.undo_button.set_label(_("Undo"))
        self.undo_button.set_is_important(True)
        self.undo_button.set_menu(gtk.Menu())
        self.undo_button.set_tooltip(
            self.tooltips, _("Undo the last action"))
        self.undo_button.set_arrow_tooltip(
            self.tooltips, _("Undo actions"))
        util.connect(self, "undo_button", "clicked")
        util.connect(self, "undo_button", "show-menu")

    def _init_video_button(self):
        """Intialize the video button on the video toolbar."""

        hbox = gtk.HBox(False, 4)
        image = gtk.image_new_from_stock(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
        hbox.pack_start(image, False, False)
        label = gtk.Label()
        label.props.xalign = 0
        label.set_ellipsize(pango.ELLIPSIZE_END)
        hbox.pack_start(label, True, True)
        hbox.pack_start(gtk.VSeparator(), False, False)
        image = gtk.image_new_from_stock(gtk.STOCK_OPEN, gtk.ICON_SIZE_MENU)
        hbox.pack_start(image, False, False)

        self.video_button = gtk.Button()
        self.video_button.add(hbox)
        self.video_button.set_data("label", label)
        self.video_button.drag_dest_set(
            gtk.DEST_DEFAULT_ALL,
            [("text/uri-list", 0, 0)],
            gtk.gdk.ACTION_COPY)
        util.connect(self, "video_button", "clicked")
        util.connect(self, "video_button", "drag-data-received")

        tool_item = gtk.ToolItem()
        tool_item.set_border_width(4)
        tool_item.set_expand(True)
        tool_item.add(self.video_button)
        self.video_toolbar.insert(tool_item, -1)

    def _init_video_label(self):
        """Intialize the video label on the video toolbar."""

        label = gtk.Label(_("Video file:"))
        tool_item = gtk.ToolItem()
        tool_item.set_border_width(4)
        tool_item.add(label)
        self.video_toolbar.insert(tool_item, -1)

    def _init_video_toolbar(self, vbox):
        """Initialize the video toolbar."""

        self.video_toolbar = gtk.Toolbar()
        self._init_video_label()
        self._init_video_button()
        self._init_framerate_label()
        self._init_framerate_combo()
        vbox.pack_start(self.video_toolbar, False, False, 0)

    def _init_window(self):
        """Initialize the window."""

        self.window = gtk.Window()
        self.window.resize(*conf.application_window.size)
        self.window.move(*conf.application_window.position)
        if conf.application_window.maximized:
            self.window.maximize()
        util.connect(self, "window", "delete-event")
        util.connect(self, "window", "window-state-event")

        icon_theme = gtk.icon_theme_get_default()
        if icon_theme.has_icon("gaupol"):
            self.window.set_icon_name("gaupol")
            gtk.window_set_default_icon_name("gaupol")
        if self.window.get_icon() is None:
            gtk.window_set_default_icon_from_file(_ICON_FILE)

    def get_current_page(self):
        """Get the currently active Page or None."""

        index = self.notebook.get_current_page()
        if index >= 0:
            return self.pages[index]
        return None
