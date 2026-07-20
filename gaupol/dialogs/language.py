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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Dialog for configuring spell-check."""

import aeidon
import contextlib
import gaupol

from aeidon.i18n   import _
from gi.repository import Gtk

class LanguageDialog(gaupol.BuilderDialog):

    """Dialog for configuring spell-check."""

    _widgets = [
        "all_radio",
        "content_box",
        "current_radio",
        "language_list",
        "language_title_label",
        "main_radio",
        "scroller",
        "target_vbox",
        "tran_radio",
    ]

    def __init__(self, parent, show_target=True):
        """Initialize a :class:`LanguageDialog` instance."""
        gaupol.BuilderDialog.__init__(self, "language-dialog.ui")
        self._init_dialog(parent)
        self._init_visibilities(show_target)
        self._init_language_list()
        self._init_values()
        self._init_scroller(show_target)

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.set_default_response(Gtk.ResponseType.CLOSE)
        self.set_transient_for(parent)
        self.set_modal(True)

    def _init_language_list(self):
        """Initialize the list of languages."""
        locales = []
        with contextlib.suppress(Exception):
            locales = aeidon.SpellChecker.list_languages()
        group = None
        for locale in locales:
            name = locale
            with contextlib.suppress(Exception):
                name = aeidon.locales.code_to_name(locale)
            radio = Gtk.CheckButton(label=name, hexpand=True, group=group)
            radio.set_active(locale == gaupol.conf.spell_check.language)
            radio.connect("toggled", self._on_language_radio_toggled)
            radio.gaupol_locale = locale
            group = group or radio
            row = Gtk.ListBoxRow(activatable=False, selectable=False)
            row.set_child(radio)
            self._language_list.append(row)

    def _init_scroller(self, show_target):
        """Set the scroller height from the target column."""
        if show_target:
            height  = self._target_vbox.measure(Gtk.Orientation.VERTICAL, -1).natural
            height += self._content_box.get_margin_top()
            height += self._content_box.get_margin_bottom()
            self._scroller.set_max_content_height(height)
        else:
            height = gaupol.util.lines_to_px(25)
            self._scroller.set_max_content_height(height)

    def _init_values(self):
        """Initialize default values for widgets."""
        field = gaupol.conf.spell_check.field
        target = gaupol.conf.spell_check.target
        self._main_radio.set_active(field == gaupol.fields.MAIN_TEXT)
        self._tran_radio.set_active(field == gaupol.fields.TRAN_TEXT)
        self._all_radio.set_active(target == gaupol.targets.ALL)
        self._current_radio.set_active(target == gaupol.targets.CURRENT)

    def _init_visibilities(self, show_target):
        """Initialize visibilities of target widgets."""
        if not show_target:
            self._language_title_label.set_visible(False)
            self._target_vbox.set_visible(False)
            self._dialog.set_title(_("Set Language"))

    def _on_current_radio_toggled(self, radio_button):
        """Save the selected target."""
        gaupol.conf.spell_check.target = (
            gaupol.targets.CURRENT
            if radio_button.get_active()
            else gaupol.targets.ALL)

    def _on_main_radio_toggled(self, radio_button):
        """Save the selected field."""
        gaupol.conf.spell_check.field = (
            gaupol.fields.MAIN_TEXT
            if radio_button.get_active()
            else gaupol.fields.TRAN_TEXT)

    def _on_language_radio_toggled(self, radio):
        """Save the selected language."""
        if radio.get_active():
            gaupol.conf.spell_check.language = radio.gaupol_locale
