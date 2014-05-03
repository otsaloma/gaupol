# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Enumerations for length unit types."""

import aeidon
_ = aeidon.i18n._

__all__ = ("length_units",)


class Char(aeidon.EnumerationItem):

    label = _("characters")


class Em(aeidon.EnumerationItem):

    label = _("ems")


length_units = aeidon.Enumeration()
length_units.CHAR = Char()
length_units.EM = Em()
