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
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Base class for dialogs for selecting subtitle files."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import Gtk

__all__ = ("FileDialog",)


class FileDialog:

    """Base class for dialogs for selecting subtitle files."""

    _use_autodetection = False

    def get_encoding(self):
        """Return the selected encoding or ``None``."""
        index = self._encoding_combo.get_active()
        if index < 0: return None
        store = self._encoding_combo.get_model()
        return store[index][0]

    def _init_encoding_combo(self):
        """Initialize the character encoding combo box."""
        store = Gtk.ListStore(str, str)
        self._encoding_combo.set_model(store)
        self._populate_encoding_combo()
        view = self._encoding_combo.get_child()
        path = gaupol.util.tree_row_to_path(0)
        view.set_displayed_row(path)
        renderer = Gtk.CellRendererText()
        self._encoding_combo.pack_start(renderer, expand=True)
        self._encoding_combo.add_attribute(renderer, "text", 1)
        func = gaupol.util.separate_combo
        self._encoding_combo.set_row_separator_func(func, None)

    def _init_filters(self):
        """Initialize file filters."""
        file_filter = Gtk.FileFilter()
        file_filter.set_name(_("All files"))
        file_filter.add_pattern("*")
        self.add_filter(file_filter)
        file_filter = Gtk.FileFilter()
        file_filter.set_name(_("All supported files"))
        for format in aeidon.formats:
            pattern = "*."
            for x in format.extension[1:]:
                pattern += "[{}{}]".format(x.upper(), x.lower())
            file_filter.add_pattern(pattern)
        self.add_filter(file_filter)
        self.set_filter(file_filter)
        for format in aeidon.formats:
            extension = format.extension
            pattern = "*."
            for x in extension[1:]:
                pattern += "[{}{}]".format(x.upper(), x.lower())
            format = format.label
            name = _("{format} (*{extension})").format(**locals())
            file_filter = Gtk.FileFilter()
            file_filter.set_name(name)
            file_filter.add_pattern(pattern)
            self.add_filter(file_filter)

    def _on_encoding_combo_changed(self, *args):
        """Show the encoding selection dialog."""
        encoding = self.get_encoding()
        if encoding != "other": return
        dialog = gaupol.MenuEncodingDialog(self)
        response = gaupol.util.run_dialog(dialog)
        encoding = dialog.get_encoding()
        visible = dialog.get_visible_encodings()
        dialog.destroy()
        self._encoding_combo.set_active(0)
        if response != Gtk.ResponseType.OK: return
        gaupol.conf.encoding.visible = visible
        if encoding is None: return
        self._populate_encoding_combo(encoding)
        self.set_encoding(encoding)

    def _populate_encoding_combo(self, custom=None):
        """Populate the encoding combo box, including custom encoding."""
        encodings = list(gaupol.conf.encoding.visible)
        locale = aeidon.encodings.get_locale_code()
        encodings.insert(0, locale)
        encodings.append(custom)
        while None in encodings:
            encodings.remove(None)
        encodings = aeidon.util.get_unique(encodings)
        encodings = encodings or ["utf_8"]
        for i, encoding in enumerate(encodings):
            name = aeidon.encodings.code_to_long_name(encoding)
            encodings[i] = (encoding, name)
        if locale is not None:
            name = aeidon.encodings.get_locale_long_name()
            encodings[0] = (locale, name)
        a = 0 if locale is None else 1
        encodings[a:] = sorted(encodings[a:], key=lambda x: x[1])
        separator = gaupol.COMBO_SEPARATOR
        if self._use_autodetection:
            encodings.append((separator, separator))
            encodings.append(("auto", _("Auto-detected")))
        encodings.append((separator, separator))
        encodings.append(("other", _("Other…")))
        self._encoding_combo.get_model().clear()
        store = self._encoding_combo.get_model()
        for encoding in encodings:
            store.append(tuple(encoding))

    def set_encoding(self, encoding):
        """Set the selected encoding."""
        if encoding is None: return
        store = self._encoding_combo.get_model()
        for i in range(len(store)):
            if store[i][0] == encoding:
                return self._encoding_combo.set_active(i)
        if aeidon.encodings.is_valid_code(encoding):
            # Add encoding if not found in store.
            self._populate_encoding_combo(encoding)
            return self.set_encoding(encoding)
        self._encoding_combo.set_active(0)
