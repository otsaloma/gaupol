# Copyright (C) 2005-2008,2010 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""GTK+ user interface controller for :class:`aeidon.Project`."""

import aeidon
import gaupol
import gtk
import itertools
import os
import pango
_ = aeidon.i18n._

__all__ = ("Application",)


class ApplicationMeta(aeidon.Contractual):

    """Application metaclass with delegated methods added.

    Delegated methods are added to the class dictionary during :meth:`__new__`
    in order to fool Sphinx (and perhaps other API documentation generators)
    into thinking that the resulting instantiated class actually contains those
    methods, which it does not since the methods are be removed during
    :meth:`Application.__init__`.
    """

    def __new__(meta, class_name, bases, dic):
        new_dict = dic.copy()
        for agent_class_name in gaupol.agents.__all__:
            agent_class = getattr(gaupol.agents, agent_class_name)
            def is_delegate_method(name):
                if (name.startswith("_") or
                    name.endswith("_require") or
                    name.endswith("_ensure")):
                    return False
                return callable(getattr(agent_class, name))
            attr_names = filter(is_delegate_method, dir(agent_class))
            for attr_name in attr_names:
                new_dict[attr_name] = getattr(agent_class, attr_name)
        return type.__new__(meta, class_name, bases, new_dict)


class Application(aeidon.Observable):

    """GTK+ user interface controller for :class:`aeidon.Project`.

    :ivar _delegations: Dictionary mapping method names to agent methods
    :ivar clipboard: Instance of :class:`aeidon.Clipboard` used
    :ivar counter: Iterator used for naming unsaved documents
    :ivar extension_manager: Instance of :class:`gaupol.ExtensionManager` used
    :ivar framerate_combo: A :class:`gtk.ComboBox` used to select framerate
    :ivar notebook: A :class:`gtk.Notebook` used to hold multiple projects
    :ivar output_window: A :class:`gtk.Window` for external process output
    :ivar pages: List of :class:`gaupol.Page` currently open
    :ivar pattern: Last used search pattern or blank if not used
    :ivar recent_manager: Instance of :class:`gtk.RecentManager` used
    :ivar replacement: Last used search replacement or blank if not used
    :ivar statusbar: A :class:`gtk.Statusbar` used to hold messages
    :ivar uim: Instance of :class:`gtk.UIManager` used
    :ivar video_button: A :class:`gtk.Button` used to select a video file
    :ivar video_toolbar: A :class:`gtk.Toolbar` for video actions
    :ivar window: A :class:`gtk.Window` used to hold all the widgets

    Signals and their arguments for callback functions:
     * ``page-added``: application, page
     * ``page-changed``: application, page
     * ``page-closed``: application, page
     * ``page-switched``: application, page
     * ``pages-reordered``: application, page, number
     * ``quit``: application
     * ``text-assistant-request-pages``: application, assistant
    """

    __metaclass__ = ApplicationMeta

    signals = ("page-added",
               "page-changed",
               "page-closed",
               "page-switched",
               "pages-reordered",
               "quit",
               "text-assistant-request-pages",)

    def __getattr__(self, name):
        """Return method delegated to an agent."""
        return self._delegations[name]

    def __init__(self):
        """Initialize an :class:`Application` object."""
        aeidon.Observable.__init__(self)
        self._delegations = {}
        self.clipboard = aeidon.Clipboard()
        self.counter = itertools.count(1)
        self.extension_manager = gaupol.ExtensionManager(self)
        self.framerate_combo = None
        self.notebook = None
        self.output_window = None
        self.pages = []
        self.pattern = ""
        self.recent_manager = gtk.recent_manager_get_default()
        self.replacement = ""
        self.statusbar = None
        self.uim = None
        self.video_button = None
        self.video_toolbar = None
        self.window = None
        self.x_clipboard = gtk.Clipboard()
        self._init_delegations()
        self._init_gui()
        self.extension_manager.find_extensions()
        self.extension_manager.setup_extensions()
        self.update_gui()
        self.window.show()

    def _finalize_uim_actions(self):
        """Connect UI manager actions to widgets and methods."""
        for name in ("main-safe", "main-unsafe"):
            action_group = self.get_action_group(name)
            for action in action_group.list_actions():
                action.finalize(self)

    def _init_delegations(self):
        """Initialize the delegation mappings."""
        for agent_class_name in gaupol.agents.__all__:
            agent = getattr(gaupol.agents, agent_class_name)(self)
            def is_delegate_method(name):
                if (name.startswith("_") or
                    name.endswith("_require") or
                    name.endswith("_ensure")):
                    return False
                return callable(getattr(agent, name))
            attr_names = filter(is_delegate_method, dir(agent))
            for attr_name in attr_names:
                attr_value = getattr(agent, attr_name)
                if attr_name in self._delegations:
                    raise ValueError("Multiple definitions of %s"
                                     % repr(attr_name))

                self._delegations[attr_name] = attr_value
                # Remove class-level function added by ApplicationMeta.
                if hasattr(self.__class__, attr_name):
                    delattr(self.__class__, attr_name)

    def _init_framerate_combo(self):
        """Intialize the framerate combo box on the video toolbar."""
        self.framerate_combo = gtk.combo_box_new_text()
        for name in (x.label for x in aeidon.framerates):
            self.framerate_combo.append_text(name)
        self.framerate_combo.set_active(gaupol.conf.editor.framerate)
        aeidon.util.connect(self, "framerate_combo", "changed")
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
        self._init_notebook(vbox)
        self._init_video_toolbar(vbox)
        self._init_statusbar(vbox)
        self._init_output_window()
        self.window.add(vbox)
        vbox.show_all()
        self._init_visibilities()
        self.set_menu_notify_events("main-safe")
        self.set_menu_notify_events("main-unsafe")
        self._finalize_uim_actions()

    def _init_main_toolbar(self, vbox):
        """Initialize the main toolbar."""
        self._init_open_button()
        self._init_redo_button()
        self._init_undo_button()
        toolbar = self.uim.get_widget("/ui/main_toolbar")
        style = gaupol.conf.application_window.toolbar_style
        if style != gaupol.toolbar_styles.DEFAULT:
            toolbar.set_style(style.value)
        gaupol.conf.connect_notify("application_window", "toolbar_style", self)
        vbox.pack_start(toolbar, False, False, 0)

    def _init_menubar(self, vbox):
        """Initialize the menubar."""
        menubar = self.uim.get_widget("/ui/menubar")
        vbox.pack_start(menubar, False, False, 0)

    def _init_notebook(self, vbox):
        """Initialize the notebook."""
        self.notebook = gtk.Notebook()
        self.notebook.set_scrollable(True)
        self.notebook.set_show_border(False)
        self.notebook.drag_dest_set(gtk.DEST_DEFAULT_ALL,
                                    [("text/uri-list", 0, 0)],
                                    gtk.gdk.ACTION_COPY)

        aeidon.util.connect(self, "notebook", "drag-data-received")
        aeidon.util.connect(self, "notebook", "page-reordered")
        callback = self.on_notebook_switch_page
        self.notebook.connect_after("switch-page", callback)
        vbox.pack_start(self.notebook, True , True , 0)

    def _init_open_button(self):
        """Initialize the open button on the main toolbar."""
        open_button = self.get_tool_item("open_main_files")
        open_button.set_menu(gtk.Menu())
        tip =  _("Open a recently used main file")
        open_button.set_arrow_tooltip_text(tip)
        callback = self.on_open_button_show_menu
        open_button.connect("show-menu", callback)

    def _init_output_window(self):
        """Initialize the output window."""
        self.output_window = gaupol.OutputWindow()
        aeidon.util.connect(self, "output_window", "notify::visible")
        self.output_window.props.visible = gaupol.conf.output_window.show

    def _init_redo_button(self):
        """Initialize the redo button on the main toolbar."""
        redo_button = self.get_tool_item("redo_action")
        redo_button.set_menu(gtk.Menu())
        tip = _("Redo undone actions")
        redo_button.set_arrow_tooltip_text(tip)
        callback = self.on_redo_button_show_menu
        redo_button.connect("show-menu", callback)

    def _init_statusbar(self, vbox):
        """Initialize the statusbar."""
        self.statusbar = gtk.Statusbar()
        self.statusbar.set_has_resize_grip(True)
        vbox.pack_start(self.statusbar, False, False, 0)

    def _init_uim(self):
        """Initialize the UI manager."""
        self.uim = gtk.UIManager()
        safe_group = gtk.ActionGroup("main-safe")
        unsafe_group = gtk.ActionGroup("main-unsafe")
        for name in gaupol.actions.__all__:
            action = getattr(gaupol.actions, name)()
            args = (action, action.accelerator)
            if action.action_group == "main-safe":
                safe_group.add_action_with_accel(*args)
            if action.action_group == "main-unsafe":
                unsafe_group.add_action_with_accel(*args)
        self._init_uim_radio_groups(safe_group)
        self._init_uim_radio_groups(unsafe_group)
        self.uim.insert_action_group(safe_group, 0)
        self.uim.insert_action_group(unsafe_group, 1)
        action_group = gtk.ActionGroup("projects")
        self.uim.insert_action_group(action_group, -1)
        ui_xml_file = os.path.join(aeidon.DATA_DIR, "ui", "ui.xml")
        self.uim.add_ui_from_file(ui_xml_file)
        self.window.add_accel_group(self.uim.get_accel_group())
        self.uim.ensure_update()

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
        undo_button = self.get_tool_item("undo_action")
        undo_button.set_menu(gtk.Menu())
        tip = _("Undo actions")
        undo_button.set_arrow_tooltip_text(tip)
        callback = self.on_undo_button_show_menu
        undo_button.connect("show-menu", callback)

    def _init_visibilities(self):
        """Initialize visibilities of hideable widgets."""
        conf = gaupol.conf.application_window
        toolbar = self.uim.get_widget("/ui/main_toolbar")
        toolbar.props.visible = conf.show_main_toolbar
        self.video_toolbar.props.visible = conf.show_video_toolbar
        self.statusbar.props.visible = conf.show_statusbar

    def _init_video_button(self):
        """Intialize the video button on the video toolbar."""
        # Let's make this resemble a gtk.FileChooserButton,
        # but not actually be one, because they are slow to instantiate.
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
        self.video_button = gtk.Button()
        self.video_button.add(hbox)
        self.video_button.set_data("label", label)
        self.video_button.drag_dest_set(gtk.DEST_DEFAULT_ALL,
                                        [("text/uri-list", 0, 0)],
                                        gtk.gdk.ACTION_COPY)

        aeidon.util.connect(self, "video_button", "clicked")
        aeidon.util.connect(self, "video_button", "drag-data-received")
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
        self.window = gtk.Window()
        self.window.set_icon_name("gaupol")
        gtk.window_set_default_icon_name("gaupol")
        self.window.resize(*gaupol.conf.application_window.size)
        self.window.move(*gaupol.conf.application_window.position)
        if gaupol.conf.application_window.maximized:
            self.window.maximize()
        aeidon.util.connect(self, "window", "delete-event")
        aeidon.util.connect(self, "window", "window-state-event")
