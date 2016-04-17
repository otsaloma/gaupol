# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""GTK+ user interface controller for :class:`aeidon.Project`."""

import aeidon
import atexit
import gaupol
import itertools
import os
import sys

from aeidon.i18n   import _
from gi.repository import Gdk
from gi.repository import Gtk

__all__ = ("Application",)


class ApplicationMeta(type):

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

    :ivar clipboard: Instance of :class:`aeidon.Clipboard` used
    :ivar counter: Iterator used for naming unsaved documents
    :ivar _delegations: Dictionary mapping method names to agent methods
    :ivar extension_manager: Instance of :class:`gaupol.ExtensionManager` used
    :ivar notebook: A :class:`Gtk.Notebook` used to hold multiple projects
    :ivar notebook_separator: A :class:`Gtk.Separator` above the notebook
    :ivar output_window: A :class:`Gtk.Window` for external process output
    :ivar pages: List of :class:`gaupol.Page` currently open
    :ivar paned: A :class:`Gtk.Paned` to hold player and subtitles
    :ivar pattern: Last used search pattern or blank if not used
    :ivar player: A :class:`gaupol.VideoPlayer` instance or ``None``
    :ivar player_box: Box containing video player etc.
    :ivar player_toolbar: A :class:`Gtk.Toolbar` for video player actions
    :ivar recent_manager: Instance of :class:`Gtk.RecentManager` used
    :ivar replacement: Last used search replacement or blank if not used
    :ivar seekbar: Video player seekbar (a :class:`Gtk.Scale` instance)
    :ivar statuslabel: Instance of :class:`gaupol.FloatingLabel` used
    :ivar uim: Instance of :class:`Gtk.UIManager` used
    :ivar volume_button: A :class:`Gtk.VolumeButton` in the player toolbar
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

    signals = (
        "page-added",
        "page-changed",
        "page-closed",
        "page-switched",
        "pages-reordered",
        "quit",
        "text-assistant-request-pages",
    )

    def __init__(self):
        """Initialize an :class:`Application` instance."""
        aeidon.Observable.__init__(self)
        self.clipboard = aeidon.Clipboard()
        self.counter = itertools.count(1)
        self._delegations = {}
        self.extension_manager = gaupol.ExtensionManager(self)
        self.notebook = None
        self.notebook_separator = None
        self.output_window = None
        self.pages = []
        self.pattern = ""
        self.player = None
        self.player_box = None
        self.player_toolbar = None
        self.recent_manager = Gtk.RecentManager.get_default()
        self.replacement = ""
        self.seekbar = None
        self.statuslabel = None
        self.uim = None
        self.volume_button = None
        self.window = None
        self.x_clipboard = None
        self._init_delegations()
        self._init_gui()
        self.extension_manager.find_extensions()
        self.extension_manager.setup_extensions()
        self.update_gui()
        self.window.show()

    def __getattr__(self, name):
        """Return method delegated to an agent."""
        try:
            return self._delegations[name]
        except KeyError:
            raise AttributeError

    def __setattr__(self, name, value):
        """Set value of attribute `name`."""
        return aeidon.Observable.__setattr__(self, name, value)

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
        style = self.window.get_style_context()
        priority = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        style.add_provider_for_screen(self.window.get_screen(),
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

    def _init_gui(self):
        """Initialize the user interface."""
        vbox = gaupol.util.new_vbox(spacing=0)
        self._init_x_clipboard()
        self._init_window()
        self._init_css()
        self._init_uim()
        self._init_menubar(vbox)
        self._init_main_toolbar(vbox)
        self._init_paned(vbox)
        self._init_player_box(self.paned)
        self._init_notebook(self.paned)
        self._init_output_window()
        self.window.add(vbox)
        vbox.show_all()
        self._init_visibilities()
        self._finalize_uim_actions()

    def _init_main_toolbar(self, vbox):
        """Initialize the main toolbar."""
        self._init_undo_button()
        self._init_redo_button()
        toolbar = self.uim.get_widget("/ui/main_toolbar")
        style = toolbar.get_style_context()
        style.add_class("primary-toolbar")
        toolbar_style = gaupol.conf.application_window.toolbar_style
        toolbar.set_style(toolbar_style.value)
        if sys.platform == "win32":
            toolbar.set_icon_size(Gtk.IconSize.MENU)
        gaupol.conf.connect_notify("application_window", "toolbar_style", self)
        gaupol.util.pack_start(vbox, toolbar)

    def _init_menubar(self, vbox):
        """Initialize the menubar."""
        menubar = self.uim.get_widget("/ui/menubar")
        gaupol.util.pack_start(vbox, menubar)

    def _init_notebook(self, paned):
        """Initialize the notebook."""
        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)
        self.notebook.set_show_border(False)
        self.notebook.set_show_tabs(False)
        self.notebook.drag_dest_set(flags=Gtk.DestDefaults.ALL,
                                    targets=None,
                                    actions=Gdk.DragAction.COPY)

        self.notebook.drag_dest_add_uri_targets()
        aeidon.util.connect(self, "notebook", "drag-data-received")
        aeidon.util.connect(self, "notebook", "page-reordered")
        callback = self._on_notebook_switch_page
        self.notebook.connect_after("switch-page", callback)
        orientation = Gtk.Orientation.HORIZONTAL
        self.notebook_separator = Gtk.Separator(orientation=orientation)
        vbox = gaupol.util.new_vbox(spacing=0)
        gaupol.util.pack_start(vbox, self.notebook_separator)
        overlay = Gtk.Overlay()
        overlay.add(self.notebook)
        self.statuslabel = gaupol.FloatingLabel()
        overlay.add_overlay(self.statuslabel)
        gaupol.util.pack_start_expand(vbox, overlay)
        paned.add2(vbox)

    def _init_output_window(self):
        """Initialize the output window."""
        self.output_window = gaupol.OutputWindow(self.window)
        aeidon.util.connect(self, "output_window", "notify::visible")
        self.output_window.set_visible(False)

    def _init_paned(self, vbox):
        """Intialize the paned layout."""
        orientation = gaupol.conf.application_window.layout
        self.paned = Gtk.Paned(orientation=orientation)
        gaupol.util.pack_start_expand(vbox, self.paned)

    def _init_player_box(self, paned):
        """Initialize the video player horizontal box."""
        # This will actually be added to paned
        # once a video is loaded for use.
        conf = gaupol.conf.application_window
        if conf.layout == Gtk.Orientation.HORIZONTAL:
            orientation = Gtk.Orientation.VERTICAL
        if conf.layout == Gtk.Orientation.VERTICAL:
            orientation = Gtk.Orientation.HORIZONTAL
        self.player_box = Gtk.Box(orientation=orientation)

    def _init_redo_button(self):
        """Initialize the redo button on the main toolbar."""
        redo_button = self.get_tool_item("redo_action")
        if isinstance(redo_button, Gtk.MenuToolButton):
            # redo_button is not necessarily a menu tool button.
            # http://bugzilla.gnome.org/show_bug.cgi?id=686608
            redo_button.set_menu(Gtk.Menu())
            tip = _("Redo undone actions")
            redo_button.set_arrow_tooltip_text(tip)
            callback = self._on_redo_button_show_menu
            redo_button.connect("show-menu", callback)

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
        action_group = Gtk.ActionGroup(name="audio-tracks")
        self.uim.insert_action_group(action_group, -1)
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
            # http://bugzilla.gnome.org/show_bug.cgi?id=686608
            undo_button.set_menu(Gtk.Menu())
            tip = _("Undo actions")
            undo_button.set_arrow_tooltip_text(tip)
            callback = self._on_undo_button_show_menu
            undo_button.connect("show-menu", callback)

    def _init_visibilities(self):
        """Initialize visibilities of hideable widgets."""
        conf = gaupol.conf.application_window
        toolbar = self.uim.get_widget("/ui/main_toolbar")
        toolbar.set_visible(conf.show_main_toolbar)
        self.notebook_separator.set_visible(False)
        self.show_message(None)

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
