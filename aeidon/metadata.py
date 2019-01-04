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
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Metadata store for one item in a desktop-style file."""

import aeidon

__all__ = ("MetadataItem",)


class MetadataItem:

    """
    Metadata store for one item in a desktop-style file.

    :ivar fields: Dictionary mapping field names to their string values

    Common localized fields with custom handling are ``Name`` and
    ``Description``; arbitrary fields are accessible with :meth:`get_field`.
    Strings ``True`` and ``False`` are used for boolean fields.

    For the string syntax and especially the localization handling, see
    freedesktop.org_'s Desktop Entry Specification_.

    .. _freedesktop.org: https://www.freedesktop.org/
    .. _Specification: https://www.freedesktop.org/wiki/Specifications/desktop-entry-spec/
    """

    def __init__(self, fields=None):
        """Initialize a :class:`MetadataItem` instance."""
        self.fields = fields or {}

    def get_description(self, localize=True):
        """Return description as defined by the ``Description`` field."""
        if not localize:
            return self.get_field("Description")
        return self._get_localized_field("Description")

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
        raise ValueError("Invalid boolean value: {!r}"
                         .format(value))

    def get_field_list(self, name, fallback=None):
        """Return the list of strings value of field or `fallback`."""
        if not name in self.fields:
            return fallback
        lst = self.fields[name].split(";")
        if not lst[-1]: lst.pop(-1)
        return lst

    def _get_localized_field(self, name):
        """Return the localized value of field."""
        locale = aeidon.locales.get_system_code()
        modifier = aeidon.locales.get_system_modifier()
        if locale is None:
            return self.get_field(name)
        # 'xx_YY@Zzzz', fall back to 'xx@Zzzz'.
        if ("_" in locale) and (modifier is not None):
            key = "{}[{}@{}]".format(name, locale, modifier)
            if key in self.fields:
                return self.get_field(key)
            locale = locale[0:2]
        # 'xx_YY', fall back to 'xx'.
        if ("_" in locale) and (modifier is None):
            key = "{}[{}]".format(name, locale)
            if key in self.fields:
                return self.get_field(key)
            locale = locale[0:2]
        # 'xx@Zzzz', fall back to unlocalized.
        if (not "_" in locale) and (modifier is not None):
            key = "{}[{}@{}]".format(name, locale, modifier)
            if key in self.fields:
                return self.get_field(key)
            return self.get_field(name)
        # 'xx', fall back to unlocalized.
        if (not "_" in locale) and (modifier is None):
            key = "{}[{}]".format(name, locale)
            if key in self.fields:
                return self.get_field(key)
            return self.get_field(name)
        return self.get_field(name)

    def get_name(self, localize=True):
        """Return name as defined by the ``Name`` field."""
        if not localize:
            return self.get_field("Name")
        return self._get_localized_field("Name")

    def has_field(self, name):
        """Return ``True`` if field exists."""
        return (name in self.fields)

    def set_field(self, name, value):
        """Set the string value of field."""
        self.fields[name] = str(value)
