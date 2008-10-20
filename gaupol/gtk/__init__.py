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

"""GTK+ user interface.

Constant 'COMBO_SEPARATOR' is a string rendered as a separator in combo boxes.
It can be inserted into the combo box's model, and 'util.separate_combo'
function will recognize it.

Constant 'EXTRA' is an amount of pixels to add to dialog size calculations.
When setting dialog sizes based on their content, we get the size request of
the scrolled window components and add the surroundings to that to get a nice
default dialog size. For this to work neatly we should add some extra to adapt
to different widget sizes in different themes, e.g. scrollbar widths and the
sizes of icons in buttons. Let the 'EXTRA' constant very vaguely account for
that and let it be added to each calculated dialog width and height.
"""

import gaupol
import gobject
import gtk.glade
import os

gaupol.util.install_module("gtk", lambda: None)
gtk.rc_parse(os.path.join(gaupol.DATA_DIR, "ui", "gtkrc"))
gtk.glade.bindtextdomain("gaupol", gaupol.LOCALE_DIR)
gtk.glade.textdomain("gaupol")
gobject.threads_init()

COMBO_SEPARATOR = "<separator/>"
EXTRA = 36

from gaupol.gtk.unittest import *
from gaupol.gtk.fields import *
from gaupol.gtk.styles import *
from gaupol.gtk.targets import *
from gaupol.gtk.units import *
from gaupol.gtk.errors import *
from gaupol.gtk import conf
from gaupol.gtk import ruler
from gaupol.gtk import util
from gaupol.gtk.meta import *
from gaupol.gtk.runner import *
from gaupol.gtk.entries import *
from gaupol.gtk.renderers import *
from gaupol.gtk.extension import *
from gaupol.gtk.extensionman import *
from gaupol.gtk.output import *
from gaupol.gtk.view import *
from gaupol.gtk.page import *
from gaupol.gtk.dialogs.about import *
from gaupol.gtk.dialogs.glade import *
from gaupol.gtk.dialogs.message import *
from gaupol.gtk.dialogs.debug import *
from gaupol.gtk.dialogs.encoding import *
from gaupol.gtk.dialogs.language import *
from gaupol.gtk.dialogs.previewerr import *
from gaupol.gtk.dialogs.textedit import *
from gaupol.gtk.dialogs.file import *
from gaupol.gtk.dialogs.open import *
from gaupol.gtk.dialogs.append import *
from gaupol.gtk.dialogs.save import *
from gaupol.gtk.dialogs.video import *
from gaupol.gtk.dialogs.duration import *
from gaupol.gtk.dialogs.framerate import *
from gaupol.gtk.dialogs.header import *
from gaupol.gtk.dialogs.insert import *
from gaupol.gtk.dialogs.multiclose import *
from gaupol.gtk.dialogs.preferences import *
from gaupol.gtk.dialogs.search import *
from gaupol.gtk.dialogs.shift import *
from gaupol.gtk.dialogs.spellcheck import *
from gaupol.gtk.dialogs.split import *
from gaupol.gtk.dialogs.transform import *
from gaupol.gtk.assistants import *
from gaupol.gtk.action import *
from gaupol.gtk import actions
from gaupol.gtk import agents
from gaupol.gtk.application import *
from gaupol.gtk import main
