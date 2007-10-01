# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Building and updating dynamic menus."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._


class MenuAgent(gaupol.Delegate):

    """Building and updating menus.

    Instance attributes:
     * _projects_id: UI manager merge ID for the projects menu
     * _redo_menu_items: Redo menu tool button menu items
     * _undo_menu_items: Undo menu tool button menu items
    """

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = gaupol.Contractual

    def __init__(self, master):

        gaupol.Delegate.__init__(self, master)
        self._projects_id = None
        self._redo_menu_items = []
        self._undo_menu_items = []

    def _add_project_action(self, page):
        """Add an action to the 'projects' action group."""

        index = self.pages.index(page)
        basename = page.get_main_basename()
        name = "activate_project_%d" % index
        label = page.tab_label.get_text().replace("_", "__")
        label = "%d. %s" % (index + 1, label)
        label = ("_%s" % label if index < 9 else label)
        tooltip = _('Activate "%s"') % basename
        action = gtk.RadioAction(name, label, tooltip, None, index)
        action_group = self.get_action_group("projects")
        group = action_group.get_action("activate_project_0")
        if group is not None:
            action.set_group(group)
        accel = ("<alt>%d" % (index + 1) if index < 9 else None)
        action_group.add_action_with_accel(action, accel)
        callback = self._on_projects_action_changed
        action.connect("changed", callback)
        action.set_active(page is self.get_current_page())
        return action.get_name()

    def _get_recent_menu(self, doc):
        """Return a new recent chooser menu."""

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
        menu.set_limit(gaupol.gtk.conf.file.max_recent)
        return menu

    def _on_redo_menu_item_activate(self, menu_item):
        """Redo the selected action and all those above it."""

        index = menu_item.get_data("index")
        self.redo(index + 1)

    def _on_redo_menu_item_enter(self, menu_item, event):
        """Show tooltip and select all actions above this one."""

        index = menu_item.get_data("index")
        for item in self._redo_menu_items[:index]:
            item.set_state(gtk.STATE_PRELIGHT)
        self.push_message(menu_item.get_data("tooltip"))

    def _on_redo_menu_item_leave(self, menu_item, event):
        """Show tooltip and unselect all actions above this one."""

        index = menu_item.get_data("index")
        for item in self._redo_menu_items[:index]:
            item.set_state(gtk.STATE_NORMAL)
        self.push_message(None)

    def _on_undo_menu_item_activate(self, menu_item):
        """Undo the selected action and all those above it."""

        index = menu_item.get_data("index")
        self.undo(index + 1)

    def _on_undo_menu_item_enter(self, menu_item, event):
        """Show tooltip and select all actions above this one."""

        index = menu_item.get_data("index")
        for item in self._undo_menu_items[:index]:
            item.set_state(gtk.STATE_PRELIGHT)
        self.push_message(menu_item.get_data("tooltip"))

    def _on_undo_menu_item_leave(self, menu_item, event):
        """Show tooltip and unselect all actions above this one."""

        index = menu_item.get_data("index")
        for item in self._undo_menu_items[:index]:
            item.set_state(gtk.STATE_NORMAL)
        self.push_message(None)

    def _on_projects_action_changed(self, item, active_item):
        """Change the page in the notebook to the selected project."""

        index = int(active_item.get_name().split("_")[-1])
        self.notebook.set_current_page(index)

    def on_open_button_show_menu(self, *args):
        """Build and attach a new recent menu on the open button."""

        menu = self._get_recent_menu(gaupol.gtk.DOCUMENT.MAIN)
        callback = self.on_recent_main_menu_item_activated
        menu.connect("item-activated", callback)
        self.get_tool_item("open_main_files").set_menu(menu)
        gaupol.gtk.util.iterate_main()

    @gaupol.gtk.util.asserted_return
    def on_page_tab_widget_button_press_event(self, button, event):
        """Display a pop-up menu with tab-related actions."""

        assert event.button == 3
        menu = self.uim.get_widget("/ui/tab_popup")
        menu.popup(None, None, None, event.button, event.time)

    def on_redo_button_show_menu(self, *args):
        """Show the menu listing all redoable actions."""

        menu = gtk.Menu()
        self._redo_menu_items = []
        page = self.get_current_page()
        for i, action in enumerate(page.project.redoables):
            item = gtk.MenuItem(action.description, False)
            item.set_data("index", i)
            item.set_data("tooltip", _('Redo "%s"') % action.description)
            callback = self._on_redo_menu_item_activate
            item.connect("activate", callback)
            callback = self._on_redo_menu_item_enter
            item.connect("enter-notify-event", callback)
            callback = self._on_redo_menu_item_leave
            item.connect("leave-notify-event", callback)
            self._redo_menu_items.append(item)
            menu.append(item)
        menu.show_all()
        self.get_tool_item("redo_action").set_menu(menu)

    @gaupol.gtk.util.asserted_return
    def on_show_projects_menu_activate(self, *args):
        """Add all open projects to the projects menu."""

        action_group = self.get_action_group("projects")
        for action in action_group.list_actions():
            action_group.remove_action(action)
        if self._projects_id is not None:
            self.uim.remove_ui(self._projects_id)
        page = self.get_current_page()
        assert page is not None
        ui = '<ui><menubar name="menubar">'
        ui += '<menu name="projects" action="show_projects_menu">'
        ui += '<placeholder name="open">'
        for i, page in enumerate(self.pages):
            name = self._add_project_action(page)
            ui += '<menuitem name="%d" action="%s"/>' % (i, name)
        ui += '</placeholder></menu></menubar></ui>'
        self._projects_id = self.uim.add_ui_from_string(ui)
        self.uim.ensure_update()
        self.set_menu_notify_events("projects")

    def on_show_recent_main_menu_activate(self, *args):
        """Show the recent main file menu."""

        item = self.get_menu_item("show_recent_main_menu")
        menu = self._get_recent_menu(gaupol.gtk.DOCUMENT.MAIN)
        callback = self.on_recent_main_menu_item_activated
        menu.connect("item-activated", callback)
        item.set_submenu(menu)
        gaupol.gtk.util.iterate_main()

    def on_show_recent_translation_menu_activate(self, *args):
        """Show the recent translation file menu."""

        item = self.get_menu_item("show_recent_translation_menu")
        menu = self._get_recent_menu(gaupol.gtk.DOCUMENT.TRAN)
        callback = self.on_recent_translation_menu_item_activated
        menu.connect("item-activated", callback)
        item.set_submenu(menu)
        gaupol.gtk.util.iterate_main()

    def on_undo_button_show_menu(self, *args):
        """Show the menu listing all undoable actions."""

        menu = gtk.Menu()
        self._undo_menu_items = []
        page = self.get_current_page()
        for i, action in enumerate(page.project.undoables):
            item = gtk.MenuItem(action.description, False)
            item.set_data("index", i)
            item.set_data("tooltip", _('Undo "%s"') % action.description)
            callback = self._on_undo_menu_item_activate
            item.connect("activate", callback)
            callback = self._on_undo_menu_item_enter
            item.connect("enter-notify-event", callback)
            callback = self._on_undo_menu_item_leave
            item.connect("leave-notify-event", callback)
            self._undo_menu_items.append(item)
            menu.append(item)
        menu.show_all()
        self.get_tool_item("undo_action").set_menu(menu)

    def set_menu_notify_events(self, name):
        """Set statusbar tooltips for menu items for action group."""

        def on_enter(menu_item, event, self, action):
            self.push_message(action.props.tooltip)
        def on_leave(menu_item, event, self, action):
            self.push_message(None)
        action_group = self.get_action_group(name)
        for action in action_group.list_actions():
            for widget in action.get_proxies():
                widget.connect("enter-notify-event", on_enter, self, action)
                widget.connect("leave-notify-event", on_leave, self, action)
