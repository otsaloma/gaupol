# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Menu updating."""


from gettext import gettext as _
import os

import gtk

from gaupol.gtk          import cons
from gaupol.gtk.delegate import Delegate
from gaupol.gtk.util     import conf


class MenuUpdateDelegate(Delegate):

    """
    Menu updating.

    Instance variables:

        _projects_id: UI manager merge ID for projects menu
        _recent_id:   UI manager merge ID for recent files

    """

    def __init__(self, *args, **kwargs):

        Delegate.__init__(self, *args, **kwargs)

        self._projects_id = None
        self._recent_id   = None

    def _get_action_group(self, name):
        """
        Get action group from UI manager.

        name: "main", "recent" or "projects"
        """
        for group in self._uim.get_action_groups():
            if group.get_name() == name:
                return group
        raise ValueError

    def _show_revert_button_menu(self, register):
        """Show undo or redo button menu."""

        page = self.get_current_page()
        menu = gtk.Menu()
        menu_items = []

        if register == cons.Action.UNDO:
            stack = page.project.undoables
            button = self._undo_button
            revert_method = self.undo
        elif register == cons.Action.REDO:
            stack = page.project.redoables
            button = self._redo_button
            revert_method = self.redo

        def on_activate(item, index):
            revert_method(index + 1)

        def on_enter(menu_item, event, index, tip):
            for i in range(index):
                menu_items[i].set_state(gtk.STATE_PRELIGHT)
            self.set_status_message(tip, False)

        def on_leave(menu_item, event, index):
            for i in range(index):
                menu_items[i].set_state(gtk.STATE_NORMAL)
            self.set_status_message(None)

        for i, action in enumerate(stack):
            desc = action.description
            if register == cons.Action.UNDO:
                tip = _('Undo up to %s') % desc[0].lower() + desc[1:]
            elif register == cons.Action.REDO:
                tip = _('Redo up to %s') % desc[0].lower() + desc[1:]
            menu_item = gtk.MenuItem(desc, False)
            menu_item.connect('activate', on_activate, i)
            menu_item.connect('enter-notify-event', on_enter, i, tip)
            menu_item.connect('leave-notify-event', on_leave, i)
            menu_items.append(menu_item)
            menu.append(menu_item)

        menu.show_all()
        button.set_menu(menu)

    def on_open_button_show_menu(self, *args):
        """Show open button menu."""

        def on_activate(menu_item, filepath):
            self.open_main_files([filepath])

        def on_enter(menu_item, event, tip):
            self.set_status_message(tip, False)

        def on_leave(menu_item, event):
            self.set_status_message(None)

        menu = gtk.Menu()
        self.validate_recent()
        for path in conf.file.recents:
            basename = os.path.basename(path)
            if len(basename) > 100:
                basename = basename[:50] + '...' + basename[-50:]
            tip = _('Open main file "%s"') % basename
            menu_item = gtk.MenuItem(basename, False)
            menu_item.connect('activate', on_activate, path)
            menu_item.connect('enter-notify-event', on_enter, tip)
            menu_item.connect('leave-notify-event', on_leave)
            menu.append(menu_item)

        menu.show_all()
        self._open_button.set_menu(menu)

    def on_redo_button_show_menu(self, *args):
        """Show redo button menu."""

        self._show_revert_button_menu(cons.Action.REDO)

    def on_show_file_menu_activate(self, *args):
        """
        Show file menu adding recent files.

        File action name fields are integers matching the file's index in
        conf.file.recents and action fields are "open_recent_file_N".
        """
        action_group = self._get_action_group('recent')
        for action in action_group.list_actions():
            action_group.remove_action(action)
        if self._recent_id is not None:
            self._uim.remove_ui(self._recent_id)

        actions = []
        self.validate_recent()
        for i, path in enumerate(conf.file.recents):
            basename = os.path.basename(path)
            label = '%d. %s' % (i + 1, basename)
            if len(label) > 40:
                label = label[:20] + '...' + label[-20:]
            label = label.replace('_', '__')
            if i < 9:
                label = '_' + label
            actions.append((
                'open_recent_file_%d' % i,
                None,
                label,
                None,
                _('Open main file "%s"') % basename,
                self.on_open_recent_file_activate
            ))
        action_group.add_actions(actions)

        ui = ''
        for i in range(len(conf.file.recents)):
            ui += '<menuitem name="%d" action="open_recent_file_%d"/>' % (i, i)
        ui = '''
        <ui><menubar><menu name="file" action="show_file_menu">
            <placeholder name="recent">%s</placeholder>
        </menu></menubar></ui>''' % ui
        self._recent_id = self._uim.add_ui_from_string(ui)

        for i in range(len(conf.file.recents)):
            path = '/ui/menubar/file/recent/%d' % i
            action = self._uim.get_action(path)
            widget = self._uim.get_widget(path)
            action.connect_proxy(widget)

        self.set_menu_notify_events('recent')

    def on_show_projects_menu_activate(self, *args):
        """
        Show projects menu adding all open projects.

        Project action name fields are integers matching the page's index in
        self.pages and action fields are "activate_project_N".
        """
        action_group = self._get_action_group('projects')
        for action in action_group.list_actions():
            action_group.remove_action(action)
        if self._projects_id is not None:
            self._uim.remove_ui(self._projects_id)

        page = self.get_current_page()
        if page is None:
            return

        radio_actions = []
        for i in range(len(self.pages)):
            basename  = self.pages[i].get_main_basename()
            label = self.pages[i].tab_label.get_text()
            label = '%d. %s' % (i + 1, label)
            if len(label) > 60:
                label = label[:30] + '...' + label[-30:]
            label = label.replace('_', '__')
            if i < 9:
                label = '_' + label
            radio_actions.append((
                'activate_project_%d' % i,
                None,
                label,
                None,
                _('Activate "%s"') % basename,
                i
            ))
        action_group.add_radio_actions(
            radio_actions,
            self._notebook.get_current_page(),
            self.on_project_toggled
        )

        ui = ''
        for i in range(len(self.pages)):
            ui += '<menuitem name="%d" action="activate_project_%d"/>' % (i, i)
        ui = '''
        <ui><menubar><menu name="projects" action="show_projects_menu">
        <placeholder name="open">%s</placeholder>
        </menu></menubar></ui>''' % ui
        self._projects_id = self._uim.add_ui_from_string(ui)

        for i in range(len(self.pages)):
            path = '/ui/menubar/projects/open/%d' % i
            action = self._uim.get_action(path)
            widget = self._uim.get_widget(path)
            action.connect_proxy(widget)

        self.set_menu_notify_events('projects')

    def on_undo_button_show_menu(self, *args):
        """Show undo button menu."""

        self._show_revert_button_menu(cons.Action.UNDO)

    def set_menu_notify_events(self, name):
        """
        Set statusbar tooltips for menu items.

        name: "main", "recent" or "projects"
        """
        def on_enter(menu_item, event, action):
            self.set_status_message(action.props.tooltip, False)

        def on_leave(menu_item, event, action):
            self.set_status_message(None)

        action_group = self._get_action_group(name)
        for action in action_group.list_actions():
            for widget in action.get_proxies():
                widget.connect('enter-notify-event', on_enter, action)
                widget.connect('leave-notify-event', on_leave, action)
