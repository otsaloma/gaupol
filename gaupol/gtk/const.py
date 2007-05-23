# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Constants."""

# pylint: disable-msg=E1101


import gtk

from gaupol.base import const
from gaupol.const import *
from gaupol.i18n import _


COLUMN = const.Section()
COLUMN.NO = const.Member()
COLUMN.NO.display_name = _("No.")
COLUMN.NO.uim_action_name = "toggle_number_column"
COLUMN.NO.uim_path = "/ui/menubar/view/columns/number"
COLUMN.START = const.Member()
COLUMN.START.display_name = _("Start")
COLUMN.START.uim_action_name = "toggle_show_column"
COLUMN.START.uim_path = "/ui/menubar/view/columns/show"
COLUMN.END = const.Member()
COLUMN.END.display_name = _("End")
COLUMN.END.uim_action_name = "toggle_hide_column"
COLUMN.END.uim_path = "/ui/menubar/view/columns/hide"
COLUMN.DURN = const.Member()
COLUMN.DURN.display_name = _("Duration")
COLUMN.DURN.uim_action_name = "toggle_duration_column"
COLUMN.DURN.uim_path = "/ui/menubar/view/columns/duration"
COLUMN.MTXT = const.Member()
COLUMN.MTXT.display_name = _("Main Text")
COLUMN.MTXT.uim_action_name = "toggle_main_text_column"
COLUMN.MTXT.uim_path = "/ui/menubar/view/columns/main_text"
COLUMN.TTXT = const.Member()
COLUMN.TTXT.display_name = _("Translation Text")
COLUMN.TTXT.uim_action_name = "toggle_translation_text_column"
COLUMN.TTXT.uim_path = "/ui/menubar/view/columns/translation_text"
COLUMN.finalize()

FRAMERATE.P24.uim_action_name = "show_framerate_24"
FRAMERATE.P24.uim_path = "/ui/menubar/view/framerate/24"
FRAMERATE.P25.uim_action_name = "show_framerate_25"
FRAMERATE.P25.uim_path = "/ui/menubar/view/framerate/25"
FRAMERATE.P30.uim_action_name = "show_framerate_30"
FRAMERATE.P30.uim_path = "/ui/menubar/view/framerate/30"
FRAMERATE.finalize()

LENGTH_UNIT = const.Section()
LENGTH_UNIT.CHAR = const.Member()
LENGTH_UNIT.CHAR.display_name = _("characters")
LENGTH_UNIT.EM = const.Member()
# Translators: Unit of measurement, equal to the width of the letter M.
LENGTH_UNIT.EM.display_name = _("ems")
LENGTH_UNIT.finalize()

MODE.TIME.uim_action_name = "show_times"
MODE.TIME.uim_path = "/ui/menubar/view/times"
MODE.FRAME.uim_action_name = "show_frames"
MODE.FRAME.uim_path = "/ui/menubar/view/frames"
MODE.finalize()

TARGET = const.Section()
TARGET.SELECTED = const.Member()
TARGET.CURRENT = const.Member()
TARGET.ALL = const.Member()
TARGET.finalize()

TOOLBAR_STYLE = const.Section()
TOOLBAR_STYLE.DEFAULT = const.Member()
TOOLBAR_STYLE.DEFAULT.value = None
TOOLBAR_STYLE.ICONS = const.Member()
TOOLBAR_STYLE.ICONS.value = gtk.TOOLBAR_ICONS
TOOLBAR_STYLE.TEXT = const.Member()
TOOLBAR_STYLE.TEXT.value = gtk.TOOLBAR_TEXT
TOOLBAR_STYLE.BOTH = const.Member()
TOOLBAR_STYLE.BOTH.value = gtk.TOOLBAR_BOTH
TOOLBAR_STYLE.BOTH_HORIZ = const.Member()
TOOLBAR_STYLE.BOTH_HORIZ.value = gtk.TOOLBAR_BOTH_HORIZ
TOOLBAR_STYLE.finalize()

__all__ = [x for x in dir() if x.isupper()]
