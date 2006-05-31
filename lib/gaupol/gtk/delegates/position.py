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


"""Shifting, adjusting and fixing mings."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _
from gettext import ngettext

import gtk

from gaupol.gtk.cons import *
from gaupol.gtk.delegates         import Delegate, UIMAction
from gaupol.gtk.dialogs.duradjust import DurationAdjustDialog
from gaupol.gtk.dialogs.frconvert import FramerateConvertDialog
from gaupol.gtk.dialogs.posadjust  import TimeFrameAdjustDialog
from gaupol.gtk.dialogs.posshift   import TimeFrameShiftDialog
from gaupol.gtk.util              import config, gtklib


class DurationAdjustAction(UIMAction):

    """Adjusting durations."""

    uim_action_item = (
        'adjust_durations',
        None,
        _('A_djust Durations'),
        'F4',
        _('Lengthen or shorten durations'),
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
        None,
        _('Convert framerate'),
        'on_convert_framerate_activated'
    )

    uim_paths = ['/ui/menubar/tools/convert_framerate']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False
        if page.project.main_file is None:
            return False

        return bool(page.project.main_file.format == Format.MICRODVD)


class TimeFrameAdjustAction(UIMAction):

    """Adjusting positions."""

    uim_action_item = (
        'adjust_positions',
        None,
        _('_Adjust Times'),
        'F3',
        _('Adjust times by linear two-point correction'),
        'on_adjust_positions_activated'
    )

    uim_paths = ['/ui/menubar/tools/adjust_positions']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return page is not None


class TimeFrameShiftAction(UIMAction):

    """Shifting positions."""

    uim_action_item = (
        'shift_positions',
        None,
        _('_Shift Times'),
        'F2',
        _('Make subtitles appear earlier or later'),
        'on_shift_positions_activated'
    )

    uim_paths = ['/ui/menubar/tools/shift_positions']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return page is not None


class TimeFrameDelegate(Delegate):

    """Shifting, adjusting and fixing positions."""

    def on_adjust_durations_activated(self, *args):
        """Adjust duration lengths."""

        page = self.get_current_page()
        dialog = DurationAdjustDialog(self.window, page)
        response = dialog.run()
        if response != gtk.RESPONSE_OK:
            dialog.destroy()
            return

        kwargs = {}
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

        if dialog.get_all_projects():
            pages = self.pages
        else:
            pages = [page]
        dialog.destroy()

        for page in pages:
            self.notebook.set_current_page(self.pages.index(page))
            rows = page.project.adjust_durations(**kwargs)
            page.view.select_rows(rows)
            length = len(rows)
            message = ngettext(
                'Adjusted duration of %d subtitle',
                'Adjusted durations of %d subtitles',
                length
            ) % length
            self.set_status_message(message)
            self.set_sensitivities(page)

    def on_adjust_positions_activated(self, *args):
        """Adjust positions by two-point correction"""

        page = self.get_current_page()
        if page.edit_mode == Mode.TIME:
            method = page.project.adjust_times
        elif page.edit_mode == Mode.FRAME:
            method = page.project.adjust_frames

        def get_rows(dialog):
            if dialog.get_adjust_all():
                return None
            else:
                return page.view.get_selected_rows()

        def on_preview(dialog, row):
            point_1 = dialog.get_first_point()
            point_2 = dialog.get_second_point()
            rows = get_rows(dialog)
            args = rows, point_1, point_2
            self.preview_changes(page, row, Document.MAIN, method, args)

        dialog = TimeFrameAdjustDialog(self.window, page)
        dialog.connect('preview', on_preview)
        response = dialog.run()
        if response != gtk.RESPONSE_OK:
            gtklib.destroy_gobject(dialog)
            return

        point_1 = dialog.get_first_point()
        point_2 = dialog.get_second_point()
        rows = get_rows(dialog)
        gtklib.destroy_gobject(dialog)

        method(rows, point_1, point_2)
        page.view.select_rows(rows or range(len(page.project.times)))
        self.set_sensitivities(page)

    def on_convert_framerate_activated(self, *args):
        """Convert framerate."""

        dialog = FramerateConvertDialog(self.window)
        response = dialog.run()
        if response != gtk.RESPONSE_OK:
            gtklib.destroy_gobject(dialog)
            return

        all_projects = dialog.get_convert_all_projects()
        current_fr = dialog.get_current_framerate()
        correct_fr = dialog.get_correct_framerate()
        gtklib.destroy_gobject(dialog)

        if all_projects:
            pages = self.pages
        else:
            pages = [self.get_current_page()]

        for page in pages:
            self.notebook.set_current_page(self.pages.index(page))
            page.project.convert_framerate(current_fr, correct_fr)
            page.view.select_rows(range(len(page.project.times)))
            self.set_sensitivities(page)

    def on_shift_positions_activated(self, *args):
        """Shift positions a constant amount."""

        page = self.get_current_page()
        if page.edit_mode == Mode.TIME:
            method = page.project.shift_seconds
        elif page.edit_mode == Mode.FRAME:
            method = page.project.shift_frames

        def get_rows(dialog):
            if dialog.get_shift_all():
                return None
            else:
                return page.view.get_selected_rows()

        def on_preview(dialog, row):
            amount = dialog.get_amount()
            rows = get_rows(dialog)
            args = rows, amount
            self.preview_changes(page, row, Document.MAIN, method, args)

        dialog = TimeFrameShiftDialog(self.window, page)
        dialog.connect('preview', on_preview)
        response = dialog.run()
        if response != gtk.RESPONSE_OK:
            gtklib.destroy_gobject(dialog)
            return

        amount = dialog.get_amount()
        rows = get_rows(dialog)
        gtklib.destroy_gobject(dialog)

        method(rows, amount)
        page.view.select_rows(rows or range(len(page.project.times)))
        self.set_sensitivities(page)


if __name__ == '__main__':

    from gaupol.gtk.application import Application
    from gaupol.test            import Test

    class TestTimeFrameDelegate(Test):

        def __init__(self):

            Test.__init__(self)
            self.application = Application()
            self.application.open_main_files([self.get_micro_dvd_path()])

        def destroy(self):

            self.application.window.destroy()

        def test_callbacks(self):

            self.application.on_adjust_durations_activated()
            self.application.on_adjust_positions_activated()
            self.application.on_convert_framerate_activated()
            self.application.on_shift_positions_activated()

    TestTimeFrameDelegate().run()
