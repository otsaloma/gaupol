# -*- coding: utf-8 -*-

# Copyright (C) 2016 Osmo Salomaa
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

"""Miscellanous enumerations."""

import aeidon

from aeidon.i18n import _
from gi.repository import Gtk

__all__ = [
    "fields",
    "length_units",
    "orientation",
    "targets",
    "toolbar_styles",
]


class FieldNumber(aeidon.EnumerationItem):
    is_position = False
    is_text = False
    label = _("No.")
    tooltip = _("Subtitle number")

class FieldStart(aeidon.EnumerationItem):
    is_position = True
    is_text = False
    label = _("Start")
    tooltip = _("Start position")

class FieldEnd(aeidon.EnumerationItem):
    is_position = True
    is_text = False
    label = _("End")
    tooltip = _("End position")

class FieldDuration(aeidon.EnumerationItem):
    is_position = True
    is_text = False
    # TRANSLATORS: 'Dur.' is short for duration. It is used in the header
    # of a column that contains numbers five digits wide.
    label = _("Dur.")
    tooltip = _("Duration")

class FieldMainText(aeidon.EnumerationItem):
    is_position = False
    is_text = True
    label = _("Text")
    tooltip = _("Text")

class FieldTranslationText(aeidon.EnumerationItem):
    is_position = False
    is_text = True
    label = _("Translation")
    tooltip = _("Translation")

fields = aeidon.Enumeration()
fields.NUMBER = FieldNumber()
fields.START = FieldStart()
fields.END = FieldEnd()
fields.DURATION = FieldDuration()
fields.MAIN_TEXT = FieldMainText()
fields.TRAN_TEXT = FieldTranslationText()


class LengthUnitChar(aeidon.EnumerationItem):
    label = _("characters")

class LengthUnitEm(aeidon.EnumerationItem):
    label = _("ems")

length_units = aeidon.Enumeration()
length_units.CHAR = LengthUnitChar()
length_units.EM = LengthUnitEm()


class OrientationHorizontal(aeidon.EnumerationItem):
    value = Gtk.Orientation.HORIZONTAL

class OrientationVertical(aeidon.EnumerationItem):
    value = Gtk.Orientation.VERTICAL

orientation = aeidon.Enumeration()
orientation.HORIZONTAL = OrientationHorizontal()
orientation.VERTICAL = OrientationVertical()


class TargetSelected(aeidon.EnumerationItem): pass
class TargetSelectedToEnd(aeidon.EnumerationItem): pass
class TargetCurrent(aeidon.EnumerationItem): pass
class TargetAll(aeidon.EnumerationItem): pass

targets = aeidon.Enumeration()
targets.SELECTED = TargetSelected()
targets.SELECTED_TO_END = TargetSelectedToEnd()
targets.CURRENT = TargetCurrent()
targets.ALL = TargetAll()


class ToolbarStyleBoth(aeidon.EnumerationItem):
    value = Gtk.ToolbarStyle.BOTH

class ToolbarStyleBothHoriz(aeidon.EnumerationItem):
    value = Gtk.ToolbarStyle.BOTH_HORIZ

class ToolbarStyleIcons(aeidon.EnumerationItem):
    value = Gtk.ToolbarStyle.ICONS

class ToolbarStyleText(aeidon.EnumerationItem):
    value = Gtk.ToolbarStyle.TEXT

toolbar_styles = aeidon.Enumeration()
toolbar_styles.ICONS = ToolbarStyleIcons()
toolbar_styles.TEXT = ToolbarStyleText()
toolbar_styles.BOTH = ToolbarStyleBoth()
toolbar_styles.BOTH_HORIZ = ToolbarStyleBothHoriz()
