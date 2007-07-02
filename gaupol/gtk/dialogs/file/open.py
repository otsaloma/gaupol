# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.


"""Dialog for selecting subtitle files to open."""


import gaupol.gtk
import os

from .subtitle import SubtitleFileDialog
from ..glade import GladeDialog


class OpenDialog(GladeDialog, SubtitleFileDialog):

    """Dialog for selecting subtitle files to open."""

    # pylint: disable-msg=E1101

    def __init__(self, parent, title, doc):

        GladeDialog.__init__(self, "open-dialog")
        SubtitleFileDialog.__init__(self)
        get_widget = self._glade_xml.get_widget
        self._smart_check = get_widget("smart_check")
        self._use_autodetection = gaupol.gtk.util.chardet_available()

        self._init_values(doc)
        self.set_title(title)
        self.set_transient_for(parent)
        gaupol.gtk.util.connect(self, self, "response")

    def _init_values(self, doc):
        """Initialize default values for widgets."""

        domain = gaupol.gtk.conf.file
        self.set_select_multiple(doc == gaupol.gtk.DOCUMENT.MAIN)
        if os.path.isdir(domain.directory):
            self.set_current_folder(domain.directory)
        self.set_encoding(domain.encoding)
        self._smart_check.set_active(domain.smart_open_translation)
        self._smart_check.props.visible = (doc == gaupol.gtk.DOCUMENT.TRAN)

    def _on_response(self, dialog, response):
        """Save widget values and dialog size."""

        domain = gaupol.gtk.conf.file
        domain.encoding = self.get_encoding()
        domain.directory = self.get_current_folder()
        domain.smart_open_translation = self._smart_check.get_active()
