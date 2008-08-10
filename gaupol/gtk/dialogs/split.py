# Copyright (C) 2006-2008 Osmo Salomaa
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

"""Dialog for splitting project in two."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._

__all__ = ("SplitDialog",)


class SplitDialog(gaupol.gtk.GladeDialog):

    """Dialog for splitting a project in two."""

    __metaclass__ = gaupol.Contractual

    def __init___require(self, parent, application):
        page = application.get_current_page()
        assert page is not None
        assert len(page.project.subtitles) > 1

    def __init__(self, parent, application):

        gaupol.gtk.GladeDialog.__init__(self, "split.glade")
        self._subtitle_spin = self._glade_xml.get_widget("subtitle_spin")
        self.application = application

        self._init_signal_handlers()
        self._init_subtitle_spin()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, self, "response")
        gaupol.util.connect(self, "_subtitle_spin", "value-changed")

    def _init_subtitle_spin(self):
        """Initialize the subtitle spin button."""

        page = self.application.get_current_page()
        self._subtitle_spin.set_range(2, len(page.project.subtitles))
        self._subtitle_spin.set_value(1)
        rows = page.view.get_selected_rows()
        subtitle = (rows[0] + 1 if rows else 1)
        self._subtitle_spin.set_value(subtitle)
        self._subtitle_spin.emit("value-changed")

    def _on_subtitle_spin_value_changed(self, spin_button):
        """Select the matching row in the view."""

        page = self.application.get_current_page()
        row = self._subtitle_spin.get_value_as_int() - 1
        page.view.set_focus(row, None)

    def _on_response(self, dialog, response):
        """Split the current project if OK responded."""

        if response == gtk.RESPONSE_OK:
            self._split_project()

    def _remove_from_source(self, source, index):
        """Remove rows from the source page."""

        indices = range(index, len(source.project.subtitles))
        source.project.block("action-done")
        source.project.remove_subtitles(indices)
        source.project.set_action_description(
            gaupol.registers.DO, _("Splitting project"))
        source.project.unblock("action-done")

    def _shift_destination(self, source, destination):
        """Shift subtitles in the destination page."""

        amount = source.project.subtitles[-1].end
        if isinstance(amount, basestring):
            if amount.startswith("-"):
                amount = amount[1:]
            else: # amount is positive.
                amount = "-%s" % amount
        elif isinstance(amount, (int, float)):
            amount = -1 * amount
        destination.project.shift_positions(None, amount, register=None)

    def _split_project(self):
        """Split the current project in two."""

        gaupol.gtk.util.set_cursor_busy(self.application.window)
        index = self._subtitle_spin.get_value_as_int() - 1
        source = self.application.get_current_page()
        destination = gaupol.gtk.Page(self.application.counter.next())
        subtitles = [x.copy() for x in source.project.subtitles[index:]]
        indices = range(len(subtitles))
        destination.project.insert_subtitles(indices, subtitles)
        destination.reload_view_all()
        self._remove_from_source(source, index)
        self._shift_destination(source, destination)
        self.application.add_new_page(destination)
        amount = len(destination.project.subtitles)
        name = destination.untitle
        message = _('Split %(amount)d subtitles to project "%(name)s"')
        self.application.flash_message(message % locals())
        gaupol.gtk.util.set_cursor_normal(self.application.window)
