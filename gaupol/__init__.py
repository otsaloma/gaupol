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

"""GTK user interface for the Gaupol subtitle editor."""

__version__ = "1.99"
COMBO_SEPARATOR = "<separator/>"

import contextlib
import sys
import warnings

if hasattr(sys, "frozen"):
    # Avoid error trying to write to non-existent stderr.
    # https://stackoverflow.com/a/35773092
    warnings.simplefilter("ignore")

# Needed for the spell-check dialog, where the '_proceed' function call is
# recursive. The recursion limit effectively defines the maximum allowed
# amount of consecutive subtitles without spelling errors, which if exceeded
# triggers a RecursionError.
sys.setrecursionlimit(10000)

import aeidon
import gi
import os

# Disable gst-vaapi as it doesn't seem to work with the GTK video sink.
# https://github.com/otsaloma/gaupol/issues/79
os.environ["LIBVA_DRIVER_NAME"] = "null"
os.environ["LIBVA_DRIVERS_PATH"] = "/dev/null"

gi.require_version("Gdk", "4.0")
gi.require_version("Graphene", "1.0")
gi.require_version("Gsk", "4.0")
gi.require_version("Gtk", "4.0")

with contextlib.suppress(Exception):
    gi.require_version("GtkSource", "5")

for module, version in {
    "Gst": "1.0",
    "GstPbutils": "1.0",
    "GstVideo": "1.0",
    "GstTag": "1.0",
}.items():
    with contextlib.suppress(Exception):
        gi.require_version(module, version)

with contextlib.suppress(Exception):
    from gi.repository import Gst
    Gst.init(None)

from gaupol.urls import *
from gaupol import util
from gaupol.enums import *
from gaupol.errors import *
from gaupol.attrdict import *
from gaupol.config import ConfigurationStore
conf = ConfigurationStore()
from gaupol import style
from gaupol import ruler
from gaupol.entries import *
from gaupol.renderers import *
from gaupol.toast import *
from gaupol.spell import *
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
from gaupol import agents
from gaupol.application import *
from gaupol.applicationman import ApplicationManager
from gaupol.unittest import *

def main(args):
    """Initialize application."""
    global appman
    aeidon.i18n.bind()
    appman = ApplicationManager(args)
    raise SystemExit(appman.run())
