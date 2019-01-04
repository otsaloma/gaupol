# -*- coding: utf-8 -*-

# Copyright (C) 2008 Osmo Salomaa
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

"""Containers for additional format-specific subtitle attributes."""


class SubRip:

    """
    Subtitle box pixel coordinates for extended SubRip format.

    :ivar x1: Subtitle corner X coordinate in pixels
    :ivar y1: Subtitle corner Y coordinate in pixels
    :ivar x2: Subtitle corner X coordinate in pixels
    :ivar y2: Subtitle corner Y coordinate in pixels
    """

    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0


class SubStationAlpha:

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


class WebVTT:

    """
    Attributes for the WebVTT format.

    :ivar comment: Optional comment string (including "NOTE")
    :ivar id: Optional cue identifier
    :ivar settings: Optional cue settings (position etc.)
    :ivar style: Optional CSS style block (including "STYLE")

    https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API
    """

    comment = ""
    id = ""
    settings = ""
    style = ""


def new(name):
    """Return a new container instance given the container's `name`."""
    if name == "ssa":
        return SubStationAlpha()
    if name == "subrip":
        return SubRip()
    if name == "webvtt":
        return WebVTT()
    raise ValueError("Invalid name: {!r}"
                     .format(name))
