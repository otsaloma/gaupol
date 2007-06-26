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


import gaupol.gtk
import gtk
_ = gaupol.i18n._

from .glade import GladeDialog


class SplitDialog(GladeDialog):

    """Dialog for splitting a project in two."""

    def __init__(self, application):

        GladeDialog.__init__(self, "split-dialog")
        self._subtitle_spin = self._glade_xml.get_widget("subtitle_spin")
        self.application = application

        self._init_signal_handlers()
        self._init_subtitle_spin()
        self._dialog.set_transient_for(application.window)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.gtk.util.connect(self, self, "response")
        gaupol.gtk.util.connect(self, "_subtitle_spin", "value-changed")

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

    @gaupol.gtk.util.asserted_return
    def _on_response(self, dialog, response):
        """Split the current project if OK responded."""

        assert response == gtk.RESPONSE_OK
        self._split_project()

    def _remove_from_source(self, source, index):
        """Remove rows from the source page."""

        indexes = range(index, len(source.project.subtitles))
        source.project.block("action-done")
        source.project.remove_subtitles(indexes)
        source.project.set_action_description(
            gaupol.gtk.REGISTER.DO, _("Splitting project"))
        source.project.unblock("action-done")

    def _shift_destination(self, source, destination):
        """Shift subtitles in the destination page."""

        amount = source.project.subtitles[-1].end
        destination.project.shift_positions(None, amount, register=None)

    def _split_project(self):
        """Split the current project in two."""

        gaupol.gtk.util.set_cursor_busy(self.application.window)
        index = self._subtitle_spin.get_value_as_int() - 1
        source = self.application.get_current_page()
        self.application.counter += 1
        destination = gaupol.gtk.Page(self.application.counter)
        subtitles = [x.copy() for x in source.project.subtitles[index:]]
        destination.subtitles = subtitles
        destination.reload_view_all()
        self._remove_from_source(source, index)
        self._shift_destination(source, destination)
        self.application.add_new_page(destination)
        amount = len(destination.project.subtitles)
        name = destination.untitle
        message = _('Split %(amount)d subtitles to project "%(name)s"')
        self.application.flash_message(message % locals())
        gaupol.gtk.util.set_cursor_normal(self.application.window)
