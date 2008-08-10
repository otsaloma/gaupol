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

"""Enumerations for subtitle field types."""

import gaupol
_ = gaupol.i18n._

__all__ = ("fields",)


class Number(gaupol.EnumerationItem):

    is_position = False
    is_text = False
    label = _("No.")


class Start(gaupol.EnumerationItem):

    is_position = True
    is_text = False
    label = _("Start")


class End(gaupol.EnumerationItem):

    is_position = True
    is_text = False
    label = _("End")


class Duration(gaupol.EnumerationItem):

    is_position = True
    is_text = False
    label = _("Duration")


class MainText(gaupol.EnumerationItem):

    is_position = False
    is_text = True
    label = _("Main Text")


class TranslationText(gaupol.EnumerationItem):

    is_position = False
    is_text = True
    label = _("Translation Text")


fields = gaupol.Enumeration()
fields.NUMBER = Number()
fields.START = Start()
fields.END = End()
fields.DURATION = Duration()
fields.MAIN_TEXT = MainText()
fields.TRAN_TEXT = TranslationText()
