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

"""Enumerations for toolbar style types."""

import aeidon

from gi.repository import Gtk

__all__ = ("toolbar_styles",)


class Both(aeidon.EnumerationItem):

    value = Gtk.ToolbarStyle.BOTH


class BothHoriz(aeidon.EnumerationItem):

    value = Gtk.ToolbarStyle.BOTH_HORIZ


class Default(aeidon.EnumerationItem):

    value = None


class Icons(aeidon.EnumerationItem):

    value = Gtk.ToolbarStyle.ICONS


class Text(aeidon.EnumerationItem):

    value = Gtk.ToolbarStyle.TEXT


toolbar_styles = aeidon.Enumeration()
toolbar_styles.DEFAULT = Default()
toolbar_styles.ICONS = Icons()
toolbar_styles.TEXT = Text()
toolbar_styles.BOTH = Both()
toolbar_styles.BOTH_HORIZ = BothHoriz()
