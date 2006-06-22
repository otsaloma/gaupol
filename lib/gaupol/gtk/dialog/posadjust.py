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


"""Dialogs for adjusting positions."""


from gettext import gettext as _

import gobject
import gtk

from gaupol.gtk            import cons
from gaupol.gtk.entry.time import EntryTime
from gaupol.gtk.util       import conf, gtklib


class _PositionAdjustDialog(gobject.GObject):

    """Base class for dialogs for adjusting positions."""

    __gsignals__ = {
        'preview': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (int,)
        ),
    }

    def __init__(self, parent, page):

        gobject.GObject.__init__(self)

        self._page = page

        glade_xml = gtklib.get_glade_xml('posadjust-dialog')
        self._correct_label_1  = glade_xml.get_widget('correct_label_1')
        self._correct_label_2  = glade_xml.get_widget('correct_label_2')
        self._current_entry_1  = glade_xml.get_widget('current_entry_1')
        self._current_entry_2  = glade_xml.get_widget('current_entry_2')
        self._current_label_1  = glade_xml.get_widget('current_label_1')
        self._current_label_2  = glade_xml.get_widget('current_label_2')
        self._current_radio    = glade_xml.get_widget('current_radio')
        self._dialog           = glade_xml.get_widget('dialog')
        self._preview_button_1 = glade_xml.get_widget('preview_button_1')
        self._preview_button_2 = glade_xml.get_widget('preview_button_2')
        self._selected_radio   = glade_xml.get_widget('selected_radio')
        self._sub_spin_1       = glade_xml.get_widget('sub_spin_1')
        self._sub_spin_2       = glade_xml.get_widget('sub_spin_2')
        self._table_1          = glade_xml.get_widget('table_1')
        self._table_2          = glade_xml.get_widget('table_2')
        self._text_view_1      = glade_xml.get_widget('text_view_1')
        self._text_view_2      = glade_xml.get_widget('text_view_2')

        self._init_sizes()
        self._init_sensitivities()
        self._init_signals()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self):
        """Initialize default values."""

        self._sub_spin_1.set_value(1)
        self._sub_spin_2.set_value(len(self._page.project.times))
        self._sub_spin_1.emit('value-changed')
        self._sub_spin_2.emit('value-changed')

        target = conf.position_adjust.target
        self._current_radio.set_active(target == cons.Target.CURRENT)
        self._selected_radio.set_active(target == cons.Target.SELECTED)

    def _init_sensitivities(self):
        """Initialize widget sensitivities."""

        if self._page.project.video_path is None:
            self._preview_button_1.set_sensitive(False)
            self._preview_button_2.set_sensitive(False)
        if self._page.project.main_file is None:
            self._preview_button_1.set_sensitive(False)
            self._preview_button_2.set_sensitive(False)

        if not self._page.view.get_selected_rows():
            self._current_radio.set_active(True)
            self._selected_radio.set_sensitive(False)

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, '_dialog'          , 'response'     )
        gtklib.connect(self, '_preview_button_1', 'clicked'      )
        gtklib.connect(self, '_preview_button_2', 'clicked'      )
        gtklib.connect(self, '_sub_spin_1'      , 'value-changed')
        gtklib.connect(self, '_sub_spin_2'      , 'value-changed')

    def _init_sizes(self):
        """Initialize widget sizes."""

        label = gtk.Label('\n'.join(['x' * 44] * 3))
        width, height = label.size_request()
        self._text_view_1.set_size_request(width + 4, height + 7)
        self._text_view_2.set_size_request(width + 4, height + 7)

    def _on_dialog_response(self, dialog, response):
        """Save settings."""

        if response == gtk.RESPONSE_OK:
            conf.position_adjust.target = self.get_target()

    def _on_preview_button_1_clicked(self, *args):
        """Emit preview."""

        self.emit('preview', self.get_first_point()[0])

    def _on_preview_button_2_clicked(self, *args):
        """Emit preview."""

        self.emit('preview', self.get_second_point()[0])

    def destroy(self):
        """Destroy dialog."""

        self._dialog.destroy()

    def get_target(self):
        """Get target."""

        if self._current_radio.get_active():
            return cons.Target.CURRENT
        elif self._selected_radio.get_active():
            return cons.Target.SELECTED

    def run(self):
        """Run dialog."""

        self._dialog.show()
        return self._dialog.run()


