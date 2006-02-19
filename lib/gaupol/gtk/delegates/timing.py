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

from gaupol.constants             import Document, Mode
from gaupol.gtk.delegates         import Delegate, UIMAction
from gaupol.gtk.dialogs.adjust    import TimingAdjustDialog
from gaupol.gtk.dialogs.frconvert import FramerateConvertDialog
from gaupol.gtk.dialogs.shift     import TimingShiftDialog
from gaupol.gtk.dialogs.duration  import DurationAdjustDialog
from gaupol.gtk.util              import config, gtklib


class DurationAdjustAction(UIMAction):

    """Adjusting durations."""

    uim_action_item = (
        'adjust_durations',
        None,
        _('A_djust Durations'),
        'F4',
        _('Adjust duration lengths'),
        'on_adjust_durations_activated'
    )

    uim_paths = ['/ui/menubar/tools/adjust_durations']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return page is not None


class FramerateConvertAction(UIMAction):

    """Converting framerate."""

    uim_action_item = (
        'convert_framerate',
        gtk.STOCK_CONVERT,
        _('Con_vert Framerate'),
        'F5',
        _('Convert framerate'),
        'on_convert_framerate_activated'
    )

    uim_paths = ['/ui/menubar/tools/convert_framerate']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return page is not None

class TimingAdjustAction(UIMAction):

    """Adjusting timings."""

    uim_action_item = (
        'adjust_timings',
        None,
        _('_Adjust Timings'),
        'F3',
        _('Adjust timings by two-point correction'),
        'on_adjust_timings_activated'
    )

    uim_paths = ['/ui/menubar/tools/adjust_timings']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return page is not None


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

    def on_adjust_durations_activated(self, *args):
        """Adjust duration lengths."""

        page = self.get_current_page()

        dialog = DurationAdjustDialog(self.window, page)
        response = dialog.run()

        kwargs = {}

        if dialog.get_all_projects():
            pages = self.pages
        else:
            pages = [page]

        if not dialog.get_all_subtitles():
            kwargs['rows'] = page.view.get_selected_rows()

        kwargs['optimal']  = dialog.get_optimal()
        kwargs['lengthen'] = dialog.get_lengthen()
        kwargs['shorten']  = dialog.get_shorten()

        if dialog.get_use_maximum():
            kwargs['maximum'] = dialog.get_maximum()
        if dialog.get_use_minimum():
            kwargs['minimum'] = dialog.get_minimum()
        if dialog.get_use_gap():
            kwargs['gap'] = dialog.get_gap()

        dialog.destroy()

        if response != gtk.RESPONSE_OK:
            return

        for entry in pages:
            self.notebook.set_current_page(self.pages.index(entry))
            rows = entry.project.adjust_durations(**kwargs)
            entry.view.select_rows(rows)
            self.set_sensitivities(entry)

    def on_adjust_timings_activated(self, *args):
        """Adjust timings by two-point correction"""

        page = self.get_current_page()

        if page.edit_mode == Mode.TIME:
            method = page.project.adjust_times
        elif page.edit_mode == Mode.FRAME:
            method = page.project.adjust_frames

        def get_rows(adjust_all):
            if adjust_all:
                return None
            else:
                return page.view.get_selected_rows()

        def on_preview(dialog, row):
            point_1 = dialog.get_first_point()
            point_2 = dialog.get_second_point()
            rows = get_rows(dialog.get_adjust_all())
            args = rows, point_1, point_2
            self.preview_changes(page, row, Document.MAIN, method, args)

        dialog = TimingAdjustDialog(self.window, page)
        dialog.connect('preview', on_preview)
        response = dialog.run()
        point_1 = dialog.get_first_point()
        point_2 = dialog.get_second_point()
        adjust_all = dialog.get_adjust_all()
        gtklib.destroy_gobject(dialog)

        if response != gtk.RESPONSE_OK:
            return

        rows = get_rows(adjust_all)
        method(rows, point_1, point_2)
        self.set_sensitivities(page)

    def on_convert_framerate_activated(self, *args):
        """Convert framerate."""

        page = self.get_current_page()
        method = page.project.convert_framerate

        def on_preview(dialog):
            current = dialog.get_current_framerate()
            correct = dialog.get_correct_framerate()
            args = current, correct
            self.preview_changes(page, 0, Document.MAIN, method, args)

        dialog = FramerateConvertDialog(self.window, page)
        dialog.connect('preview', on_preview)
        response = dialog.run()
        all_projects = dialog.get_convert_all_projects()
        current = dialog.get_current_framerate()
        correct = dialog.get_correct_framerate()
        gtklib.destroy_gobject(dialog)

        if response != gtk.RESPONSE_OK:
            return

        if all_projects:
            pages = self.pages
        else:
            pages = [page]

        for entry in pages:
            entry.project.convert_framerate(current, correct)
        self.set_sensitivities(page)

    def on_shift_timings_activated(self, *args):
        """Shift timings a constant amount."""

        page = self.get_current_page()

        if page.edit_mode == Mode.TIME:
            method = page.project.shift_seconds
        elif page.edit_mode == Mode.FRAME:
            method = page.project.shift_frames

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
            args = rows, amount
            self.preview_changes(page, row, Document.MAIN, method, args)

        dialog = TimingShiftDialog(self.window, page)
        dialog.connect('preview', on_preview)
        response = dialog.run()
        amount = dialog.get_amount()
        shift_all = dialog.get_shift_all()
        gtklib.destroy_gobject(dialog)

        if response != gtk.RESPONSE_OK:
            return

        rows = get_rows(shift_all)[1]
        method(rows, amount)
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

            self.application.on_adjust_durations_activated()
            self.application.on_adjust_timings_activated()
            self.application.on_convert_framerate_activated()
            self.application.on_shift_timings_activated()

    TestTimingDelegate().run()
