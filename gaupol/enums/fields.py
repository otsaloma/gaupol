# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009 Osmo Salomaa
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

"""Enumerations for subtitle field types."""

import aeidon
_ = aeidon.i18n._

__all__ = ("fields",)


class Number(aeidon.EnumerationItem):

    is_position = False
    is_text = False
    label = _("No.")
    tooltip = _("Subtitle number")


class Start(aeidon.EnumerationItem):

    is_position = True
    is_text = False
    label = _("Start")
    tooltip = _("Start position")


class End(aeidon.EnumerationItem):

    is_position = True
    is_text = False
    label = _("End")
    tooltip = _("End position")


class Duration(aeidon.EnumerationItem):

    is_position = True
    is_text = False
    # Translators: 'Dur.' is short for duration. It is used in the header of a
    # tree view column that contains numbers five characters wide.
    label = _("Dur.")
    tooltip = _("Duration")


class MainText(aeidon.EnumerationItem):

    is_position = False
    is_text = True
    label = _("Main Text")
    tooltip = _("Main text")


class TranslationText(aeidon.EnumerationItem):

    is_position = False
    is_text = True
    label = _("Translation Text")
    tooltip = _("Translation text")


fields = aeidon.Enumeration()
fields.NUMBER = Number()
fields.START = Start()
fields.END = End()
fields.DURATION = Duration()
fields.MAIN_TEXT = MainText()
fields.TRAN_TEXT = TranslationText()
