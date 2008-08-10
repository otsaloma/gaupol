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

"""Wrapper for Glade constructed dialogs."""

import gaupol.gtk

__all__ = ("GladeDialog",)


class GladeDialog(gaupol.Delegate, gaupol.gtk.Runner):

    """Wrapper for Glade constructed dialogs.

    The gtk.glade.XML widget tree is saved as instance variable '_glade_xml'
    and from the tree the widget name 'dialog' as '_dialog'.
    """

    def __init__(self, name):

        glade_xml = gaupol.gtk.util.get_glade_xml("dialogs", name)
        dialog = glade_xml.get_widget("dialog")
        gaupol.Delegate.__init__(self, dialog)
        self._dialog = dialog
        self._glade_xml = glade_xml

    def run(self):
        """Show the dialog, run it and return response."""

        self._dialog.show()
        return self._dialog.run()
