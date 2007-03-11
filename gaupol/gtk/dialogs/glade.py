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


"""Wrapper for Glade constructed dialogs."""


from gaupol.base import Delegate
from gaupol.gtk import util
from gaupol.gtk.runner import Runner


class GladeDialog(Delegate, Runner):

    """Wrapper for Glade constructed dialogs.

    Instance variables:

        _dialog:    gtk.Dialog
        _glade_xml: gtk.glade.XML
    """

    # pylint: disable-msg=W0231
    def __init__(self, name):

        glade_xml = util.get_glade_xml(name)
        dialog = glade_xml.get_widget("dialog")
        Delegate.__init__(self, dialog)

        self._dialog = dialog
        self._glade_xml = glade_xml

    def run(self):
        """Show the dialog, run it and return response."""

        self._dialog.show()
        return self._dialog.run()
