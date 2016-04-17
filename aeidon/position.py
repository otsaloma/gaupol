# -*- coding: utf-8 -*-

# Copyright (C) 2011 Osmo Salomaa
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

"""Mapping position types to basic Python types."""

# aeidon handles frames as integers, seconds as floats and times as strings.
# Some functions accept a "position" argument, which will be interpreted based
# on its type. These functions are introduced here so that callers can use
# 'as_*' to ensure argument types and functions can use 'is_*' to check
# argument types, all in a way which is compatible with the old ambiguous way
# of using int, float and str directly.

__all__ = (
    "as_frame",
    "as_seconds",
    "as_time",
    "is_frame",
    "is_seconds",
    "is_time",
)

def as_frame(pos):
    """Return `pos` as type frame."""
    return int(pos)

def as_seconds(pos):
    """Return `pos` as type seconds."""
    return float(pos)

def as_time(pos):
    """Return `pos` as type time."""
    return str(pos)

def is_frame(pos):
    """Return ``True`` if `pos` is of type frame."""
    return isinstance(pos, int)

def is_seconds(pos):
    """Return ``True`` if `pos` is of type seconds."""
    return isinstance(pos, float)

def is_time(pos):
    """Return ``True`` if `pos` is of type time."""
    return isinstance(pos, str)
