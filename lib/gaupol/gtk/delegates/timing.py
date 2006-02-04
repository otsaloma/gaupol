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


"""Shifting, adjusting and fixing timings."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _

import gtk

from gaupol.constants         import Document, Mode
from gaupol.gtk.delegates     import Delegate, UIMAction
from gaupol.gtk.dialogs.shift import TimingShiftDialog
from gaupol.gtk.util          import config, gtklib


class TimingShiftAction(UIMAction):

    """Shifting timings."""

    uim_action_item = (
        'shift_timings',
        None,
        _('_Shift Timings'),
        'F2',
        _('Shift timings a constant amount'),
        'on_shift_timings_activated'
    )

    uim_paths = ['/ui/menubar/tools/shift_timings']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return page is not None


class TimingDelegate(Delegate):

    """Shifting, adjusting and fixing timings."""

    def on_shift_timings_activated(self, *args):
        """Shift timings a constant amount."""

        page = self.get_current_page()

        def get_rows(shift_all):
            if shift_all:
                return 0, None
            else:
                rows = page.view.get_selected_rows()
                row  = rows[0]
                return row, rows

        def on_preview(dialog):
            amount = dialog.get_amount()
            row, rows = get_rows(dialog.get_shift_all())
            if page.edit_mode == Mode.TIME:
                method = page.project.shift_seconds
            elif page.edit_mode == Mode.FRAME:
                method = page.project.shift_frames
            args = rows, amount
            self.preview_changes(page, row, Document.MAIN, method, args)

        dialog = TimingShiftDialog(self.window, page)
        dialog.connect('preview', on_preview)
        response  = dialog.run()
        amount    = dialog.get_amount()
        shift_all = dialog.get_shift_all()
        gtklib.destroy_gobject(dialog)

        if response != gtk.RESPONSE_OK:
            return

        rows = get_rows(dialog.get_shift_all())[1]
        if page.edit_mode == Mode.TIME:
            page.project.shift_seconds(rows, amount)
        elif page.edit_mode == Mode.FRAME:
            page.project.shift_frames(rows, amount)

        self.set_sensitivities(page)


if __name__ == '__main__':

    from gaupol.gtk.application import Application
    from gaupol.test            import Test

    class TestTimingDelegate(Test):

        def __init__(self):

            Test.__init__(self)
            self.application = Application()
            self.application.open_main_files([self.get_subrip_path()])

        def destroy(self):

            self.application.window.destroy()

        def test_callbacks(self):

            self.application.on_shift_timings_activated()

    TestTimingDelegate().run()

