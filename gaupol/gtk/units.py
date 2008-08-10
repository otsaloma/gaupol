# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Enumerations for length unit types."""

import gaupol
_ = gaupol.i18n._

__all__ = ("length_units",)


class Char(gaupol.EnumerationItem):

    label = _("characters")


class Em(gaupol.EnumerationItem):

    label = _("ems")


length_units = gaupol.Enumeration()
length_units.CHAR = Char()
length_units.EM = Em()
