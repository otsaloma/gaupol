# Copyright (C) 2005-2007 Osmo Salomaa
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


"""Dialogs for adjusting positions."""


import gtk
from gettext import gettext as _

from gaupol.gtk import conf, cons, util
from gaupol.gtk.entries import TimeEntry
from .glade import GladeDialog


class _PositionAdjustDialog(GladeDialog):

    """Base class for dialogs for adjusting positions.

    Instance variables:

        _correct_label_1:  gtk.Label
        _correct_label_2:  gtk.Label
        _current_entry_1:  gtk.Entry
        _current_entry_2:  gtk.Entry
        _current_label_1:  gtk.Label
        _current_label_2:  gtk.Label
        _current_radio:    gtk.RadioButton
        _preview_button_1: gtk.Button
        _preview_button_2: gtk.Button
        _selected_radio:   gtk.RadioButton
        _sub_spin_1:       gtk.SpinButton
        _sub_spin_2:       gtk.SpinButton
        _table_1:          gtk.Table
        _table_2:          gtk.Table
        _text_view_1:      gtk.TextView
        _text_view_2:      gtk.TextView
        application:       Associated Application
    """

    def __init__(self, parent, application):

        GladeDialog.__init__(self, "posadjust-dialog")
        get_widget = self._glade_xml.get_widget
        self._correct_label_1  = get_widget("correct_label_1")
        self._correct_label_2  = get_widget("correct_label_2")
        self._current_entry_1  = get_widget("current_entry_1")
        self._current_entry_2  = get_widget("current_entry_2")
        self._current_label_1  = get_widget("current_label_1")
        self._current_label_2  = get_widget("current_label_2")
        self._current_radio    = get_widget("current_radio")
        self._preview_button_1 = get_widget("preview_button_1")
        self._preview_button_2 = get_widget("preview_button_2")
        self._selected_radio   = get_widget("selected_radio")
        self._sub_spin_1       = get_widget("sub_spin_1")
        self._sub_spin_2       = get_widget("sub_spin_2")
        self._table_1          = get_widget("table_1")
        self._table_2          = get_widget("table_2")
        self._text_view_1      = get_widget("text_view_1")
        self._text_view_2      = get_widget("text_view_2")
        self.application = application

        self._init_signal_handlers()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _adjust(self):
        """Adjust positions in subtitles."""

        method = self._get_adjust_method()
        rows = self._get_target_rows()
        point_1 = self._get_first_point()
        point_2 = self._get_second_point()
        method(rows, point_1, point_2)

    def _get_target(self):
        """Get the selected target."""

        if self._selected_radio.get_active():
            return cons.TARGET.SELECTED
        if self._current_radio.get_active():
            return cons.TARGET.CURRENT
        raise ValueError

    def _get_target_rows(self):
        """Get rows corresponding to target."""

        target = self._get_target()
        if target == cons.TARGET.SELECTED:
            page = self.application.get_current_page()
            return page.view.get_selected_rows()
        return None

    def _init_data(self):
        """Intialize default values for widgets."""

        page = self.application.get_current_page()
        self._sub_spin_1.set_value(1)
        self._sub_spin_2.set_value(len(page.project.times))
        self._sub_spin_1.emit("value-changed")
        self._sub_spin_2.emit("value-changed")

        target = conf.position_adjust.target
        self._selected_radio.set_active(target == cons.TARGET.SELECTED)
        self._current_radio.set_active(target == cons.TARGET.CURRENT)

        rows = page.view.get_selected_rows()
        if not rows and target == cons.TARGET.SELECTED:
            self._current_radio.set_active(True)
            self._selected_radio.set_sensitive(False)

        if page.project.video_path is None:
            self._preview_button_1.set_sensitive(False)
            self._preview_button_2.set_sensitive(False)
        if page.project.main_file is None:
            self._preview_button_1.set_sensitive(False)
            self._preview_button_2.set_sensitive(False)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, "_preview_button_1", "clicked")
        util.connect(self, "_preview_button_2", "clicked")
        util.connect(self, "_sub_spin_1", "value-changed")
        util.connect(self, "_sub_spin_2", "value-changed")
        util.connect(self, self, "response")

    def _init_sizes(self):
        """Initialize the widget sizes."""

        label = gtk.Label("\n".join(["M" * 36] * 3))
        width, height = label.size_request()
        self._text_view_1.set_size_request(width + 4, height + 7)
        self._text_view_2.set_size_request(width + 4, height + 7)

    def _init_widgets(self):
        """Initialize widgets."""

        page = self.application.get_current_page()
        last_sub = len(page.project.times)
        self._sub_spin_1.set_range(1, last_sub)
        self._sub_spin_2.set_range(1, last_sub)

    def _on_preview_button_1_clicked(self, *args):
        """Preview changes at the first point."""

        page = self.application.get_current_page()
        row = self._sub_spin_1.get_value_as_int() - 1
        doc = cons.DOCUMENT.MAIN
        method = self._get_adjust_method()
        rows = self._get_target_rows()
        point_1 = self._get_first_point()
        point_2 = self._get_second_point()
        args = (rows, point_1, point_2)
        self.application.preview_changes(page, row, doc, method, args)

    def _on_preview_button_2_clicked(self, *args):
        """Preview changes at the second point."""

        page = self.application.get_current_page()
        row = self._sub_spin_2.get_value_as_int() - 1
        doc = cons.DOCUMENT.MAIN
        method = self._get_adjust_method()
        rows = self._get_target_rows()
        point_1 = self._get_first_point()
        point_2 = self._get_second_point()
        args = (rows, point_1, point_2)
        self.application.preview_changes(page, row, doc, method, args)

    @util.ignore_exceptions(AssertionError)
    def _on_response(self, dialog, response):
        """Save settings and adjust positions."""

        conf.position_adjust.target = self._get_target()
        assert response == gtk.RESPONSE_OK
        self._adjust()


