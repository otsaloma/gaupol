# Copyright (C) 2005-2007 Osmo Salomaa
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


"""Constants."""

# pylint: disable-msg=E1101,W0201


import gaupol
import gtk
_ = gaupol.i18n._

from gaupol.const import *


COLUMN = gaupol.ConstantSection()
COLUMN.NUMBER = gaupol.ConstantMember()
COLUMN.NUMBER.action = "toggle_number_column"
COLUMN.NUMBER.label = _("No.")
COLUMN.START = gaupol.ConstantMember()
COLUMN.START.action = "toggle_start_column"
COLUMN.START.label = _("Start")
COLUMN.END = gaupol.ConstantMember()
COLUMN.END.action = "toggle_end_column"
COLUMN.END.label = _("End")
COLUMN.DURATION = gaupol.ConstantMember()
COLUMN.DURATION.action = "toggle_duration_column"
COLUMN.DURATION.label = _("Duration")
COLUMN.MAIN_TEXT = gaupol.ConstantMember()
COLUMN.MAIN_TEXT.action = "toggle_main_text_column"
COLUMN.MAIN_TEXT.label = _("Main Text")
COLUMN.TRAN_TEXT = gaupol.ConstantMember()
COLUMN.TRAN_TEXT.action = "toggle_translation_text_column"
COLUMN.TRAN_TEXT.label = _("Translation Text")
COLUMN.finalize()

FRAMERATE.P24.action = "show_framerate_24"
FRAMERATE.P25.action = "show_framerate_25"
FRAMERATE.P30.action = "show_framerate_30"
FRAMERATE.finalize()

LENGTH_UNIT = gaupol.ConstantSection()
LENGTH_UNIT.CHAR = gaupol.ConstantMember()
LENGTH_UNIT.CHAR.label = _("characters")
LENGTH_UNIT.EM = gaupol.ConstantMember()
LENGTH_UNIT.EM.label = _("ems")
LENGTH_UNIT.finalize()

MODE.TIME.action = "show_times"
MODE.FRAME.action = "show_frames"
MODE.finalize()

TARGET = gaupol.ConstantSection()
TARGET.SELECTED = gaupol.ConstantMember()
TARGET.CURRENT = gaupol.ConstantMember()
TARGET.ALL = gaupol.ConstantMember()
TARGET.finalize()

TOOLBAR_STYLE = gaupol.ConstantSection()
TOOLBAR_STYLE.DEFAULT = gaupol.ConstantMember()
TOOLBAR_STYLE.DEFAULT.value = None
TOOLBAR_STYLE.ICONS = gaupol.ConstantMember()
TOOLBAR_STYLE.ICONS.value = gtk.TOOLBAR_ICONS
TOOLBAR_STYLE.TEXT = gaupol.ConstantMember()
TOOLBAR_STYLE.TEXT.value = gtk.TOOLBAR_TEXT
TOOLBAR_STYLE.BOTH = gaupol.ConstantMember()
TOOLBAR_STYLE.BOTH.value = gtk.TOOLBAR_BOTH
TOOLBAR_STYLE.BOTH_HORIZ = gaupol.ConstantMember()
TOOLBAR_STYLE.BOTH_HORIZ.value = gtk.TOOLBAR_BOTH_HORIZ
TOOLBAR_STYLE.finalize()

__all__ = [x for x in dir() if x.isupper()]
