# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Dialog for selecting a video file."""


import gaupol.gtk
import gtk
_ = gaupol.i18n._


class VideoDialog(gtk.FileChooserDialog):

    """Dialog for selecting a video file."""

    def __init__(self, parent):

        gtk.FileChooserDialog.__init__(self)
        self.set_title(_("Select Video"))
        self.set_transient_for(parent)
        self.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(_("_Select"), gtk.RESPONSE_OK)
        self.set_default_response(gtk.RESPONSE_OK)
        self._init_filters()

    def _init_filters(self):
        """Intialize the file filters."""

        file_filter = gtk.FileFilter()
        file_filter.add_pattern("*")
        file_filter.set_name(_("All files"))
        self.add_filter(file_filter)

        file_filter = gtk.FileFilter()
        file_filter.add_mime_type("video/*")
        file_filter.set_name(_("Video files"))
        self.add_filter(file_filter)
        self.set_filter(file_filter)
