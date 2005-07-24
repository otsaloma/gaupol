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


"""GUI updater to update GUI components' properties."""


import os

try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk

from gaupol.gui.constants import COLUMN_NAMES
from gaupol.gui.constants import FRAMERATE_NAMES
from gaupol.gui.constants import NO, SHOW, HIDE, DURN, ORIG, TRAN
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.util import gui


class GUIUpdater(Delegate):

    """GUI updater to update GUI components' properties."""

    def add_to_recent_files(self, path):
        """Add path to recent file menus."""
    
        recent_files = self.config.getlist('file', 'recent_files')
        maximum = self.config.getint('file', 'maximum_recent_files')
        
        try:
            recent_files.remove(path)
        except ValueError:
            pass
        
        recent_files.insert(0, path)
        
        while len(recent_files) > maximum:
            recent_files.pop()

        self.config.setlist('file', 'recent_files', recent_files)
        self.refresh_recent_file_menus()

    def _get_action_group(self, name):
        """
        Get action group from UI Manager.
        
        name: "main", "recent" or "documents"
        """
        
        action_groups = self.uim.get_action_groups()
        action_group_names = [ag.get_name() for ag in action_groups]
        index = action_group_names.index(name)
        return action_groups[index]
    
    def _on_menu_action_enter_notify_event(self, item, event, action):
        """Set a tooltip to message statusbar, when mouse moves over item."""

        message = action.get_property('tooltip')
        self.set_status_message(message, False)

    def _on_menu_action_leave_notify_event(self, item, event):
        """Clear message statusbar, when mouse moves away from item."""

        self.set_status_message(None)

    def on_next_activated(self, *args):
        """Switch to next page in notebook."""
        
        self.notebook.next_page()

    def on_notebook_page_switched(self, notebook, pointer, new_page):
        """Adjust GUI properties to suit the project switched to."""

        if not self.projects:
            return
        
        project   = self.projects[new_page]
        prj_index = self.projects.index(project)

        self.window.set_title(project.tab_label.get_text())
        self.set_sensitivities_and_visiblities(project)

        edit_mode = project.edit_mode
        framerate = project.data.framerate
        fr_index  = FRAMERATE_NAMES.index(project.data.framerate)

        actions = [
            '/ui/menubar/view/%ss' % edit_mode,
            '/ui/menubar/view/framerate/%s' % framerate,
            '/ui/menubar/documents/open/document-%d' % prj_index,
        ]
        
        for name in actions:
            self.uim.get_action(name).set_active(True)

        # Set correct framerate active in the framerate combo box.
        self.fr_cmbox.set_active(fr_index)

        # Set correct columns active in the menu.
        for i in range(len(COLUMN_NAMES)):
            column = project.tree_view.get_column(i)
            visible = column.get_property('visible')
            name = '/ui/menubar/view/columns/%s' % COLUMN_NAMES[i]
            action = self.uim.get_action(name)
            if not visible is action.get_active():
                action.set_active(visible)
        
        # Set sensitivity of "Next" and "Previous" in the Documents menu.
        prev_action = self.uim.get_action('/ui/menubar/documents/previous')
        next_action = self.uim.get_action('/ui/menubar/documents/next')
        prev_action.set_sensitive(bool(prj_index != 0))
        next_action.set_sensitive(bool(prj_index != len(self.projects) - 1))

    def on_previous_activated(self, *args):
        """Switch to previous page in notebook."""
        
        self.notebook.prev_page()
        
    def on_document_toggled(self, some_action, new_action):
        """Switch page in notebook when file toggled in Subtitles menu."""

        index = int(new_action.get_name().split('-')[-1])
        self.notebook.set_current_page(index)

    def on_window_state_event(self, window, event):
        """Remember whether window is maximized or not."""

        state = event.new_window_state
        maximized = bool(state & gtk.gdk.WINDOW_STATE_MAXIMIZED)
        self.config.setboolean('main_window', 'maximized', maximized)

    def refresh_documents_menu(self):
        """
        Refresh the list of open documents in the Documents menu.
        
        Documents' action names are "document-N", where N is an integer, which
        matches the project's index in projects list and the page index in the
        notebook.
        """
        for project in self.projects:
            if project.uim_id is not None:
                self.uim.remove_ui(project.uim_id)

        action_group = self._get_action_group('documents')
        self.uim.remove_action_group(action_group)

        action_group = gtk.ActionGroup('documents')
        radio_actions = []

        # Add actions to action group.

        for i in range(len(self.projects)):
        
            basename = self.projects[i].get_main_basename()
            name     = 'document-%d' % i
            label    = '%d. %s' % (i + 1, basename)
            tooltip  = _('Activate "%s"') % basename

            # Unaccelerate underscores.
            label = label.replace('_', '__')

            # Add an underscore accelerator to the first 9 documents.
            if i < 9:
                label = '_' + label
            
            # Name, Stock-icon, Label, Accelerator, Tooltip, Index
            radio_actions.append((name, None, label, None, tooltip, i))

        index = self.notebook.get_current_page()
        
        action_group.add_radio_actions(
            radio_actions, index, self.on_document_toggled
        )
        self.uim.insert_action_group(action_group, -1)

        # Add action items to menu.

        for i in range(len(self.projects)):
        
            ui = '''
            <ui>
                <menubar>
                    <menu action="documents">
                        <placeholder name="open">
                            <menuitem action="document-%d"/>
                        </placeholder>
                    </menu>
                </menubar>
            </ui>''' % i

            self.projects[i].uim_id = self.uim.add_ui_from_string(ui)
            
            # To get the message statusbar tooltips working, proxies need to be
            # connected.
            name = '/ui/menubar/documents/open/document-%d' % i
            action = self.uim.get_action(name)
            widget = self.uim.get_widget(name)
            action.connect_proxy(widget)

        self.set_menu_tooltips('documents')

    def refresh_recent_file_menus(self):
        """
        Refresh the list of recent files in the File and open button menus.
        
        Files' action names are "recent-menu-N" and "recent-ob-N", where N is
        an integer, which matches the file's index in recent files list.
        """
        all_recent_files = self.config.getlist('file', 'recent_files')
        recent_files     = []
        
        for path in all_recent_files:
            if os.path.isfile(path):
                recent_files.append(path)
                
        self.config.setlist('file', 'recent_files', recent_files)
        
        basenames = [os.path.basename(path) for path in recent_files]

        if self.recent_uim_id is not None:
            self.uim.remove_ui(self.recent_uim_id)

        action_group = self._get_action_group('recent')
        self.uim.remove_action_group(action_group)

        action_group = gtk.ActionGroup('recent')
        menu_actions = []
        ob_actions   = []

        # Add actions to actions group.

        for i in range(len(basenames)):
        
            menu_name  = 'recent-menu-%d' % i
            menu_label = '%d. %s' % (i + 1, basenames[i])
            tooltip    = _('Open "%s"') % basenames[i]

            # Ellipsize too long menu item names.
            if len(menu_label) > 50:
                menu_label = menu_label[:50] + '...'

            # Unaccelerate underscores.
            menu_label = menu_label.replace('_', '__')

            # Add an underscore accelerator to the first 9 files.
            if i < 9:
                menu_label = '_' + menu_label

            menu_actions.append((
                menu_name, None, menu_label, None, tooltip,
                self.on_recent_file_activated
            ))

            ob_name  = 'recent-ob-%d' % i
            ob_label = basenames[i]

            # Unaccelerate underscores.
            ob_label = ob_label.replace('_', '__')

            # Ellipsize too long menu item names.
            if len(ob_label) > 80:
                ob_label = ob_label[:80] + '...'

            ob_actions.append((
                ob_name, None, ob_label, None, tooltip,
                self.on_recent_file_activated
            ))

        action_group.add_actions(menu_actions, None)
        action_group.add_actions(ob_actions  , None)

        self.uim.insert_action_group(action_group, -1)

        # Add action items to menu.

        ui_start = '''
        <ui>
            <menubar>
                <menu action="file">
                    <placeholder name="recent">'''
        ui_middle = '''
                    </placeholder>
                </menu>
            </menubar>
            <popup name="recent_popup">'''
        ui_end = '''
            </popup>
        </ui>'''

        for i in range(len(basenames)):
            ui_start  += '<menuitem action="recent-menu-%d"/>' % i
            ui_middle += '<menuitem action="recent-ob-%d"/>'   % i

        ui = ui_start + ui_middle + ui_end
        self.recent_uim_id = self.uim.add_ui_from_string(ui)
        self.open_button.set_menu(self.uim.get_widget('/ui/recent_popup'))

        for i in range(len(basenames)):

            # To get the message statusbar tooltips working, proxies need to be
            # connected.

            names = (
                '/ui/menubar/file/recent/recent-menu-%d' % i,
                '/ui/recent_popup/recent-ob-%d'          % i,
            )
            
            for name in names:
                action = self.uim.get_action(name)
                widget = self.uim.get_widget(name)
                action.connect_proxy(widget)
        
        self.set_menu_tooltips('recent')

    def _set_document_open(self):
        """Set GUI properties to suit main document open state."""

        is_open = bool(self.projects)

        uim_actions = [
            '/ui/menubar/file/import_translation',
            '/ui/menubar/file/save_as',
            '/ui/menubar/file/save_a_copy',
            '/ui/menubar/file/save_translation_as',
            '/ui/menubar/file/save_a_copy_of_translation',
            '/ui/menubar/file/close',
            '/ui/menubar/view/times',
            '/ui/menubar/view/frames',
            '/ui/menubar/view/columns',
            '/ui/menubar/documents/save_all',
            '/ui/menubar/documents/close_all',
            '/ui/menubar/documents/previous',
            '/ui/menubar/documents/next',
        ]

        for action in uim_actions:
            self.uim.get_action(action).set_sensitive(is_open)

        if is_open:
            self.ttips_open.enable()
        else:
            self.ttips_open.disable()
            self.set_status_message(None)
            self.window.set_title('Gaupol')
        
    def _set_main_document_changed(self, project):
        """Set GUI properties to suit main document changed state."""

        if project is None:
            is_changed = False
        else:
            is_changed = project.main_changed

        uim_actions = (
            '/ui/menubar/file/save',
        )
        
        for action in uim_actions:
            self.uim.get_action(action).set_sensitive(is_changed)

    def _set_main_file_exists(self, project):
        """Set GUI properties to suit main file exist state."""

        if project is None:
            exists = False
        else:
            exists = bool(project.data.main_file)
        
        name = '/ui/menubar/view/framerate'
        self.uim.get_action(name).set_sensitive(exists)
        
        self.fr_cmbox.set_sensitive(exists)
        gui.get_event_box(self.fr_cmbox).set_sensitive(exists)

    def set_menu_tooltips(self, action_group_name):
        """
        Set menu actions' tooltips to be displayed in the message statusbar.
        
        action_group_name: "main", "recent" or "documents"
        """
        action_group = self._get_action_group(action_group_name)
        
        actions = action_group.list_actions()
        for action in actions:
        
            widgets = action.get_proxies()
            for widget in widgets:
            
                widget.connect(
                    'enter-notify-event',
                    self._on_menu_action_enter_notify_event, action
                )
                widget.connect(
                    'leave-notify-event',
                    self._on_menu_action_leave_notify_event
                )

    def _set_revert_sensitivity(self, project):
        """Set sensitivity of revert menu item."""

        name = '/ui/menubar/file/revert'

        if project is None:
            self.uim.get_action(name).set_sensitive(False)
            return
        
        sensitive = False

        if project.main_changed and project.data.main_file is not None:
            sensitive = True
        if project.tran_changed and project.data.tran_file is not None:
            sensitive = True
            
        self.uim.get_action(name).set_sensitive(sensitive)

    def set_sensitivities_and_visiblities(self, project=None):
        """
        Set sensitivities and visibilities of GUI components.
        
        Sensitivities and visibilities of actions and widgets are set to suit
        the properties of project.

        project needs to be given when not setting the properties for the
        project currently active in the notebook.
        """
        project = project or self.get_current_project()

        self._set_document_open()
        self._set_main_document_changed(project)
        self._set_main_file_exists(project)
        self._set_revert_sensitivity(project)
        self._set_translation_document_changed(project)
        self._set_visibility_of_statusbars(project)

    def set_status_message(self, message, clear=True):
        """
        Set message to message statusbar.
        
        If message is None, statusbar will be cleared.
        Return: False (to clear statusbar only once with gobject.timeout_add)
        """
        self.msg_stbar.pop(0)

        # Stop previous vanishing event from affecting this new entry.
        if self.msg_stbar_gobj_tag is not None:
            gobject.source_remove(self.msg_stbar_gobj_tag)

        # Set tooltip
        event_box = gui.get_event_box(self.msg_stbar)
        self.ttips_open.set_tip(event_box, message)

        if message is None:
            return False

        self.msg_stbar.push(0, message)

        # Clear message after 5 seconds.
        if clear:
            self.msg_stbar_gobj_tag = \
                gobject.timeout_add(5000, self.set_status_message, None)

        return False

    def _set_translation_document_changed(self, project=None):
        """Set GUI properties to suit translation document changed state."""

        if project is None:
            is_changed = False
        else:
            is_changed = project.tran_changed

        uim_actions = (
            '/ui/menubar/file/save_translation',
        )
        
        for action in uim_actions:
            self.uim.get_action(action).set_sensitive(is_changed)

    def _set_visibility_of_statusbars(self, project=None):
        """Set visibility of the statusbars based on tree view columns."""

        if project is None:
            self.orig_stbar.hide()
            self.tran_stbar.hide()
            self.msg_stbar.set_has_resize_grip(True)
            return
        
        orig_visible = project.tree_view.get_column(ORIG).get_visible()
        tran_visible = project.tree_view.get_column(TRAN).get_visible()
        
        self.orig_stbar.set_property('visible', orig_visible)
        self.tran_stbar.set_property('visible', tran_visible)
        
        self.msg_stbar.set_has_resize_grip(False)
        self.orig_stbar.set_has_resize_grip(False)
        self.tran_stbar.set_has_resize_grip(False)

        if tran_visible:
             self.tran_stbar.set_has_resize_grip(True)
        else:
            if orig_visible:
                self.orig_stbar.set_has_resize_grip(True)
            else:
                self.msg_stbar.set_has_resize_grip(True)
