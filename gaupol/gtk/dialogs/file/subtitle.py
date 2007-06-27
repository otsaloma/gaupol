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


"""Base class for dialogs for selecting subtitle files."""


import gaupol.gtk
import gobject
import gtk
_ = gaupol.i18n._

from ..encoding import AdvEncodingDialog


class SubtitleFileDialog(object):

    """Base class for dialogs for selecting subtitle files."""

    # pylint: disable-msg=E1101

    __metaclass__ = gaupol.Contractual

    def __init__(self):

        get_widget = self._glade_xml.get_widget
        self._encoding_combo = get_widget("encoding_combo")
        self._use_autodetection = False
        self._init_filters()
        self._init_encoding_combo()

    def _init_encoding_combo(self):
        """Initialize the encoding combo box."""

        store = gtk.ListStore(*(gobject.TYPE_STRING,) * 2)
        self._encoding_combo.set_model(store)
        self._populate_encoding_combo()
        view = self._encoding_combo.get_child()
        view.set_displayed_row(0)
        renderer = view.get_cell_renderers()[0]
        self._encoding_combo.set_attributes(renderer, text=1)
        function = gaupol.gtk.util.separate_combo
        self._encoding_combo.set_row_separator_func(function)
        gaupol.gtk.util.connect(self, "_encoding_combo", "changed")

    def _init_filters(self):
        """Initialize the file filters."""

        file_filter = gtk.FileFilter()
        file_filter.set_name(_("All files"))
        file_filter.add_pattern("*")
        self.add_filter(file_filter)

        file_filter = gtk.FileFilter()
        file_filter.set_name(_("Plain text files"))
        file_filter.add_mime_type("text/plain")
        self.add_filter(file_filter)

        for format in gaupol.gtk.FORMAT.members:
            pattern = "*%s" % format.extension
            format = format.label
            name = _("%(format)s (%(pattern)s)") % locals()
            file_filter = gtk.FileFilter()
            file_filter.set_name(name)
            file_filter.add_pattern(pattern)
            self.add_filter(file_filter)

    @gaupol.gtk.util.asserted_return
    def _on_encoding_combo_changed(self, *args):
        """Show the encoding selection dialog."""

        encoding = self.get_encoding()
        assert encoding == "other"
        dialog = AdvEncodingDialog(self._dialog)
        response = self.run_dialog(dialog)
        encoding = dialog.get_encoding()
        visibles = dialog.get_visible_encodings()
        dialog.destroy()
        self._encoding_combo.set_active(0)
        assert response == gtk.RESPONSE_OK
        gaupol.gtk.conf.encoding.visibles = visibles
        self._populate_encoding_combo(encoding)
        self.set_encoding(encoding)

    def _populate_encoding_combo(self, custom=None):
        """Populate the encoding combo box, including custom encoding."""

        encodings = list(gaupol.gtk.conf.encoding.visibles)
        locale = gaupol.encodings.get_locale_python_name()
        encodings.insert(0, locale)
        encodings.append(custom)
        while None in encodings:
            encodings.remove(None)
        encodings = gaupol.gtk.util.get_unique(encodings)
        encodings = encodings or ["utf_8"]
        for i, encoding in enumerate(encodings):
            name = gaupol.encodings.get_long_name(encoding)
            encodings[i] = (encoding, name)
        if locale is not None:
            name = gaupol.encodings.get_locale_long_name()
            encodings[0] = (locale, name)
        a = (0 if locale is None else 1)
        encodings[a:] = sorted(encodings[a:], key=lambda x: x[1])

        separator = gaupol.gtk.COMBO_SEPARATOR
        if self._use_autodetection:
            encodings.append((separator, separator))
            encodings.append(("auto", _("Auto-detected")))
        encodings.append((separator, separator))
        encodings.append(("other", _("Other\342\200\246")))

        self._encoding_combo.get_model().clear()
        store = self._encoding_combo.get_model()
        for encoding in encodings:
            store.append(list(encoding))

    def get_encoding_ensure(self, value):
        if value not in ("auto", "other", None):
            assert gaupol.encodings.is_valid(value)

    @gaupol.gtk.util.asserted_return
    def get_encoding(self):
        """Get the selected encoding or None."""

        index = self._encoding_combo.get_active()
        assert index >= 0
        store = self._encoding_combo.get_model()
        return store[index][0]

    @gaupol.gtk.util.asserted_return
    def set_encoding(self, encoding):
        """Set the selected encoding."""

        assert encoding is not None
        store = self._encoding_combo.get_model()
        for i in range(len(store)):
            if store[i][0] == encoding:
                return self._encoding_combo.set_active(i)
        if gaupol.encodings.is_valid(encoding):
            self._populate_encoding_combo(encoding)
            return self.set_encoding(encoding)
        self._encoding_combo.set_active(0)
