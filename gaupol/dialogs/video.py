# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

"""Dialog for selecting a video file."""

import aeidon
import sys
_ = aeidon.i18n._

from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("VideoDialog",)


class VideoDialog(Gtk.FileChooserDialog):

    """Dialog for selecting a video file."""

    def __init__(self, parent, title, button_label):
        """Initialize a :class:`VideoDialog` object."""
        GObject.GObject.__init__(self)
        self.set_title(title)
        self.set_transient_for(parent)
        self.set_action(Gtk.FileChooserAction.OPEN)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(button_label, Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self._init_filters()

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
        if sys.platform == "win32":
            # Mimetype detection seems unreliable on Windows.
            # We could enumerate filename extensions instead
            # of using mimetypes, but I'm feeling lazy.
            self.set_filter(all_filter)
        else:
            self.set_filter(video_filter)
