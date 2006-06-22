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


"""Updating application GUI."""


from gettext import gettext as _
import os

import gobject
import gtk

from gaupol.gtk          import cons
from gaupol.gtk.colcons  import *
from gaupol.gtk.delegate import Delegate, UIMAction, UIMActions
from gaupol.gtk.util     import config, gtklib


class ActivateNextProjectAction(UIMAction):

    """Activate next page in notebook."""

    action_item = (
        'activate_next_project',
        None,
        _('_Next'),
        '<control>Page_Down',
        _('Activate the project in the next tab'),
        'on_activate_next_project_activate'
    )

    paths = ['/ui/menubar/projects/next']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        try:
            app.pages[app.pages.index(page) + 1]
            return True
        except IndexError:
            return False


class ActivatePreviousProjectAction(UIMAction):

    """Activate previous page in notebook."""

    action_item = (
        'activate_previous_project',
        None,
        _('_Previous'),
        '<control>Page_Up',
        _('Activate the project in the previous tab'),
        'on_activate_previous_project_activate'
    )

    paths = ['/ui/menubar/projects/previous']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        return app.pages.index(page) > 0


class AppUpdateDelegate(Delegate):

    """
    Updating of application GUI.

    Instance variables:

        _message_id:  Message statusbar message ID
        _message_tag: Message statusbar GObject timeout tag

    """

    def __init__(self, *args, **kwargs):

        Delegate.__init__(self, *args, **kwargs)

        self._message_id  = None
        self._message_tag = None

    def _update_actions(self, page):
        """Set sensitivities of all actions for page."""

        for cls in UIMActions.classes:
            doable = cls.is_doable(self, page)
            for path in cls.paths:
                self._uim.get_action(path).set_sensitive(doable)
            for widget in cls.widgets:
                getattr(self, widget).set_sensitive(doable)

    def _update_revert(self, page):
        """Set tooltips for undo and redo."""

        if page is None:
            return

        if page.project.can_undo():
            description = page.project.undoables[0].description
            tip = _('Undo %s') % description[0].lower() + description[1:]
            self._undo_button.set_tooltip(self._tooltips, tip)
            self._uim.get_action('/ui/menubar/edit/undo').props.tooltip = tip

        if page.project.can_redo():
            description = page.project.redoables[0].description
            tip = _('Redo %s') % description[0].lower() + description[1:]
            self._redo_button.set_tooltip(self._tooltips, tip)
            self._uim.get_action('/ui/menubar/edit/redo').props.tooltip = tip

    def _update_statusbars(self, page):
        """Set visibilities of statusbars based on visible columns."""

        if page is None:
            self._main_statusbar.hide()
            self._tran_statusbar.hide()
            self._msg_statusbar.set_has_resize_grip(True)
            return

        main_visible = page.view.get_column(MTXT).get_visible()
        tran_visible = page.view.get_column(TTXT).get_visible()
        if main_visible == self._main_statusbar.props.visible and \
           tran_visible == self._tran_statusbar.props.visible:
            return
        self._main_statusbar.props.visible = main_visible
        self._tran_statusbar.props.visible = tran_visible

        def set_resize_grip(msg, main, tran):
            self._msg_statusbar.set_has_resize_grip(msg)
            self._main_statusbar.set_has_resize_grip(main)
            self._tran_statusbar.set_has_resize_grip(tran)

        if tran_visible:
            set_resize_grip(False, False, True)
        elif main_visible:
            set_resize_grip(False, True, False)
        else:
            set_resize_grip(True, False, False)

    def _update_widgets(self, page):
        """Set the states of various widgets."""

        if page is None:
            self._tooltips.disable()
            self._window.set_title('Gaupol')
            self._video_label.set_text('')
            self.set_status_message(None)
            return

        self._tooltips.enable()
        self._window.set_title(page.update_tab_labels())

        path = cons.Mode.uim_paths[page.edit_mode]
        self._uim.get_action(path).set_active(True)

        path = cons.Framerate.uim_paths[page.project.framerate]
        self._uim.get_action(path).set_active(True)
        self._framerate_combo.set_active(page.project.framerate)

        for i in range(len(cons.Column.uim_paths)):
            visible = page.view.get_column(i).props.visible
            path = cons.Column.uim_paths[i]
            self._uim.get_action(path).set_active(visible)

        if page.project.video_path is not None:
            basename = os.path.basename(page.project.video_path)
            self._video_label.set_text(basename)
        else:
            self._video_label.set_text('')
        self._tooltips.set_tip(self._video_button, page.project.video_path)

    def on_activate_next_project_activate(self, *args):
        """Switch to next page in notebook."""

        self._notebook.next_page()
        self._notebook.grab_focus()

    def on_activate_previous_project_activate(self, *args):
        """Switch to previous page in notebook."""

        self._notebook.prev_page()
        self._notebook.grab_focus()

    def on_notebook_switch_page(self, notebook, pointer, pageno):
        """Set GUI properties for page switched to."""

        if not self.pages:
            return
        page = self.pages[pageno]
        self.set_sensitivities(page)
        page.view.grab_focus()

    def on_project_toggled(self, unknown, action):
        """Switch page in notebook."""

        index = int(action.get_name().split('_')[-1])
        self._notebook.set_current_page(index)

    def on_window_window_state_event(self, window, event):
        """Save window maximization."""

        state = event.new_window_state
        maximized = bool(state & gtk.gdk.WINDOW_STATE_MAXIMIZED)
        config.application_window.maximized = maximized

    def set_sensitivities(self, page=None):
        """Set sensitivities and visibilities of actions and widgets."""

        page = page or self.get_current_page()
        self._update_widgets(page)
        self._update_statusbars(page)
        self._update_actions(page)
        self._update_revert(page)

    def set_status_message(self, message, clear=True):
        """
        Set message to message statusbar.

        message: None to clear
        Return False to avoid iteration with gobject.timeout_add.
        """
        if self._message_tag is not None:
            gobject.source_remove(self._message_tag)
        if self._message_id is not None:
            self._msg_statusbar.remove(0, self._message_id)

        try:
            event_box = gtklib.get_event_box(self._msg_statusbar)
            self._tooltips.set_tip(event_box, message)
        except AttributeError:
            pass

        if message is None:
            return False

        self._message_id = self._msg_statusbar.push(0, message)
        if clear:
            self._message_tag = gobject.timeout_add(
                6000, self.set_status_message, None)
        return False
