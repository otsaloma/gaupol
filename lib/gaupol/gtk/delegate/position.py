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


"""Advanced editing of positions."""


from gettext import gettext as _
from gettext import ngettext

import gtk

from gaupol.gtk                  import cons
from gaupol.gtk.icons            import *
from gaupol.gtk.delegate         import Delegate, UIMAction
from gaupol.gtk.dialog.duradjust import DurationAdjustDialog
from gaupol.gtk.dialog.frconvert import FramerateConvertDialog
from gaupol.gtk.dialog.posadjust import FrameAdjustDialog, TimeAdjustDialog
from gaupol.gtk.dialog.posshift  import FrameShiftDialog, TimeShiftDialog
from gaupol.gtk.util             import gtklib


class AdjustDurationsAction(UIMAction):

    """Adjusting durations."""

    action_item = (
        'adjust_durations',
        None,
        _('Ad_just Durations...'),
        '',
        _('Lengthen or shorten durations'),
        'on_adjust_durations_activate'
    )

    paths = ['/ui/menubar/tools/adjust_durations']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return page is not None


class AdjustPositionsAction(UIMAction):

    """Adjusting positions."""

    action_item = (
        'adjust_positions',
        None,
        _('A_djust Positions...'),
        'F3',
        _('Adjust positions by linear two-point correction'),
        'on_adjust_positions_activate'
    )

    paths = ['/ui/menubar/tools/adjust_positions']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return page is not None


class ConvertFramerateAction(UIMAction):

    """Converting framerate."""

    action_item = (
        'convert_framerate',
        gtk.STOCK_CONVERT,
        _('Con_vert Framerate...'),
        None,
        _('Convert framerate'),
        'on_convert_framerate_activate'
    )

    paths = ['/ui/menubar/tools/convert_framerate']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        if page.project.main_file is None:
            return False
        return True


class ShiftPositionsAction(UIMAction):

    """Shifting positions."""

    action_item = (
        'shift_positions',
        None,
        _('S_hift Positions...'),
        'F2',
        _('Make subtitles appear earlier or later'),
        'on_shift_positions_activate'
    )

    paths = ['/ui/menubar/tools/shift_positions']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return page is not None


class PositionDelegate(Delegate):

    """Advanced editing of positions."""

    def get_target_pages(self, target):
        """Get list of pages corresponding to target."""

        if target == cons.Target.ALL:
            return self.pages
        if target == cons.Target.CURRENT:
            return [self.get_current_page()]
        if target == cons.Target.SELECTED:
            return [self.get_current_page()]

    def get_target_rows(self, target):
        """Get rows corresponding to target."""

        if target == cons.Target.ALL:
            return None
        if target == cons.Target.CURRENT:
            return None
        if target == cons.Target.SELECTED:
            page = self.get_current_page()
            return page.view.get_selected_rows()

    def on_adjust_durations_activate(self, *args):
        """Adjust durations."""

        page = self.get_current_page()
        has_selection = bool(page.view.get_selected_rows())
        dialog = DurationAdjustDialog(self._window, has_selection)
        response = dialog.run()
        if response != gtk.RESPONSE_OK:
            dialog.destroy()
            return

        kwargs = {}
        kwargs['optimal'] = dialog.get_optimal()
        kwargs['lengthen'] = dialog.get_lengthen()
        kwargs['shorten'] = dialog.get_shorten()
        if dialog.get_use_maximum():
            kwargs['maximum'] = dialog.get_maximum()
        if dialog.get_use_minimum():
            kwargs['minimum'] = dialog.get_minimum()
        if dialog.get_use_gap():
            kwargs['gap'] = dialog.get_gap()
        target = dialog.get_target()
        pages = self.get_target_pages(target)
        kwargs['rows'] = self.get_target_rows(target)
        dialog.destroy()

        for page in pages:
            self._notebook.set_current_page(self.pages.index(page))
            rows = page.project.adjust_durations(**kwargs)
            page.view.select_rows(rows)
            message = ngettext(
                'Adjusted duration of %d subtitle',
                'Adjusted durations of %d subtitles',
                len(rows)
            ) % len(rows)
            self.set_status_message(message)

    def on_adjust_positions_activate(self, *args):
        """Adjust positions by linear two-point correction"""

        page = self.get_current_page()
        if page.edit_mode == cons.Mode.TIME:
            dialog = TimeAdjustDialog(self._window, page)
            method = page.project.adjust_times
        elif page.edit_mode == cons.Mode.FRAME:
            dialog = FrameAdjustDialog(self._window, page)
            method = page.project.adjust_frames

        def on_preview(dialog, row):
            point_1 = dialog.get_first_point()
            point_2 = dialog.get_second_point()
            rows = self.get_target_rows(dialog.get_target())
            args = [rows, point_1, point_2]
            self.preview_changes(page, row, MAIN, method, args)

        dialog.connect('preview', on_preview)
        response = dialog.run()
        if response != gtk.RESPONSE_OK:
            gtklib.destroy_gobject(dialog)
            return

        point_1 = dialog.get_first_point()
        point_2 = dialog.get_second_point()
        rows = self.get_target_rows(dialog.get_target())
        gtklib.destroy_gobject(dialog)
        method(rows, point_1, point_2)
        page.view.select_rows(rows or range(len(page.project.times)))

    def on_convert_framerate_activate(self, *args):
        """Convert framerate."""

        dialog = FramerateConvertDialog(self._window)
        response = dialog.run()
        if response != gtk.RESPONSE_OK:
            gtklib.destroy_gobject(dialog)
            return

        target = dialog.get_target()
        pages = self.get_target_pages(target)
        rows = self.get_target_rows(target)
        current = dialog.get_current()
        correct = dialog.get_correct()
        gtklib.destroy_gobject(dialog)

        for page in pages:
            self._notebook.set_current_page(self.pages.index(page))
            page.project.convert_framerate(rows, current, correct)
            page.view.select_rows(rows or range(len(page.project.times)))

    def on_shift_positions_activate(self, *args):
        """Shift positions a constant amount."""

        page = self.get_current_page()
        if page.edit_mode == cons.Mode.TIME:
            dialog = TimeShiftDialog(self._window, page)
            method = page.project.shift_seconds
        elif page.edit_mode == cons.Mode.FRAME:
            dialog = FrameShiftDialog(self._window, page)
            method = page.project.shift_frames

        def on_preview(dialog, row):
            amount = dialog.get_amount()
            rows = self.get_target_rows(dialog.get_target())
            args = [rows, amount]
            self.preview_changes(page, row, MAIN, method, args)

        dialog.connect('preview', on_preview)
        response = dialog.run()
        if response != gtk.RESPONSE_OK:
            gtklib.destroy_gobject(dialog)
            return

        amount = dialog.get_amount()
        rows = self.get_target_rows(dialog.get_target())
        gtklib.destroy_gobject(dialog)
        method(rows, amount)
        page.view.select_rows(rows or range(len(page.project.times)))
