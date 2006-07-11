# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Application configuration."""


import ConfigParser
import os
import sys
import urllib

from gaupol            import __version__
from gaupol.base.paths import PROFILE_DIR
from gaupol.base.util  import filelib
from gaupol.gtk        import cons
from gaupol.gtk.icons  import *


_CONFIG_FILE = os.path.join(PROFILE_DIR, 'gaupol.gtk.conf')
_LIST_START  = '['
_LIST_SEP    = ','
_LIST_END    = ']'


class _Type(object):

    """Types of configuration variables."""

    STRING        = 0
    INTEGER       = 1
    FLOAT         = 2
    BOOLEAN       = 3
    CONSTANT      = 4
    STRING_LIST   = 5
    INTEGER_LIST  = 6
    FLOAT_LIST    = 7
    BOOLEAN_LIST  = 8
    CONSTANT_LIST = 9

    @staticmethod
    def is_list(type_):
        """Return True if type is a list type."""

        return type_ > 4


class _Section(object):

    """Base class for configuration classes."""

    constants = {}
    privates  = ()
    types     = {}

    @classmethod
    def get_options(cls):
        """Get options defined."""

        options = []
        for name in dir(cls):
            if not name.startswith('_'):
                if not hasattr(_Section, name):
                    options.append(name)
        return options


class application_window(_Section):

    maximized          = False
    position           = [0, 0]
    show_main_toolbar  = True
    show_statusbar     = True
    show_video_toolbar = True
    size               = [600, 371]


class debug(_Section):

    editor = 'emacs'


class duration_adjust(_Section):

    gap      = 0.200
    lengthen = True
    max      = 6.000
    min      = 1.500
    optimal  = 0.065
    shorten  = False
    target   = cons.Target.CURRENT
    use_gap  = False
    use_max  = False
    use_min  = True

    constants = {
        'target': cons.Target,
    }


class editor(_Section):

    font             = ''
    framerate        = cons.Framerate.FR_23_976
    limit_undo       = False
    mode             = cons.Mode.TIME
    undo_levels      = 50
    use_default_font = True
    visible_cols     = [NUMB, SHOW, HIDE, DURN, MTXT]

    constants = {
        'framerate'   : cons.Framerate,
        'mode'        : cons.Mode,
        'visible_cols': cons.Column,
    }


class encoding(_Section):

    fallbacks  = ['utf_8', 'cp1252']
    try_auto   = True
    try_locale = True
    visibles   = ['utf_8', 'cp1252']


class file(_Section):

    directory  = os.path.expanduser('~')
    encoding   = ''
    format     = cons.Format.SUBRIP
    max_recent = 5
    newlines   = cons.Newlines.UNIX
    recents    = []
    smart_tran = True
    warn_ssa   = True

    constants = {
        'format'  : cons.Format,
        'newlines': cons.Newlines,
    }

    types = {
        'recents': _Type.STRING_LIST,
    }


class find(_Section):

    cols         = [MTXT]
    dot_all      = True
    ignore_case  = True
    max_history  = 10
    multiline    = True
    pattern      = ''
    patterns     = []
    regex        = False
    replacement  = ''
    replacements = []
    target       = cons.Target.CURRENT

    constants = {
        'cols'  : cons.Column,
        'target': cons.Target,
    }

    privates = (
        'pattern',
        'replacement',
    )

    types = {
        'patterns'    : _Type.STRING_LIST,
        'replacements': _Type.STRING_LIST,
    }


class framerate_convert(_Section):

    target = cons.Target.CURRENT

    constants = {
        'target': cons.Target,
    }


class general(_Section):

    version = __version__


class output_window(_Section):

    maximized = False
    position  = [0, 0]
    show      = False
    size      = [500, 309]


class position_adjust(_Section):

    target = cons.Target.CURRENT

    constants = {
        'target': cons.Target,
    }


class position_shift(_Section):

    frames  = 0
    seconds = 0.000
    target  = cons.Target.CURRENT

    constants = {
        'target': cons.Target,
    }


class preview(_Section):

    custom_command = ''
    offset         = 5.0
    use_predefined = True
    video_player   = cons.VideoPlayer.MPLAYER

    if sys.platform == 'win32':
        video_player = cons.VideoPlayer.VLC

    constants = {
        'video_player': cons.VideoPlayer,
    }


class spell_check(_Section):

    cols      = [MTXT]
    main_lang = 'en'
    max_repl  = 1000
    target    = cons.Target.CURRENT
    tran_lang = 'en'

    constants = {
        'cols'  : cons.Column,
        'target': cons.Target,
    }


class srtx(_Section):

    directory = ''
    max_width = 400

    privates = (
        'directory',
    )


class subtitle_insert(_Section):

    above  = False
    amount = 1


def _get_boolean(arg):
    """
    Get boolean from string or string from boolean.

    Raise ValueError if arg not convertable.
    """
    booleans = [ True ,  False ]
    strings  = ['true', 'false']

    if isinstance(arg, basestring):
        return booleans[strings.index(arg)]
    if isinstance(arg, bool):
        return strings[booleans.index(arg)]
    raise ValueError

def _get_constant(section, option, arg):
    """
    Get constant from string or string from constant.

    Raise AttributeError if attribute not found.
    Raise ValueError if arg not convertable.
    """
    cls = eval(section).constants[option]

    if isinstance(arg, basestring):
        return getattr(cls, arg.upper())
    if isinstance(arg, int):
        return cls.get_name(arg).lower()
    raise ValueError

