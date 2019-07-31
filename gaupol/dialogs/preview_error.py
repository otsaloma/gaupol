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

"""Dialog for informing that preview failed."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import GObject
from gi.repository import Gtk


class PreviewErrorDialog(Gtk.MessageDialog):

    """Dialog for informing that preview failed."""

    def __init__(self, parent, output):
        """Initialize a :class:`PreviewErrorDialog` instance."""
        GObject.GObject.__init__(self,
                                 message_type=Gtk.MessageType.ERROR,
                                 text=_("Preview in video player failed"),
                                 secondary_text=_("There is probably a problem with either the video file or the video player. See the preferences dialog to choose the video player or to customize the command."))

        self._text_view = Gtk.TextView()
        self._init_dialog(parent)
        self._init_text_view(output)

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.add_button(_("_Close"), Gtk.ResponseType.CLOSE)
        self.set_default_response(Gtk.ResponseType.CLOSE)
        self.set_transient_for(parent)
        self.set_modal(True)

    def _init_text_view(self, output):
        """Initialize the text view."""
        self._text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self._text_view.set_editable(False)
        self._text_view.set_cursor_visible(False)
        self._text_view.set_accepts_tab(False)
        self._text_view.set_left_margin(6)
        self._text_view.set_right_margin(6)
        with aeidon.util.silent(AttributeError):
            # Available since GTK 3.18.
            self._text_view.set_top_margin(6)
            self._text_view.set_bottom_margin(6)
        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(output)
        gaupol.style.use_font(self._text_view, "monospace")
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(*((Gtk.PolicyType.AUTOMATIC,)*2))
        scroller.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        scroller.add(self._text_view)
        box = self.get_message_area()
        gaupol.util.pack_start_expand(box, scroller)
        gaupol.util.scale_to_content(self._text_view,
                                     min_nchar=60,
                                     max_nchar=100,
                                     min_nlines=10,
                                     max_nlines=25,
                                     font="monospace")

        box.show_all()
