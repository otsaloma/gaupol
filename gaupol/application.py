# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010,2012 Osmo Salomaa
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
import atexit
import gaupol
import itertools
import os
_ = aeidon.i18n._

from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import Pango

__all__ = ("Application",)


class ApplicationMeta(aeidon.Contractual):

    """
    Application metaclass with delegated methods added.

    Public methods are added to the class dictionary during :meth:`__new__`
    in order to fool Sphinx (and perhaps other API documentation generators)
    into thinking that the resulting instantiated class actually contains those
    methods, which it does not since the methods are removed during
    :meth:`Application.__init__`.
    """

    def __new__(meta, class_name, bases, dic):
        new_dict = dic.copy()
        for agent_class_name in gaupol.agents.__all__:
            agent_class = getattr(gaupol.agents, agent_class_name)
            def is_delegate_method(name):
                value = getattr(agent_class, name)
                return (callable(value) and
                        hasattr(value, "export") and
                        value.export is True)

            attr_names = list(filter(is_delegate_method, dir(agent_class)))
            for attr_name in attr_names:
                new_dict[attr_name] = getattr(agent_class, attr_name)
        return type.__new__(meta, class_name, bases, new_dict)


class Application(aeidon.Observable, metaclass=ApplicationMeta):

    """
    GTK+ user interface controller for :class:`aeidon.Project`.

    :ivar _delegations: Dictionary mapping method names to agent methods
    :ivar clipboard: Instance of :class:`aeidon.Clipboard` used
    :ivar counter: Iterator used for naming unsaved documents
    :ivar extension_manager: Instance of :class:`gaupol.ExtensionManager` used
    :ivar framerate_combo: A :class:`Gtk.ComboBox` used to select framerate
    :ivar notebook: A :class:`Gtk.Notebook` used to hold multiple projects
    :ivar output_window: A :class:`Gtk.Window` for external process output
    :ivar pages: List of :class:`gaupol.Page` currently open
    :ivar pattern: Last used search pattern or blank if not used
    :ivar recent_manager: Instance of :class:`Gtk.RecentManager` used
    :ivar replacement: Last used search replacement or blank if not used
    :ivar statusbar: A :class:`Gtk.Statusbar` used to hold messages
    :ivar uim: Instance of :class:`Gtk.UIManager` used
    :ivar video_button: A :class:`Gtk.Button` used to select a video file
    :ivar video_toolbar: A :class:`Gtk.Toolbar` for video actions
    :ivar window: A :class:`Gtk.Window` used to hold all the widgets
    :ivar x_clipboard: A :class:`Gtk.Clipboard` used for desktop-wide copying

    Signals and their arguments for callback functions:
     * ``page-added``: application, page
     * ``page-changed``: application, page
     * ``page-closed``: application, page
     * ``page-switched``: application, page
     * ``pages-reordered``: application, page, number
     * ``quit``: application
     * ``text-assistant-request-pages``: application, assistant
    """

    signals = ("page-added",
               "page-changed",
               "page-closed",
               "page-switched",
               "pages-reordered",
               "quit",
               "text-assistant-request-pages",)

    def __getattr__(self, name):
        """Return method delegated to an agent."""
        try:
            return self._delegations[name]
        except KeyError:
            raise AttributeError

    def __setattr__(self, name, value):
        return aeidon.Observable.__setattr__(self, name, value)

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
        self.recent_manager = Gtk.RecentManager.get_default()
        self.replacement = ""
        self.statusbar = None
        self.uim = None
        self.video_button = None
        self.video_toolbar = None
        self.window = None
        self.x_clipboard = None
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

    def _init_css(self):
        """Init custom CSS theming rules for screen."""
        provider = Gtk.CssProvider.get_default()
        path = os.path.join(aeidon.DATA_DIR, "ui", "gaupol.css")
        provider.load_from_path(path)
        context = self.window.get_style_context()
        priority = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        context.add_provider_for_screen(self.window.get_screen(),
                                        provider,
                                        priority)

    def _init_delegations(self):
        """Initialize the delegation mappings."""
        for agent_class_name in gaupol.agents.__all__:
            agent = getattr(gaupol.agents, agent_class_name)(self)
            def is_delegate_method(name):
                value = getattr(agent, name)
                return (callable(value) and
                        hasattr(value, "export") and
                        value.export is True)

            attr_names = list(filter(is_delegate_method, dir(agent)))
            for attr_name in attr_names:
                attr_value = getattr(agent, attr_name)
                if attr_name in self._delegations:
                    raise ValueError("Multiple definitions of {}"
                                     .format(repr(attr_name)))

                self._delegations[attr_name] = attr_value
                # Remove class-level function added by ApplicationMeta.
                if hasattr(self.__class__, attr_name):
                    delattr(self.__class__, attr_name)

    def _init_framerate_combo(self):
        """Intialize the framerate combo box on the video toolbar."""
        self.framerate_combo = Gtk.ComboBoxText()
        for name in (x.label for x in aeidon.framerates):
            self.framerate_combo.append_text(name)
        self.framerate_combo.set_active(gaupol.conf.editor.framerate)
        aeidon.util.connect(self, "framerate_combo", "changed")
        tool_item = Gtk.ToolItem()
        tool_item.add(self.framerate_combo)
        self.video_toolbar.insert(tool_item, -1)

    def _init_framerate_label(self):
        """Intialize the framerate label on the video toolbar."""
        label = Gtk.Label(label=_("Framerate:"))
        alignment = Gtk.Alignment(left_padding=6, right_padding=6)
        alignment.add(label)
        tool_item = Gtk.ToolItem()
        tool_item.add(alignment)
        self.video_toolbar.insert(tool_item, -1)

    def _init_gui(self):
        """Initialize the user interface."""
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self._init_x_clipboard()
        self._init_window()
        self._init_css()
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
        self._init_undo_button()
        self._init_redo_button()
        toolbar = self.uim.get_widget("/ui/main_toolbar")
        context = toolbar.get_style_context()
        context.add_class("primary-toolbar")
        style = gaupol.conf.application_window.toolbar_style
        if style != gaupol.toolbar_styles.DEFAULT:
            toolbar.set_style(style.value)
        gaupol.conf.connect_notify("application_window",
                                   "toolbar_style",
                                   self)

        vbox.pack_start(toolbar,
                        expand=False,
                        fill=False,
                        padding=0)

    def _init_menubar(self, vbox):
        """Initialize the menubar."""
        menubar = self.uim.get_widget("/ui/menubar")
        vbox.pack_start(menubar,
                        expand=False,
                        fill=False,
                        padding=0)

    def _init_notebook(self, vbox):
        """Initialize the notebook."""
        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)
        self.notebook.set_show_border(False)
        self.notebook.drag_dest_set(flags=Gtk.DestDefaults.ALL,
                                    targets=None,
                                    actions=Gdk.DragAction.COPY)

        self.notebook.drag_dest_add_uri_targets()
        aeidon.util.connect(self, "notebook", "drag-data-received")
        aeidon.util.connect(self, "notebook", "page-reordered")
        callback = self._on_notebook_switch_page
        self.notebook.connect_after("switch-page", callback)
        vbox.pack_start(self.notebook,
                        expand=True,
                        fill=True,
                        padding=0)

    def _init_output_window(self):
        """Initialize the output window."""
        self.output_window = gaupol.OutputWindow()
        aeidon.util.connect(self, "output_window", "notify::visible")
        self.output_window.props.visible = gaupol.conf.output_window.show

    def _init_redo_button(self):
        """Initialize the redo button on the main toolbar."""
        redo_button = self.get_tool_item("redo_action")
        if isinstance(redo_button, Gtk.MenuToolButton):
            # redo_button is not necessarily a menu tool button.
            # https://bugzilla.gnome.org/show_bug.cgi?id=686608
            redo_button.set_menu(Gtk.Menu())
            tip = _("Redo undone actions")
            redo_button.set_arrow_tooltip_text(tip)
            callback = self._on_redo_button_show_menu
            redo_button.connect("show-menu", callback)

    def _init_statusbar(self, vbox):
        """Initialize the statusbar."""
        self.statusbar = Gtk.Statusbar()
        vbox.pack_start(self.statusbar,
                        expand=False,
                        fill=False,
                        padding=0)

    def _init_uim(self):
        """Initialize the UI manager."""
        self.uim = Gtk.UIManager()
        safe_group = Gtk.ActionGroup(name="main-safe")
        unsafe_group = Gtk.ActionGroup(name="main-unsafe")
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
        action_group = Gtk.ActionGroup(name="projects")
        self.uim.insert_action_group(action_group, -1)
        ui_xml_file = os.path.join(aeidon.DATA_DIR, "ui", "ui.xml")
        self.uim.add_ui_from_file(ui_xml_file)
        self.window.add_accel_group(self.uim.get_accel_group())
        path = os.path.join(aeidon.CONFIG_HOME_DIR, "accels.conf")
        if os.path.isfile(path):
            Gtk.AccelMap.load(path)
        atexit.register(Gtk.AccelMap.save, path)
        self.uim.ensure_update()

    def _init_uim_radio_groups(self, action_group):
        """Initialize the groups of radio actions in action group."""
        actions = action_group.list_actions()
        actions = [x for x in actions if isinstance(x, Gtk.RadioAction)]
        for group in set(x.group for x in actions):
            instance = None
            for action in (x for x in actions if x.group == group):
                if instance is not None:
                    action.join_group(instance)
                instance = instance or action

    def _init_undo_button(self):
        """Initialize the undo button on the main toolbar."""
        undo_button = self.get_tool_item("undo_action")
        if isinstance(undo_button, Gtk.MenuToolButton):
            # undo_button is not necessarily a menu tool button.
            # https://bugzilla.gnome.org/show_bug.cgi?id=686608
            undo_button.set_menu(Gtk.Menu())
            tip = _("Undo actions")
            undo_button.set_arrow_tooltip_text(tip)
            callback = self._on_undo_button_show_menu
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
        # Let's make this resemble a Gtk.FileChooserButton,
        # but not actually be one, because they are slow to instantiate.
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        image = Gtk.Image(stock=Gtk.STOCK_FILE,
                          icon_size=Gtk.IconSize.MENU)

        hbox.pack_start(image,
                        expand=False,
                        fill=False,
                        padding=4)

        label = Gtk.Label()
        label.props.xalign = 0
        label.set_ellipsize(Pango.EllipsizeMode.END)
        hbox.pack_start(label,
                        expand=True,
                        fill=True,
                        padding=0)

        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(separator,
                        expand=False,
                        fill=False,
                        padding=4)

        image = Gtk.Image(stock=Gtk.STOCK_OPEN,
                          icon_size=Gtk.IconSize.MENU)

        hbox.pack_start(image,
                        expand=False,
                        fill=False,
                        padding=4)

        self.video_button = Gtk.Button()
        self.video_button.add(hbox)
        self.video_button.gaupol_label = label
        self.video_button.drag_dest_set(flags=Gtk.DestDefaults.ALL,
                                        targets=None,
                                        actions=Gdk.DragAction.COPY)

        self.video_button.drag_dest_add_uri_targets()
        aeidon.util.connect(self, "video_button", "clicked")
        aeidon.util.connect(self, "video_button", "drag-data-received")
        tool_item = Gtk.ToolItem()
        tool_item.set_expand(True)
        tool_item.add(self.video_button)
        self.video_toolbar.insert(tool_item, -1)

    def _init_video_label(self):
        """Intialize the video label on the video toolbar."""
        label = Gtk.Label(label=_("Video file:"))
        alignment = Gtk.Alignment(right_padding=6)
        alignment.add(label)
        tool_item = Gtk.ToolItem()
        tool_item.add(alignment)
        self.video_toolbar.insert(tool_item, -1)

    def _init_video_toolbar(self, vbox):
        """Initialize the video toolbar."""
        self.video_toolbar = Gtk.Toolbar()
        self.video_toolbar.set_border_width(2)
        self._init_video_label()
        self._init_video_button()
        self._init_framerate_label()
        self._init_framerate_combo()
        vbox.pack_start(self.video_toolbar,
                        expand=False,
                        fill=False,
                        padding=0)

    def _init_window(self):
        """Initialize the main window."""
        self.window = Gtk.Window()
        self.window.set_icon_name("gaupol")
        Gtk.Window.set_default_icon_name("gaupol")
        self.window.resize(*gaupol.conf.application_window.size)
        self.window.move(*gaupol.conf.application_window.position)
        if gaupol.conf.application_window.maximized:
            self.window.maximize()
        aeidon.util.connect(self, "window", "delete-event")
        aeidon.util.connect(self, "window", "window-state-event")

    def _init_x_clipboard(self):
        """Initialize the desktop-wide, persistent clipboard."""
        atom = Gdk.atom_intern("CLIPBOARD", True)
        self.x_clipboard = Gtk.Clipboard.get(atom)
        self.x_clipboard.set_can_store(None)
