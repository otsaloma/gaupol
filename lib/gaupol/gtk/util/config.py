# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if falset, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""
Application settings.

Other modules can get and set variables through the grouping classes and their
class variables.

ConfigParser is used for reading and writing the ini-style configuration file.
The configuration file is an .ini-style file in ~/.gaupol/gaupol.conf. Values
"true" or "false" are used for boolean fields and pipe-separated strings for
lists. All stored values are strings.
"""


import ConfigParser
import inspect
import logging
import os

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol import __version__
from gaupol.constants import *
from gaupol.gtk.colcons import *


logger = logging.getLogger()


# Configuration file constants
CONFIG_DIR    = os.path.join(os.path.expanduser('~'), '.gaupol')
CONFIG_PATH   = os.path.join(CONFIG_DIR, 'gaupol.conf')
CONFIG_HEADER = \
'''# Gaupol configuration file
#
# This file is rewritten on each successful application exit. Entered values
# are checked for correct type, but not for correct value. To return to
# default settings, delete the corresponding entries or this entire file.

'''


class TYPE(object):

    """Types for configuration variables."""

    STRING        = 0
    INTEGER       = 1
    BOOLEAN       = 2
    CONSTANT      = 3
    
    STRING_LIST   = 4
    INTEGER_LIST  = 5
    BOOLEAN_LIST  = 6
    CONSTANT_LIST = 7

    def is_list(type_):
        """Return True if type_ is a list type."""
        
        return type_ in [4, 5, 6, 7]

    is_list = staticmethod(is_list)


class application_window(object):

    maximized       = False
    _maximized_type = TYPE.BOOLEAN
    
    position        = [0, 0]
    _position_type  = TYPE.INTEGER_LIST
    
    size            = [600, 400]
    _size_type      = TYPE.INTEGER_LIST

class editor(object):

    edit_mode         = MODE.TIME
    _edit_mode_type   = TYPE.CONSTANT
    _edit_mode_class  = MODE
    
    framerate         = FRAMERATE.FR_23_976
    _framerate_type   = TYPE.CONSTANT
    _framerate_class  = FRAMERATE
    
    limit_undo        = True
    _limit_undo_type  = TYPE.BOOLEAN
    
    undo_levels       = 25
    _undo_levels_type = TYPE.INTEGER

class encoding_dialog(object):

    size       = [400, 400]
    _size_type = TYPE.INTEGER_LIST

class file(object):

    directory                  = os.path.expanduser('~')
    _directory_type            = TYPE.STRING

    encoding                   = None
    _encoding_type             = TYPE.STRING

    fallback_encodings         = ['utf8', 'windows1252']
    _fallback_encodings_type   = TYPE.STRING_LIST

    format                     = FORMAT.SUBRIP
    _format_type               = TYPE.CONSTANT
    _format_class              = FORMAT

    maximum_recent_files       = 5
    _maximum_recent_files_type = TYPE.INTEGER

    newlines                   = NEWLINE.UNIX
    _newlines_type             = TYPE.CONSTANT
    _newlines_class            = NEWLINE

    recent_files               = []
    _recent_files_type         = TYPE.STRING_LIST

    try_locale_encoding        = True
    _try_locale_encoding_type  = TYPE.BOOLEAN

    visible_encodings          = ['utf8', 'windows1252']
    _visible_encodings_type    = TYPE.STRING_LIST

class general(object):

    version       = __version__
    _version_type = TYPE.STRING

class subtitle_insert(object):

    amount          = 1
    _amount_type    = TYPE.INTEGER

    position        = POSITION.BELOW
    _position_type  = TYPE.CONSTANT
    _position_class = POSITION

class spell_check(object):

    check_all_projects         = False
    _check_all_projects_type   = TYPE.BOOLEAN

    check_text                 = True
    _check_text_type           = TYPE.BOOLEAN

    check_translation          = False
    _check_translation_type    = TYPE.BOOLEAN

    text_language              = None
    _text_language_type        = TYPE.STRING

    translation_language       = None
    _translation_language_type = TYPE.STRING

class view(object):

    font                   = None
    _font_type             = TYPE.STRING

    use_default_font       = True
    _use_default_font_type = TYPE.BOOLEAN

    statusbar              = True
    _statusbar_type        = TYPE.BOOLEAN

    toolbar                = True
    _toolbar_type          = TYPE.BOOLEAN

    columns                = [NO, SHOW, HIDE, DURN, TEXT]
    _columns_type          = TYPE.CONSTANT_LIST
    _columns_class         = COLUMN


def _get_boolean(arg):
    """
    Get boolean from string or string from boolean.

    Raise ValueError if arg not convertable.
    """
    booleans = [ True ,  False ]
    strings  = ['true', 'false']
    
    if isinstance(arg, basestring):
        return booleans[strings.index(arg)]
    elif isinstance(arg, bool):
        return strings[booleans.index(arg)]
    else:
        raise ValueError('Wrong argument type: %s.' % type(arg))

def _get_constant(section, option, arg):
    """
    Get constant from string or string from constant.

    Raise AttributeError if some attribute not found.
    Raise ValueError if arg not convertable.
    """
    constant_class = eval('%s._%s_class' % (section, option))

    if isinstance(arg, basestring):
        return constant_class.ID_NAMES.index(arg)
    elif isinstance(arg, int):
        return constant_class.ID_NAMES[arg]
    else:
        raise ValueError('Wrong argument type: %s.' % type(arg))

def get_options(section):
    """Get a list of all options in section."""

    options = []

    for name in dir(eval(section)):
        if not name.startswith('_'):
            options.append(name)

    return options

def get_sections():
    """Get a list of sections."""

    sections = []

    module = inspect.getmodule(TYPE)
    for name, value in inspect.getmembers(module):

        if not inspect.isclass(value):
            continue

        # Disregard imported classes.
        if inspect.getmodule(value) != module:
            continue

        if name == 'TYPE':
            continue

        sections.append(name)

    return sections

def read():
    """Read and parse settings from file."""

    parser = ConfigParser.RawConfigParser()

    # Read from file.
    result = parser.read([CONFIG_PATH])
    if not result:
        message  = 'Failed to read settings from file "%s".' % CONFIG_PATH
        message += ' Using default settings.'
        logger.info(message)

    # Set config options.
    sections = parser.sections()
    for section in sections:

        options = parser.options(section)
        for option in options:

            try:
                _set_config_option(parser, section, option)
            except (AttributeError, NameError, ValueError), detail:
                path = section, option
                message = 'Failed to load setting %s.%s from file' % path
                logger.warning('%s: %s.' % (message, detail))

    # Set version to current version.
    general.version = __version__

def _set_config_option(parser, section, option):
    """
    Set value of config option from parser string.
    
    Raise ValueError, AttributeError or NameError if something goes wrong.
    """
    string = parser.get(section, option)
    type_  = eval('%s._%s_type' % (section, option))

    # Convert string to proper data type.
    if string == '':
        if TYPE.is_list(type_):
            value = []
        else:
            value = None
            
    elif type_ == TYPE.STRING:
        value = string
        
    elif type_ == TYPE.INTEGER:
        value = int(string)
        
    elif type_ == TYPE.BOOLEAN:
        value = _get_boolean(string)
        
    elif type_ == TYPE.CONSTANT:
        value = _get_constant(section, option, string)
        
    elif type_ == TYPE.STRING_LIST:
        value = string.split('|')
        
    elif type_ == TYPE.INTEGER_LIST:
        str_list = string.split('|')
        value = [int(entry) for entry in str_list]
        
    elif type_ == TYPE.BOOLEAN_LIST:
        str_list = string.split('|')
        value = [_get_boolean(entry) for entry in str_list]
        
    elif type_ == TYPE.CONSTANT_LIST:
        str_list = string.split('|')
        value = [_get_constant(section, option, entry) for entry in str_list]

    # Set value.
    attr = eval('%s.%s' % (section, option))
    attr = value

def _set_parser_option(parser, section, option):
    """
    Set value of parser string from config option.
    
    Raise ValueError, AttributeError or NameError if something goes wrong.
    """
    value = eval('%s.%s'       % (section, option))
    type_ = eval('%s._%s_type' % (section, option))

    # Convert data type to string.
    if value == None:
        string = ''
        
    elif type_ == TYPE.STRING:
        string = value
        
    elif type_ == TYPE.INTEGER:
        string = str(value)
        
    elif type_ == TYPE.BOOLEAN:
        string = _get_boolean(value)
        
    elif type_ == TYPE.CONSTANT:
        string = _get_constant(section, option, value)
        
    elif type_ == TYPE.STRING_LIST:
        string = '|'.join(value)
        
    elif type_ == TYPE.INTEGER_LIST:
        str_list = [str(entry) for entry in value]
        string = '|'.join(str_list)
        
    elif type_ == TYPE.BOOLEAN_LIST:
        str_list = [_get_boolean(entry) for entry in value]
        string = '|'.join(str_list)
        
    elif type_ == TYPE.CONSTANT_LIST:
        str_list = [_get_constant(section, option, entry) for entry in value]
        string = '|'.join(str_list)

    # Set value.
    parser.set(section, option, string)

def write():
    """Assemble and write settings to file."""

    parser = ConfigParser.RawConfigParser()

    # Set parser options.
    sections = get_sections()
    for section in sections:
        parser.add_section(section)

        options = get_options(section)
        for option in options:

            try:
                _set_parser_option(parser, section, option)
            except (AttributeError, NameError, ValueError), detail:
                path = section, option
                message = 'Failed to write setting %s.%s to file' % path
                logger.error('%s: %s.' % (message, detail))

    # Create directory ~/.gaupol if it doesn't exist.
    if not os.path.isdir(CONFIG_DIR):
        try:
            os.makedirs(CONFIG_DIR)
        except OSError, detail:
            info = CONFIG_DIR, detail
            message = 'Failed to create profile directory "%s": %s.' % info
            logger.error(message)

    try:
    
        # Write header.
        config_file = open(CONFIG_PATH, 'w')
        try:
            config_file.write(CONFIG_HEADER)
        finally:
            config_file.close()
        
        # Write settings.
        config_file = open(CONFIG_PATH, 'a')
        try:
            parser.write(config_file)
        finally:
            config_file.close()

    except IOError, (errno, detail):
        info = CONFIG_PATH, detail
        message = 'Failed to write settings to file "%s": %s.' % info
        logger.error(message)
