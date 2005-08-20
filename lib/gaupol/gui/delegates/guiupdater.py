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


"""GUI component state updating."""


import os

try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk

from gaupol.constants import FRAMERATE, MODE
from gaupol.gui.cellrend.multiline import CellRendererMultilineText
from gaupol.gui.colcons import *
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.util import gui


class GUIUpdater(Delegate):

    """GUI component state updating."""

    def _get_action_group(self, name):
        """
        Get action group from UIManager.
        
        name: "main", "recent", "documents" or "undo_redo"
        """
        action_groups = self.uim.get_action_groups()
        action_group_names = [group.get_name() for group in action_groups]
        index = action_group_names.index(name)

        return action_groups[index]

    def on_document_toggled(self, some_action, new_action):
        """Switch page in notebook."""

        index = int(new_action.get_name().split('-')[-1])
        self.notebook.set_current_page(index)
    
    def _on_menu_item_enter_notify_event(self, item, event, action):
        """Set GUI properties when mouse moves over item."""

        message = action.get_property('tooltip')
        self.set_status_message(message, False)
        
        # Set selections for undo and redo menu items.

        name = action.get_name()
        prefix = name[:5]
                
        if prefix not in ['undo-', 'redo-']:
            return
        
        part = name[:4]
        index = int(name.split('-')[-1])

        for i in range(index):
            path = '/ui/%s_popup/%s-%d' % (part, part, i)
            self.uim.get_widget(path).set_state(gtk.STATE_PRELIGHT)

    def _on_menu_item_leave_notify_event(self, item, event, action):
        """Set GUI properties when mouse moves away from item."""

        self.set_status_message(None)

        # Set selections for undo and redo menu items.

        name = action.get_name()
        prefix = name[:5]
                
        if prefix not in ['undo-', 'redo-']:
            return
        
        part = name[:4]
        index = int(name.split('-')[-1])

        for i in range(index):
            path = '/ui/%s_popup/%s-%d' % (part, part, i)
            self.uim.get_widget(path).set_state(gtk.STATE_NORMAL)

    def on_next_activated(self, *args):
        """Switch to next page in notebook."""
        
        self.notebook.next_page()

    def on_notebook_page_switched(self, notebook, pointer, new_page):
        """Adjust GUI properties to suit the project switched to."""

        if not self.projects:
            return

        project = self.projects[new_page]
        self.set_sensitivities(project)

        project.tree_view.grab_focus()

    def on_previous_activated(self, *args):
        """Switch to previous page in notebook."""
        
        self.notebook.prev_page()

    def on_tree_view_button_press_event(self, project, event):
        """
        Display a menu on TreeView right-click.
        
        Return: True or False
        """
        # True is returned to stop other handlers or False to not to.

        if event.button != 3:
            return False

        x = int(event.x)
        y = int(event.y)
        path_info = project.tree_view.get_path_at_pos(x, y)

        if path_info is None:
            return False

        row, tree_view_column, x, y = path_info
        selected_rows = project.get_selected_rows()

        # Row is a one-tuple. Make that an integer.
        row = row[0]

        # Move focus if user right-clicked outside the selection.
        if row not in selected_rows:

            project.tree_view.set_cursor(row, tree_view_column)
            project.tree_view.grab_focus()
            project.set_active_column()

            self._set_edit_cell_sensitivity(project)
            self._set_row_operation_sensitivities(project)
            self._set_text_operation_sensitivities(project)
            self._set_character_status(project)

        # If user right-clicked in the selection, the focus cannot be moved,
        # because moving focus always changes selection as well.
        
        menu = self.uim.get_widget('/ui/tree_view_popup')
        menu.popup(None, None, None, event.button, event.time)

        return True

    def on_tree_view_cursor_moved(self, *args):
        """Update GUI properties when TreeView cursor has moved."""

        project = self.get_current_project()
        self._set_edit_cell_sensitivity(project)
        self._set_text_operation_sensitivities(project)
        
    def on_tree_view_selection_changed(self, *args):
        """Update GUI properties when TreeView selection has changed."""

        project = self.get_current_project()
        self._set_edit_cell_sensitivity(project)
        self._set_row_operation_sensitivities(project)
        self._set_text_operation_sensitivities(project)
        self._set_character_status(project)

    def on_window_state_event(self, window, event):
        """Remember whether window is maximized or not."""

        state = event.new_window_state
        maximized = bool(state & gtk.gdk.WINDOW_STATE_MAXIMIZED)
        self.config.setboolean('application_window', 'maximized', maximized)

    def _refresh_documents_menu(self, project):
        """
        Refresh the list of open documents in the Documents menu.
        
        Documents' action names are "document-N", where N is an integer, which
        matches the project's index in projects list and the page index in the
        notebook.
        """
        if self.documents_uim_id is not None:
            self.uim.remove_ui(self.documents_uim_id)

        action_group = self._get_action_group('documents')
        self.uim.remove_action_group(action_group)
        action_group = gtk.ActionGroup('documents')
        
        if project is None:
            self.uim.insert_action_group(action_group, -1)
            return
            
        radio_actions = []

        # Add actions to action group.

        for i in range(len(self.projects)):
        
            basename  = self.projects[i].get_main_basename()
            tab_label = self.projects[i].tab_label.get_text()

            name     = 'document-%d' % i
            label    = '%d. %s' % (i + 1, tab_label)

            # TRANSLATORS: Activate a document - "Activate <basename>".
            tooltip  = _('Activate "%s"') % basename

            # Ellipsize too long menu item names.
            if len(label) > 50:
                label = label[:25] + '...' + label[-25:]

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

        ui_start = '''
        <ui>
            <menubar>
                <menu action="documents">
                    <placeholder name="open">'''
        ui_middle = ''
        ui_end    = '''
                    </placeholder>
                </menu>
            </menubar>
        </ui>'''

        for i in range(len(self.projects)):
            ui_middle += '<menuitem action="document-%d"/>' % i

        ui = ui_start + ui_middle + ui_end
        self.documents_uim_id = self.uim.add_ui_from_string(ui)

        for i in range(len(self.projects)):
        
            # To get the message statusbar tooltips working, proxies need to
            # be connected.
            path = '/ui/menubar/documents/open/document-%d' % i
            action = self.uim.get_action(path)
            widget = self.uim.get_widget(path)
            action.connect_proxy(widget)

        self.set_menu_notify_events('documents')

    def _refresh_recent_file_menus(self):
        """
        Refresh the list of recent files in the File and open button menus.
        
        Files' action names are "recent-menu-N" and "recent-open-button-N",
        where N is an integer, which matches the file's index in recent files
        list.
        """
        all_recent_files = self.config.getlist('file', 'recent_files')
        recent_files = []
        
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
        menu_actions        = []
        open_button_actions = []

        # Add actions to actions group.

        for i in range(len(basenames)):
        
            name    = 'recent-menu-%d' % i
            label   = '%d. %s' % (i + 1, basenames[i])

            # TRANSLATORS: Open a document - "Open <basename>".
            tooltip = _('Open "%s"') % basenames[i]

            # Ellipsize too long menu item names.
            if len(label) > 50:
                label = label[:25] + '...' + label[-25:]

            # Unaccelerate underscores.
            label = label.replace('_', '__')

            # Add an underscore accelerator to the first 9 files.
            if i < 9:
                label = '_' + label

            menu_actions.append((
                name, None, label, None, tooltip,
                self.on_recent_file_activated
            ))

            name  = 'recent-open-button-%d' % i
            label = basenames[i]

            # Unaccelerate underscores.
            label = label.replace('_', '__')

            # Ellipsize too long menu item names.
            if len(label) > 100:
                label = label[:50] + '...' + label[-50:]

            open_button_actions.append((
                name, None, label, None, tooltip,
                self.on_recent_file_activated
            ))

        action_group.add_actions(menu_actions         , None)
        action_group.add_actions(open_button_actions  , None)

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
            ui_start  += '<menuitem action="recent-menu-%d"/>'          % i
            ui_middle += '<menuitem action="recent-open-button-%d"/>'   % i

        ui = ui_start + ui_middle + ui_end
        self.recent_uim_id = self.uim.add_ui_from_string(ui)
        self.open_button.set_menu(self.uim.get_widget('/ui/recent_popup'))

        for i in range(len(basenames)):

            # To get the message statusbar tooltips working, proxies need to
            # be connected.

            names = (
                '/ui/menubar/file/recent/recent-menu-%d' % i,
                '/ui/recent_popup/recent-open-button-%d' % i
            )
            
            for name in names:
                action = self.uim.get_action(name)
                widget = self.uim.get_widget(name)
                action.connect_proxy(widget)
        
        self.set_menu_notify_events('recent')

    def _refresh_undo_and_redo_menus(self, project):
        """
        Refresh the list of action in the undo and redo button menus.
        
        Action names are "undo-N" and "redo-N", where N is an integer, which
        matches the action's index in project.undoables or project.redoables
        list.
        """
        if self.undo_redo_uim_id is not None:
            self.uim.remove_ui(self.undo_redo_uim_id)

        action_group = self._get_action_group('undo_redo')
        self.uim.remove_action_group(action_group)
        action_group = gtk.ActionGroup('undo_redo')

        if project is None:
            self.uim.insert_action_group(action_group, -1)
            self.undo_button.set_menu(gtk.Menu())
            self.redo_button.set_menu(gtk.Menu())
            return
        
        undo_actions = []
        redo_actions = []

        # Add actions to actions group.

        for i in range(len(project.undoables)):
        
            name    = 'undo-%d' % i
            label   = project.undoables[i].description
            tooltip = _('Undo up to %s') % project.undoables[i].description
            
            # Unaccelerate underscores.
            label = label.replace('_', '__')

            undo_actions.append((
                name, None, label, None, tooltip, self.on_undo_item_activated
            ))

        for i in range(len(project.redoables)):
        
            name    = 'redo-%d' % i
            label   = project.redoables[i].description
            tooltip = _('Redo up to %s') % project.redoables[i].description

            # Unaccelerate underscores.
            label = label.replace('_', '__')

            redo_actions.append((
                name, None, label, None, tooltip, self.on_redo_item_activated
            ))

        action_group.add_actions(undo_actions, None)
        action_group.add_actions(redo_actions, None)

        self.uim.insert_action_group(action_group, -1)

        # Add action items to menu.

        ui_undo  = '''
        <ui>
            <popup name="undo_popup">'''
        ui_redo  = '''
            </popup>
            <popup name="redo_popup">'''
        ui_close = '''
            </popup>
        </ui>'''

        for i in range(len(project.undoables)):
            ui_undo += '<menuitem action="undo-%d"/>' % i

        for i in range(len(project.redoables)):
            ui_redo += '<menuitem action="redo-%d"/>' % i

        ui = ui_undo + ui_redo + ui_close
        self.undo_redo_uim_id = self.uim.add_ui_from_string(ui)
            
        self.undo_button.set_menu(self.uim.get_widget('/ui/undo_popup'))
        self.redo_button.set_menu(self.uim.get_widget('/ui/redo_popup'))

        # To get the message statusbar tooltips working, proxies need to be
        # connected.

        for i in range(len(project.undoables)):
            name = '/ui/undo_popup/undo-%d' % i
            action = self.uim.get_action(name)
            widget = self.uim.get_widget(name)
            action.connect_proxy(widget)

        for i in range(len(project.redoables)):
            name = '/ui/redo_popup/redo-%d' % i
            action = self.uim.get_action(name)
            widget = self.uim.get_widget(name)
            action.connect_proxy(widget)

        # Set tooltips.

        if project.undoables:
            tip = _('Undo %s') % project.undoables[0].description
            self.undo_button.set_tooltip(self.tooltips, tip)
            action = self.uim.get_action('/ui/menubar/edit/undo')
            action.set_property('tooltip', tip)

        if project.redoables:
            tip = _('Redo %s') % project.redoables[0].description
            self.redo_button.set_tooltip(self.tooltips, tip)
            action = self.uim.get_action('/ui/menubar/edit/redo')
            action.set_property('tooltip', tip)
        
        self.set_menu_notify_events('undo_redo')

    def _set_character_status(self, project):
        """Set charcter length info to statusbar."""

        # Remove existing messages.
        self.text_statusbar.pop(0)
        self.tran_statusbar.pop(0)

        if project is None:
            return
        
        # Single row must be selected.
        selection = project.tree_view.get_selection()
        if selection.count_selected_rows() != 1:
            return

        row = project.get_selected_rows()[0]
        statusbars = [self.text_statusbar, self.tran_statusbar]

        for i in range(2):
        
            statusbar = statusbars[i]
            
            try:
                lengths, total = project.data.get_character_count(row, i)
            except IndexError:
                return
            lengths = [str(length) for length in lengths]
            message = '+'.join(lengths) + '=' + str(total)

            statusbar.push(0, message)
            
            # Get width required to display message.
            label = gtk.Label(message)
            width = label.size_request()[0]

            # Account 12 pixels for general extra (paddings, borders, etc)
            # and height for resize grip.
            new_width = width + 12
            if statusbar.get_has_resize_grip():
                new_width += statusbar.size_request()[1]
            new_width = max(100, new_width)
            
            statusbar.set_size_request(new_width, -1)

    def _set_current_document(self, project):
        """Set GUI properties to suit current document."""

        prev_action = self.uim.get_action('/ui/menubar/documents/previous')
        next_action = self.uim.get_action('/ui/menubar/documents/next')

        if project is None:
            prev_action.set_sensitive(False)
            next_action.set_sensitive(False)
            return

        project_index = self.projects.index(project)

        sensitive = bool(project_index != 0)
        prev_action.set_sensitive(sensitive)
        
        sensitive = bool(project_index != len(self.projects) - 1)
        next_action.set_sensitive(sensitive)

        title = project.set_tab_labels()
        self.window.set_title(title)
        
        edit_mode_name = MODE.NAMES[project.edit_mode]
        framerate_name = FRAMERATE.NAMES[project.data.framerate]

        uim_paths = (
            '/ui/menubar/view/%ss' % edit_mode_name,
            '/ui/menubar/view/framerate/%s' % framerate_name,
            '/ui/menubar/documents/open/document-%d' % project_index,
        )
        
        for path in uim_paths:
            self.uim.get_action(path).set_active(True)

        self.framerate_combo_box.set_active(project.data.framerate)

        for i in range(len(COLUMN.NAMES)):
            tree_view_column = project.tree_view.get_column(i)
            visible = tree_view_column.get_property('visible')
            path = '/ui/menubar/view/columns/%s' % COLUMN.NAMES[i]
            self.uim.get_action(path).set_active(visible)

    def _set_document_open(self):
        """Set GUI properties to suit whether a document is open or not."""

        is_open = bool(self.projects)

        uim_paths = (
            '/ui/menubar/file/import_translation',
            '/ui/menubar/file/save_as',
            '/ui/menubar/file/save_a_copy',
            '/ui/menubar/file/save_translation_as',
            '/ui/menubar/file/save_a_copy_of_translation',
            '/ui/menubar/file/close',
            '/ui/menubar/edit/select_all',
            '/ui/menubar/edit/unselect_all',
            '/ui/menubar/edit/invert_selection',
            '/ui/menubar/view/times',
            '/ui/menubar/view/frames',
            '/ui/menubar/view/columns',
            '/ui/menubar/documents/save_all',
            '/ui/menubar/documents/close_all',
        )

        for path in uim_paths:
            self.uim.get_action(path).set_sensitive(is_open)

        if is_open:
            self.tooltips.enable()
        else:
            self.tooltips.disable()
            self.set_status_message(None)
            self.window.set_title('Gaupol')

    def _set_edit_cell_sensitivity(self, project):
        """Set sensitivity of "Edit" action."""
        
        action = self.uim.get_action('/ui/menubar/edit/edit_cell')

        if project is None:
            action.set_sensitive(False)
            return

        # A cell must have focus.
        row, col = project.get_focus()[:2]
        if row is not None and col is not None:
            action.set_sensitive(True)
        else:
            action.set_sensitive(False)

    def _set_file_sensitivities(self, project):
        """Set file action properties to suit main document state."""
        
        if project is None:
            main_changed = False
            tran_changed = False
            tran_active = False
            main_file = None
            tran_file = None
        else:
            main_changed = bool(project.main_changed)
            tran_changed = bool(project.tran_changed)
            tran_active = project.tran_active
            main_file = project.data.main_file
            tran_file = project.data.tran_file
            
        path = '/ui/menubar/file/save'
        self.uim.get_action(path).set_sensitive(main_changed)

        path = '/ui/menubar/file/save_translation'
        self.uim.get_action(path).set_sensitive(tran_active and tran_changed)

        # Revert sensitivity.
        if main_changed and main_file is not None:
            sensitive = True
        elif tran_active and tran_changed and tran_file is not None:
            sensitive = True
        else:
            sensitive = False
            
        path = '/ui/menubar/file/revert'
        self.uim.get_action(path).set_sensitive(sensitive)

    def _set_format_sensitivities(self, project):
        """Set sensitivities of text formatting actions."""

        uim_paths = (
            '/ui/menubar/format/dialog',
            '/ui/menubar/format/italic',
            '/ui/menubar/format/case',
            '/ui/menubar/format/case/title',
            '/ui/menubar/format/case/sentence',
            '/ui/menubar/format/case/upper',
            '/ui/menubar/format/case/lower',
        )

        if project is None:
            for path in uim_paths:
                self.uim.get_action(path).set_sensitive(False)
            return

        selection = project.tree_view.get_selection()
        selected_count = selection.count_selected_rows()
        col = project.get_focus()[1]

        sensitive = True

        # Something must be selected.
        if selected_count == 0:
            sensitive = False

        # A text column must have focus and file format must be known.
        if col == TEXT:
            if project.data.main_file is None:
                sensitive = False
        elif col == TRAN:
            if project.data.tran_file is None:
                if project.data.main_file is None:
                    sensitive = False
        else:
            sensitive = False

        for path in uim_paths:
            self.uim.get_action(path).set_sensitive(sensitive)

    def _set_framerate_sensitivities(self, project):
        """Set sensitivities of framerate widgets and actions."""

        if project is None:
            exists = False
        else:
            exists = bool(project.data.main_file)

        path = '/ui/menubar/view/framerate'
        self.uim.get_action(path).set_sensitive(exists)
        
        self.framerate_combo_box.set_sensitive(exists)
        gui.get_event_box(self.framerate_combo_box).set_sensitive(exists)

    def set_menu_notify_events(self, action_group_name):
        """
        Set GUI properties when mouse hovers over a menu item.
        
        action_group_name: "main", "recent", "documents" or "undo_redo"
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

    def _set_row_operation_sensitivities(self, project):
        """Set sensitivity of row-operating actions."""

        uim_paths = (
            '/ui/menubar/edit/insert_subtitles',
            '/ui/menubar/edit/remove_subtitles',
        )

        if project is None:
            sensitive = False
        
        else:

            # If not subtitles exist, inserting must be possible.
            if not project.data.times:
                self.uim.get_action(uim_paths[0]).set_sensitive(True)
                self.uim.get_action(uim_paths[1]).set_sensitive(False)
                return
                
            selection = project.tree_view.get_selection()
            selected_count = selection.count_selected_rows()
            sensitive = bool(selected_count > 0)

        for path in uim_paths:
            self.uim.get_action(path).set_sensitive(sensitive)

    def set_sensitivities(self, project=None):
        """
        Set sensitivities and visibilities of GUI components.
        
        Sensitivities and visibilities of actions and widgets are set to suit
        the properties of project.

        project needs to be given when not setting the properties for the
        project currently active in the notebook.
        """
        # TODO:
        # This is a method is a tradeoff gaining simple code and losing in
        # performance. Just about everything in the GUI is updated, which is
        # usually overkill. If in the future this is considered too costly
        # performance-wise, other modules can be made to directly call the
        # methods listed below.

        project = project or self.get_current_project()

        self._refresh_documents_menu(project)
        self._refresh_recent_file_menus()
        self._refresh_undo_and_redo_menus(project)

        self._set_character_status(project)
        self._set_current_document(project)
        self._set_document_open()
        self._set_edit_cell_sensitivity(project)
        self._set_file_sensitivities(project)
        self._set_framerate_sensitivities(project)
        self._set_row_operation_sensitivities(project)
        self._set_text_operation_sensitivities(project)
        self._set_undo_and_redo_sensitivities(project)
        self._set_visibility_of_statusbars(project)

    def set_status_message(self, message, clear=True):
        """
        Set message to message statusbar.
        
        If message is None, statusbar will be cleared.
        Return: False (to clear statusbar only once with gobject.timeout_add)
        """
        self.message_statusbar.pop(0)

        # Stop previous vanishing event from affecting this new entry.
        if self.message_tag is not None:
            gobject.source_remove(self.message_tag)

        # Set tooltip
        event_box = gui.get_event_box(self.message_statusbar)
        self.tooltips.set_tip(event_box, message)

        if message is None:
            return False

        self.message_statusbar.push(0, message)

        # Clear message after 5 seconds.
        if clear:
            method = self.set_status_message
            self.message_tag = gobject.timeout_add(5000, method, None)

        return False

    def _set_text_edit_sensitivities(self, project):
        """Set sensitivities of text editing actions."""

        uim_paths = (
            '/ui/menubar/edit/clear',
            '/ui/menubar/edit/copy',
            '/ui/menubar/edit/cut',
            '/ui/menubar/edit/paste',
        )

        if project is None:
            for path in uim_paths:
                self.uim.get_action(path).set_sensitive(False)
            return

        selection = project.tree_view.get_selection()
        selected_count = selection.count_selected_rows()
        col = project.get_focus()[1]

        sensitive = True

        # Something must be selected.
        if selected_count == 0:
            sensitive = False

        # A text column must have focus.
        if col not in [TEXT, TRAN]:
            sensitive = False

        for path in uim_paths:
            self.uim.get_action(path).set_sensitive(sensitive)

        # Paste action requires something on the clipboard.
        if self.clipboard.data is None:
            path = '/ui/menubar/edit/paste'
            self.uim.get_action(path).set_sensitive(False)

    def _set_text_operation_sensitivities(self, project):
        """Set sensitivities of text-operating actions."""

        self._set_format_sensitivities(project)
        self._set_text_edit_sensitivities(project)

    def _set_undo_and_redo_sensitivities(self, project):
        """Set sensitivities of undo and redo actions."""
        
        if project is None:
            undoable = False
            redoable = False
        else:
            undoable = bool(project.undoables)
            redoable = bool(project.redoables)

        self.uim.get_action('/ui/menubar/edit/undo').set_sensitive(undoable)
        self.uim.get_action('/ui/menubar/edit/redo').set_sensitive(redoable)

        self.undo_button.set_sensitive(undoable)
        self.redo_button.set_sensitive(redoable)

    def _set_visibility_of_statusbars(self, project):
        """Set visibility of the statusbars based on tree view columns."""

        if project is None:
            self.text_statusbar.hide()
            self.tran_statusbar.hide()
            self.message_statusbar.set_has_resize_grip(True)
            return
        
        text_visible = project.tree_view.get_column(TEXT).get_visible()
        tran_visible = project.tree_view.get_column(TRAN).get_visible()
        
        self.text_statusbar.set_property('visible', text_visible)
        self.tran_statusbar.set_property('visible', tran_visible)
        
        if tran_visible:
            self.message_statusbar.set_has_resize_grip(False)
            self.text_statusbar.set_has_resize_grip(False)
            self.tran_statusbar.set_has_resize_grip(True)
        else:
            if text_visible:
                self.message_statusbar.set_has_resize_grip(False)
                self.text_statusbar.set_has_resize_grip(True)
                self.tran_statusbar.set_has_resize_grip(False)
            else:
                self.message_statusbar.set_has_resize_grip(True)
                self.text_statusbar.set_has_resize_grip(False)
                self.tran_statusbar.set_has_resize_grip(False)
