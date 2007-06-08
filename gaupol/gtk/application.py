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


"""GTK user interface controller."""


import gaupol.gtk
import gtk
import os
import pango
_ = gaupol.i18n._


class Application(gaupol.Observable, gaupol.gtk.Runner):

    """GTK user interface controller.

    Instance variables:
     * _delegations: Dictionary mapping method names to agent methods
     * clipboard: Internal global subtitle text clipboard
     * counter: Integer used for naming unsaved documents
     * pages: List of Pages currently open
     * pattern: Last used search pattern or blank if not used
     * replacement: Last used search replacement or blank if not used

    Signals:
     * page-added (application, page)
     * page-changed (application, page)
     * page-closed (application, page)
     * pages-reordered (application, page, number)

    See gaupol.gtk.agents for application methods provided by agents.
    """

    __metaclass__ = gaupol.Contractual

    _signals = [
        "page-added",
        "page-changed",
        "page-closed",
        "pages-reordered",]

    def __getattr__(self, name):

        return self._delegations[name]

    def __init__(self):

        # pylint: disable-msg=W0231
        gaupol.Observable.__init__(self)
        self._delegations = {}
        self.clipboard = gaupol.Clipboard()
        self.counter = 0
        self.framerate_combo = None
        self.notebook = None
        self.output_window = None
        self.pages = []
        self.pattern = ""
        self.recent_manager = gtk.recent_manager_get_default()
        self.replacement = ""
        self.static_tooltips = gtk.Tooltips()
        self.statusbar = None
        self.tooltips = gtk.Tooltips()
        self.uim = None
        self.video_button = None
        self.video_toolbar = None
        self.window = None
        self.x_clipboard = gtk.Clipboard()

        self._init_delegations()
        self._init_gui()

    def _init_delegations(self):
        """Initialize the delegation mappings."""

        for agent_class_name in gaupol.gtk.agents.__all__:
            agent = getattr(gaupol.gtk.agents, agent_class_name)(self)
            attrs = [x for x in dir(agent) if not x.startswith("_")]
            attrs = [(x, getattr(agent, x)) for x in attrs]
            attrs = [(x, y) for (x, y) in attrs if callable(y)]
            for attr_name, attr in attrs:
                if attr_name in self._delegations:
                    raise ValueError("Agents overlap")
                self._delegations[attr_name] = attr

    def _init_framerate_combo(self):
        """Intialize the framerate combo box on the video toolbar."""

        # FIX:
        self.framerate_combo = gtk.combo_box_new_text()
        for name in gaupol.gtk.FRAMERATE.labels:
            self.framerate_combo.append_text(name)
        #self.framerate_combo.set_active(gaupol.gtk.conf.editor.framerate)
        #gaupol.gtk.util.connect(self, "framerate_combo", "changed")

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

        # FIX:
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
        self._init_visibilities()
        #self.set_menu_notify_events("main")
        #self.update_gui()
        self.window.show()

    def _init_main_toolbar(self, vbox):
        """Initialize the main toolbar."""

        # FIX:
        #self._init_open_button()
        #self._init_redo_button()
        #self._init_undo_button()
        toolbar = self.uim.get_widget("/ui/main_toolbar")
        style = gaupol.gtk.conf.application_window.toolbar_style
        if style != gaupol.gtk.TOOLBAR_STYLE.DEFAULT:
            toolbar.set_style(style.value)
        #gaupol.gtk.conf.connect(self, "application_window", "toolbar_style")
        vbox.pack_start(toolbar, False, False, 0)

    def _init_menubar(self, vbox):
        """Initialize the menubar."""

        menubar = self.uim.get_widget("/ui/menubar")
        vbox.pack_start(menubar, False, False, 0)

    def _init_notebook(self, vbox):
        """Initialize the notebook."""

        # FIX:
        self.notebook = gtk.Notebook()
        self.notebook.set_scrollable(True)
        flags = gtk.DEST_DEFAULT_ALL
        targets = [("text/uri-list", 0, 0)]
        types = gtk.gdk.ACTION_COPY
        self.notebook.drag_dest_set(flags, targets, types)
        #gaupol.gtk.util.connect(self, "notebook", "drag-data-received")
        #gaupol.gtk.util.connect(self, "notebook", "page-reordered")
        #callback = self.on_notebook_switch_page
        #self.notebook.connect_after("switch-page", callback)
        vbox.pack_start(self.notebook, True , True , 0)

    def _init_open_button(self):
        """Initialize the open button on the main toolbar."""

        # FIX:
        open_button = self.uim.get_widget("/ui/main_toolbar/open_main")
        open_button.set_menu(gtk.Menu())
        tip =  _("Open a recently used main file")
        open_button.set_arrow_tooltip(self.static_tooltips, tip)
        #callback = self._on_open_button_show_menu
        #open_button.connect("show-menu", callback)

    def _init_output_window(self):
        """Initialize the output window."""

        # FIX:
        self.output_window = gaupol.gtk.OutputWindow()
        #gaupol.gtk.util.connect(self, "output_window", "notify::visible")
        self.output_window.props.visible = gaupol.gtk.conf.output_window.show

    def _init_recent_menus(self):
        """Initialize the recent file menus."""

        # FIX:
        path = "/ui/menubar/file/recent_main"
        #self.uim.get_widget(path).set_submenu(gtk.Menu())
        path = "/ui/menubar/file/recent_translation"
        #self.uim.get_widget(path).set_submenu(gtk.Menu())
        #open_button = self.uim.get_widget("/ui/toolbar/open_main")
        #open_button.set_submenu(gtk.Menu())
        #callback = self._on_open_button_show_submenu
        #open_button.connect("show-menu", callback)

    def _init_redo_button(self):
        """Initialize the redo button on the main toolbar."""

        # FIX:
        redo_button = self.uim.get_widget("/ui/main_toolbar/redo")
        redo_button.set_menu(gtk.Menu())
        tip = _("Redo undone actions")
        redo_button.set_arrow_tooltip(self.tooltips, tip)
        #callback = self._on_redo_button_show_menu
        #redo_button.connect("show-menu", callback)

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
        for name in gaupol.gtk.actions.__all__:
            action = getattr(gaupol.gtk.actions, name)()
            action.finalize(self)
            action_group.add_action_with_accel(action, action.accelerator)
        self._init_uim_radio_groups(action_group)
        self.uim.insert_action_group(action_group, 0)
        action_group = gtk.ActionGroup("recent")
        self.uim.insert_action_group(action_group, -1)
        action_group = gtk.ActionGroup("projects")
        self.uim.insert_action_group(action_group, -1)
        ui_xml_file = os.path.join(gaupol.DATA_DIR, "ui.xml")
        self.uim.add_ui_from_file(ui_xml_file)
        self.window.add_accel_group(self.uim.get_accel_group())
        self.uim.ensure_update()

    def _init_uim_menus(self, action_group):
        """Initialize the top-level UI manager menus."""

        actions = [
            ("show_file_menu", None, _("_File")),
            ("show_edit_menu", None, _("_Edit")),
            ("show_view_menu", None, _("_View")),
            ("show_text_menu", None, _("_Text")),
            ("show_tools_menu", None, _("T_ools")),
            ("show_projects_menu", None, _("_Projects")),
            ("show_help_menu", None, _("_Help")),]
        action_group.add_actions(actions)

        # FIX:
        action = self.uim.get_action("/ui/menubar/projects")
        #callback = self.on_show_projects_menu_activate
        #action.connect("activate", callback)

    def _init_uim_radio_groups(self, action_group):
        """Initialize the groups of radio actions in action group."""

        actions = action_group.list_actions()
        actions = [x for x in actions if isinstance(x, gtk.RadioAction)]
        for group in set((x.group for x in actions)):
            instance = None
            for action in (x for x in actions if x.group == group):
                if instance is not None:
                    action.set_group(instance)
                instance = instance or action

    def _init_undo_button(self):
        """Initialize the undo button on the main toolbar."""

        # FIX:
        undo_button = self.uim.get_widget("/ui/main_toolbar/undo")
        undo_button.set_menu(gtk.Menu())
        tip = _("Undo actions")
        undo_button.set_arrow_tooltip(self.tooltips, tip)
        #callback = self._on_undo_button_show_menu
        #undo_button.connect("show-menu", callback)

    def _init_visibilities(self):
        """Initialize visibilities of hideable widgets."""

        visible = gaupol.gtk.conf.application_window.show_main_toolbar
        toolbar = self.uim.get_widget("/ui/main_toolbar")
        toolbar.props.visible = visible
        visible = gaupol.gtk.conf.application_window.show_video_toolbar
        self.video_toolbar.props.visible = visible
        visible = gaupol.gtk.conf.application_window.show_statusbar
        self.statusbar.props.visible = visible

    def _init_video_button(self):
        """Intialize the video button on the video toolbar."""

        hbox = gtk.HBox(False, 4)
        size = gtk.ICON_SIZE_MENU
        image = gtk.image_new_from_stock(gtk.STOCK_FILE, size)
        hbox.pack_start(image, False, False)
        label = gtk.Label()
        label.props.xalign = 0
        label.set_ellipsize(pango.ELLIPSIZE_END)
        hbox.pack_start(label, True, True)
        hbox.pack_start(gtk.VSeparator(), False, False)
        image = gtk.image_new_from_stock(gtk.STOCK_OPEN, size)
        hbox.pack_start(image, False, False)

        # FIX:
        self.video_button = gtk.Button()
        self.video_button.add(hbox)
        self.video_button.set_data("label", label)
        flags = gtk.DEST_DEFAULT_ALL
        targets = [("text/uri-list", 0, 0)]
        types = gtk.gdk.ACTION_COPY
        self.video_button.drag_dest_set(flags, targets, types)
        #gaupol.gtk.util.connect(self, "video_button", "clicked")
        #gaupol.gtk.util.connect(self, "video_button", "drag-data-received")

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
        """Initialize the main window."""

        # FIX:
        self.window = gtk.Window()
        icon_theme = gtk.icon_theme_get_default()
        self.window.set_icon_name("gaupol")
        gtk.window_set_default_icon_name("gaupol")
        self.window.resize(*gaupol.gtk.conf.application_window.size)
        self.window.move(*gaupol.gtk.conf.application_window.position)
        if gaupol.gtk.conf.application_window.maximized:
            self.window.maximize()
        #gaupol.gtk.util.connect(self, "window", "delete-event")
        #gaupol.gtk.util.connect(self, "window", "window-state-event")

    def _invariant(self):
        for i, page in enumerate(self.pages):
            value = self.notebook.get_nth_page(i)
            assert value.get_child() == page.view

    @gaupol.gtk.util.asserted_return
    def get_current_page(self):
        """Get the currently active page or None."""

        index = self.notebook.get_current_page()
        assert index >= 0
        return self.pages[index]

    def set_current_page_require(self, page):
        assert page in self.pages

    def set_current_page(self, page):
        """Set the currently active page."""

        index = self.pages.index(page)
        self.notebook.set_current_page(index)
