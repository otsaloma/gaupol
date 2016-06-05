# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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

"""
GTK+ user interface for the Gaupol subtitle editor.

:var COMBO_SEPARATOR: String used as a separator for :class:`Gtk.ComboBox`

   :attr:`COMBO_SEPARATOR` can be inserted into a combo box's model,
   and :func:`gaupol.util.separate_combo` will recognize it.

:var BUG_REPORT_URL: Web page where to submit bug reports
:var DOCUMENTATION_URL: Documentation for users
:var HOMEPAGE_URL: Gaupol web pages
:var REGEX_HELP_URL: Documentation on regular expressions

:var fields: Enumerations for subtitle field types
:var length_units: Enumerations for length unit types
:var orientation: Enumerations for orientation types
:var targets: Enumerations for action target types
:var toolbar_styles: Enumerations for toolbar style types

:var field_actions: Dictionary mapping :attr:`gaupol.formats` to actions
:var framerate_actions: Dictionary mapping :attr:`aeidon.framerates` to actions
:var mode_actions: Dictionary mapping :attr:`aeidon.modes` to actions

:var conf: Instance of :class:`gaupol.ConfigurationStore` used
"""

__version__ = "0.28.2"
COMBO_SEPARATOR = "<separator/>"

import aeidon
import os

import gi
gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")

with aeidon.util.silent(Exception):
    gi.require_version("GdkX11", "3.0")
    gi.require_version("Gst", "1.0")
    gi.require_version("GstPbutils", "1.0")

from gi.repository import GLib
from gi.repository import GObject

GLib.threads_init()
GObject.threads_init()

with aeidon.util.silent(Exception):
    from gi.repository import Gst
    Gst.init(None)

from gaupol.urls import *
from gaupol import util
from gaupol.enums import *
from gaupol.enum_actions import *
from gaupol.errors import *
from gaupol.attrdict import *
from gaupol.config import *
conf = ConfigurationStore()
from gaupol import style
from gaupol import ruler
from gaupol.entries import *
from gaupol.renderers import *
from gaupol.floatlabel import *
from gaupol.view import *
from gaupol.page import *
from gaupol.player import *
from gaupol.dialogs.builder import *
from gaupol.dialogs.file import *
from gaupol.dialogs.open import *
from gaupol.dialogs.save import *
from gaupol.dialogs.video import *
from gaupol.dialogs.append import *
from gaupol.dialogs.about import *
from gaupol.dialogs.debug import *
from gaupol.dialogs.duration_adjust import *
from gaupol.dialogs.encoding import *
from gaupol.dialogs.framerate_convert import *
from gaupol.dialogs.insert import *
from gaupol.dialogs.language import *
from gaupol.dialogs.message import *
from gaupol.dialogs.multi_close import *
from gaupol.dialogs.multi_save import *
from gaupol.dialogs.preferences import *
from gaupol.dialogs.preview_error import *
from gaupol.dialogs.search import *
from gaupol.dialogs.position_shift import *
from gaupol.dialogs.spell_check import *
from gaupol.dialogs.split import *
from gaupol.dialogs.text_edit import *
from gaupol.dialogs.position_transform import *
from gaupol.assistants import *
from gaupol.action import *
from gaupol import actions
from gaupol.extension import *
from gaupol.extensionman import *
from gaupol import agents
from gaupol.application import *
from gaupol.applicationman import *
from gaupol.unittest import *

def main(args):
    """Initialize application."""
    global appman
    appman = ApplicationManager(args)
    raise SystemExit(appman.run())