class FrameAdjustDialog(_PositionAdjustDialog):

    """Dialog for adjusting times."""

    def __init__(self, parent, page):

        _PositionAdjustDialog.__init__(self, parent, page)

        self._correct_spin_1 = gtk.SpinButton()
        self._correct_spin_2 = gtk.SpinButton()

        self._init_widgets()
        self._init_data()

    def _init_widgets(self):
        """Initialize widgets."""

        last_sub = len(self._page.project.times)
        self._sub_spin_1.set_range(1, last_sub)
        self._sub_spin_2.set_range(1, last_sub)

        self._current_label_1.set_text(_('Current frame:'))
        self._correct_label_1.set_text(_('C_orrect frame:'))
        self._correct_label_1.set_use_underline(True)
        self._correct_label_1.set_mnemonic_widget(self._correct_spin_1)
        self._current_label_2.set_text(_('Current frame:'))
        self._correct_label_2.set_text(_('Co_rrect frame:'))
        self._correct_label_2.set_use_underline(True)
        self._correct_label_2.set_mnemonic_widget(self._correct_spin_2)

        for spin_button in (self._correct_spin_1, self._correct_spin_2):
            spin_button.set_digits(0)
            spin_button.set_increments(1, 10)
            spin_button.set_range(0, 999999)

        opts = gtk.FILL
        self._table_1.attach(self._correct_spin_1, 1, 2, 2, 3, opts, opts)
        self._table_2.attach(self._correct_spin_2, 1, 2, 2, 3, opts, opts)
        self._table_1.show_all()
        self._table_2.show_all()

    def _on_sub_spin_1_value_changed(self, spin_button):
        """Update data."""

        project = self._page.project
        row = spin_button.get_value_as_int() - 1
        self._current_entry_1.set_text(str(project.frames[row][0]))
        self._correct_spin_1.set_value(project.frames[row][0])
        text_buffer = self._text_view_1.get_buffer()
        text_buffer.set_text(project.main_texts[row])
        self._sub_spin_2.props.adjustment.props.lower = row + 2

    def _on_sub_spin_2_value_changed(self, spin_button):
        """Update data."""

        project = self._page.project
        row = spin_button.get_value_as_int() - 1
        self._current_entry_2.set_text(str(project.frames[row][0]))
        self._correct_spin_2.set_value(project.frames[row][0])
        text_buffer = self._text_view_2.get_buffer()
        text_buffer.set_text(project.main_texts[row])
        self._sub_spin_1.props.adjustment.props.upper = row

    def get_first_point(self):
        """Return two-tuple: row, correct frame."""

        row = self._sub_spin_1.get_value_as_int() - 1
        return row, self._correct_spin_1.get_value_as_int()

    def get_second_point(self):
        """Return two-tuple: row, correct frame."""

        row = self._sub_spin_2.get_value_as_int() - 1
        return row, self._correct_spin_2.get_value_as_int()


class TimeAdjustDialog(_PositionAdjustDialog):

    """Dialog for adjusting frames."""

    def __init__(self, parent, page):

        _PositionAdjustDialog.__init__(self, parent, page)

        self._correct_entry_1 = EntryTime()
        self._correct_entry_2 = EntryTime()

        self._init_widgets()
        self._init_data()

    def _init_widgets(self):
        """Initialize widgets."""

        last_sub = len(self._page.project.times)
        self._sub_spin_1.set_range(1, last_sub)
        self._sub_spin_2.set_range(1, last_sub)

        self._current_label_1.set_text(_('Current time:'))
        self._correct_label_1.set_text(_('C_orrect time:'))
        self._correct_label_1.set_use_underline(True)
        self._correct_label_1.set_mnemonic_widget(self._correct_entry_1)
        self._current_label_2.set_text(_('Current time:'))
        self._correct_label_2.set_text(_('Co_rrect time:'))
        self._correct_label_2.set_use_underline(True)
        self._correct_label_2.set_mnemonic_widget(self._correct_entry_2)

        opts = gtk.FILL
        self._table_1.attach(self._correct_entry_1, 1, 2, 2, 3, opts, opts)
        self._table_2.attach(self._correct_entry_2, 1, 2, 2, 3, opts, opts)
        self._table_1.show_all()
        self._table_2.show_all()

    def _on_sub_spin_1_value_changed(self, spin_button):
        """Update data."""

        project = self._page.project
        row = spin_button.get_value_as_int() - 1
        self._current_entry_1.set_text(project.times[row][0])
        self._correct_entry_1.set_text(project.times[row][0])
        text_buffer = self._text_view_1.get_buffer()
        text_buffer.set_text(project.main_texts[row])
        self._sub_spin_2.props.adjustment.props.lower = row + 2

    def _on_sub_spin_2_value_changed(self, spin_button):
        """Update data."""

        project = self._page.project
        row = spin_button.get_value_as_int() - 1
        self._current_entry_2.set_text(project.times[row][0])
        self._correct_entry_2.set_text(project.times[row][0])
        text_buffer = self._text_view_2.get_buffer()
        text_buffer.set_text(project.main_texts[row])
        self._sub_spin_1.props.adjustment.props.upper = row

    def get_first_point(self):
        """Return two-tuple: row, correct time."""

        row = self._sub_spin_1.get_value_as_int() - 1
        return row, self._correct_entry_1.get_text()

    def get_second_point(self):
        """Return two-tuple: row, correct time."""

        row = self._sub_spin_2.get_value_as_int() - 1
        return row, self._correct_entry_2.get_text()
