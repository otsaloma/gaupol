# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Menu updating."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _
import os

import gtk

from gaupol.constants     import Action
from gaupol.gtk.delegates import Delegate
from gaupol.gtk.util      import config, gtklib


class MenuUpdateDelegate(Delegate):

    """Menu updating."""

    def _get_action_group(self, name):
        """
        Get action group from UI manager.

        name: "main", "recent" or "projects"
        """
        assert name in ('main', 'recent', 'projects')
        action_groups = self.uim.get_action_groups()
        action_group_names = list(group.get_name() for group in action_groups)
        index = action_group_names.index(name)
        return action_groups[index]

    def on_open_button_show_menu(self, *args):
        """Build the recent files menu."""

        recent_files = config.file.recent_files
        for i in reversed(range(len(recent_files))):
            if not os.path.isfile(recent_files[i]):
                recent_files.pop(i)

        menu = gtk.Menu()

        def on_activate(item, filepath):
            self.open_main_files([filepath])

        def on_enter_notify_event(item, event, tooltip):
            self.set_status_message(tooltip, False)

        def on_leave_notify_event(item, event):
            self.set_status_message(None)

        for filepath in recent_files:

            basename = os.path.basename(filepath)
            if len(basename) > 100:
                basename = basename[:50] + '...' + basename[-50:]
            tip = _('Open main file "%s"') % basename

            item = gtk.MenuItem(basename, False)
            item.connect('activate'          , on_activate, filepath     )
            item.connect('enter-notify-event', on_enter_notify_event, tip)
            item.connect('leave-notify-event', on_leave_notify_event     )
            menu.append(item)

        menu.show_all()
        self.open_button.set_menu(menu)

    def _on_menu_item_enter_notify_event(self, item, event, action):
        """Set item's tooltips to statusbar."""

        self.set_status_message(action.props.tooltip, False)

    def _on_menu_item_leave_notify_event(self, item, event, action):
        """Clear item's tooltip from statusbar."""

        self.set_status_message(None)

    def on_redo_button_show_menu(self, *args):
        """Build the redo menu."""

        self._show_revert_button_menu(Action.REDO)

    def on_show_file_menu_activated(self, *args):
        """
        Build the file menu by adding all open projects.

        Project action name fields are integers matching the file's index in
        config.file.recent_files and action fields are "open_recent_file_N".
        """
        # Remove old actions.
        action_group = self._get_action_group('recent')
        for action in action_group.list_actions():
            action_group.remove_action(action)

        # Remove old menu items.
        if self.recent_uim_id is not None:
            self.uim.remove_ui(self.recent_uim_id)

        recent_files = config.file.recent_files
        for i in reversed(range(len(recent_files))):
            if not os.path.isfile(recent_files[i]):
                recent_files.pop(i)

        actions  = []
        callback = self.on_open_recent_file_activated

        # Create actions.
        for i in range(len(recent_files)):

            basename = os.path.basename(recent_files[i])
            name     = 'open_recent_file_%d' % i
            label    = '%d. %s' % (i + 1, basename)
            tooltip  = _('Open main file "%s"') % basename

            # Fix labels by ellipsizing too long names, unaccelerating
            # underscores and adding an accelerator to the first 9 items.
            if len(label) > 50:
                label = label[:25] + '...' + label[-25:]
            label = label.replace('_', '__')
            if i < 9:
                label = '_' + label

            actions.append((name, None, label, None, tooltip, callback))

        # Add actions to action group.
        action_group.add_actions(actions)

        # Add menu items.
        ui_start  = '''
        <ui>
            <menubar>
                <menu name="file" action="show_file_menu">
                    <placeholder name="recent">'''
        ui_middle = ''
        ui_end    = '''
                    </placeholder>
                </menu>
            </menubar>
        </ui>'''

        for i in range(len(recent_files)):
            ui_middle += '<menuitem name="%d" action="open_recent_file_%d"/>' \
                         % (i, i)

        ui = ui_start + ui_middle + ui_end
        self.recent_uim_id = self.uim.add_ui_from_string(ui)

        # Connect proxies to get the message statusbar tooltips working.
        for i in range(len(recent_files)):
            path = '/ui/menubar/file/recent/%d' % i
            action = self.uim.get_action(path)
            widget = self.uim.get_widget(path)
            action.connect_proxy(widget)

        self.set_menu_notify_events('recent')

    def on_show_projects_menu_activated(self, *args):
        """
        Build the projects menu by adding all open projects.

        Project action name fields are integers matching the page's index in
        self.pages and action fields are "activate_project_N".
        """
        page = self.get_current_page()

        # Remove old actions.
        action_group = self._get_action_group('projects')
        for action in action_group.list_actions():
            action_group.remove_action(action)

        # Remove old menu items.
        if self.projects_uim_id is not None:
            self.uim.remove_ui(self.projects_uim_id)

        if page is None:
            return

        radio_actions = []

        # Create actions.
        for i in range(len(self.pages)):

            basename  = self.pages[i].get_main_basename()
            tab_label = self.pages[i].tab_label.get_text()
            name      = 'activate_project_%d' % i
            label     = '%d. %s' % (i + 1, tab_label)

            # Translators: Activate a project, "Activate <basename>".
            tooltip  = _('Activate "%s"') % basename

            # Fix labels by ellipsizing too long names, unaccelerating
            # underscores and adding an accelerator to the first 9 items.
            if len(label) > 50:
                label = label[:25] + '...' + label[-25:]
            label = label.replace('_', '__')
            if i < 9:
                label = '_' + label

            radio_actions.append((name, None, label, None, tooltip, i))

        # Add actions to action group.
        action_group.add_radio_actions(
            radio_actions,
            self.notebook.get_current_page(),
            self.on_project_toggled
        )

        # Add menu items.
        ui_start  = '''
        <ui>
            <menubar>
                <menu name="projects" action="show_projects_menu">
                    <placeholder name="open">'''
        ui_middle = ''
        ui_end    = '''
                    </placeholder>
                </menu>
            </menubar>
        </ui>'''

        for i in range(len(self.pages)):
            ui_middle += '<menuitem name="%d" action="activate_project_%d"/>' \
                         % (i, i)

        ui = ui_start + ui_middle + ui_end
        self.projects_uim_id = self.uim.add_ui_from_string(ui)

        # Connect proxies to get the message statusbar tooltips working.
        for i in range(len(self.pages)):
            path = '/ui/menubar/projects/open/%d' % i
            action = self.uim.get_action(path)
            widget = self.uim.get_widget(path)
            action.connect_proxy(widget)

        self.set_menu_notify_events('projects')

    def on_undo_button_show_menu(self, *args):
        """Build the undo menu."""

        self._show_revert_button_menu(Action.UNDO)

    def set_menu_notify_events(self, action_group_name):
        """
        Set GUI properties when mouse hovers over a menu item.

        action_group_name: "main", "recent" or "projects"
        """
        action_group = self._get_action_group(action_group_name)

        signals = (
            'enter-notify-event',
            'leave-notify-event'
        )
        methods = (
            self._on_menu_item_enter_notify_event,
            self._on_menu_item_leave_notify_event
        )

        actions = action_group.list_actions()
        for action in actions:
            widgets = action.get_proxies()
            for widget in widgets:
                widget.connect(signals[0], methods[0], action)
                widget.connect(signals[1], methods[1], action)

    def _show_revert_button_menu(self, register):
        """Show undo or redo button's menu."""

        page = self.get_current_page()
        menu = gtk.Menu()
        menu_items = []

        if register == Action.UNDO:
            stack = page.project.undoables
            button = self.undo_button
            revert_method = self.undo
        elif register == Action.REDO:
            stack = page.project.redoables
            button = self.redo_button
            revert_method = self.redo

        def on_activate(item, index):
            revert_method(index + 1)

        def on_enter_notify_event(item, event, index, tip):
            for i in range(0, index):
                menu_items[i].set_state(gtk.STATE_PRELIGHT)
            self.set_status_message(tip, False)

        def on_leave_notify_event(item, event, index):
            for i in range(0, index):
                menu_items[i].set_state(gtk.STATE_NORMAL)
            self.set_status_message(None)

        for i in range(len(stack)):

            desc = stack[i].description

            if register == Action.UNDO:
                tip = _('Undo up to %s') % desc[0].lower() + desc[1:]
            elif register == Action.REDO:
                tip = _('Redo up to %s') % desc[0].lower() + desc[1:]

            item = gtk.MenuItem(desc, False)
            item.connect('activate'          , on_activate          , i     )
            item.connect('enter-notify-event', on_enter_notify_event, i, tip)
            item.connect('leave-notify-event', on_leave_notify_event, i     )

            menu_items.append(item)
            menu.append(item)

        menu.show_all()
        button.set_menu(menu)
