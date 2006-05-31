# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Application configuration."""


import ConfigParser
import os
import sys

from gaupol          import __version__
from gaupol.gtk.cons import NO, SHOW, HIDE, DURN, MTXT, TTXT
from gaupol.gtk.cons import Column, Format, Framerate, Mode, Newlines
from gaupol.gtk.cons import VideoPlayer


CONFIG_DIR  = os.path.join(os.path.expanduser('~'), '.gaupol')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'gaupol.gtk.conf')

config_header = \
'''# Gaupol GTK user interface configuration file
#
# This file is rewritten on each successful application exit. You may edit the
# entries if you\'re careful. To return to default settings, delete the
# corresponding lines or this entire file.

'''

LIST_SEP    = '|'


class Type(object):

    """Types of configuration variables."""

    STRING   = 0
    INTEGER  = 1
    BOOLEAN  = 2
    CONSTANT = 3

    STRING_LIST   = 10
    INTEGER_LIST  = 11
    BOOLEAN_LIST  = 12
    CONSTANT_LIST = 13

    @staticmethod
    def is_list(type_):
        """Return True if type is a list type."""

        return type_ > 9


class Section(object):

    """Base class for configuration classes."""

    types = {}
    classes = {}
    run_time_only = ()

    @classmethod
    def get_options(cls):
        """Get options defined."""

        options = []
        for name in dir(cls):
            if name.startswith('_'):
                continue
            if name in (
                'types',
                'classes',
                'run_time_only',
                'get_options',
            ):
                continue
            options.append(name)

        return options


class app_window(Section):

    """Application window configurations."""

    maximized          = False
    position           = [0, 0]
    show_main_toolbar  = True
    show_statusbar     = True
    show_video_toolbar = True
    size               = [600, 371]

    types = {
        'maximized'         : Type.BOOLEAN,
        'position'          : Type.INTEGER_LIST,
        'show_main_toolbar' : Type.BOOLEAN,
        'show_statusbar'    : Type.BOOLEAN,
        'show_video_toolbar': Type.BOOLEAN,
        'size'              : Type.INTEGER_LIST,
    }


class debug(Section):

    """Debug configurations."""

    editor = 'emacs'

    types = {
        'editor': Type.STRING,
    }


class duration_adjust(Section):

    """Duration adjust configurations."""

    all_projects  = False
    all_subtitles = True
    gap           = '0.050'
    lengthen      = True
    maximum       = '6.000'
    minimum       = '1.000'
    optimal       = '0.065'
    shorten       = False
    use_gap       = False
    use_maximum   = False
    use_minimum   = True

    types = {
        'all_projects' : Type.BOOLEAN,
        'all_subtitles': Type.BOOLEAN,
        'gap'          : Type.STRING,
        'lengthen'     : Type.BOOLEAN,
        'maximum'      : Type.STRING,
        'minimum'      : Type.STRING,
        'optimal'      : Type.STRING,
        'shorten'      : Type.BOOLEAN,
        'use_gap'      : Type.BOOLEAN,
        'use_maximum'  : Type.BOOLEAN,
        'use_minimum'  : Type.BOOLEAN,
    }


class editor(Section):

    """Editor configurations."""

    font             = ''
    framerate        = Framerate.FR_23_976
    limit_undo       = True
    mode             = Mode.TIME
    undo_levels      = 50
    use_default_font = True
    visible_cols     = [NO, SHOW, HIDE, DURN, MTXT]

    types = {
        'font'            : Type.STRING,
        'framerate'       : Type.CONSTANT,
        'limit_undo'      : Type.BOOLEAN,
        'mode'            : Type.CONSTANT,
        'undo_levels'     : Type.INTEGER,
        'use_default_font': Type.BOOLEAN,
        'visible_cols'    : Type.CONSTANT_LIST,
    }

    classes = {
        'framerate'   : Framerate,
        'mode'        : Mode,
        'visible_cols': Column,
    }


