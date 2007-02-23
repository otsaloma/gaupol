# Copyright (C) 2006-2007 Osmo Salomaa
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


"""Dialog for splitting project in two."""


import copy
from gettext import gettext as _

import gtk

from gaupol.gtk import cons, util
from gaupol.gtk.page import Page
from .glade import GladeDialog


class SplitDialog(GladeDialog):

    """Dialog for splitting a project in two.

    Instance variables:

        _dialog:        gtk.Dialog
        _subtitle_spin: gtk.SpinButton, first subtitle of new project
        application:    Associated application
    """

    def __init__(self, application):

        GladeDialog.__init__(self, "split-dialog")
        self._dialog        = self._glade_xml.get_widget("dialog")
        self._subtitle_spin = self._glade_xml.get_widget("subtitle_spin")
        self.application    = application

        self._init_subtitle_spin()
        self._init_signal_handlers()
        self._dialog.set_transient_for(application.window)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, self, "response")

    def _init_subtitle_spin(self):
        """Initialize the subtitle spin button."""

        page = self.application.get_current_page()
        self._subtitle_spin.set_range(2, len(page.project.times))
        self._subtitle_spin.set_value(1)
        rows = page.view.get_selected_rows()
        subtitle = (rows[0] + 1 if rows else 1)
        self._subtitle_spin.set_value(subtitle)

    def _on_response(self, dialog, response):
        """Split the current project if OK."""

        if response == gtk.RESPONSE_OK:
            self._split_project()

    def _remove_from_source(self, source, row):
        """Remove rows from the source page."""

        rows = range(row, len(source.project.times))
        source.project.block("action-done")
        source.project.remove_subtitles(rows)
        source.project.set_action_description(
            cons.REGISTER.DO, _("Splitting project"))
        source.project.unblock("action-done")

    def _shift_destination(self, source, destination):
        """Shift subtitles in the destination page."""

        mode = destination.project.get_mode()
        calc = destination.project.calc
        if mode == cons.MODE.TIME:
            count = source.project.times[-1][1]
            count = -1 * calc.time_to_seconds(count)
            method = destination.project.shift_seconds
        elif mode == cons.MODE.FRAME:
            count = -1 * source.project.frames[-1][1]
            method = destination.project.shift_frames
        method([], count, register=None)

    def _split_project(self):
        """Split the current project in two."""

        util.set_cursor_busy(self.application.window)
        row = self._subtitle_spin.get_value_as_int() - 1
        source = self.application.get_current_page()
        self.application.counter += 1
        destination = Page(self.application.counter)

        times = copy.deepcopy(source.project.times[row:])
        frames = copy.deepcopy(source.project.frames[row:])
        main_texts = copy.deepcopy(source.project.main_texts[row:])
        tran_texts = copy.deepcopy(source.project.tran_texts[row:])
        destination.project.times = times
        destination.project.frames = frames
        destination.project.main_texts = main_texts
        destination.project.tran_texts = tran_texts
        destination.reload_view_all()

        self._remove_from_source(source, row)
        self._shift_destination(source, destination)
        self.application.add_new_page(destination)
        amount = len(destination.project.times)
        fields = {'amount': amount, 'name': destination.untitle}
        self.application.push_message(
            _('Split %(amount)d subtitles to project "%(name)s"') % fields)
        util.set_cursor_normal(self.application.window)
