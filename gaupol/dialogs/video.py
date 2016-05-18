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

"""Dialog for selecting a video file."""

import sys

from aeidon.i18n   import _
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("VideoDialog",)


class VideoDialog(Gtk.FileChooserDialog):

    """Dialog for selecting a video file."""

    def __init__(self, parent, title, button_label):
        """Initialize a :class:`VideoDialog` instance."""
        GObject.GObject.__init__(self)
        self._init_dialog(parent, title, button_label)
        self._init_filters()

    def _init_dialog(self, parent, title, button_label):
        """Initialize the dialog."""
        self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(button_label, Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_transient_for(parent)
        self.set_title(title)
        self.set_action(Gtk.FileChooserAction.OPEN)

    def _init_filters(self):
        """Intialize the file filters."""
        all_filter = Gtk.FileFilter()
        all_filter.add_pattern("*")
        all_filter.set_name(_("All files"))
        self.add_filter(all_filter)
        video_filter = Gtk.FileFilter()
        video_filter.add_mime_type("video/*")
        video_filter.set_name(_("Video files"))
        self.add_filter(video_filter)
        # Mimetype detection seems unreliable on Windows.
        self.set_filter(all_filter if sys.platform == "win32"
                        else video_filter)
