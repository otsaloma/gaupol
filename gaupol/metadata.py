# Copyright (C) 2007-2008 Osmo Salomaa
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

"""Metadata store for one item in a desktop-style file."""

import gaupol

__all__ = ("MetadataItem",)


class MetadataItem(object):

    """Metadata store for one item in a desktop-style file.

    Instance variable 'field' is a dictionary mapping field names to their
    string values. Common localized fields with custom handling are 'Name' and
    'Description'; arbitrary fields are accessible with 'get_field'. Strings
    'True' and 'False' are used for boolean fields.

    For the string syntax and especially the localization handling, see
    freedesktop.org's Desktop Entry Specification.
    http://www.freedesktop.org/wiki/Specifications/desktop-entry-spec
    """

    def __init__(self, fields=None):
        """Initialize a MetadataItem object."""

        self.fields = fields or {}

    def _get_localized_field(self, name):
        """Return the localized value of field."""

        locale = gaupol.locales.get_system_code()
        modifier = gaupol.locales.get_system_modifier()
        if locale is None:
            return self.get_field(name)
        if ("_" in locale) and (modifier is not None):
            key = "%s[%s@%s]" % (name, locale, modifier)
            if key in self.fields:
                return self.get_field(key)
        if "_" in locale:
            key = "%s[%s]" % (name, locale)
            if key in self.fields:
                return self.get_field(key)
        if (not "_" in locale) and (modifier is not None):
            key = "%s[%s@%s]" % (name, locale, modifier)
            if key in self.fields:
                return self.get_field(key)
        if (not "_" in locale):
            key = "%s[%s]" % (name, locale)
            if key in self.fields:
                return self.get_field(key)
        return self.get_field(name)

    def get_description(self, localize=True):
        """Return the description of item."""

        if not localize:
            return self.get_field("Description")
        return self._get_localized_field("Description")

    def get_field(self, name, fallback=None):
        """Return the string value of field or fallback."""

        if not name in self.fields:
            return fallback
        return self.fields[name]

    def get_field_boolean(self, name, fallback=None):
        """Return the boolean value of field or fallback."""

        if not name in self.fields:
            return fallback
        value = self.fields[name]
        if value == "True":
            return True
        if value == "False":
            return False
        raise ValueError

    def get_field_list(self, name, fallback=None):
        """Return the list of strings value of field or fallback."""

        if not name in self.fields:
            return fallback
        lst = self.fields[name].split(";")
        if not lst[-1]: lst.pop(-1)
        return lst

    def get_name(self, localize=True):
        """Return the name of item."""

        if not localize:
            return self.get_field("Name")
        return self._get_localized_field("Name")

    def has_field(self, name):
        """Return True if field exists."""

        return (name in self.fields)

    def set_field(self, name, value):
        """Set the string value of field."""

        self.fields[unicode(name)] = unicode(value)