def _get_sections():
    """Get list of all sections."""

    sections = []
    for name in globals():
        if name.startswith('_'):
            continue
        try:
            if issubclass(eval(name), _Section):
                sections.append(name)
        except TypeError:
            pass

    return sections

def _get_type(section, option):
    """Get type of option."""

    cls = eval(section)
    value = getattr(cls, option)

    if not isinstance(value, list):
        if isinstance(value, basestring):
            return _Type.STRING
        if isinstance(value, bool):
            return _Type.BOOLEAN
        if cls.constants.has_key(option):
            return _Type.CONSTANT
        if isinstance(value, int):
            return _Type.INTEGER
        if isinstance(value, float):
            return _Type.FLOAT
        raise ValueError

    if not value:
        return cls.types[option]
    if isinstance(value[0], basestring):
        return _Type.STRING_LIST
    if isinstance(value[0], bool):
        return _Type.BOOLEAN_LIST
    if cls.constants.has_key(option):
        return _Type.CONSTANT_LIST
    if isinstance(value[0], int):
        return _Type.INTEGER_LIST
    if isinstance(value[0], float):
        return _Type.FLOAT_LIST


def _set_conf_option(parser, section, option):
    """
    Set value of conf option from parser string.

    Raise Exception if something goes wrong.
    """
    string = parser.get(section, option)
    type_  = _get_type(section, option)

    if _Type.is_list(type_):
        if not string.startswith(_LIST_START):
            raise ValueError
        if not string.endswith(_LIST_END):
            raise ValueError
        str_list = string[1:-1].split(_LIST_SEP)
        str_list = list(urllib.unquote(x) for x in str_list)

    if type_ == _Type.STRING:
        value = string
    elif type_ == _Type.INTEGER:
        value = int(string)
    elif type_ == _Type.FLOAT:
        value = float(string)
    elif type_ == _Type.BOOLEAN:
        value = _get_boolean(string)
    elif type_ == _Type.CONSTANT:
        value = _get_constant(section, option, string)
    elif string == '':
        value = []
    elif type_ == _Type.STRING_LIST:
        value = str_list
    elif type_ == _Type.INTEGER_LIST:
        value = list(int(x) for x in str_list)
    elif type_ == _Type.FLOAT_LIST:
        value = list(float(x) for x in str_list)
    elif type_ == _Type.BOOLEAN_LIST:
        value = list(_get_boolean(x) for x in str_list)
    elif type_ == _Type.CONSTANT_LIST:
        value = list(_get_constant(section, option, x) for x in str_list)

    setattr(eval(section), option, value)

def _set_parser_option(parser, section, option):
    """
    Set value of parser string from conf option.

    Raise Exception if something goes wrong.
    """
    value = getattr(eval(section), option)
    type_ = _get_type(section, option)

    if value is None:
        string = ''
    elif type_ == _Type.STRING:
        string = value
    elif type_ == _Type.INTEGER:
        string = str(value)
    elif type_ == _Type.FLOAT:
        string = '%.3f' % value
    elif type_ == _Type.BOOLEAN:
        string = _get_boolean(value)
    elif type_ == _Type.CONSTANT:
        string = _get_constant(section, option, value)
    elif type_ == _Type.STRING_LIST:
        str_list = value
    elif type_ == _Type.INTEGER_LIST:
        str_list = list(str(x) for x in value)
    elif type_ == _Type.FLOAT_LIST:
        str_list = list('%.3f' % x for x in value)
    elif type_ == _Type.BOOLEAN_LIST:
        str_list = list(_get_boolean(x) for x in value)
    elif type_ == _Type.CONSTANT_LIST:
        str_list = list(_get_constant(section, option, x) for x in value)

    if _Type.is_list(type_):
        str_list = list(urllib.quote(x) for x in str_list)
        string = _LIST_START + _LIST_SEP.join(str_list) + _LIST_END

    parser.set(section, option, string)

def read():
    """Read configurations from file."""

    parser = ConfigParser.RawConfigParser()
    result = parser.read([_CONFIG_FILE])
    if not result:
        if os.path.isfile(_CONFIG_FILE):
            print 'Failed to read configuration file "%s".' % _CONFIG_FILE
        return

    sections = _get_sections()
    for section in parser.sections():
        if not section in sections:
            print 'Unrecognized configuration section "%s".' % section
            continue
        options = eval(section).get_options()
        for option in parser.options(section):
            if not option in options:
                print 'Unrecognized configuration option "%s.%s".' % (
                    section, option)
                continue
            try:
                _set_conf_option(parser, section, option)
            except Exception:
                print 'Failed to load configuration option "%s.%s".' % (
                    section, option)

def write():
    """Write configurations to file."""

    general.version = __version__
    parser = ConfigParser.RawConfigParser()

    for section in _get_sections():
        parser.add_section(section)
        for option in eval(section).get_options():
            if option in eval(section).privates:
                continue
            try:
                _set_parser_option(parser, section, option)
            except Exception:
                print 'Failed to save configuration option "%s.%s".' % (
                    section, option)

    try:
        filelib.make_profile_directory()
    except OSError:
        return
    try:
        fobj = open(_CONFIG_FILE, 'w')
        try:
            parser.write(fobj)
        finally:
            fobj.close()
    except IOError, (no, message):
        print 'Failed to write configuration file "%s": %s.' % (
            _CONFIG_FILE, message)
