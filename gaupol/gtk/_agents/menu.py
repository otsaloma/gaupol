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


"""Building and updating menus."""


import os
from gettext import gettext as _

import gtk

from gaupol import util
from gaupol.base import Delegate
from gaupol.gtk import conf, cons


class MenuAgent(Delegate):

    """Building and updating menus.

    Instance attributes:

        _projects_id: UI manager merge ID for the projects menu
    """

    # pylint: disable-msg=E0203,W0201

    def __init__(self, master):

        Delegate.__init__(self, master)

        self._projects_id = None

    def _get_action_group(self, name):
        """Get action group from the UI manager.

        name should be 'main' or 'projects'.
        """
        for group in self.uim.get_action_groups():
            if group.get_name() == name:
                return group
        raise ValueError

    def _get_project_actions(self):
        """Get a list of UI manager actions for the projects menu."""

        radio_actions = []
        for i in range(len(self.pages)):
            name = "activate_project_%d" % i
            basename  = self.pages[i].get_main_basename()
            label = self.pages[i].tab_label.get_text()
            label = "%d. %s" % (i + 1, label)
            if len(label) > 60:
                label = label[:60] + "..."
            label = label.replace("_", "__")
            label = ("_%s" % label if i < 9 else label)
            key = ("<alt>%d" % (i + 1) if i < 9 else None)
            tip = _('Activate "%s"') % basename
            radio_actions.append((name, None, label, key, tip, i))
        return radio_actions

    def _get_project_ui_string(self):
        """Get a UI manager layout string for the projects menu."""

        ui = ""
        for i in range(len(self.pages)):
            ui += '<menuitem name="%d" action="activate_project_%d"/>' % (i, i)
        ui = """
        <ui>
          <menubar>
            <menu name="projects" action="show_projects_menu">
              <placeholder name="open">%s</placeholder>
            </menu>
          </menubar>
        </ui>""" % ui
        return ui

    def _get_recent_menu(self, doc):
        """Return a new gtk.RecentChooserMenu."""

        menu = gtk.RecentChooserMenu(self.recent_manager)
        menu.set_show_not_found(False)
        menu.set_show_tips(False)
        menu.set_sort_type(gtk.RECENT_SORT_MRU)

        group = ("gaupol-main", "gaupol-translation")[doc]
        recent_filter = gtk.RecentFilter()
        recent_filter.add_group(group)
        menu.add_filter(recent_filter)
        menu.set_filter(recent_filter)
        menu.set_data("group", group)

        self._update_recent_menu(menu)
        return menu

    def _show_revert_button_menu(self, register):
        """Show the undo or redo button menu."""

        menu_items = []
        menu = gtk.Menu()
        page = self.get_current_page()
        if register == cons.REGISTER.UNDO:
            stack = page.project.undoables
            button = self.undo_button
            revert_method = self.undo
            get_tip = lambda desc: _('Undo "%s"') % desc
        elif register == cons.REGISTER.REDO:
            stack = page.project.redoables
            button = self.redo_button
            revert_method = self.redo
            get_tip = lambda desc: _('Redo "%s"') % desc

        def on_activate(menu_item, index):
            revert_method(index + 1)
        def on_enter(menu_item, event, index, tip):
            for i in range(index):
                menu_items[i].set_state(gtk.STATE_PRELIGHT)
            self.push_message(tip, False)
        def on_leave(menu_item, event, index):
            for i in range(index):
                menu_items[i].set_state(gtk.STATE_NORMAL)
            self.push_message(None)

        for i, action in enumerate(stack):
            tip = get_tip(action.description)
            menu_item = gtk.MenuItem(action.description, False)
            menu_item.connect("activate", on_activate, i)
            menu_item.connect("enter-notify-event", on_enter, i, tip)
            menu_item.connect("leave-notify-event", on_leave, i)
            menu_items.append(menu_item)
            menu.append(menu_item)
        menu.show_all()
        button.set_menu(menu)

    def _update_recent_menu(self, menu):
        """Update recent menu item limit."""

        if conf.file.max_recent < 1:
            return menu.set_limit(0)
        i = -1
        matches = 0
        group = menu.get_data("group")
        menu.set_limit(i)
        # pylint: disable-msg=W0631
        for i, item in enumerate(menu.get_items()):
            if not item.has_group(group):
                continue
            path = util.uri_to_path(item.get_uri())
            if not os.path.isfile(path):
                continue
            matches += 1
            if matches >= conf.file.max_recent:
                break
        return menu.set_limit(i + 1)

    def on_open_button_show_menu(self, *args):
        """Build and attach a new recent menu on the open button."""

        menu = self._get_recent_menu(cons.DOCUMENT.MAIN)
        method = self.on_recent_main_menu_item_activated
        menu.connect("item-activated", method)
        self.open_button.set_menu(menu)
        while gtk.events_pending():
            gtk.main_iteration()

    def on_page_tab_widget_button_press_event(self, button, event):
        """Display a tab pop-up menu."""

        if event.button == 3:
            menu = self.uim.get_widget("/ui/tab_popup")
            menu.popup(None, None, None, event.button, event.time)

    def on_redo_button_show_menu(self, *args):
        """Show the redo button menu."""

        self._show_revert_button_menu(cons.REGISTER.REDO)

    def on_show_projects_menu_activate(self, *args):
        """Add all open projects to the projects menu."""

        action_group = self._get_action_group("projects")
        for action in action_group.list_actions():
            action_group.remove_action(action)
        if self._projects_id is not None:
            self.uim.remove_ui(self._projects_id)
        page = self.get_current_page()
        if page is None:
            return

        def switch(item, active_item):
            index = int(active_item.get_name().split("_")[-1])
            self.notebook.set_current_page(index)
        radio_actions = self._get_project_actions()
        active = self.notebook.get_current_page()
        action_group.add_radio_actions(radio_actions, active, switch)
        ui = self._get_project_ui_string()
        self._projects_id = self.uim.add_ui_from_string(ui)

        for i in range(len(self.pages)):
            path = "/ui/menubar/projects/open/%d" % i
            action = self.uim.get_action(path)
            widget = self.uim.get_widget(path)
            action.connect_proxy(widget)
        self.set_menu_notify_events("projects")

    def on_show_recent_main_menu_activate(self, *args):
        """Show the recent main file menu."""

        item = self.uim.get_widget("/ui/menubar/file/recent_main")
        menu = self._get_recent_menu(cons.DOCUMENT.MAIN)
        method = self.on_recent_main_menu_item_activated
        menu.connect("item-activated", method)
        item.set_submenu(menu)
        while gtk.events_pending():
            gtk.main_iteration()

    def on_show_recent_translation_menu_activate(self, *args):
        """Show the recent translation file menu."""

        item = self.uim.get_widget("/ui/menubar/file/recent_translation")
        menu = self._get_recent_menu(cons.DOCUMENT.TRAN)
        method = self.on_recent_translation_menu_item_activated
        menu.connect("item-activated", method)
        item.set_submenu(menu)
        while gtk.events_pending():
            gtk.main_iteration()

    def on_undo_button_show_menu(self, *args):
        """Show the undo button menu."""

        self._show_revert_button_menu(cons.REGISTER.UNDO)

    def set_menu_notify_events(self, name):
        """Set statusbar tooltips for menu items.

        name should be 'main' or 'projects'.
        """
        def on_enter(menu_item, event, action):
            self.push_message(action.props.tooltip, False)
        def on_leave(menu_item, event, action):
            self.push_message(None)

        for action in self._get_action_group(name).list_actions():
            for widget in action.get_proxies():
                widget.connect("enter-notify-event", on_enter, action)
                widget.connect("leave-notify-event", on_leave, action)
