# Copyright (C) 2008 Osmo Salomaa
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

"""Containers for additional format-specific subtitle attributes.

Instances of containers must be able to gracefully survive a copy.deepcopy
operation. If the container is in some way complicated, it should implement
__copy__  and __deepcopy__ methods to ensure this.
"""


class SubRip(object):

    """Subtitle box pixel coordinates for extended SubRip format."""

    x1 = y1 = x2 = y2 = 0


class SubStationAlpha(object):

    """Attributes for all versions of Sub Station Alpha formats."""

    marked = 0
    layer = 0
    style = "Default"
    name = ""
    margin_l = 0
    margin_r = 0
    margin_v = 0
    effect = ""


def new(name):
    """Return a new container instance given the container's name."""

    if name == "ssa":
        return SubStationAlpha()
    if name == "subrip":
        return SubRip()
    raise ValueError