class encoding(Section):

    """Character encoding configurations."""

    fallbacks  = ['utf_8', 'cp1252']
    try_locale = True
    visibles   = ['utf_8', 'cp1252']

    types = {
        'fallbacks' : Type.STRING_LIST,
        'try_locale': Type.BOOLEAN,
        'visibles'  : Type.STRING_LIST,
    }


class file(Section):

    """File configurations."""

    directory  = os.path.expanduser('~')
    encoding   = ''
    format     = Format.SUBRIP
    max_recent = 5
    newlines   = Newlines.UNIX
    recent     = []
    warn_ssa   = True

    types = {
        'directory' : Type.STRING,
        'encoding'  : Type.STRING,
        'format'    : Type.CONSTANT,
        'max_recent': Type.INTEGER,
        'newlines'  : Type.CONSTANT,
        'recent'    : Type.STRING_LIST,
        'warn_ssa'  : Type.BOOLEAN,
    }

    classes = {
        'format'  : Format,
        'newlines': Newlines,
    }


class find(Section):

    """Find and replace configurations."""

    all_projects = False
    dot_all      = True
    ignore_case  = True
    main_col     = True
    multiline    = True
    pattern      = ''
    patterns     = []
    regex        = False
    replacement  = ''
    replacements = []
    tran_col     = True

    types = {
        'all_projects': Type.BOOLEAN,
        'dot_all'     : Type.BOOLEAN,
        'ignore_case' : Type.BOOLEAN,
        'main_col'    : Type.BOOLEAN,
        'multiline'   : Type.BOOLEAN,
        'pattern'     : Type.STRING,
        'patterns'    : Type.STRING_LIST,
        'regex'       : Type.BOOLEAN,
        'replacement' : Type.STRING,
        'replacements': Type.STRING_LIST,
        'tran_col'    : Type.BOOLEAN,
    }

    run_time_only = (
        'pattern',
        'replacement',
    )


class framerate_convert(Section):

    """Framerate convert configurations."""

    all_projects = True

    types = {
        'all_projects': Type.BOOLEAN,
    }


class general(Section):

    """General configurations."""

    version = __version__

    types = {
        'version': Type.STRING,
    }


class output_window(Section):

    """Output window configurations."""

    maximized = False
    position  = [0, 0]
    show      = False
    size      = [500, 309]

    types = {
        'maximized': Type.BOOLEAN,
        'position' : Type.INTEGER_LIST,
        'show'     : Type.BOOLEAN,
        'size'     : Type.INTEGER_LIST,
    }


class position_adjust(Section):

    """Position adjust configurations."""

    all_subtitles = True

    types = {
        'all_subtitles': Type.BOOLEAN,
    }


class position_shift(Section):

    """Position shift configurations."""

    all_subtitles = True
    frames        = 0
    seconds       = '0.000'

    types = {
        'all_subtitles': Type.BOOLEAN,
        'frames'       : Type.INTEGER,
        'seconds'      : Type.STRING,
    }


class preview(Section):

    """Preview configurations."""

    command        = ''
    offset         = '5.0'
    use_predefined = True
    video_player   = VideoPlayer.MPLAYER

    if sys.platform == 'win32':
        video_player = VideoPlayer.VLC

    types = {
        'command'       : Type.STRING,
        'offset'        : Type.STRING,
        'use_predefined': Type.BOOLEAN,
        'video_player'  : Type.CONSTANT,
    }

    classes = {
        'video_player': VideoPlayer,
    }


class spell_check(Section):

    """Spell-check configurations."""

    all_projects = False
    main         = True
    main_lang    = ''
    tran         = False
    tran_lang    = ''

    types = {
        'all_projects': Type.BOOLEAN,
        'main'        : Type.BOOLEAN,
        'main_lang'   : Type.STRING,
        'tran'        : Type.BOOLEAN,
        'tran_lang'   : Type.STRING,
    }


class subtitle_insert(Section):

    """Subtitle insert configurations."""

    amount = 1
    below  = True

    types = {
        'amount': Type.INTEGER,
        'below' : Type.BOOLEAN,
    }


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
    cls = eval(section).classes[option]

    if isinstance(arg, basestring):
        return getattr(cls, arg.upper())
    if isinstance(arg, int):
        return cls.get_name(arg).lower()
    raise ValueError

