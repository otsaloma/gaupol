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


"""Subtitle file writing."""


import copy
import logging
import os
import shutil
import tempfile

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.constants import FORMAT, MODE
from gaupol.base.colcons import *
from gaupol.base.delegates.delegate import Delegate
from gaupol.base.files.classes import *
from gaupol.base.tags.tagconv import TagConverter


logger = logging.getLogger()


class FileWriter(Delegate):
    
    """Subtitle file writing."""
    
    def _create_temporary_backup_file(self, path, bak_path):
        """
        Create a temporary backup file before writing.

        Return success (True or False).
        """
        try:
            shutil.copyfile(path, bak_path)
            return True
        except IOError, (errno, detail):
            info = bak_path, detail
            msg = 'Failed to create temporary backup file "%s": %s.' % info
            logger.warning(msg)
            return False

    def _remove_failed_file(self, path):
        """Remove empty file after failing writing."""
        
        try:
            os.remove(path)
        except OSError, (errno, detail):
            msg  = 'Failed to remove file "%s"' % path
            msg += ' after failing to write it: %s.' % detail
            logger.warning(msg)
        
    def _remove_temporary_backup_file(self, bak_path):
        """Remove temporary backup file after successful writing."""
        
        try:
            os.remove(bak_path)
        except OSError, (errno, detail):
            info = bak_path, detail
            msg = 'Failed to remove temporary backup file "%s": %s.' % info
            logger.warning(msg)

    def _restore_original_file(self, path, bak_path):
        """Restore file from temporary backup after failing writing."""
        
        try:
            shutil.move(bak_path, path)
        except IOError, (errno, detail):
            msg  = 'Failed to restore file "%s" ' % path
            msg += ' from temporary backup file "%s"' % bak_path
            msg += ' after failing to write it: %s.' % detail
            logger.error(msg)

    def _write_file(self, col, keep_changes,
                    path, format, encoding, newlines):
        """
        Write subtitle file.
        
        Raise IOError if reading fails.
        Raise UnicodeError if encoding fails.
        """
        files = [self.main_file, self.tran_file]
        current_file = files[col]
        
        # Create a copy of texts, because possible tag conversions might be
        # only temporary.
        new_texts = copy.deepcopy(self.texts)

        # Convert tags if saving in different format.
        if current_file is not None and format is not None:
            if current_file.FORMAT != format:
                conv = TagConverter(current_file.FORMAT, format)
                for i in range(len(new_texts)):
                    new_texts[i][col] = conv.convert_tags(new_texts[i][col])

        # Get subtitle file object.
        if None in [path, format, encoding, newlines]:
            subtitle_file = current_file
            path = current_file.path
        else:
            format_name = FORMAT.CLASS_NAMES[format]
            subtitle_file = eval(format_name)(path, encoding, newlines)

        # Prepare data for writing.
        shows = []
        hides = []
        texts = []

        if subtitle_file.MODE == MODE.TIME:
            times = self.times
            for i in range(len(times)):
                shows.append(times[i][SHOW])
                hides.append(times[i][HIDE])
                texts.append(new_texts[i][col])

        elif subtitle_file.MODE == MODE.FRAME:
            frames = self.frames
            for i in range(len(frames)):
                shows.append(frames[i][SHOW])
                hides.append(frames[i][HIDE])
                texts.append(new_texts[i][col])

        # If the file to be written already exists, a temporary backup copy of
        # it is made in case writing fails. If the file does not exist and
        # writing fails, the resulting file is removed.

        file_existed = os.path.isfile(path)

        # Create backup.
        if file_existed:
            temp_dir = tempfile.gettempdir()
            basename = os.path.basename(path)
            bak_path = os.path.join(temp_dir, basename, '.gaupol')
            bak_success = self._create_temporary_backup_file(path, bak_path)

        # Write file.
        write_success = False
        try:
            subtitle_file.write(shows, hides, texts)
            write_success = True

        # Clean up.
        finally:
            if file_existed and bak_success and (not write_success):
                self._restore_original_file(path, bak_path)
            elif (not file_existed) and (not write_success):
                self._remove_failed_file(path)
            elif file_existed and bak_success and write_success:
                self._remove_temporary_backup_file(bak_path)

        # After successful writing, instance variables can be set.
        if keep_changes:
            if col == TEXT:
                self.main_file = subtitle_file
            elif col == TRAN:
                self.tran_file = subtitle_file
            self.texts = new_texts

    def write_main_file(
        self, keep_changes=True,
        path=None, format=None, encoding=None, newlines=None
    ):
        """
        Write main file.
        
        Raise IOError if reading fails.
        Raise UnicodeError if encoding fails.
        """
        self._write_file(TEXT, keep_changes, path, format, encoding, newlines)

    def write_translation_file(
        self, keep_changes=True,
        path=None, format=None, encoding=None, newlines=None
    ):
        """
        Write translation file.
        
        Raise IOError if reading fails.
        Raise UnicodeError if encoding fails.
        """
        self._write_file(TRAN, keep_changes, path, format, encoding, newlines)
