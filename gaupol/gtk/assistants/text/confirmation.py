# Copyright (C) 2007 Osmo Salomaa
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

"""Page to confirm changes made after performing all tasks."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._

from .page import TextAssistantPage


class ConfirmationPage(TextAssistantPage):

    """Page to confirm changes made after performing all tasks."""

    def __init__(self):

        TextAssistantPage.__init__(self)
        self.page_title = _("Confirm Changes")
        self.page_type = gtk.ASSISTANT_PAGE_CONFIRM

        name = "text-assistant-confirmation-page"
        self._glade_xml = gaupol.gtk.util.get_glade_xml(name)
        get_widget = self._glade_xml.get_widget
        self._tree_view = get_widget("tree_view")
        get_widget("vbox").reparent(self)

        self._init_properties()
