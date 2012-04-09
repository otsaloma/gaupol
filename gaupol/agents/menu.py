# -*- coding: utf-8-unix -*-

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

"""Building and updating dynamic menus."""

import aeidon
from gi.repository import Gtk
_ = aeidon.i18n._


class MenuAgent(aeidon.Delegate, metaclass=aeidon.Contractual):

    """
    Building and updating menus.

    :ivar _projects_id: :class:`Gtk.UIManager` merge ID for projects menu
    :ivar _redo_menu_items: Redo menu tool button menu items
    :ivar _undo_menu_items: Undo menu tool button menu items
    """

    def __init__(self, master):
        """Initialize a MenuAgent object."""
        aeidon.Delegate.__init__(self, master)
        self._projects_id = None
        self._redo_menu_items = []
        self._undo_menu_items = []

    def _add_project_action(self, page):
        """Add an action to the "projects" action group for `page`."""
        index = self.pages.index(page)
        basename = page.get_main_basename()
        name = "activate_project_{:d}".format(index)
        label = page.tab_label.get_text().replace("_", "__")
        label = "{:d}. {}".format(index + 1, label)
        label = ("_{}".format(label)if index < 9 else label)
        tooltip = _('Activate "{}"').format(basename)
        action = Gtk.RadioAction(name, label, tooltip, None, index)
        action_group = self.get_action_group("projects")
        group = action_group.get_action("activate_project_0")
        if group is not None:
            action.set_group(group)
        accel = ("<alt>{:d}".format(index + 1) if index < 9 else None)
        action_group.add_action_with_accel(action, accel)
        action.connect("changed", self._on_projects_action_changed)
        action.set_active(page is self.get_current_page())
        return action.get_name()

    def _on_projects_action_changed(self, item, active_item):
        """Change the page in the notebook to the selected project."""
        index = int(active_item.get_name().split("_")[-1])
        self.notebook.set_current_page(index)

    @aeidon.deco.export
    def _on_redo_button_show_menu(self, *args):
        """Show a menu listing all redoable actions."""
        menu = Gtk.Menu()
        self._redo_menu_items = []
        page = self.get_current_page()
        for i, action in enumerate(page.project.redoables):
            item = Gtk.MenuItem(action.description, False)
            item.set_data("index", i)
            item.set_data("tooltip", _('Redo "{}"').format(action.description))
            callback = self._on_redo_menu_item_activate
            item.connect("activate", callback)
            callback = self._on_redo_menu_item_enter_notify_event
            item.connect("enter-notify-event", callback)
            callback = self._on_redo_menu_item_leave_notify_event
            item.connect("leave-notify-event", callback)
            self._redo_menu_items.append(item)
            menu.append(item)
        menu.show_all()
        self.get_tool_item("redo_action").set_menu(menu)

    def _on_redo_menu_item_activate(self, menu_item):
        """Redo the selected action and all those above it."""
        index = menu_item.get_data("index")
        self.redo(index + 1)

    def _on_redo_menu_item_enter_notify_event(self, menu_item, event):
        """Show tooltip and select all actions above `menu_item`."""
        index = menu_item.get_data("index")
        for item in self._redo_menu_items[:index]:
            item.set_state(Gtk.StateType.PRELIGHT)
        self.push_message(menu_item.get_data("tooltip"))

    def _on_redo_menu_item_leave_notify_event(self, menu_item, event):
        """Hide tooltip and unselect all actions above `menu_item`."""
        index = menu_item.get_data("index")
        for item in self._redo_menu_items[:index]:
            item.set_state(Gtk.StateType.NORMAL)
        self.push_message(None)

    @aeidon.deco.export
    def _on_show_projects_menu_activate(self, *args):
        """Update all project actions in the projects menu."""
        action_group = self.get_action_group("projects")
        for action in action_group.list_actions():
            action_group.remove_action(action)
        if self._projects_id is not None:
            self.uim.remove_ui(self._projects_id)
        page = self.get_current_page()
        if page is None: return
        ui  = '<ui><menubar name="menubar">'
        ui += '<menu name="projects" action="show_projects_menu">'
        ui += '<placeholder name="open">'
        for i, page in enumerate(self.pages):
            name = self._add_project_action(page)
            ui += '<menuitem name="{:d}" action="{}"/>'.format(i, name)
        ui += '</placeholder></menu></menubar></ui>'
        self._projects_id = self.uim.add_ui_from_string(ui)
        self.uim.ensure_update()
        self.set_menu_notify_events("projects")

    @aeidon.deco.export
    def _on_tab_widget_button_press_event(self, button, event, page):
        """Display a pop-up menu with tab-related actions."""
        if event.button != 3: return
        if page is not self.get_current_page():
            self.set_current_page(page)
        menu = self.uim.get_widget("/ui/tab_popup")
        menu.popup(None, None, None, event.button, event.time)

    @aeidon.deco.export
    def _on_undo_button_show_menu(self, *args):
        """Show a menu listing all undoable actions."""
        menu = Gtk.Menu()
        self._undo_menu_items = []
        page = self.get_current_page()
        for i, action in enumerate(page.project.undoables):
            item = Gtk.MenuItem(action.description, False)
            item.set_data("index", i)
            item.set_data("tooltip", _('Undo "{}"').format(action.description))
            callback = self._on_undo_menu_item_activate
            item.connect("activate", callback)
            callback = self._on_undo_menu_item_enter_notify_event
            item.connect("enter-notify-event", callback)
            callback = self._on_undo_menu_item_leave_notify_event
            item.connect("leave-notify-event", callback)
            self._undo_menu_items.append(item)
            menu.append(item)
        menu.show_all()
        self.get_tool_item("undo_action").set_menu(menu)
    def _on_undo_menu_item_activate(self, menu_item):
        """Undo the selected action and all those above it."""
        index = menu_item.get_data("index")
        self.undo(index + 1)

    def _on_undo_menu_item_enter_notify_event(self, menu_item, event):
        """Show tooltip and select all actions above `menu_item`."""
        index = menu_item.get_data("index")
        for item in self._undo_menu_items[:index]:
            item.set_state(Gtk.StateType.PRELIGHT)
        self.push_message(menu_item.get_data("tooltip"))

    def _on_undo_menu_item_leave_notify_event(self, menu_item, event):
        """Hide tooltip and unselect all actions above `menu_item`."""
        index = menu_item.get_data("index")
        for item in self._undo_menu_items[:index]:
            item.set_state(Gtk.StateType.NORMAL)
        self.push_message(None)

    @aeidon.deco.export
    def set_menu_notify_events(self, name):
        """Set statusbar tooltips for menu items of action group."""
        def on_enter(menu_item, event, self, action):
            self.push_message(action.props.tooltip)
        def on_leave(menu_item, event, self, action):
            self.push_message(None)
        action_group = self.get_action_group(name)
        for action in action_group.list_actions():
            for widget in action.get_proxies():
                widget.connect("enter-notify-event", on_enter, self, action)
                widget.connect("leave-notify-event", on_leave, self, action)
