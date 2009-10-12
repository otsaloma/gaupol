# Copyright (C) 2005-2009 Osmo Salomaa
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

"""Enumerations for framerate types."""

import aeidon
_ = aeidon.i18n._

__all__ = ("framerates",)


class Framerate24(aeidon.EnumerationItem):

    label = _("24 fps")
    mpsub = "23.98"
    value = 24 / 1.001


class Framerate25(aeidon.EnumerationItem):

    label = _("25 fps")
    mpsub = "25.00"
    value = 25.0


class Framerate30(aeidon.EnumerationItem):

    label = _("30 fps")
    mpsub = "29.97"
    value = 30 / 1.001


framerates = aeidon.Enumeration()
framerates.FPS_24 = Framerate24()
framerates.FPS_25 = Framerate25()
framerates.FPS_30 = Framerate30()
