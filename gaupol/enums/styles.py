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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Enumerations for toolbar style types."""

import aeidon
import gtk

__all__ = ("toolbar_styles",)


class Both(aeidon.EnumerationItem):

    value = gtk.TOOLBAR_BOTH


class BothHoriz(aeidon.EnumerationItem):

    value = gtk.TOOLBAR_BOTH_HORIZ


class Default(aeidon.EnumerationItem):

    value = None


class Icons(aeidon.EnumerationItem):

    value = gtk.TOOLBAR_ICONS


class Text(aeidon.EnumerationItem):

    value = gtk.TOOLBAR_TEXT


toolbar_styles = aeidon.Enumeration()
toolbar_styles.DEFAULT = Default()
toolbar_styles.ICONS = Icons()
toolbar_styles.TEXT = Text()
toolbar_styles.BOTH = Both()
toolbar_styles.BOTH_HORIZ = BothHoriz()
