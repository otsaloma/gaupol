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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""GTK user interface controller for :class:`aeidon.Project`."""

import aeidon
import gaupol
import itertools

from aeidon.i18n   import _
from gi.repository import Gdk
from gi.repository import Gtk

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
        for agent_class in gaupol.agents.classes:
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
    GTK user interface controller for :class:`aeidon.Project`.

    :ivar clipboard: Instance of :class:`aeidon.Clipboard` used
    :ivar counter: Iterator used for naming unsaved documents
    :ivar _delegations: Dictionary mapping method names to agent methods
    :ivar notebook: A :class:`Gtk.Notebook` used to hold multiple projects
    :ivar pages: List of :class:`gaupol.Page` currently open
    :ivar paned: A :class:`Gtk.Paned` to hold player and subtitles
    :ivar pattern: Last used search pattern or blank if not used
    :ivar play_button: The play/pause button on the video player toolbar
    :ivar player: A :class:`gaupol.VideoPlayer` instance or ``None``
    :ivar player_box: Box containing video player etc.
    :ivar player_toolbar: A toolbar :class:`Gtk.Box` for video player actions
    :ivar recent_manager: Instance of :class:`Gtk.RecentManager` used
    :ivar replacement: Last used search replacement or blank if not used
    :ivar seekbar: Video player seekbar (a :class:`Gtk.Scale` instance)
    :ivar toast: Instance of :class:`gaupol.Toast` used
    :ivar volume_button: A :class:`Gtk.VolumeButton` in the player toolbar
    :ivar window: A :class:`Gtk.ApplicationWindow` used to hold all the widgets
    :ivar x_clipboard: A :class:`Gdk.Clipboard` used for desktop-wide copying

    Signals and their arguments for callback functions:
     * ``init-done``: application
     * ``page-added``: application, page
     * ``page-changed``: application, page
     * ``page-closed``: application, page
     * ``page-saved``: application, page
     * ``page-switched``: application, page
     * ``pages-reordered``: application, page, number
     * ``quit``: application
    """

    signals = (
        "init-done",
        "page-added",
        "page-changed",
        "page-closed",
        "page-saved",
        "page-switched",
        "pages-reordered",
        "quit",
    )

    def __init__(self):
        """Initialize an :class:`Application` instance."""
        aeidon.Observable.__init__(self)
        self.clipboard = aeidon.Clipboard()
        self.counter = itertools.count(1)
        self._delegations = {}
        self.notebook = None
        self.pages = []
        self.pattern = ""
        self.play_button = None
        self.player = None
        self.player_box = None
        self.player_toolbar = None
        self.recent_manager = Gtk.RecentManager.get_default()
        self.replacement = ""
        self.seekbar = None
        self.toast = None
        self.volume_button = None
        self.window = None
        self.x_clipboard = None
        self._init_delegations()
        self._init_custom_framerates()
        self._init_gui()
        self.update_gui()
        self.window.present()
        self.emit("init-done")

    def __getattr__(self, name):
        """Return method delegated to an agent."""
        try:
            return self._delegations[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        """Set value of attribute `name`."""
        return aeidon.Observable.__setattr__(self, name, value)

    def _init_actions(self):
        """Initialize user-activatable actions."""
        for action_class in gaupol.actions.classes:
            action = action_class()
            name = f"win.{action.props.name}"
            if hasattr(gaupol, "appman"):
                gaupol.appman.set_accels_for_action(
                    name, action.accelerators)
            stub = action.props.name.replace("-", "_")
            callback = f"_on_{stub}_activate"
            action.connect("activate", getattr(self, callback))
            self.window.add_action(action)

    def _init_custom_framerates(self):
        """Add framerates from ``conf.editor.custom_framerates``."""
        menu = self.get_menubar_section("custom-framerates-placeholder")
        for value in sorted(gaupol.conf.editor.custom_framerates):
            name = f"FPS_{value:.3f}".replace(".", "_")
            if hasattr(aeidon.framerates, name): continue
            setattr(aeidon.framerates, name, aeidon.EnumerationItem())
            framerate = getattr(aeidon.framerates, name)
            framerate.label = _("{:.3f} fps").format(value)
            framerate.value = float(value)
            if menu is not None:
                # Menubar not available when running unit tests.
                action = f"win.set-framerate::{name}"
                menu.append(framerate.label, action)

    def _init_delegations(self):
        """Initialize the delegation mappings."""
        for agent_class in gaupol.agents.classes:
            agent = agent_class(self)
            def is_delegate_method(name):
                value = getattr(agent, name)
                return (callable(value) and
                        hasattr(value, "export") and
                        value.export is True)

            attr_names = list(filter(is_delegate_method, dir(agent)))
            for attr_name in attr_names:
                attr_value = getattr(agent, attr_name)
                if attr_name in self._delegations:
                    raise ValueError(f"Multiple definitions of {attr_name!r}")

                self._delegations[attr_name] = attr_value
                # Remove class-level function added by ApplicationMeta.
                if hasattr(self.__class__, attr_name):
                    delattr(self.__class__, attr_name)

    def _init_gui(self):
        """Initialize the user interface."""
        vbox = gaupol.util.new_vbox(spacing=0)
        self._init_x_clipboard()
        self._init_window()
        self._init_actions()
        self._init_header_bar()
        self._init_paned(vbox)
        self._init_player_box(self.paned)
        self._init_notebook(self.paned)
        self.window.set_child(vbox)
        self._init_visibilities()

    def _init_header_bar(self):
        """Initialize the window header bar."""
        header = Gtk.HeaderBar()
        # Open split button: win.open-main-files
        # plus a menu listing recent files.
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.add_css_class("linked")
        button = Gtk.Button(icon_name="document-open-symbolic")
        button.set_action_name("win.open-main-files")
        button.set_tooltip_text(_("Open main files"))
        box.append(button)
        button = Gtk.MenuButton(icon_name="pan-down-symbolic")
        button.set_menu_model(self.get_menubar_section("open-recent-main-placeholder"))
        button.set_tooltip_text(_("Open a recently used main file"))
        box.append(button)
        header.pack_start(box)
        # win.save-main-document
        button = Gtk.Button(icon_name="document-save-symbolic")
        button.set_action_name("win.save-main-document")
        button.set_tooltip_text(_("Save the current main document"))
        header.pack_start(button)
        # win.undo-action and win.redo-action as a group
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.add_css_class("linked")
        button = Gtk.Button(icon_name="edit-undo-symbolic")
        button.set_action_name("win.undo-action")
        button.set_tooltip_text(_("Undo the last action"))
        box.append(button)
        button = Gtk.Button(icon_name="edit-redo-symbolic")
        button.set_action_name("win.redo-action")
        button.set_tooltip_text(_("Redo the last undone action"))
        box.append(button)
        header.pack_start(box)
        # win.preview
        button = Gtk.Button(icon_name="media-playback-start-symbolic")
        button.set_action_name("win.preview")
        button.set_tooltip_text(_("Preview from selected position with a video player"))
        header.pack_end(button)
        # win.find-and-replace
        button = Gtk.Button(icon_name="edit-find-symbolic")
        button.set_action_name("win.find-and-replace")
        button.set_tooltip_text(_("Search for and replace text"))
        header.pack_end(button)
        self.window.set_titlebar(header)

    def _init_notebook(self, paned):
        """Initialize the notebook."""
        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)
        self.notebook.set_show_border(False)
        self.notebook.set_show_tabs(False)
        target = Gtk.DropTarget.new(Gdk.FileList, Gdk.DragAction.COPY)
        target.connect("drop", self._on_notebook_drop)
        self.notebook.add_controller(target)
        aeidon.util.connect(self, "notebook", "page-reordered")
        callback = self._on_notebook_switch_page
        self.notebook.connect_after("switch-page", callback)
        overlay = Gtk.Overlay()
        overlay.set_child(self.notebook)
        self.toast = gaupol.Toast()
        overlay.add_overlay(self.toast)
        paned.set_end_child(overlay)

    def _init_paned(self, vbox):
        """Intialize the paned layout."""
        orientation = gaupol.conf.application_window.layout
        self.paned = Gtk.Paned(orientation=orientation)
        gaupol.util.pack_start_expand(vbox, self.paned)

    def _init_player_box(self, paned):
        """Initialize the video player horizontal box."""
        # This will actually be added to paned once a video is loaded.
        layout = gaupol.conf.application_window.layout
        if layout == Gtk.Orientation.HORIZONTAL:
            self.player_box = gaupol.util.new_vbox(spacing=0)
        if layout == Gtk.Orientation.VERTICAL:
            self.player_box = gaupol.util.new_hbox(spacing=0)
        # Keep hidden until a video is loaded. Tab visibility logic
        # in UpdateAgent._update_widgets depends on this too.
        self.player_box.set_visible(False)

    def _init_visibilities(self):
        """Initialize visibilities of hideable widgets."""
        self.show_message(None)

    def _init_window(self):
        """Initialize the main window."""
        self.window = Gtk.ApplicationWindow(
            application=getattr(gaupol, "appman", None))
        self.window.set_show_menubar(True)
        self.window.set_icon_name("io.otsaloma.gaupol")
        Gtk.Window.set_default_icon_name("io.otsaloma.gaupol")
        self.window.set_default_size(*gaupol.conf.application_window.size)
        if gaupol.conf.application_window.maximized:
            self.window.maximize()
        aeidon.util.connect(self, "window", "close-request")
        aeidon.util.connect(self, "window", "notify::maximized")
        gaupol.style.load_css(self.window)

    def _init_x_clipboard(self):
        """Initialize the desktop-wide clipboard."""
        self.x_clipboard = Gdk.Display.get_default().get_clipboard()
