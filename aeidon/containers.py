# -*- coding: utf-8-unix -*-

# Copyright (C) 2008-2009 Osmo Salomaa
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

"""
Containers for additional format-specific subtitle attributes.

Instances of containers must be able to gracefully survive a
:func:`copy.deepcopy` operation. If the container is in some way complicated,
it should implement :meth:`__copy__` and :meth:`__deepcopy__` methods to ensure
this.
"""


class SubRip(object):

    """
    Subtitle box pixel coordinates for extended SubRip format.

    :ivar x1: Subtitle corner X coordinate in pixels
    :ivar y1: Subtitle corner Y coordinate in pixels
    :ivar x2: Subtitle corner X coordinate in pixels
    :ivar y2: Subtitle corner Y coordinate in pixels
    """

    x1 = y1 = x2 = y2 = 0


class SubStationAlpha(object):

    """
    Attributes for all versions of Sub Station Alpha formats.

    :ivar marked: 0 for not marked or 1 for marked (default 0)
    :ivar layer: Layer used by collusion detection (default 0)
    :ivar style: Style name (default "Default")
    :ivar name: Name of the character speaking (default "")
    :ivar margin_l: Left margin override (default 0, i.e. default margins)
    :ivar margin_r: Right margin override (default 0, i.e. default margins)
    :ivar margin_v: Bottom margin override (default 0, i.e. default margins)
    :ivar effect: Transition effect (default "", i.e. no effect)
    """

    marked = 0
    layer = 0
    style = "Default"
    name = ""
    margin_l = 0
    margin_r = 0
    margin_v = 0
    effect = ""


def new(name):
    """Return a new container instance given the container's `name`."""
    if name == "ssa":
        return SubStationAlpha()
    if name == "subrip":
        return SubRip()
    raise ValueError("Invalid name: {}"
                     .format(repr(name)))
