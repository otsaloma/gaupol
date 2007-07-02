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


"""GTK user interface.

Module variables:
 * BUSY_CURSOR: gtk.gdk.Cursor used when application not idle
 * COMBO_SEPARATOR: String rendered as a separator in combo boxes
 * EXTRA: Extra length to add to size calculations
 * HAND_CURSOR: gtk.gdk.Cursor for use with hyperlinks
 * INSERT_CURSOR: gtk.gdk.Cursor for editable text widgets
 * NORMAL_CURSOR: gtk.gdk.Cursor used by default

When setting dialog sizes based on their content, we get the size request of
the scrolled window component and add the surroundings to that. For this to
work neatly we should add some extra to adapt to different widget sizes in
different themes. Let the EXTRA constant very vaguely account for that.
"""


import gaupol
import gobject
import gtk.glade
import inspect
import os

module = inspect.getmodule(lambda: True)
gaupol.__dict__["gtk"] = module
gtk.rc_parse(os.path.join(gaupol.DATA_DIR, "gtkrc"))
gtk.glade.bindtextdomain("gaupol", gaupol.LOCALE_DIR)
gtk.glade.textdomain("gaupol")
gobject.threads_init()


EXTRA = 36
COMBO_SEPARATOR = "<separator/>"

BUSY_CURSOR = gtk.gdk.Cursor(gtk.gdk.WATCH)
HAND_CURSOR = gtk.gdk.Cursor(gtk.gdk.HAND2)
INSERT_CURSOR = gtk.gdk.Cursor(gtk.gdk.XTERM)
NORMAL_CURSOR = gtk.gdk.Cursor(gtk.gdk.LEFT_PTR)


from gaupol.gtk.const import *
from gaupol.gtk.errors import *
from gaupol.gtk import conf
from gaupol.gtk import ruler
from gaupol.gtk import util
from gaupol.gtk.meta import *
from gaupol.gtk.runner import *
from gaupol.gtk.tooltips import *
from gaupol.gtk.entries import *
from gaupol.gtk.renderers import *
from gaupol.gtk.output import *
from gaupol.gtk.view import *
from gaupol.gtk.page import *
from gaupol.gtk.dialogs import *
from gaupol.gtk import actions
from gaupol.gtk import agents
from gaupol.gtk.application import *
from gaupol.gtk import main
