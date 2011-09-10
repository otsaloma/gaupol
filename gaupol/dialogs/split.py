# Copyright (C) 2006-2008,2010 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Dialog for splitting a project in two."""

import aeidon
import gaupol
import gtk
_ = aeidon.i18n._

__all__ = ("SplitDialog",)


class SplitDialog(gaupol.BuilderDialog, metaclass=aeidon.Contractual):

    """Dialog for splitting a project in two."""
    _widgets = ("subtitle_spin",)

    def __init___require(self, parent, application):
        page = application.get_current_page()
        assert page is not None
        assert len(page.project.subtitles) > 1

    def __init__(self, parent, application):
        """Initialize a :class:`SplitDialog` object."""
        gaupol.BuilderDialog.__init__(self, "split-dialog.ui")
        self.application = application
        self._init_subtitle_spin()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_subtitle_spin(self):
        """Initialize the subtitle spin button."""
        page = self.application.get_current_page()
        rows = page.view.get_selected_rows()
        subtitle = (rows[0] + 1 if rows else 2)
        self._subtitle_spin.set_value(subtitle)
        self._subtitle_spin.set_range(2, len(page.project.subtitles))

    def _on_subtitle_spin_value_changed(self, spin_button):
        """Select matching row in the view."""
        page = self.application.get_current_page()
        row = self._subtitle_spin.get_value_as_int() - 1
        page.view.set_focus(row, None)

    def _on_response(self, dialog, response):
        """Split the current project if OK'd."""
        if response == gtk.RESPONSE_OK:
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
        amount = src.project.subtitles[-1].end
        if isinstance(amount, str):
            amount = (amount[1:] if amount.startswith("-") else "-%s" % amount)
        if isinstance(amount, (int, float)):
            amount = -1 * amount
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
        amount = len(dst.project.subtitles)
        name = dst.untitle
        message = _('Split %(amount)d subtitles to project "%(name)s"')
        self.application.flash_message(message % locals())
        gaupol.util.set_cursor_normal(self.application.window)
