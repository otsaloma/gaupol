# -*- coding: utf-8 -*-

# Copyright (C) 2007 Osmo Salomaa
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

"""Metadata store for one item in a desktop-style file."""

from aeidon.i18n import _

class MetadataItem:

    """
    Metadata store for one item in a desktop-style file.

    :ivar fields: Dictionary mapping field names to their string values

    Common translated fields with custom handling are ``Name`` and
    ``Description``; arbitrary fields are accessible with :meth:`get_field`.
    Strings ``True`` and ``False`` are used for boolean fields.

    For the string syntax, see freedesktop.org_'s Desktop Entry
    Specification_, of which translations are the notable exception:
    fields are stored in English only and translated at runtime.

    .. _freedesktop.org: https://www.freedesktop.org/
    .. _Specification: https://www.freedesktop.org/wiki/Specifications/desktop-entry-spec/
    """

    def __init__(self, fields=None):
        """Initialize a :class:`MetadataItem` instance."""
        self.fields = fields or {}

    def get_description(self, localize=True):
        """Return description as defined by the ``Description`` field."""
        description = self.get_field("Description")
        return _(description) if localize else description

    def get_field(self, name, fallback=None):
        """Return the string value of field or `fallback`."""
        if not name in self.fields:
            return fallback
        return self.fields[name]

    def get_field_boolean(self, name, fallback=None):
        """Return the boolean value of field or `fallback`."""
        if not name in self.fields:
            return fallback
        value = self.fields[name]
        if value == "True":
            return True
        if value == "False":
            return False
        raise ValueError(f"Invalid boolean value: {value!r}")

    def get_field_list(self, name, fallback=None):
        """Return the list of strings value of field or `fallback`."""
        if not name in self.fields:
            return fallback
        lst = self.fields[name].split(";")
        if not lst[-1]: lst.pop(-1)
        return lst

    def get_name(self, localize=True):
        """Return name as defined by the ``Name`` field."""
        name = self.get_field("Name")
        return _(name) if localize else name

    def has_field(self, name):
        """Return ``True`` if field exists."""
        return (name in self.fields)

    def set_field(self, name, value):
        """Set the string value of field."""
        self.fields[name] = str(value)
