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

"""Task and page for removing hearing impaired parts from subtitles."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._

from .page import TextAssistantPage


class HearingImpairedPage(TextAssistantPage):

    """Task and page for removing hearing impaired parts from subtitles."""

    def __init__(self):

        TextAssistantPage.__init__(self)
        self.description = _("Remove explanatory "
            "texts meant for the hearing impaired")
        self.handle = "hearing-impaired"
        self.page_title = _("Define Hearing Impaired Patterns")
        self.page_type = gtk.ASSISTANT_PAGE_CONTENT
        self.title = _("Remove hearing impaired texts")

        name = "text-assistant-hearing-impaired-page"
        self._glade_xml = gaupol.gtk.util.get_glade_xml(name)
        get_widget = self._glade_xml.get_widget
        self._country_combo = get_widget("country_combo")
        self._language_combo = get_widget("language_combo")
        self._script_combo = get_widget("script_combo")
        self._tree_view = get_widget("tree_view")
        get_widget("vbox").reparent(self)

        self._init_properties()