def make_profile_directory():
    """
    Make profile directory if it does no exist.

    Raise OSError if unsuccessful.
    """
    if os.path.isdir(CONFIG_DIR):
        return

    try:
        os.makedirs(CONFIG_DIR)
    except OSError, message:
        print 'Failed to create profile directory "%s": %s.' % (
            CONFIG_DIR, message)
        raise

def _get_sections():
    """Get a list of all sections."""

    sections = []
    for name in globals():
        if name == 'Section':
            continue
        try:
            if issubclass(eval(name), Section):
                sections.append(name)
        except TypeError:
            pass

    return sections

def read():
    """Read and parse settings from file."""

    parser = ConfigParser.RawConfigParser()
    result = parser.read([CONFIG_FILE])
    if not result:
        if os.path.isfile(CONFIG_FILE):
            print 'Failed to read configuration file "%s".' % CONFIG_FILE

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
                _set_config_option(parser, section, option)
            except Exception, message:
                print 'Failed to load configuration option "%s.%s".' % (
                    section, option)

def _set_config_option(parser, section, option):
    """
    Set value of config option from parser string.

    Raise Exception if something goes wrong.
    """
    string = parser.get(section, option)
    type_  = eval(section).types[option]

    if Type.is_list(type_):
        str_list = string.split(LIST_SEP)

    if type_ == Type.STRING:
        value = string
    elif type_ == Type.INTEGER:
        value = int(string)
    elif type_ == Type.BOOLEAN:
        value = _get_boolean(string)
    elif type_ == Type.CONSTANT:
        value = _get_constant(section, option, string)
    elif string == '':
        value = []
    elif type_ == Type.STRING_LIST:
        value = str_list
    elif type_ == Type.INTEGER_LIST:
        value = list(int(x) for x in str_list)
    elif type_ == Type.BOOLEAN_LIST:
        value = list(_get_boolean(x) for x in str_list)
    elif type_ == Type.CONSTANT_LIST:
        value = list(_get_constant(section, option, x) for x in str_list)

    setattr(eval(section), option, value)

def _set_parser_option(parser, section, option):
    """
    Set value of parser string from config option.

    Raise Exception if something goes wrong.
    """
    value = getattr(eval(section), option)
    type_ = eval(section).types[option]

    if value is None:
        string = ''
    elif type_ == Type.STRING:
        string = value
    elif type_ == Type.INTEGER:
        string = str(value)
    elif type_ == Type.BOOLEAN:
        string = _get_boolean(value)
    elif type_ == Type.CONSTANT:
        string = _get_constant(section, option, value)
    elif type_ == Type.STRING_LIST:
        str_list = value
    elif type_ == Type.INTEGER_LIST:
        str_list = list(str(x) for x in value)
    elif type_ == Type.BOOLEAN_LIST:
        str_list = list(_get_boolean(x) for x in value)
    elif type_ == Type.CONSTANT_LIST:
        str_list = list(_get_constant(section, option, x) for x in value)

    if Type.is_list(type_):
        string = LIST_SEP.join(str_list)

    parser.set(section, option, string)

def write():
    """Write configurations to file."""

    general.version = __version__
    parser = ConfigParser.RawConfigParser()

    for section in _get_sections():
        parser.add_section(section)
        for option in eval(section).get_options():
            if option in eval(section).run_time_only:
                continue
            try:
                _set_parser_option(parser, section, option)
            except Exception, message:
                print 'Failed to save configuration option "%s.%s".' % (
                    section, option)

    try:
        make_profile_directory()
    except OSError:
        return

    try:
        fobj = open(CONFIG_FILE, 'w')
        try:
            fobj.write(config_header)
        finally:
            fobj.close()
        fobj = open(CONFIG_FILE, 'a')
        try:
            parser.write(fobj)
        finally:
            fobj.close()
    except IOError, (no, message):
        print 'Failed to write configuration file "%s": %s.' % (
            CONFIG_FILE, message)
