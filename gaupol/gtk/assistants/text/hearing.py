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

"""Page for removing hearing impaired parts from subtitles."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._

from .locale import LocalePage


class HearingImpairedPage(LocalePage):

    """Page for removing hearing impaired parts from subtitles."""

    def __init__(self):

        LocalePage.__init__(self)
        self._manager = gaupol.PatternManager("hearing-impaired")
        self.description = _("Remove explanatory "
            "texts meant for the hearing impaired")
        self.handle = "hearing-impaired"
        self.page_title = _("Select Hearing Impaired Patterns")
        self.page_type = gtk.ASSISTANT_PAGE_CONTENT
        self.title = _("Remove hearing impaired texts")

        name = "text-assistant-hearing-impaired-page"
        self._glade_xml = gaupol.gtk.util.get_glade_xml(name)
        get_widget = self._glade_xml.get_widget
        self._country_combo = get_widget("country_combo")
        self._country_label = get_widget("country_label")
        self._language_combo = get_widget("language_combo")
        self._language_label = get_widget("language_label")
        self._script_combo = get_widget("script_combo")
        self._script_label = get_widget("script_label")
        self._tree_view = get_widget("tree_view")
        get_widget("vbox").reparent(self)

        self._init_signal_handlers()
        self._init_tree_view()
        self._init_script_combo()
        self._init_language_combo()
        self._init_country_combo()

    def _get_conf_domain(self):
        """Get the configuration domain for locale options."""

        return gaupol.gtk.conf.hearing_impaired

    def correct_texts(self, project, indices, doc):
        """Correct texts in project."""

        script = self._get_script()
        language = self._get_language()
        country = self._get_country()
        codes = (script, language, country)
        self._manager.save(*codes)
        patterns = self._manager.get_patterns(*codes)
        project.remove_hearing_impaired(indices, doc, patterns)
