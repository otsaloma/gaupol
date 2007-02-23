# Copyright (C) 2006-2007 Osmo Salomaa
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


"""Wrapper classes for easier use of ConfigObj."""


import functools
import os
import sys

from gaupol import util
from gaupol.base import Observable
from gaupol.gtk import cons
from gaupol.gtk.errors import ConfigParseError
from . import configobj, validate


class Config(configobj.ConfigObj):

    """Reading, writing and storing configurations.

    This is a convenience wrapper around ConfigObj. Methods defined in this
    class are as error-tolerant as possible. Validation includes extensions to
    handle Gaupol's constants, which can be defined in the spec file as
    CONSTANT and CONSTANT_list for each constant.
    """

    def __init__(self, config_file, spec_file):
        """Initialize a Config object.

        Raise ConfigParseError if parsing config_file fails.
        """
        try:
            configobj.ConfigObj.__init__(
                self, config_file, configspec=spec_file,
                encoding=util.get_default_encoding(),
                write_empty_values=True)
        except IOError:
            util.handle_read_io(sys.exc_info(), config_file)
            # pylint: disable-msg=W0233
            configobj.ConfigObj.__init__(
                self, None, configspec=spec_file,
                encoding=util.get_default_encoding())
        except configobj.ConfigObjError, obj:
            print "Errors parsing configuration file '%s':" % config_file
            for error in obj.errors:
                print "  Line %d: %s" % (error.line_number, error.message)
            raise ConfigParseError(obj)

        validator = self.__init_validator()
        spec = self.__init_spec(validator, spec_file)
        self.__remove_crap(spec)
        self.__validate(validator, spec)

    def __init_spec(self, validator, spec_file):
        """Initialize and return spec ConfigObj."""

        spec = configobj.ConfigObj(None, configspec=spec_file)
        result = spec.validate(validator)
        if result is True:
            return spec
        print "The spec is erroneous!"
        for error in configobj.flatten_errors(spec, result):
            sections, option, result = error
            for section in sections:
                print "  %s.%s: %s" % (section, option, result)
        raise SystemExit

    def __init_validator(self):
        """Initialize and return validator."""

        validator = validate.Validator()

        def check_constant(name, value):
            index = validator.check("integer", value)
            members = getattr(cons, name).members
            try:
                return members[index]
            except IndexError:
                raise validate.VdtValueError(value)

        def check_constant_list(name, value):
            lst = validator.check("int_list", value)
            members = getattr(cons, name).members
            try:
                return list(members[x] for x in lst)
            except IndexError:
                raise validate.VdtValueError(value)

        for name in (x for x in dir(cons) if x.isupper()):
            func = functools.partial(check_constant, name)
            validator.functions[name] = func
            func = functools.partial(check_constant_list, name)
            validator.functions["%s_list" % name] = func

        return validator

    def __remove_crap(self, spec):
        """Remove sections and options not in spec."""

        sections = set(self.keys())
        sections -= set(spec.keys())
        if sections:
            print "Discarding unrecognized configuration sections:"
        for section in sections:
            print "  %s" % section
            del self[section]

        first = True
        for section in self.iterkeys():
            options = set(self[section].keys())
            options -= set(spec[section].keys())
            if options and first:
                print "Discarding unrecognized configuration options:"
                first = False
            for option in options:
                print "  %s.%s" % (section, option)
                del self[section][option]

    def __validate(self, validator, spec):
        """Validate options according to spec."""

        result = self.validate(validator, preserve_errors=True)
        if result is True:
            return
        print "Discarding erroneous configuration options:"
        for error in configobj.flatten_errors(self, result):
            sections, option, result = error
            for section in sections:
                print "  %s.%s: %s" % (section, option, result)
                self[section][option] = spec[section][option]
                self[section].defaults.append(option)

    def write_to_file(self):
        """Write configurations to file."""

        try:
            util.makedirs(os.path.dirname(self.filename))
            configobj.ConfigObj.write(self)
        except (IOError, OSError):
            util.handle_write_io(sys.exc_info(), self.filename)


class Container(Observable):

    """Configuration data container.

    Instance variables:

        root: A dictionary in a ConfigObj

    This class can be a configuration section or a container for the entire
    configuration data if there are no sections. This class is instantiated
    with a 'root', which is a lowest (sub)dictionary of a ConfigObj instance.
    This class provides convenient attribute access and notifications for
    configuration variables as per the Observable API.
    """

    __slots__ = ["root"]

    def __getattr__(self, name):

        return self.root[name]

    def __init__(self, root):

        Observable.__init__(self)

        self.root = root
        for name in root.keys():
            self._add_signal("notify::%s" % name)

    def __setattr__(self, name, value):

        if name in self.__slots__ or name in Observable.__slots__:
            return Observable.__setattr__(self, name, value)
        if value != self.root[name]:
            self.root[name] = value
            self.emit("notify::" + name)