class FrameAdjustDialog(_PositionAdjustDialog):

    """Dialog for adjusting frames.

    Instance variables:

        _correct_spin_1: gtk.SpinButton
        _correct_spin_2: gtk.SpinButton
    """

    def __init__(self, parent, application):

        _PositionAdjustDialog.__init__(self, parent, application)

        self._correct_spin_1 = gtk.SpinButton()
        self._correct_spin_2 = gtk.SpinButton()

        self._init_widgets()
        self._init_data()

    def _get_adjust_method(self):
        """Get the project method to use for adjusting."""

        page = self.application.get_current_page()
        return page.project.adjust_frames

    def _get_first_point(self):
        """Get row, correct frame of the first sync point."""

        row = self._sub_spin_1.get_value_as_int() - 1
        frame = self._correct_spin_1.get_value_as_int()
        return row, frame

    def _get_second_point(self):
        """Get row, correct frame of the second sync point."""

        row = self._sub_spin_2.get_value_as_int() - 1
        frame = self._correct_spin_2.get_value_as_int()
        return row, frame

    def _init_widgets(self):
        """Initialize widgets."""

        _PositionAdjustDialog._init_widgets(self)
        self._current_label_1.set_text(_("Current frame:"))
        self._correct_label_1.set_text(_("C_orrect frame:"))
        self._correct_label_1.set_use_underline(True)
        self._correct_label_1.set_mnemonic_widget(self._correct_spin_1)
        self._current_label_2.set_text(_("Current frame:"))
        self._correct_label_2.set_text(_("Co_rrect frame:"))
        self._correct_label_2.set_use_underline(True)
        self._correct_label_2.set_mnemonic_widget(self._correct_spin_2)

        spins = (self._correct_spin_1, self._correct_spin_2)
        for spin_button in spins:
            spin_button.set_digits(0)
            spin_button.set_increments(1, 10)
            spin_button.set_range(0, 999999)
        for i, table in enumerate((self._table_1, self._table_2)):
            table.attach(spins[i], 1, 2, 2, 3, gtk.FILL, gtk.FILL)
            table.show_all()

    def _on_sub_spin_1_value_changed(self, spin_button):
        """Update data in widgets."""

        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        self._current_entry_1.set_text(str(page.project.frames[row][0]))
        self._correct_spin_1.set_value(page.project.frames[row][0])
        text_buffer = self._text_view_1.get_buffer()
        text_buffer.set_text(page.project.main_texts[row])
        self._sub_spin_2.props.adjustment.props.lower = row + 2

    def _on_sub_spin_2_value_changed(self, spin_button):
        """Update data in widgets."""

        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        self._current_entry_2.set_text(str(page.project.frames[row][0]))
        self._correct_spin_2.set_value(page.project.frames[row][0])
        text_buffer = self._text_view_2.get_buffer()
        text_buffer.set_text(page.project.main_texts[row])
        self._sub_spin_1.props.adjustment.props.upper = row


