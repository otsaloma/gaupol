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

"""Page for breaking text into lines."""

import gaupol.gtk
import gtk
import sys
_ = gaupol.i18n._

from .locale import LocalePage
from .page import TextAssistantPage


class LineBreakPage(LocalePage):

    """Page for breaking text into lines."""

    def __init__(self):

        LocalePage.__init__(self)
        self._manager = gaupol.PatternManager("line-break")
        self.description = _("Break text into lines of defined length")
        self.handle = "line-break"
        self.page_title = _("Select Line-Break Patterns")
        self.page_type = gtk.ASSISTANT_PAGE_CONTENT
        self.title = _("Break lines")

        name = "text-assistant-line-break-page"
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

        return gaupol.gtk.conf.line_break

    def _get_max_skip_length(self):
        """Return the maximum line length to skip."""

        domain = self._get_conf_domain()
        if domain.skip_length:
            return domain.max_skip_length
        return sys.maxint

    def _get_max_skip_lines(self):
        """Return the maximum amount of lines to skip."""

        domain = self._get_conf_domain()
        if domain.skip_lines:
            return domain.max_skip_lines
        return sys.maxint

    def correct_texts(self, project, indices, doc):
        """Correct texts in project."""

        script = self._get_script()
        language = self._get_language()
        country = self._get_country()
        codes = (script, language, country)
        self._manager.save(*codes)
        patterns = self._manager.get_patterns(*codes)
        domain = self._get_conf_domain()
        project.break_lines(
            indices, doc, patterns,
            gaupol.gtk.ruler.get_length_function(domain.length_unit),
            domain.max_length, domain.max_lines, domain.max_deviation,
            (domain.skip_length or domain.skip_lines),
            self._get_max_skip_length(), self._get_max_skip_lines())


class LineBreakOptionsPage(TextAssistantPage):

    """Page for editing line-break options."""

    def __init__(self):

        TextAssistantPage.__init__(self)
        self.page_title = _("Set Line-Break Options")
        self.page_type = gtk.ASSISTANT_PAGE_CONTENT

        name = "text-assistant-line-break-options-page"
        self._glade_xml = gaupol.gtk.util.get_glade_xml(name)
        get_widget = self._glade_xml.get_widget
        self._max_length_spin = get_widget("max_length_spin")
        self._max_lines_spin = get_widget("max_lines_spin")
        self._max_skip_length_spin = get_widget("max_skip_length_spin")
        self._max_skip_lines_spin = get_widget("max_skip_lines_spin")
        self._skip_length_check = get_widget("skip_length_check")
        self._skip_lines_check = get_widget("skip_lines_check")
        self._skip_unit_combo = get_widget("skip_unit_combo")
        self._unit_combo = get_widget("unit_combo")
        get_widget("vbox").reparent(self)

        self._init_unit_combos()
        self._init_signal_handlers()
        self._init_values()

    def _get_conf_domain(self):
        """Get the configuration domain for locale options."""

        return gaupol.gtk.conf.line_break

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.gtk.util.connect(self, "_max_length_spin", "value-changed")
        gaupol.gtk.util.connect(self, "_max_lines_spin", "value-changed")
        gaupol.gtk.util.connect(self, "_max_skip_length_spin", "value-changed")
        gaupol.gtk.util.connect(self, "_max_skip_lines_spin", "value-changed")
        gaupol.gtk.util.connect(self, "_skip_length_check", "toggled")
        gaupol.gtk.util.connect(self, "_skip_lines_check", "toggled")
        gaupol.gtk.util.connect(self, "_skip_unit_combo", "changed")
        gaupol.gtk.util.connect(self, "_unit_combo", "changed")

    def _init_unit_combos(self):
        """Initialize the line length unit combo boxes."""

        store = self._unit_combo.get_model()
        for name in gaupol.gtk.LENGTH_UNIT.labels:
            store.append([name])
        store = self._skip_unit_combo.get_model()
        for name in gaupol.gtk.LENGTH_UNIT.labels:
            store.append([name])

    def _init_values(self):
        """Initialize default values for widgets."""

        domain = self._get_conf_domain()
        self._max_length_spin.set_value(domain.max_length)
        self._max_lines_spin.set_value(domain.max_lines)
        self._max_skip_length_spin.set_value(domain.max_skip_length)
        self._max_skip_lines_spin.set_value(domain.max_skip_lines)
        self._skip_length_check.set_active(domain.skip_length)
        self._skip_lines_check.set_active(domain.skip_lines)
        self._skip_unit_combo.set_active(domain.length_unit)
        self._unit_combo.set_active(domain.length_unit)

    def _on_max_length_spin_value_changed(self, spin_button):
        """Save the maximum line length value."""

        domain = self._get_conf_domain()
        domain.max_length = spin_button.get_value_as_int()

    def _on_max_lines_spin_value_changed(self, spin_button):
        """Save the maximum line amount value."""

        domain = self._get_conf_domain()
        domain.max_lines = spin_button.get_value_as_int()

    def _on_max_skip_length_spin_value_changed(self, spin_button):
        """Save the maximum line length to skip value."""

        domain = self._get_conf_domain()
        domain.max_skip_length = spin_button.get_value_as_int()

    def _on_max_skip_lines_spin_value_changed(self, spin_button):
        """Save the maximum line amount to skip value."""

        domain = self._get_conf_domain()
        domain.max_skip_lines = spin_button.get_value_as_int()

    def _on_skip_length_check_toggled(self, check_button):
        """Save the skip by line length value."""

        domain = self._get_conf_domain()
        domain.skip_length = check_button.get_active()

    def _on_skip_lines_check_toggled(self, check_button):
        """Save the skip by line amount value."""

        domain = self._get_conf_domain()
        domain.skip_lines = check_button.get_active()

    def _on_skip_unit_combo_changed(self, combo_box):
        """Save and sync the length unit value."""

        domain = self._get_conf_domain()
        index = combo_box.get_active()
        length_unit = gaupol.gtk.LENGTH_UNIT.members[index]
        domain.length_unit = length_unit
        self._unit_combo.set_active(index)

    def _on_unit_combo_changed(self, combo_box):
        """Save and sync the length unit value."""

        domain = self._get_conf_domain()
        index = combo_box.get_active()
        length_unit = gaupol.gtk.LENGTH_UNIT.members[index]
        domain.length_unit = length_unit
        self._skip_unit_combo.set_active(index)
