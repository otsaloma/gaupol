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


"""Dialog for selecting subtitle files to open."""


import os

from gaupol.gtk import conf, const, util
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
        self._use_autodetection = util.chardet_available()

        self._init_values(doc)
        self.set_title(title)
        self.set_transient_for(parent)
        util.connect(self, self, "response")

    def _init_values(self, doc):
        """Initialize default values for widgets."""

        if all(conf.open_dialog.size):
            self.set_default_size(*conf.open_dialog.size)
        self.set_select_multiple(doc == const.DOCUMENT.MAIN)
        if os.path.isdir(conf.file.directory):
            self.set_current_folder(conf.file.directory)
        self.set_encoding(conf.file.encoding)
        self._smart_check.set_active(conf.file.smart_tran)
        self._smart_check.props.visible = (doc == const.DOCUMENT.TRAN)

    def _on_response(self, dialog, response):
        """Save widget values and dialog size."""

        conf.file.encoding = self.get_encoding()
        conf.file.directory = self.get_current_folder()
        conf.file.smart_tran = self._smart_check.get_active()
        conf.open_dialog.size = self.get_size()
