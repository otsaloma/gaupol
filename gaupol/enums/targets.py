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

"""Enumerations for action target types."""

import aeidon

__all__ = ("targets",)


class Selected(aeidon.EnumerationItem):

    pass


class SelectedToEnd(aeidon.EnumerationItem):

    pass


class Current(aeidon.EnumerationItem):

    pass


class All(aeidon.EnumerationItem):

    pass


targets = aeidon.Enumeration()
targets.SELECTED = Selected()
targets.SELECTED_TO_END = SelectedToEnd()
targets.CURRENT = Current()
targets.ALL = All()
