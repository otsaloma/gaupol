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

"""Regular expression based correction to subtitle text."""

import gaupol
import re

__all__ = ["Pattern"]


class Pattern(object):

    """Regular expression based correction to subtitle text.

    Instance variables:
     * enabled: True if pattern should be used, False if not
     * fields: Dictionary of field names and values
     * local: True if pattern is defined by user, False for system
    """

    def __init__(self, fields=None):

        self.enabled = True
        self.fields = fields or {}
        self.local = False

    def _get_localized_field(self, name):
        """Get the localized value of field."""

        # Handle as in freedesktop.org's Desktop Entry Specification
        # http://www.freedesktop.org/wiki/Specifications/desktop-entry-spec
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
        """Get the description of pattern."""

        if not localize:
            return self.get_field("Description")
        return self._get_localized_field("Description")

    def get_field(self, name):
        """Get the value of field."""

        return self.fields[name]

    def get_field_boolean(self, name):
        """Get the boolean value of field."""

        value = self.fields[name]
        if value == "True":
            return True
        if value == "False":
            return False
        raise ValueError

    def get_field_list(self, name):
        """Get the list value of field."""

        return self.fields[name].split(",")

    def get_flags(self):
        """Get the evaluated value of the 'Flags' field."""

        flags = 0
        for name in self.get_field("Flags").split(","):
            flags = flags | getattr(re, name)
        return flags

    def get_name(self, localize=True):
        """Get the name of pattern."""

        if not localize:
            return self.get_field("Name")
        return self._get_localized_field("Name")

    def set_field(self, name, value):
        """Set the value of field."""

        self.fields[unicode(name)] = unicode(value)
