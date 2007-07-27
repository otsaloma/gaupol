# Copyright (C) 2006-2007 Osmo Salomaa
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
    handle Gaupol's constants, which can be defined in the spec file as
    CONSTANT and CONSTANT_list for each CONSTANT.
    """

    __metaclass__ = gaupol.Contractual

    def __check_constant(self, validator, section, value):
        """Validate and return constant or raise VdtValueError."""

        name = validator.check("string", value)
        section = getattr(gaupol.gtk, section)
        try:
            index = section.names.index(name)
            return section.members[index]
        except ValueError:
            raise validate.VdtValueError(value)

    def __check_constant_list(self, validator, section, value):
        """Validate and return constant list or raise VdtValueError."""

        names = validator.check("string_list", value)
        section = getattr(gaupol.gtk, section)
        try:
            indexes = [section.names.index(x) for x in names]
            return [section.members[x] for x in indexes]
        except ValueError:
            raise validate.VdtValueError(value)

    def __init___require(self, config_file, spec_file):
        assert os.path.isfile(spec_file)

    def __init__(self, config_file, spec_file):
        """Initialize a Config object.

        config_file can be None for default configuration.
        Raise ConfigParseError if parsing config_file fails.
        """
        try:
            configobj.ConfigObj.__init__(
                self, config_file, configspec=spec_file,
                encoding=gaupol.util.get_default_encoding(),
                write_empty_values=True)
        except IOError:
            gaupol.util.handle_read_io(sys.exc_info(), config_file)
            # pylint: disable-msg=W0233
            configobj.ConfigObj.__init__(
                self, None, configspec=spec_file,
                encoding=gaupol.util.get_default_encoding())
        except configobj.ConfigObjError, obj:
            print "Errors parsing configuration file '%s':" % config_file
            for error in obj.errors:
                print "Line %d: %s" % (error.line_number, error.message)
            raise gaupol.gtk.ConfigParseError(obj)

        validator = self.__init_validator()
        spec = self.__init_spec(validator, spec_file)
        self.__remove_sections(spec)
        self.__remove_options(spec)
        self.__validate(validator, spec)

    def __init_spec(self, validator, spec_file):
        """Initialize and return ConfigObj of spec."""

        spec = configobj.ConfigObj(None, configspec=spec_file)
        result = spec.validate(validator)
        if result is True:
            return spec
        print "Errors parsing configuration spec file '%s':" % spec_file
        for error in configobj.flatten_errors(spec, result):
            sections, option, message = error
            for section in sections:
                print "%s.%s: %s" % (section, option, message)
        raise SystemExit("Must exit.")

    def __init_validator(self):
        """Initialize and return validator."""

        from gaupol.gtk import const
        partial = functools.partial
        validator = validate.Validator()
        for name in (x for x in dir(const) if x.isupper()):
            # pylint: disable-msg=E1102
            func = partial(self.__check_constant, validator, name)
            validator.functions[name] = func
            func = partial(self.__check_constant_list, validator, name)
            validator.functions["%s_list" % name] = func
        return validator

    @gaupol.util.asserted_return
    def __remove_options(self, spec):
        """Remove options in config, but not in spec."""

        first = True
        for section in self.iterkeys():
            options = set(self[section].keys())
            options -= set(spec[section].keys())
            if options and first:
                print "Discarding unrecognized configuration options:"
                first = False
            for option in options:
                print "%s.%s" % (section, option)
                del self[section][option]

    @gaupol.util.asserted_return
    def __remove_sections(self, spec):
        """Remove sections in config, but not in spec."""

        sections = set(self.keys())
        sections -= set(spec.keys())
        assert sections
        print "Discarding unrecognized configuration sections:"
        for section in sections:
            print section
            del self[section]

    @gaupol.util.asserted_return
    def __validate(self, validator, spec):
        """Validate options according to spec."""

        result = self.validate(validator, preserve_errors=True)
        assert not result
        print "Discarding erroneous configuration options:"
        for error in configobj.flatten_errors(self, result):
            sections, option, message = error
            for section in sections:
                print "%s.%s: %s" % (section, option, message)
                self[section][option] = spec[section][option]
                self[section].defaults.append(option)

    @gaupol.util.asserted_return
    def translate_none(self, section, option, value):
        """Translate a default None value to value."""

        assert option in self[section].defaults
        assert self[section][option] is None
        self[section][option] = value
        self[section].defaults.append(option)

    def write_to_file_require(self):
        assert self.filename is not None

    def write_to_file_ensure(self, value):
        assert os.path.isfile(self.filename)

    def write_to_file(self):
        """Write configurations to file."""

        try:
            gaupol.util.makedirs(os.path.dirname(self.filename))
            configobj.ConfigObj.write(self)
        except (IOError, OSError):
            gaupol.util.handle_write_io(sys.exc_info(), self.filename)