class TimeAdjustDialog(_PositionAdjustDialog):

    """Dialog for adjusting frames.

    Instance variables:

        _correct_entry_1: TimeEntry
        _correct_entry_2: TimeEntry
    """

    def __init__(self, parent, application):

        _PositionAdjustDialog.__init__(self, parent, application)

        self._correct_entry_1 = TimeEntry()
        self._correct_entry_2 = TimeEntry()

        self._init_widgets()
        self._init_data()

    def _get_adjust_method(self):
        """Get the project method to use for adjusting."""

        page = self.application.get_current_page()
        return page.project.adjust_times

    def _get_first_point(self):
        """Get row, correct time of the first sync point."""

        row = self._sub_spin_1.get_value_as_int() - 1
        time = self._correct_entry_1.get_text()
        return row, time

    def _get_second_point(self):
        """Get row, correct time of the second sync point."""

        row = self._sub_spin_2.get_value_as_int() - 1
        time = self._correct_entry_2.get_text()
        return row, time

    def _init_widgets(self):
        """Initialize widgets."""

        _PositionAdjustDialog._init_widgets(self)
        self._current_label_1.set_text(_("Current time:"))
        self._correct_label_1.set_text(_("C_orrect time:"))
        self._correct_label_1.set_use_underline(True)
        self._correct_label_1.set_mnemonic_widget(self._correct_entry_1)
        self._current_label_2.set_text(_("Current time:"))
        self._correct_label_2.set_text(_("Co_rrect time:"))
        self._correct_label_2.set_use_underline(True)
        self._correct_label_2.set_mnemonic_widget(self._correct_entry_2)

        entries = (self._correct_entry_1, self._correct_entry_2)
        for i, table in enumerate((self._table_1, self._table_2)):
            table.attach(entries[i], 1, 2, 2, 3, gtk.FILL, gtk.FILL)
            table.show_all()

    def _on_sub_spin_1_value_changed(self, spin_button):
        """Update data in widgets."""

        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        self._current_entry_1.set_text(page.project.times[row][0])
        self._correct_entry_1.set_text(page.project.times[row][0])
        text_buffer = self._text_view_1.get_buffer()
        text_buffer.set_text(page.project.main_texts[row])
        self._sub_spin_2.props.adjustment.props.lower = row + 2
        # Allow the slow TimeEntry to update.
        while gtk.events_pending():
            gtk.main_iteration()

    def _on_sub_spin_2_value_changed(self, spin_button):
        """Update data in widgets."""

        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        self._current_entry_2.set_text(page.project.times[row][0])
        self._correct_entry_2.set_text(page.project.times[row][0])
        text_buffer = self._text_view_2.get_buffer()
        text_buffer.set_text(page.project.main_texts[row])
        self._sub_spin_1.props.adjustment.props.upper = row
        # Allow the slow TimeEntry to update.
        while gtk.events_pending():
            gtk.main_iteration()
