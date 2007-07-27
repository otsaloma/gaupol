# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Dialog for selecting a subtitle file to append to project."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._

from .open import OpenDialog


class AppendDialog(OpenDialog):

    """Dialog for selecting a subtitle file to append to project."""

    # pylint: disable-msg=E1101

    def __init__(self, parent):

        doc = gaupol.gtk.DOCUMENT.MAIN
        OpenDialog.__init__(self, parent, _("Append File"), doc)
        self.set_select_multiple(False)
        button = self.action_area.get_children()[0]
        gaupol.gtk.util.set_button(button, _("_Append"), gtk.STOCK_ADD)
