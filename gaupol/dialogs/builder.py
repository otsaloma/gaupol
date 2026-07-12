# -*- coding: utf-8 -*-

# Copyright (C) 2006 Osmo Salomaa
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

"""Baseclass and wrapper for :class:`Gtk.Builder` constructed dialogs."""

import aeidon

from gi.repository import Gtk
from pathlib import Path

class BuilderDialog:

    """
    Baseclass and wrapper for :class:`Gtk.Builder` constructed dialogs.

    :cvar _widgets: List of names of widgets to be assigned as attributes

    All widgets defined in :attr:`_widgets` are assigned as instance variables
    with names preceded by a single underscore. All signals defined in the UI
    definition file are connected to ``self``. All :func:`getattr` calls not
    found in ``self`` are delegated to :attr:`self._dialog` allowing ``self``
    to look and act like a :class:`Gtk.Dialog`.
    """

    _widgets = []

    def __init__(self, ui_file_path):
        """Initialize a :class:`BuilderDialog` instance from `ui_file_path`."""
        ui_file_path = Path(ui_file_path)
        if not ui_file_path.is_absolute():
            ui_file_path = aeidon.DATA_DIR / "ui" / ui_file_path
        # Signal handlers are resolved against self already when
        # the UI definition file is parsed, i.e. before _dialog is set.
        self._builder = Gtk.Builder(self)
        self._builder.set_translation_domain("gaupol")
        self._builder.add_from_file(str(ui_file_path))
        self._dialog = self._builder.get_object("dialog")
        self._set_attributes(self._widgets)

    def __getattr__(self, name):
        """Return attribute from :attr:`_dialog`."""
        if name == "_dialog":
            raise AttributeError(name)
        return getattr(self._dialog, name)

    def _set_attributes(self, widgets, prefix=None):
        """Assign all names in `widgets` as attributes of `self`."""
        for name in widgets:
            widget = self._builder.get_object(name)
            if prefix and name.startswith(prefix):
                name = name.replace(prefix, "")
            setattr(self, f"_{name}", widget)
