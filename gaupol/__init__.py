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

"""GTK+ user interface for the Gaupol subtitle editor."""

__version__ = "1.6"
COMBO_SEPARATOR = "<separator/>"

import sys
import warnings

if hasattr(sys, "frozen"):
    # Avoid error trying to write to non-existent stderr.
    # https://stackoverflow.com/a/35773092
    warnings.simplefilter("ignore")

import aeidon
import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")

for module, version in {
    "Gst": "1.0",
    "GstPbutils": "1.0",
    "GstVideo": "1.0",
}.items():
    with aeidon.util.silent(Exception):
        gi.require_version(module, version)

from gi.repository import GLib

with aeidon.util.silent(Exception):
    from gi.repository import Gst
    Gst.init(None)

from gaupol.urls import * # noqa
from gaupol import util # noqa
from gaupol.enums import * # noqa
from gaupol.errors import * # noqa
from gaupol.attrdict import * # noqa
from gaupol.config import ConfigurationStore # noqa
conf = ConfigurationStore()
from gaupol import style # noqa
from gaupol import ruler # noqa
from gaupol.entries import * # noqa
from gaupol.renderers import * # noqa
from gaupol.floatlabel import * # noqa
from gaupol.spell import * # noqa
from gaupol.view import * # noqa
from gaupol.page import * # noqa
from gaupol.player import * # noqa
from gaupol.dialogs.builder import * # noqa
from gaupol.dialogs.file import * # noqa
from gaupol.dialogs.open import * # noqa
from gaupol.dialogs.save import * # noqa
from gaupol.dialogs.video import * # noqa
from gaupol.dialogs.append import * # noqa
from gaupol.dialogs.about import * # noqa
from gaupol.dialogs.debug import * # noqa
from gaupol.dialogs.duration_adjust import * # noqa
from gaupol.dialogs.encoding import * # noqa
from gaupol.dialogs.framerate_convert import * # noqa
from gaupol.dialogs.insert import * # noqa
from gaupol.dialogs.language import * # noqa
from gaupol.dialogs.message import * # noqa
from gaupol.dialogs.multi_close import * # noqa
from gaupol.dialogs.multi_save import * # noqa
from gaupol.dialogs.preferences import * # noqa
from gaupol.dialogs.preview_error import * # noqa
from gaupol.dialogs.search import * # noqa
from gaupol.dialogs.position_shift import * # noqa
from gaupol.dialogs.spell_check import * # noqa
from gaupol.dialogs.split import * # noqa
from gaupol.dialogs.text_edit import * # noqa
from gaupol.dialogs.position_transform import * # noqa
from gaupol.assistants import * # noqa
from gaupol.action import * # noqa
from gaupol import actions # noqa
from gaupol.extension import * # noqa
from gaupol.extensionman import * # noqa
from gaupol import agents # noqa
from gaupol.application import * # noqa
from gaupol.applicationman import ApplicationManager # noqa
from gaupol.unittest import * # noqa

def main(args):
    """Initialize application."""
    global appman
    # Needed to see application icon on Wayland, while we don't yet
    # use the reverse domain application ID with Gtk.Application.
    # https://wiki.gnome.org/Projects/GnomeShell/ApplicationBased
    # https://github.com/otsaloma/gaupol/issues/62
    GLib.set_prgname("gaupol")
    aeidon.i18n.bind()
    appman = ApplicationManager(args)
    raise SystemExit(appman.run())
