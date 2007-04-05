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


"""Dialog for converting framerates."""


import gtk

from gaupol.gtk import conf, const, util
from .glade import GladeDialog


class FramerateConvertDialog(GladeDialog):

    """Dialog for converting framerates.

    Instance variables:

        _all_radio:     gtk.RadioButton
        _correct_combo: gtk.ComboBox
        _current_combo: gtk.ComboBox
        _current_radio: gtk.RadioButton
        application:    Associated Application
    """

    def __init__(self, parent, application):

        GladeDialog.__init__(self, "frconvert-dialog")
        get_widget = self._glade_xml.get_widget
        self._all_radio     = get_widget("all_radio")
        self._correct_combo = get_widget("correct_combo")
        self._current_combo = get_widget("current_combo")
        self._current_radio = get_widget("current_radio")
        self.application = application

        self._init_signal_handlers()
        self._init_data()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _convert(self):
        """Convert framerates."""

        current = self._current_combo.get_active()
        current = const.FRAMERATE.members[current]
        correct = self._correct_combo.get_active()
        correct = const.FRAMERATE.members[correct]
        for page in self._get_target_pages():
            index = self.application.pages.index(page)
            self.application.notebook.set_current_page(index)
            page.project.convert_framerate(None, current, correct)

    def _get_target(self):
        """Get the selected target."""

        if self._current_radio.get_active():
            return const.TARGET.CURRENT
        if self._all_radio.get_active():
            return const.TARGET.ALL
        raise ValueError

    def _get_target_pages(self):
        """Get pages corresponding to target."""

        target = self._get_target()
        if target == const.TARGET.ALL:
            return self.application.pages
        return [self.application.get_current_page()]

    def _init_data(self):
        """Intialize default values for widgets."""

        for combo_box in (self._current_combo, self._correct_combo):
            store = combo_box.get_model()
            store.clear()
            for name in const.FRAMERATE.display_names:
                store.append([name])
            combo_box.set_active(conf.editor.framerate)

        target = conf.framerate_convert.target
        self._current_radio.set_active(target == const.TARGET.CURRENT)
        self._all_radio.set_active(target == const.TARGET.ALL)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, "_correct_combo", "changed")
        util.connect(self, "_current_combo", "changed")
        util.connect(self, self, "response")

    def _on_correct_combo_changed(self, *args):
        """Set response sensitivity."""

        current = self._current_combo.get_active()
        correct = self._correct_combo.get_active()
        sensitive = current != correct
        self._dialog.set_response_sensitive(gtk.RESPONSE_OK, sensitive)

    def _on_current_combo_changed(self, *args):
        """Set response sensitivity."""

        current = self._current_combo.get_active()
        correct = self._correct_combo.get_active()
        sensitive = current != correct
        self._dialog.set_response_sensitive(gtk.RESPONSE_OK, sensitive)

    @util.silent(AssertionError)
    def _on_response(self, dialog, response):
        """Save settings and convert framerates."""

        conf.position_shift.target = self._get_target()
        assert response == gtk.RESPONSE_OK
        self._convert()
