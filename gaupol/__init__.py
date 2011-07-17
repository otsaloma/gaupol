# Copyright (C) 2005-2010 Osmo Salomaa
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

"""GTK+ user interface for the Gaupol subtitle editor.

:var COMBO_SEPARATOR: String used as a separator for :class:`gtk.ComboBox`

   :attr:`COMBO_SEPARATOR` can be inserted into a combo box's model, and
   :func:`gaupol.util.separate_combo` will recognize it.

:var BUG_REPORT_URL: Web page where to submit new bug reports
:var EXTENSIONS_URL: Web page listing third party extensions
:var HOMEPAGE_URL: Web page of the Gaupol project
:var PREVIEW_HELP_URL: Documentation on the preview function
:var REGEX_HELP_URL: Documentation on regular expressions
:var SPEECH_RECOGNITION_HELP_URL: Documentation on speech recognition
:var WIKI_URL: Wiki documentation

:var fields: Enumerations for subtitle field types
:var length_units: Enumerations for length unit types
:var targets: Enumerations for action target types
:var toolbar_styles: Enumerations for toolbar style types

:var field_actions: Dictionary mapping :attr:`gaupol.formats` to actions
:var framerate_actions: Dictionary mapping :attr:`aeidon.framerates` to actions
:var mode_actions: Dictionary mapping :attr:`aeidon.modes` to actions

:var conf: Instance of :class:`gaupol.ConfigurationStore` used
"""

import aeidon
import glib
import gobject
import gtk
import os

__version__ = "0.19"
COMBO_SEPARATOR = "<separator/>"

glib.threads_init()
gtk.rc_parse(os.path.join(aeidon.DATA_DIR, "ui", "gtkrc"))

from gaupol.urls import *
from gaupol import util
from gaupol.enums.fields import *
from gaupol.enums.styles import *
from gaupol.enums.targets import *
from gaupol.enums.units import *
from gaupol.enumuim import *
from gaupol.errors import *
from gaupol.attrdict import *
from gaupol.config import *
conf = ConfigurationStore()
from gaupol import ruler
from gaupol.meta import *
from gaupol.entries import *
from gaupol.renderers import *
from gaupol.output import *
from gaupol.view import *
from gaupol.page import *
from gaupol.extension import *
from gaupol.dialogs.builder import *
from gaupol.dialogs.file import *
from gaupol.dialogs.open import *
from gaupol.dialogs.save import *
from gaupol.dialogs.video import *
from gaupol.dialogs.append import *
from gaupol.dialogs.about import *
from gaupol.dialogs.debug import *
from gaupol.dialogs.duration import *
from gaupol.dialogs.encoding import *
from gaupol.dialogs.framerate import *
from gaupol.dialogs.header import *
from gaupol.dialogs.insert import *
from gaupol.dialogs.language import *
from gaupol.dialogs.message import *
from gaupol.dialogs.multiclose import *
from gaupol.dialogs.multisave import *
from gaupol.dialogs.preferences import *
from gaupol.dialogs.previewerr import *
from gaupol.dialogs.recognition import *
from gaupol.dialogs.search import *
from gaupol.dialogs.shift import *
from gaupol.dialogs.spellcheck import *
from gaupol.dialogs.split import *
from gaupol.dialogs.textedit import *
from gaupol.dialogs.transform import *
from gaupol.assistants import *
from gaupol.action import *
from gaupol import actions
from gaupol.extension import *
from gaupol.extensionman import *
from gaupol import agents
from gaupol.application import *
from gaupol import main
from gaupol.unittest import *
