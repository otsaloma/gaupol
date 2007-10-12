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

"""Page for correcting common human and OCR errors."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._

from .locale import LocalePage


class CommonErrorPage(LocalePage):

    """Page for correcting common human and OCR errors."""

    def __init__(self):

        LocalePage.__init__(self)
        self._manager = gaupol.PatternManager("common-error")
        self.description = _("Correct common errors "
            "made by humans or image recognition software")
        self.handle = "common-error"
        self.page_title = _("Select Common Error Patterns")
        self.page_type = gtk.ASSISTANT_PAGE_CONTENT
        self.title = _("Correct common errors")

        name = "text-assistant-common-error-page"
        self._glade_xml = gaupol.gtk.util.get_glade_xml(name)
        get_widget = self._glade_xml.get_widget
        self._country_combo = get_widget("country_combo")
        self._country_label = get_widget("country_label")
        self._human_check = get_widget("human_check")
        self._language_combo = get_widget("language_combo")
        self._language_label = get_widget("language_label")
        self._ocr_check = get_widget("ocr_check")
        self._script_combo = get_widget("script_combo")
        self._script_label = get_widget("script_label")
        self._tree_view = get_widget("tree_view")
        get_widget("vbox").reparent(self)

        self._init_signal_handlers()
        self._init_tree_view()
        self._init_script_combo()
        self._init_language_combo()
        self._init_country_combo()
        self._init_values()

    def _filter_patterns(self, patterns):
        """Return a subset of patterns to show."""

        check_human = self._human_check.get_active()
        check_ocr = self._ocr_check.get_active()
        def use(pattern):
            classes = pattern.get_field_list("Classes")
            human = check_human and ("Human" in classes)
            ocr = check_ocr and ("OCR" in classes)
            return bool(human or ocr)
        return [x for x in patterns if use(x)]

    def _get_conf_domain(self):
        """Get the configuration domain for locale options."""

        return gaupol.gtk.conf.common_error

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        LocalePage._init_signal_handlers(self)
        gaupol.gtk.util.connect(self, "_human_check", "toggled")
        gaupol.gtk.util.connect(self, "_ocr_check", "toggled")

    def _init_values(self):
        """Initialize default values for widgets."""

        domain = self._get_conf_domain()
        self._human_check.set_active(domain.human)
        self._ocr_check.set_active(domain.ocr)

    def _on_human_check_toggled(self, check_button):
        """Populate the tree view with the correct patterns."""

        domain = self._get_conf_domain()
        domain.human = check_button.get_active()
        self._populate_tree_view()

    def _on_ocr_check_toggled(self, check_button):
        """Populate the tree view with the correct patterns."""

        domain = self._get_conf_domain()
        domain.ocr = check_button.get_active()
        self._populate_tree_view()

    def correct_texts(self, project, indices, doc):
        """Correct texts in project."""

        script = self._get_script()
        language = self._get_language()
        country = self._get_country()
        codes = (script, language, country)
        self._manager.save(*codes)
        patterns = self._manager.get_patterns(*codes)
        project.correct_common_errors(indices, doc, patterns)
