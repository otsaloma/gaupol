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


"""Dialog for informing that preview failed."""


import gtk
import pango

from gaupol.gtk import util
from .glade import GladeDialog


class PreviewErrorDialog(GladeDialog):

    """Dialog for informing that preview failed.

    Instance variables:

        _text_view: gtk.TextView
    """

    def __init__(self, parent, output):

        GladeDialog.__init__(self, "previewerr-dialog")
        self._text_view = self._glade_xml.get_widget("text_view")

        self._init_data(output)
        self._init_sizes(output)
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self, output):
        """Initialize the output data in the text view."""

        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag("code", family="monospace")
        end_iter = text_buffer.get_end_iter()
        text_buffer.insert_with_tags_by_name(end_iter, output, "code")

    def _init_sizes(self, output):
        """Initialize widget sizes."""

        label = gtk.Label()
        attrs = pango.AttrList()
        attrs.insert(pango.AttrFamily("monospace", 0, -1))
        label.set_attributes(attrs)
        label.set_text(output)
        width, height = label.size_request()
        width = width + 112 + util.EXTRA
        height = height + 148 + util.EXTRA
        util.resize_message_dialog(self._dialog, width, height)
