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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

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

from gaupol.urls import BUG_REPORT_URL
from gaupol.urls import DOCUMENTATION_URL
from gaupol.urls import HOMEPAGE_URL
from gaupol.urls import REGEX_HELP_URL
from gaupol import util
from gaupol.enums import fields
from gaupol.enums import length_units
from gaupol.enums import orientation
from gaupol.enums import targets
from gaupol.errors import Default
from gaupol.attrdict import AttributeDictionary
from gaupol.config import ConfigurationStore
conf = ConfigurationStore()
from gaupol import style
from gaupol import ruler
from gaupol.entries import TimeEntry
from gaupol.renderers import FloatCellRenderer
from gaupol.renderers import IntegerCellRenderer
from gaupol.renderers import MultilineCellRenderer
from gaupol.renderers import MultilineDiffCellRenderer
from gaupol.renderers import TimeCellRenderer
from gaupol.toast import Toast
from gaupol.spell import SpellChecker
from gaupol.view import View
from gaupol.page import Page
from gaupol.player import VideoPlayer
from gaupol.dialogs.builder import BuilderDialog
from gaupol.dialogs.file import FileDialog
from gaupol.dialogs.open import OpenDialog
from gaupol.dialogs.save import SaveDialog
from gaupol.dialogs.video import VideoDialog
from gaupol.dialogs.append import AppendDialog
from gaupol.dialogs.about import AboutDialog
from gaupol.dialogs.debug import DebugDialog
from gaupol.dialogs.duration_adjust import DurationAdjustDialog
from gaupol.dialogs.encoding import EncodingDialog
from gaupol.dialogs.encoding import MenuEncodingDialog
from gaupol.dialogs.framerate_convert import FramerateConvertDialog
from gaupol.dialogs.insert import InsertDialog
from gaupol.dialogs.language import LanguageDialog
from gaupol.dialogs.message import ErrorDialog
from gaupol.dialogs.message import InfoDialog
from gaupol.dialogs.message import QuestionDialog
from gaupol.dialogs.message import WarningDialog
from gaupol.dialogs.multi_close import MultiCloseDialog
from gaupol.dialogs.multi_save import MultiSaveDialog
from gaupol.dialogs.preferences import PreferencesDialog
from gaupol.dialogs.preview_error import PreviewErrorDialog
from gaupol.dialogs.search import SearchDialog
from gaupol.dialogs.position_shift import FrameShiftDialog
from gaupol.dialogs.position_shift import TimeShiftDialog
from gaupol.dialogs.spell_check import SpellCheckDialog
from gaupol.dialogs.split import SplitDialog
from gaupol.dialogs.text_edit import TextEditDialog
from gaupol.dialogs.position_transform import FrameTransformDialog
from gaupol.dialogs.position_transform import TimeTransformDialog
from gaupol.assistants import TextAssistant
from gaupol.assistants import TextAssistantPage
from gaupol.action import Action
from gaupol.action import OpenRecentTranslationFileAction
from gaupol.action import RadioAction
from gaupol.action import ToggleAction
from gaupol import actions
from gaupol import agents
from gaupol.application import Application
from gaupol.applicationman import ApplicationManager
from gaupol.unittest import TestCase

def main(args):
    """Initialize application."""
    global appman
    aeidon.i18n.bind()
    appman = ApplicationManager(args)
    raise SystemExit(appman.run())
