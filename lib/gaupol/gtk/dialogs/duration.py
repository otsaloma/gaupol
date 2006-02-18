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


"""Dialog for adjusting durations."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk

from gaupol.gtk.util  import config, gtklib


class DurationAdjustDialog(object):

    """Dialog for adjusting timings."""

    def __init__(self, parent, page):

        glade_xml = gtklib.get_glade_xml('duration-dialog.glade')
        get_widget = glade_xml.get_widget

        self._dialog = get_widget('dialog')

        self._init_radio_groups()
        self._init_mnemonics(glade_xml)
        self._init_sensitivities()
        self._init_signals()
        self._init_data()

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self):
        """Initialize default values."""

        pass

    def _init_mnemonics(self, glade_xml):
        """Initialize mnemonics."""

        pass

    def _init_radio_groups(self):
        """Initialize radio button groups."""

        pass

    def _init_sensitivities(self):
        """Initialize widget sensitivities."""

        pass

    def _init_signals(self):
        """Initialize signals."""

        pass

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def run(self):
        """Show and run the dialog."""

        self._dialog.show()
        return self._dialog.run()


if __name__ == '__main__':

    from gaupol.gtk.application import Application
    from gaupol.test            import Test

    class TestDurationAdjustDialog(Test):

        def __init__(self):

            Test.__init__(self)
            self.application = Application()
            self.application.open_main_files([self.get_subrip_path()])
            self.page = self.application.get_current_page()
            self.dialog = DurationAdjustDialog(gtk.Window(), self.page)

        def destroy(self):

            self.application.window.destroy()

        def test_gets(self):

            pass

        def test_signals(self):

            pass

    TestDurationAdjustDialog().run()
