# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Dialog to inform that preview command failed."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk
import pango

from gaupol.gtk.util import config, gtklib


class PreviewErrorDialog(object):

    """Dialog to inform that preview command failed."""

    def __init__(self, parent, output):

        glade_xml = gtklib.get_glade_xml('previewerror-dialog')

        self._dialog    = glade_xml.get_widget('dialog')
        self._text_view = glade_xml.get_widget('text_view')

        self._init_data(output)
        self._init_sizes(output)

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self, output):
        """Initialize output data."""

        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag('code', family='monospace')
        end_iter = text_buffer.get_end_iter()
        text_buffer.insert_with_tags_by_name(end_iter, output, 'code')

    def _init_sizes(self, output):
        """Initialize dialog size."""

        label = gtk.Label()
        attrs = pango.AttrList()
        attrs.insert(pango.AttrFamily('monospace', 0, -1))
        label.set_attributes(attrs)
        label.set_text(output)
        width, height = label.size_request()
        width  = width  + 112 + gtklib.EXTRA
        height = height + 148 + gtklib.EXTRA
        gtklib.resize_message_dialog(self._dialog, width, height)

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def run(self):
        """Show and run the dialog."""

        self._dialog.show()
        return self._dialog.run()


if __name__ == '__main__':

    from gaupol.test import Test

    class TestPreviewErrorDialog(Test):

        def test_init(self):

            dialog = PreviewErrorDialog(gtk.Window(), 'test')

    TestPreviewErrorDialog().run()
