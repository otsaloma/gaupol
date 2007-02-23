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


"""Constants.

Module variables:

    COLUMN.NO
    COLUMN.SHOW
    COLUMN.HIDE
    COLUMN.DURN
    COLUMN.MTXT
    COLUMN.TTXT
    COLUMN.display_names
    COLUMN.members
    COLUMN.names
    COLUMN.uim_action_names
    COLUMN.uim_paths

    DOCUMENT.MAIN
    DOCUMENT.TRAN
    DOCUMENT.members
    DOCUMENT.names

    FORMAT.ASS
    FORMAT.MICRODVD
    FORMAT.MPL2
    FORMAT.MPSUB
    FORMAT.SSA
    FORMAT.SUBRIP
    FORMAT.SUBVIEWER2
    FORMAT.TMPLAYER
    FORMAT.class_names
    FORMAT.display_names
    FORMAT.extensions
    FORMAT.members
    FORMAT.names

    FRAMERATE.FR_23_976
    FRAMERATE.FR_25
    FRAMERATE.FR_29_97
    FRAMERATE.display_names
    FRAMERATE.members
    FRAMERATE.names
    FRAMERATE.mpsub_names
    FRAMERATE.uim_action_names
    FRAMERATE.uim_paths
    FRAMERATE.values

    LENGTH_UNIT.CHAR
    LENGTH_UNIT.EM
    LENGTH_UNIT.display_names
    LENGTH_UNIT.members
    LENGTH_UNIT.names

    MODE.TIME
    MODE.FRAME
    MODE.members
    MODE.names
    MODE.uim_action_names
    MODE.uim_paths

    NEWLINE.MAC
    NEWLINE.UNIX
    NEWLINE.WINDOWS
    NEWLINE.display_names
    NEWLINE.members
    NEWLINE.names
    NEWLINE.values

    REGISTER.DO
    REGISTER.UNDO
    REGISTER.REDO
    REGISTER.DO_MULTIPLE
    REGISTER.UNDO_MULTIPLE
    REGISTER.REDO_MULTIPLE
    REGISTER.members
    REGISTER.names
    REGISTER.shifts
    REGISTER.signals

    TARGET.SELECTED
    TARGET.CURRENT
    TARGET.ALL
    TARGET.members
    TARGET.names

    TOOLBAR_STYLE.DEFAULT
    TOOLBAR_STYLE.ICONS
    TOOLBAR_STYLE.TEXT
    TOOLBAR_STYLE.BOTH
    TOOLBAR_STYLE.BOTH_HORIZ
    TOOLBAR_STYLE.members
    TOOLBAR_STYLE.names
    TOOLBAR_STYLE.values

    VIDEO_PLAYER.MPLAYER
    VIDEO_PLAYER.VLC
    VIDEO_PLAYER.commands
    VIDEO_PLAYER.display_names
    VIDEO_PLAYER.members
    VIDEO_PLAYER.names
"""

# pylint: disable-msg=E1101


from gettext import gettext as _

import gtk

from gaupol.base import cons
from gaupol.cons import *


__all__ = [
    "COLUMN",
    "DOCUMENT",
    "FORMAT",
    "FRAMERATE",
    "LENGTH_UNIT",
    "MODE",
    "NEWLINE",
    "REGISTER",
    "TARGET",
    "TOOLBAR_STYLE",
    "VIDEO_PLAYER",]

COLUMN = cons.Section()
COLUMN.NO = cons.Member()
COLUMN.NO.display_name = _("No.")
COLUMN.NO.uim_action_name = "toggle_number_column"
COLUMN.NO.uim_path = "/ui/menubar/view/columns/number"
COLUMN.SHOW = cons.Member()
COLUMN.SHOW.display_name = _("Show")
COLUMN.SHOW.uim_action_name = "toggle_show_column"
COLUMN.SHOW.uim_path = "/ui/menubar/view/columns/show"
COLUMN.HIDE = cons.Member()
COLUMN.HIDE.display_name = _("Hide")
COLUMN.HIDE.uim_action_name = "toggle_hide_column"
COLUMN.HIDE.uim_path = "/ui/menubar/view/columns/hide"
COLUMN.DURN = cons.Member()
COLUMN.DURN.display_name = _("Duration")
COLUMN.DURN.uim_action_name = "toggle_duration_column"
COLUMN.DURN.uim_path = "/ui/menubar/view/columns/duration"
COLUMN.MTXT = cons.Member()
COLUMN.MTXT.display_name = _("Main Text")
COLUMN.MTXT.uim_action_name = "toggle_main_text_column"
COLUMN.MTXT.uim_path = "/ui/menubar/view/columns/main_text"
COLUMN.TTXT = cons.Member()
COLUMN.TTXT.display_name = _("Translation Text")
COLUMN.TTXT.uim_action_name = "toggle_translation_text_column"
COLUMN.TTXT.uim_path = "/ui/menubar/view/columns/translation_text"
COLUMN.finalize()

FRAMERATE.FR_23_976.uim_action_name = "show_framerate_23_976"
FRAMERATE.FR_23_976.uim_path = "/ui/menubar/view/framerate/23_976"
FRAMERATE.FR_25.uim_action_name = "show_framerate_25"
FRAMERATE.FR_25.uim_path = "/ui/menubar/view/framerate/25"
FRAMERATE.FR_29_97.uim_action_name = "show_framerate_29_97"
FRAMERATE.FR_29_97.uim_path = "/ui/menubar/view/framerate/29_97"
FRAMERATE.finalize()

LENGTH_UNIT = cons.Section()
LENGTH_UNIT.CHAR = cons.Member()
LENGTH_UNIT.CHAR.display_name = _("characters")
LENGTH_UNIT.EM = cons.Member()
LENGTH_UNIT.EM.display_name = _("ems")
LENGTH_UNIT.finalize()

MODE.TIME.uim_action_name = "show_times"
MODE.TIME.uim_path = "/ui/menubar/view/times"
MODE.FRAME.uim_action_name = "show_frames"
MODE.FRAME.uim_path = "/ui/menubar/view/frames"
MODE.finalize()

TARGET = cons.Section()
TARGET.SELECTED = cons.Member()
TARGET.CURRENT = cons.Member()
TARGET.ALL = cons.Member()
TARGET.finalize()

TOOLBAR_STYLE = cons.Section()
TOOLBAR_STYLE.DEFAULT = cons.Member()
TOOLBAR_STYLE.DEFAULT.value = None
TOOLBAR_STYLE.ICONS = cons.Member()
TOOLBAR_STYLE.ICONS.value = gtk.TOOLBAR_ICONS
TOOLBAR_STYLE.TEXT = cons.Member()
TOOLBAR_STYLE.TEXT.value = gtk.TOOLBAR_TEXT
TOOLBAR_STYLE.BOTH = cons.Member()
TOOLBAR_STYLE.BOTH.value = gtk.TOOLBAR_BOTH
TOOLBAR_STYLE.BOTH_HORIZ = cons.Member()
TOOLBAR_STYLE.BOTH_HORIZ.value = gtk.TOOLBAR_BOTH_HORIZ
TOOLBAR_STYLE.finalize()
