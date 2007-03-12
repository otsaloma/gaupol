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


"""Editing times and frames."""


from gaupol.base import Delegate
from gaupol.gtk.dialogs import FrameShiftDialog, TimeShiftDialog


class PositionAgent(Delegate):

    """Editing times and frames."""

    # pylint: disable-msg=E0203,W0201

    def on_shift_positions_activate(self, *args):
        """Make subtitles appear earlier or later."""

        page = self.get_current_page()
        cls = (TimeShiftDialog, FrameShiftDialog)[page.edit_mode]
        dialog = cls(self.window, self)
        self.flash_dialog(dialog)
