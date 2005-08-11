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


"""Application settings."""


from ConfigParser import RawConfigParser
import logging
import os

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.constants import VERSION


logger = logging.getLogger()


CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.gaupol', 'gaupol.conf')

HEADER = \
'''# Gaupol configuration file
#
# This file is rewritten on each successful application exit. Entered values
# are not checked for correctness. To return to default settings, delete this
# file.

'''

KEY, VALUE = 0, 1

DEFAULTS = {
    'editor':
    (
        ('edit_mode'  , 'time'  ),
        ('framerate'  , '23.976'),
        ('limit_undo' , 'true'  ),
        ('undo_levels', '25'    ),
    ),
    'encoding_dialog':
    (
        ('size', '400|400'),
    ),
    'file':
    (
        ('directory'           , os.path.expanduser('~')),
        ('encoding'            , ''                     ),
        ('format'              , 'SubRip'               ),
        ('maximum_recent_files', '5'                    ),
        ('newlines'            , 'Unix'                 ),
        ('recent_files'        , ''                     ),
        ('visible_encodings'   , 'utf_8'                ),
    ),
    'general':
    (
        ('version', VERSION),
    ),
    'insert_subtitles':
    (
        ('amount'  , 1      ),
        ('position', 'below'),
    ),
    'main_window':
    (
        ('maximized', 'false'  ),
        ('position' , '0|0'    ),
        ('size'     , '600|400'),
    ),
    'view':
    (
        ('font'     , ''                              ),
        ('statusbar', 'true'                          ),
        ('toolbar'  , 'true'                          ),
        ('columns'  , 'no|show|hide|duration|original'),
    ),
}


class Config(RawConfigParser):

    """
    Application settings.

    Settings are stored in an .ini-style file in ~/.gaupol/gaupol.conf. Values
    'true' or 'false' are used for boolean fields and pipe-separated strings
    for lists. All stored values are strings. Functions can be used to get or
    set other value types than strings.

    This class will both read and write settings as well as store settings so
    that they can be requested while application is running.
    """
    
    def getfloat(self, section, key):
        """
        Get a float from key.

        Raise NoSectionError if section doesn't exist.
        """
        return float(self.get(section, key))

    def getlist(self, section, key):
        """
        Get a list from key.

        Raise NoSectionError if section doesn't exist.
        """
        string = self.get(section, key)
        
        return string.split('|')

    def getlistint(self, section, key):
        """
        Get a list of integers from key.

        Raise NoSectionError if section doesn't exist.
        Raise ValueError if values are not intergers.
        """
        string = self.get(section, key)
        
        string_list  = string.split('|')
        integer_list = [int(value) for value in string_list]
        
        return integer_list

    def read_from_file(self):
        """
        Read and parse settings from file.

        If settings don't exist in file, defaults will be used.
        """
        self._set_defaults()
        
        # Read from file.
        result = self.read([CONFIG_PATH])
        if not result:
            logger.info( \
                'Failed to read settings from file "%s". Using default settings.' \
                % CONFIG_PATH \
            )

        # Accept only keys and sections that exist.
        sections = self.sections()
        for section in sections:
        
            if not section in DEFAULTS:
                self.remove_section(section)
                continue
                
            options       = self.options(section)
            valid_options = [entry[KEY] for entry in DEFAULTS[section]]

            for option in options:
                if option not in valid_options:
                    self.remove_option(section, option)

    def setboolean(self, section, key, value):
        """
        Set a boolean value to key.

        Raise NoSectionError if section doesn't exist.
        """
        if value:
            self.set(section, key, 'true')
        else:
            self.set(section, key, 'false')

    def setint(self, section, key, value):
        """
        Set an integer value to key.

        Raise NoSectionError if section doesn't exist.
        """
        self.set(section, key, str(value))

    def setlist(self, section, key, string_list):
        """
        Set a list of strings to key.

        Raise NoSectionError if section doesn't exist.
        """
        string = '|'.join(string_list)
        
        self.set(section, key, string)

    def setlistint(self, section, key, integer_list):
        """
        Set a list of intergers to key.

        Raise NoSectionError if section doesn't exist.
        """
        string_list = [str(value) for value in integer_list]
        string = '|'.join(string_list)
        
        self.set(section, key, string)

    def _set_defaults(self):
        """Set default values for all settings."""

        for section in DEFAULTS:
            self.add_section(section)
            for setting in DEFAULTS[section]:
                self.set(section, setting[KEY], setting[VALUE])

    def write_to_file(self):
        """Write settings to file."""

        try:
        
            # Write header.
            config_file = open(CONFIG_PATH, 'w')
            try:
                config_file.write(HEADER)
            finally:
                config_file.close()
            
            # Write settings.
            config_file = open(CONFIG_PATH, 'a')
            try:
                self.write(config_file)
            finally:
                config_file.close()

        except IOError, (errno, detail):
            logger.error('Failed to write settings to file "%s": %s.' \
                         % (CONFIG_PATH, detail))
