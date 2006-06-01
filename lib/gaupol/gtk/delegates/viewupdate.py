# Copyright (C) 2005 Osmo Salomaa
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


"""View updating."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.gtk.colcons import *
from gaupol.gtk.cons import *
from gaupol.gtk.delegates import Delegate


test_label = gtk.Label()


class ViewUpdateDelegate(Delegate):

    """View updating."""

    def on_view_button_press_event(self, view, event):
        """
        Build the right-click menu.

        Return True to stop other handlers or False to not to.
        """
        if event.button != 3:
            return False

        x = int(event.x)
        y = int(event.y)
        try:
            row, tree_view_column, x, y = view.get_path_at_pos(x, y)
        except TypeError:
            return False

        # Move focus if user right-clicked outside the selection.
        if row[0] not in view.get_selected_rows():
            view.set_cursor(row, tree_view_column)
            view.grab_focus()
            view.set_active_column()
        # If user right-clicked in the selection, the focus cannot be moved,
        # because moving focus always changes selection as well and rebuilding
        # a lost selection would be far too slow and awkward.

        menu = self.uim.get_widget('/ui/view')
        menu.popup(None, None, None, event.button, event.time)
        return True

    def on_view_move_cursor_event(self, *args):
        """Update GUI after cursor has moved in the view."""

        page = self.get_current_page()
        page.view.set_active_column()
        self.set_sensitivities(page)

    def on_view_selection_changed_event(self, *args):
        """Update GUI after the view's selection has changed."""

        page = self.get_current_page()
        page.view.set_active_column()
        self.set_sensitivities(page)
        self.set_character_status(page)

    def set_character_status(self, page):
        """Set character lengths info to statusbars."""

        self.main_statusbar.pop(0)
        self.tran_statusbar.pop(0)
        if page is None:
            return

        # Single row must be selected.
        rows = page.view.get_selected_rows()
        if len(rows) != 1:
            return
        row = rows[0]

        def set_status(statusbar, document):

            try:
                info = page.project.get_character_count(row, document)
                lengths, total = info
            except IndexError:
                return

            lengths = list(str(length) for length in lengths)
            message = '+'.join(lengths)
            if len(lengths) > 1:
                message += '=%d' % total
            statusbar.push(0, message)

            test_label.set_text(message)
            width = test_label.size_request()[0] + 12
            if statusbar.get_has_resize_grip():
                width += statusbar.size_request()[1]
            width = max(100, width)
            statusbar.set_size_request(width, -1)

        if self.main_statusbar.props.visible:
            set_status(self.main_statusbar, Document.MAIN)
        if self.tran_statusbar.props.visible:
            set_status(self.tran_statusbar, Document.TRAN)


if __name__ == '__main__':

    from gaupol.gtk.application  import Application
    from gaupol.gtk.cons import *
    from gaupol.test             import Test

    class TestViewUpdateDelegate(Test):

        def __init__(self):

            Test.__init__(self)
            self.application = Application()
            self.application.open_main_files([self.get_subrip_path()])

        def destroy(self):

            self.application.window.destroy()

        def test_actions(self):

            page = self.application.get_current_page()
            page.view.set_focus(1, MTXT)

            self.application.on_view_move_cursor_event()
            self.application.on_view_selection_changed_event()
            self.application.set_character_status(page)

    TestViewUpdateDelegate().run()
