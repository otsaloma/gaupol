# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Dialog for selecting a subtitle file to append to project."""

import aeidon
import gaupol

from aeidon.i18n import _

__all__ = ("AppendDialog",)


class AppendDialog(gaupol.OpenDialog):

    """Dialog for selecting a subtitle file to append to project."""

    def __init__(self, parent):
        """Initialize an :class:`AppendDialog` instance."""
        doc = aeidon.documents.MAIN
        gaupol.OpenDialog.__init__(self, parent, _("Append File"), doc)
        self.set_select_multiple(False)
