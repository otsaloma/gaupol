# Copyright (C) 2006-2008 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Reading, writing and storing configurations."""

import functools
import gaupol.gtk
import os
import sys

from . import configobj, validate


class Config(configobj.ConfigObj):

    """Reading, writing and storing configurations.

    This is a convenience wrapper around ConfigObj. Methods defined in this
    class are as error-tolerant as possible. Validation includes extensions to
    handle Gaupol's enumerations, which can be defined in the spec file as
    ENUMERATION and ENUMERATION_list for each ENUMERATION.
    """

    __metaclass__ = gaupol.Contractual

    def __get_enumerations(self):
        """Return a dictionary mapping enumeration names to values."""

        enumerations = {} # name: value
        for name in dir(gaupol):
            value = getattr(gaupol, name)
            if isinstance(value, gaupol.Enumeration):
                enumerations[name] = value
        for name in dir(gaupol.gtk):
            value = getattr(gaupol.gtk, name)
            if isinstance(value, gaupol.Enumeration):
                enumerations[name] = value
        return enumerations

    def __check_enum(self, validator, enum, value):
        """Validate and return enumeration item or raise VdtValueError."""

        name = validator.check("string", value)
        try:
            return getattr(enum, name.upper())
        except AttributeError:
            raise validate.VdtValueError(value)

    def __check_enum_list(self, validator, enum, value):
        """Validate and return enumeration item list or raise VdtValueError."""

        names = validator.check("string_list", value)
        try:
            return [getattr(enum, x.upper()) for x in names]
        except AttributeError:
            raise validate.VdtValueError(value)

    def __init___require(self, config_file, spec_file, **kwargs):
        assert os.path.isfile(spec_file)

    def __init__(self, config_file, spec_file, print_unrecognized=True):
        """Initialize a Config object.

        config_file can be None for default configuration.
        Raise ConfigParseError if parsing config_file fails.
        """
        # pylint: disable-msg=W0233
        try:
            configobj.ConfigObj.__init__(
                self, config_file, configspec=spec_file,
                encoding=gaupol.util.get_default_encoding(),
                write_empty_values=True)
        except IOError:
            gaupol.util.print_read_io(sys.exc_info(), config_file)
            configobj.ConfigObj.__init__(
                self, None, configspec=spec_file,
                encoding=gaupol.util.get_default_encoding())
        except UnicodeError:
            configobj.ConfigObj.__init__(
                self, config_file, configspec=spec_file,
                encoding="utf_8", write_empty_values=True)
        except configobj.ConfigObjError, obj:
            print "Errors parsing configuration file '%s':" % config_file
            for error in obj.errors:
                print "Line %d: %s" % (error.line_number, error.message)
            raise gaupol.gtk.ConfigParseError(obj)

        self.__print_unrecognized = print_unrecognized
        validator = self.__init_validator()
        spec = self.__init_spec(validator, spec_file)
        self.__remove_sections(spec)
        for section in self.keys():
            self.__remove_options(spec, section)
        self.__validate(validator, spec)

    def __init_spec(self, validator, spec_file):
        """Initialize and return ConfigObj of spec."""

        spec = configobj.ConfigObj(None, configspec=spec_file)
        result = spec.validate(validator)
        if result is True: return spec
        print "Errors parsing configuration spec file '%s':" % spec_file
        for error in configobj.flatten_errors(spec, result):
            sections, option, message = error
            for section in sections:
                print "%s.%s: %s" % (section, option, message)
        raise SystemExit("Must exit.")

    def __init_validator(self):
        """Initialize and return validator."""

        validator = validate.Validator()
        for name, value in self.__get_enumerations().items():
            args = (self.__check_enum, validator, value)
            function = functools.partial(*args)
            validator.functions[name] = function
            args = (self.__check_enum_list, validator, value)
            function = functools.partial(*args)
            validator.functions["%s_list" % name] = function
        return validator

    def __remove_options(self, spec, section):
        """Remove options in config, but not in spec."""

        options = set(self[section].keys())
        options -= set(spec[section].keys())
        if section == "extensions":
            # Keep all options of extensions, i.e. subsections of the
            # extensions section to allow extensions to be activated at a later
            # time and to defer processing of those options to that time.
            for option in tuple(options):
                if isinstance(self[section][option], dict):
                    options.remove(option)
        if not options: return
        if self.__print_unrecognized:
            print "Discarding unrecognized configuration options:"
        for option in options:
            if self.__print_unrecognized:
                print "%s.%s" % (section, option)
            del self[section][option]

    def __remove_sections(self, spec):
        """Remove sections in config, but not in spec."""

        sections = set(self.keys())
        sections -= set(spec.keys())
        if not sections: return
        if self.__print_unrecognized:
            print "Discarding unrecognized configuration sections:"
        for section in sections:
            if self.__print_unrecognized:
                print section
            del self[section]

    def __validate(self, validator, spec):
        """Validate options according to spec."""

        result = self.validate(validator, preserve_errors=True)
        if result is True: return
        print "Discarding erroneous configuration options:"
        for error in configobj.flatten_errors(self, result):
            sections, option, message = error
            for section in sections:
                print "%s.%s: %s" % (section, option, message)
                self[section][option] = spec[section][option]
                self[section].defaults.append(option)

    def write_to_file_require(self):
        assert self.filename is not None

    def write_to_file_ensure(self, value):
        assert os.path.isfile(self.filename)

    def write_to_file(self):
        """Write configurations to file."""

        # pylint: disable-msg=W0201
        try:
            gaupol.util.makedirs(os.path.dirname(self.filename))
            configobj.ConfigObj.write(self)
        except (IOError, OSError):
            gaupol.util.print_write_io(sys.exc_info(), self.filename)
        except UnicodeError:
            if self.encoding != "utf_8":
                self.encoding = "utf_8"
                return self.write_to_file()
            raise # UnicodeError
