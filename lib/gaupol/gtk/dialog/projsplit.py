# Copyright (C) 2006 Osmo Salomaa
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


import gtk

from gaupol.gtk.util import gtklib


class ProjectSplitDialog(object):

    """Dialog for splitting project in two."""

    def __init__(self, parent, page):

        glade_xml = gtklib.get_glade_xml('projsplit-dialog')
        self._dialog      = glade_xml.get_widget('dialog')
        self._spin_button = glade_xml.get_widget('spin_button')

        self._init_spin_button(page)
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_spin_button(self, page):
        """Initialize spin button."""

        self._spin_button.set_range(2, len(page.project.times))
        try:
            self._spin_button.set_value(page.view.get_selected_rows()[0] + 1)
        except IndexError:
            self._spin_button.set_value(1)

    def destroy(self):
        """Destroy dialog."""

        self._dialog.destroy()

    def get_subtitle(self):
        """Return first subtitle of new project."""

        return self._spin_button.get_value_as_int()

    def run(self):
        """Run dialog."""

        self._dialog.show()
        return self._dialog.run()
