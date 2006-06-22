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


"""Updating view."""


import gtk

from gaupol.gtk.colcons  import *
from gaupol.gtk.delegate import Delegate


_TEST_LABEL = gtk.Label()


class ViewUpdateDelegate(Delegate):

    """Updating view."""

    def on_view_button_press_event(self, view, event):
        """
        Display pop-up menu.

        Return True to stop other handlers or False to not to.
        """
        if event.button != 3:
            return False
        x = int(event.x)
        y = int(event.y)
        try:
            row, column, x, y = view.get_path_at_pos(x, y)
        except TypeError:
            return False

        # Move focus if user clicked outside the selection.  If user
        # right-clicked in the selection, the focus cannot be moved, because
        # moving focus always changes selection as well and rebuilding a lost
        # selection would be far too slow and awkward.
        if row[0] not in view.get_selected_rows():
            view.set_cursor(row, column)
            view.grab_focus()
            view.set_focus_column()

        menu = self._uim.get_widget('/ui/view')
        menu.popup(None, None, None, event.button, event.time)
        return True

    def on_view_move_cursor(self, *args):
        """Update GUI after moving cursor."""

        page = self.get_current_page()
        page.view.set_focus_column()
        self.set_sensitivities(page)

    def on_view_selection_changed(self, *args):
        """Update GUI after changing selection."""

        page = self.get_current_page()
        page.view.set_focus_column()
        self.set_sensitivities(page)
        self.set_character_status(page)

    def set_character_status(self, page):
        """Update line lengths in statusbar."""

        self._main_statusbar.pop(0)
        self._tran_statusbar.pop(0)
        if page is None:
            return

        rows = page.view.get_selected_rows()
        if len(rows) != 1:
            return
        row = rows[0]

        def set_status(statusbar, doc):
            try:
                lengths = page.project.get_line_lengths(row, doc)
            except IndexError:
                return
            message = '/'.join(list(str(x) for x in lengths))
            statusbar.push(0, message)
            _TEST_LABEL.set_text(message)
            width = _TEST_LABEL.size_request()[0] + 12
            if statusbar.get_has_resize_grip():
                width += statusbar.size_request()[1]
            statusbar.set_size_request(max(60, width), -1)

        if self._main_statusbar.props.visible:
            set_status(self._main_statusbar, MAIN)
        if self._tran_statusbar.props.visible:
            set_status(self._tran_statusbar, TRAN)
