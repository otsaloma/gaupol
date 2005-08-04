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
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Subtitle project data."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.lib.delegates.analyzer import Analyzer
from gaupol.lib.delegates.editor import Editor
from gaupol.lib.delegates.filereader import FileReader
from gaupol.lib.delegates.filewriter import FileWriter
from gaupol.lib.delegates.formatter import Formatter
from gaupol.lib.delegates.frconv import FramerateConverter
from gaupol.lib.time.timeframe import TimeFrameConverter


class Data(object):
    
    """
    Subtitle project data.

    This is the main class for gaupol.lib. This class holds the all the
    subtitle data of one project. All methods are outsourced to delegates.
    
    times    : list of lists of strings : [[show-1, hide-1, duration-1],...]
    frames   : list of lists of integers: [[show-1, hide-1, duration-1],...]
    texts    : list of lists of strings : [[original-1, translation-1],...]
    framerate: string
    """
    
    def __init__(self, framerate):

        self.times  = []
        self.frames = []
        self.texts  = []

        self.framerate = framerate
        self.tf_conv   = TimeFrameConverter(framerate)

        self.main_file = None
        self.tran_file = None

        self._delegations = None

        self._assign_delegations()

    def _assign_delegations(self):
        """Map method names to Delegate objects."""
        
        analyzer    = Analyzer(self)
        editor      = Editor(self)
        file_reader = FileReader(self)
        file_writer = FileWriter(self)
        formatter   = Formatter(self)
        fr_conv     = FramerateConverter(self)

        self._delegations = {
            'change_case'           : formatter,
            'change_framerate'      : fr_conv,
            'clear_texts'           : editor,
            'get_character_count'   : analyzer,
            'get_format'            : formatter,
            'insert_subtitles'      : editor,
            'read_main_file'        : file_reader,
            'read_translation_file' : file_reader,
            'remove_subtitles'      : editor,
            'set_frame'             : editor,
            'set_text'              : editor,
            'set_texts'             : editor,
            'set_time'              : editor,
            'toggle_dialog_lines'   : formatter,
            'toggle_italicization'  : formatter,
            'write_main_file'       : file_writer,
            'write_translation_file': file_writer,
        }
        
    def __getattr__(self, name):
        """Delegate method calls to Delegate objects."""
        
        return self._delegations[name].__getattribute__(name)
