# -*- coding: utf-8 -*-

# Copyright (C) 2006 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Dialog for splitting a project in two."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import Gtk

__all__ = ("SplitDialog",)


class SplitDialog(gaupol.BuilderDialog):

    """Dialog for splitting a project in two."""

    _widgets = ["subtitle_spin"]

    def __init__(self, parent, application):
        """Initialize a :class:`SplitDialog` instance."""
        gaupol.BuilderDialog.__init__(self, "split-dialog.ui")
        self.application = application
        self._init_dialog(parent)
        self._init_subtitle_spin()

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("_Split"), Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_transient_for(parent)
        self.set_modal(True)

    def _init_subtitle_spin(self):
        """Initialize the subtitle spin button."""
        page = self.application.get_current_page()
        rows = page.view.get_selected_rows()
        subtitle = rows[0] + 1 if rows else 2
        self._subtitle_spin.set_value(subtitle)
        self._subtitle_spin.set_range(2, len(page.project.subtitles))
        self._subtitle_spin.emit("value-changed")

    def _on_subtitle_spin_value_changed(self, spin_button):
        """Select matching row in the view."""
        page = self.application.get_current_page()
        row = self._subtitle_spin.get_value_as_int() - 1
        page.view.set_focus(row, None)

    def _on_response(self, dialog, response):
        """Split the current project if OK'd."""
        if response == Gtk.ResponseType.OK:
            self._split_project()

    def _remove_from_source(self, page, index):
        """Remove rows starting at `index` from `page`."""
        indices = list(range(index, len(page.project.subtitles)))
        page.project.block("action-done")
        page.project.remove_subtitles(indices)
        page.project.set_action_description(
            aeidon.registers.DO, _("Splitting project"))
        page.project.unblock("action-done")

    def _shift_destination(self, src, dst):
        """Shift subtitles in `dst` page."""
        amount = -1 * src.project.subtitles[-1].end_seconds
        dst.project.shift_positions(None, amount, register=None)

    def _split_project(self):
        """Split the current project in two."""
        gaupol.util.set_cursor_busy(self.application.window)
        index = self._subtitle_spin.get_value_as_int() - 1
        src = self.application.get_current_page()
        dst = gaupol.Page(next(self.application.counter))
        subtitles = [x.copy() for x in src.project.subtitles[index:]]
        indices = list(range(len(subtitles)))
        dst.project.insert_subtitles(indices, subtitles)
        dst.reload_view_all()
        self._remove_from_source(src, index)
        self._shift_destination(src, dst)
        self.application.add_page(dst)
        message = _('Split {amount:d} subtitles to project "{name}"').format(
            amount=len(dst.project.subtitles), name=dst.untitle)
        self.application.flash_message(message)
        gaupol.util.set_cursor_normal(self.application.window)
