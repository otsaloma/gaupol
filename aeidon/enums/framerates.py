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

"""Enumerations for framerate types."""

import aeidon
_ = aeidon.i18n._

__all__ = ("framerates",)


class Framerate23976(aeidon.EnumerationItem):

    label = _("23.976 fps")
    mpsub = "23.98"
    value = 24 / 1.001


class Framerate24000(aeidon.EnumerationItem):

    label = _("24.000 fps")
    mpsub = "24.00"
    value = 24.0


class Framerate25000(aeidon.EnumerationItem):

    label = _("25.000 fps")
    mpsub = "25.00"
    value = 25.0


class Framerate29970(aeidon.EnumerationItem):

    label = _("29.970 fps")
    mpsub = "29.97"
    value = 30 / 1.001


framerates = aeidon.Enumeration()
framerates.FPS_23_976 = Framerate23976()
framerates.FPS_24_000 = Framerate24000()
framerates.FPS_25_000 = Framerate25000()
framerates.FPS_29_970 = Framerate29970()
