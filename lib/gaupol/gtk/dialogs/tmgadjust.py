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


"""Dialog for adjusting timings."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _

import gobject
import gtk

from gaupol.constants        import Mode
from gaupol.gtk.entries.time import TimeEntry
from gaupol.gtk.util         import config, gtklib


class TimingAdjustDialog(gobject.GObject):

    """Dialog for shifting timings."""

    __gsignals__ = {
        'preview': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (int,)
        ),
    }

    def __init__(self, parent, page):

        gobject.GObject.__init__(self)

        glade_xml = gtklib.get_glade_xml('tmgadjust-dialog.glade')
        get_widget = glade_xml.get_widget

        self._all_radio        = get_widget('all_radio_button')
        self._current_entry_1  = get_widget('current_entry_1')
        self._current_entry_2  = get_widget('current_entry_2')
        self._dialog           = get_widget('dialog')
        self._preview_button_1 = get_widget('preview_button_1')
        self._preview_button_2 = get_widget('preview_button_2')
        self._selected_radio   = get_widget('selected_radio_button')
        self._subtitle_spin_1  = get_widget('subtitle_spin_button_1')
        self._subtitle_spin_2  = get_widget('subtitle_spin_button_2')
        self._text_view_1      = get_widget('text_view_1')
        self._text_view_2      = get_widget('text_view_2')

        # Time entries
        self._correct_entry_1 = None
        self._correct_entry_2 = None

        # Frame spin buttons
        self._correct_spin_1  = None
        self._correct_spin_2  = None

        self._page = page

        self._init_widgets(glade_xml)
        self._init_sizes()
        self._init_sensitivities()
        self._init_signals()
        self._init_data()

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self):
        """Initialize default values."""

        last_subtitle = len(self._page.project.times)
        self._subtitle_spin_1.set_value(1)
        self._subtitle_spin_1.emit('value-changed')
        self._subtitle_spin_2.set_value(last_subtitle)
        self._subtitle_spin_2.emit('value-changed')

        self._all_radio.set_active(config.timing_shift.shift_all)

    def _init_sensitivities(self):
        """Initialize widget sensitivities."""

        if self._page.project.video_path is None:
            self._preview_button_1.set_sensitive(False)
            self._preview_button_2.set_sensitive(False)
        if self._page.project.main_file is None:
            self._preview_button_1.set_sensitive(False)
            self._preview_button_2.set_sensitive(False)

        if not self._page.view.get_selected_rows():
            self._all_radio.set_active(True)
            self._selected_radio.set_sensitive(False)

    def _init_signals(self):
        """Initialize signals."""

        method = self._on_subtitle_spin_1_value_changed
        self._subtitle_spin_1.connect('value-changed', method)
        method = self._on_subtitle_spin_2_value_changed
        self._subtitle_spin_2.connect('value-changed', method)

        method = self._on_preview_button_1_clicked
        self._preview_button_1.connect('clicked', method)
        method = self._on_preview_button_2_clicked
        self._preview_button_2.connect('clicked', method)

        method = self._on_all_radio_toggled
        self._all_radio.connect('toggled', method)

    def _init_sizes(self):
        """Initialize widget sizes."""

        # Set text view width to 42 ex and height to 3 lines.
        label = gtk.Label('\n'.join(['x' * 42] * 3))
        width, height = label.size_request()

        self._text_view_1.set_size_request(width + 4, height + 7)
        self._text_view_2.set_size_request(width + 4, height + 7)

    def _init_widgets(self, glade_xml):
        """Initialize widgets."""

        FILL = gtk.FILL

        table_1 = glade_xml.get_widget('table_1')
        table_2 = glade_xml.get_widget('table_2')

        def get_frame_spin_button():
            spin_button =  gtk.SpinButton()
            spin_button.set_digits(0)
            spin_button.set_increments(1, 10)
            spin_button.set_range(0, 9999999)
            return spin_button

        if self._page.edit_mode == Mode.TIME:

            # Entries
            self._correct_entry_1 = TimeEntry()
            self._correct_entry_2 = TimeEntry()
            table_1.attach(self._correct_entry_1, 1, 2, 2, 3, FILL, FILL)
            table_2.attach(self._correct_entry_2, 1, 2, 2, 3, FILL, FILL)

            # Current labels
            label = glade_xml.get_widget('current_label_1')
            label.set_text(_('Current time:'))
            label = glade_xml.get_widget('current_label_2')
            label.set_text(_('Current time:'))

            # Correct labels
            label = glade_xml.get_widget('correct_label_1')
            label.set_text(_('C_orrect time:'))
            label.set_use_underline(True)
            label.set_mnemonic_widget(self._correct_entry_1)
            label = glade_xml.get_widget('correct_label_2')
            label.set_text(_('Co_rrect time:'))
            label.set_use_underline(True)
            label.set_mnemonic_widget(self._correct_entry_2)

        elif self._page.edit_mode == Mode.FRAME:

            # Spin buttons
            self._correct_spin_1 = get_frame_spin_button()
            self._correct_spin_2 = get_frame_spin_button()
            table_1.attach(self._correct_spin_1, 1, 2, 2, 3, FILL, FILL)
            table_2.attach(self._correct_spin_2, 1, 2, 2, 3, FILL, FILL)

            # Current labels
            label = glade_xml.get_widget('current_label_1')
            label.set_text(_('Current frame:'))
            label = glade_xml.get_widget('current_label_2')
            label.set_text(_('Current frame:'))

            # Correct labels
            label = glade_xml.get_widget('correct_label_1')
            label.set_text(_('C_orrect frame:'))
            label.set_use_underline(True)
            label.set_mnemonic_widget(self._correct_spin_1)
            label = glade_xml.get_widget('correct_label_2')
            label.set_text(_('Co_rrect frame:'))
            label.set_use_underline(True)
            label.set_mnemonic_widget(self._correct_spin_2)

        table_1.show_all()
        table_2.show_all()

        last_subtitle = len(self._page.project.times)
        self._subtitle_spin_1.set_range(1, last_subtitle)
        self._subtitle_spin_2.set_range(1, last_subtitle)

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def get_adjust_all(self):
        """Get adjust all setting."""

        return self._all_radio.get_active()

    def get_first_point(self):
        """Return two-tuple of row, correct time/frame."""

        row = self._subtitle_spin_1.get_value_as_int() - 1
        if self._page.edit_mode == Mode.TIME:
            return row, self._correct_entry_1.get_text()
        elif self._page.edit_mode == Mode.FRAME:
            return row, self._correct_spin_1.get_value_as_int()

    def get_second_point(self):
        """Return two-tuple of row, correct time/frame."""

        row = self._subtitle_spin_2.get_value_as_int() - 1
        if self._page.edit_mode == Mode.TIME:
            return row, self._correct_entry_2.get_text()
        elif self._page.edit_mode == Mode.FRAME:
            return row, self._correct_spin_2.get_value_as_int()

    def _on_all_radio_toggled(self, radio_button):
        """Save radio button value."""

        config.timing_shift.shift_all = radio_button.get_active()

    def _on_preview_button_1_clicked(self, button):
        """Preview changes."""

        row = self.get_first_point()[0]
        self.emit('preview', row)

    def _on_preview_button_2_clicked(self, button):
        """Preview changes."""

        row = self.get_second_point()[0]
        self.emit('preview', row)

    def _on_subtitle_spin_1_value_changed(self, spin_button):
        """Update data."""

        project = self._page.project
        row = spin_button.get_value_as_int() - 1

        if self._page.edit_mode == Mode.TIME:
            self._current_entry_1.set_text(project.times[row][0])
            self._correct_entry_1.set_text(project.times[row][0])
        elif self._page.edit_mode == Mode.FRAME:
            self._current_entry_1.set_text(str(project.frames[row][0]))
            self._correct_spin_1.set_value(project.frames[row][0])

        text_buffer = self._text_view_1.get_buffer()
        text_buffer.set_text(project.main_texts[row])

        self._subtitle_spin_2.props.adjustment.props.lower = row + 2

    def _on_subtitle_spin_2_value_changed(self, spin_button):
        """Update data."""

        project = self._page.project
        row = spin_button.get_value_as_int() - 1

        if self._page.edit_mode == Mode.TIME:
            self._current_entry_2.set_text(project.times[row][0])
            self._correct_entry_2.set_text(project.times[row][0])
        elif self._page.edit_mode == Mode.FRAME:
            self._current_entry_2.set_text(str(project.frames[row][0]))
            self._correct_spin_2.set_value(project.frames[row][0])

        text_buffer = self._text_view_2.get_buffer()
        text_buffer.set_text(project.main_texts[row])

        self._subtitle_spin_1.props.adjustment.props.upper = row

    def run(self):
        """Show and run the dialog."""

        self._dialog.show()
        return self._dialog.run()


if __name__ == '__main__':

    from gaupol.gtk.application import Application
    from gaupol.test            import Test

    class TestTimingAdjustDialog(Test):

        def __init__(self):

            Test.__init__(self)
            self.application = Application()
            self.application.open_main_files([self.get_subrip_path()])
            self.page = self.application.get_current_page()
            self.dialog = TimingAdjustDialog(gtk.Window(), self.page)

        def destroy(self):

            self.application.window.destroy()

        def test_get_adjust_all(self):

            assert isinstance(self.dialog.get_adjust_all(), bool)

        def test_get_points(self):

            row_1, value_1 = self.dialog.get_first_point()
            row_2, value_2 = self.dialog.get_second_point()

            assert isinstance(row_1, int)
            assert isinstance(row_2, int)

            if self.page.edit_mode == Mode.TIME:
                assert isinstance(value_1, str)
                assert isinstance(value_2, str)
            elif self.page.edit_mode == Mode.FRAME:
                assert isinstance(value_1, int)
                assert isinstance(value_2, int)

        def test_signals(self):

            self.dialog._subtitle_spin_1.set_value(3)
            self.dialog._subtitle_spin_2.set_value(4)

            self.dialog._all_radio.set_active(True)
            self.dialog._all_radio.set_active(False)

    TestTimingAdjustDialog().run()
