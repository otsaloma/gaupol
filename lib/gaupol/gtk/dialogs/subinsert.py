# Copyright (C) 2005 Osmo Salomaa
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


"""Dialog for inserting new subtitles."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.gtk.util import config, gtklib


class SubtitleInsertDialog(object):

    """Dialog for inserting new subtitles."""

    def __init__(self, parent, page):

        glade_xml = gtklib.get_glade_xml('subinsert-dialog')
        get_widget = glade_xml.get_widget

        self._amount_spin    = get_widget('amount_spin_button')
        self._dialog         = get_widget('dialog')
        self._position_combo = get_widget('position_combo_box')
        self._position_label = get_widget('position_label')

        self._init_sensitivities(page)
        self._init_data()
        self._init_signals()

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self):
        """Initialize the data."""

        self._position_combo.set_active(int(config.subtitle_insert.below))
        self._amount_spin.set_value(config.subtitle_insert.amount)

    def _init_sensitivities(self, page):
        """Initialize widget sensitivities."""

        if not page.project.times:
            self._position_label.set_sensitive(False)
            self._position_combo.set_sensitive(False)

    def _init_signals(self):
        """Initialize signals."""

        method = self._on_position_combo_changed
        self._position_combo.connect('changed', method)

        method = self._on_amount_spin_value_changed
        self._amount_spin.connect('value-changed', method)

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def get_amount(self):
        """Get amount of subtitles to insert."""

        self._amount_spin.update()
        return self._amount_spin.get_value_as_int()

    def get_position(self):
        """
        Get position to insert subtitles to.
        """
        # FIX: this returns is_below
        return bool(self._position_combo.get_active())

    def _on_amount_spin_value_changed(self, spin_button):
        """Save amount setting."""

        config.subtitle_insert.amount = spin_button.get_value_as_int()

    def _on_position_combo_changed(self, combo_box):
        """Save position setting."""

        config.subtitle_insert.below = bool(combo_box.get_active())

    def run(self):
        """Show and run the dialog."""

        self._dialog.show()
        return self._dialog.run()


if __name__ == '__main__':

    from gaupol.gtk.page import Page
    from gaupol.test     import Test

    class TestSubtitleInsertDialog(Test):

        def __init__(self):

            Test.__init__(self)
            page = Page()
            page.project = self.get_project()
            self.dialog = SubtitleInsertDialog(gtk.Window(), page)

        def test_gets(self):

            assert isinstance(self.dialog.get_amount(), int)
            assert isinstance(self.dialog.get_position(), int)

        def test_signals(self):

            self.dialog._position_combo.set_active(0)
            self.dialog._position_combo.set_active(1)
            self.dialog._amount_spin.set_value(33)

    TestSubtitleInsertDialog().run()
