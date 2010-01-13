# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Dialog for selecting subtitle files to open."""

import gaupol
import os

__all__ = ("OpenDialog",)


class OpenDialog(gaupol.FileDialog):

    """Dialog for selecting subtitle files to open."""

    def __init__(self, parent, title, doc):
        """Initialize an OpenDialog object."""

        gaupol.FileDialog.__init__(self, "open.glade")
        get_widget = self._glade_xml.get_widget
        self._align_combo = get_widget("align_combo")
        self._align_label = get_widget("align_label")
        self._encoding_combo = get_widget("encoding_combo")
        self._use_autodetection = aeidon.util.chardet_available()
        self.conf = gaupol.conf.file

        self._init_filters()
        self._init_encoding_combo()
        self._init_values(doc)
        self.set_title(title)
        self.set_transient_for(parent)
        aeidon.util.connect(self, self, "response")

    def _init_values(self, doc):
        """Initialize default values for widgets."""

        self.set_select_multiple(doc == aeidon.documents.MAIN)
        if os.path.isdir(self.conf.directory):
            self.set_current_folder(self.conf.directory)
        self.set_encoding(self.conf.encoding)
        store = self._align_combo.get_model()
        for align_method in aeidon.align_methods:
            store.append((align_method.label,))
        self._align_combo.set_active(self.conf.align_method)
        self._align_combo.props.visible = (doc == aeidon.documents.TRAN)
        self._align_label.props.visible = (doc == aeidon.documents.TRAN)

    def _on_response(self, dialog, response):
        """Save widget values and dialog size."""

        self.conf.encoding = self.get_encoding()
        self.conf.directory = self.get_current_folder()
        index = self._align_combo.get_active()
        self.conf.align_method = aeidon.align_methods[index]
