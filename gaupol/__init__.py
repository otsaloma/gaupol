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

import aeidon
import gobject
import gtk.glade
import os

aeidon.util.install_module("gtk", lambda: None)
gtk.rc_parse(os.path.join(aeidon.DATA_DIR, "ui", "gtkrc"))
gtk.glade.bindtextdomain("aeidon", aeidon.LOCALE_DIR)
gtk.glade.textdomain("aeidon")
gobject.threads_init()

COMBO_SEPARATOR = "<separator/>"
EXTRA = 36

from gaupol.unittest import *
from gaupol.fields import *
from gaupol.styles import *
from gaupol.targets import *
from gaupol.units import *
from gaupol.enumuim import *
from gaupol.errors import *
from gaupol import conf
from gaupol.conf import *
from gaupol import ruler
from gaupol import util
from gaupol.meta import *
from gaupol.runner import *
from gaupol.entries import *
from gaupol.renderers import *
from gaupol.extension import *
from gaupol.extensionman import *
from gaupol.output import *
from gaupol.view import *
from gaupol.page import *
from gaupol.dialogs.about import *
from gaupol.dialogs.glade import *
from gaupol.dialogs.message import *
from gaupol.dialogs.debug import *
from gaupol.dialogs.encoding import *
from gaupol.dialogs.language import *
from gaupol.dialogs.previewerr import *
from gaupol.dialogs.textedit import *
from gaupol.dialogs.file import *
from gaupol.dialogs.open import *
from gaupol.dialogs.append import *
from gaupol.dialogs.save import *
from gaupol.dialogs.video import *
from gaupol.dialogs.duration import *
from gaupol.dialogs.framerate import *
from gaupol.dialogs.header import *
from gaupol.dialogs.insert import *
from gaupol.dialogs.multiclose import *
from gaupol.dialogs.preferences import *
from gaupol.dialogs.search import *
from gaupol.dialogs.shift import *
from gaupol.dialogs.spellcheck import *
from gaupol.dialogs.split import *
from gaupol.dialogs.transform import *
from gaupol.assistants import *
from gaupol.action import *
from gaupol import actions
from gaupol import agents
from gaupol.application import *
from gaupol import main
