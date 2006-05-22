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


"""Saving subtitle files."""


try:
    from psyco.classes import *
except ImportError:
    pass

import copy
import logging
import os
import shutil
import tempfile

from gaupol.base.cons import SHOW, HIDE, DURN
from gaupol.base.delegates      import Delegate
from gaupol.base.files.classes  import *
from gaupol.base.tags.converter import TagConverter
from gaupol.base.cons           import Document, Format, Mode


logger = logging.getLogger()


class FileSaveDelegate(Delegate):

    """Saving subtitle files."""

    def _create_backup_file(self, path, bak_path):
        """
        Create a temporary backup file before writing.

        Return success (True or False).
        """
        try:
            shutil.copyfile(path, bak_path)
            return True
        except IOError, (no, message):
            message = 'Failed to create temporary backup file "%s": %s.' \
                      % (bak_path, message)
            logger.warning(message)
            return False

    def _remove_failed_file(self, path):
        """Remove empty file after failing writing."""

        try:
            os.remove(path)
        except OSError, (no, message):
            message = 'Failed to remove file "%s" after failing to write ' \
                      'it: %s.' % (path, message)
            logger.warning(message)

    def _remove_backup_file(self, bak_path):
        """Remove temporary backup file after successful writing."""

        try:
            os.remove(bak_path)
        except OSError:
            pass

    def _restore_original_file(self, path, bak_path):
        """Restore file from temporary backup after failing writing."""

        try:
            shutil.move(bak_path, path)
        except IOError, (no, message):
            message = 'Failed to restore file "%s" from temporary backup ' \
                      'file "%s" after failing to write it: %s.' \
                      % (path, bak_path, message)
            logger.error(message)

    def _save_file(self, document, keep_changes, properties):
        """
        Save subtitle file.

        properties: path, format, encoding, newlines
        Raise IOError if reading fails.
        Raise UnicodeError if encoding fails.
        """
        current_file  = [self.main_file , self.tran_file ][document]
        current_texts = [self.main_texts, self.tran_texts][document]
        path, format, encoding, newlines = properties or [None] * 4

        # Create a copy of texts, because possible tag conversions might be
        # only temporary.
        new_texts = copy.deepcopy(current_texts)

        # Convert tags if saving in different format.
        if current_file is not None and format is not None:
            if current_file.format != format:
                conv = TagConverter(current_file.format, format)
                for i in range(len(new_texts)):
                    new_texts[i] = conv.convert_tags(new_texts[i])

        # Get subtitle file object.
        if None in (path, format, encoding, newlines):
            subtitle_file = current_file
            path = current_file.path
        else:
            format_name = Format.CLASS_NAMES[format]
            subtitle_file = eval(format_name)(path, encoding, newlines)
            # Copy header if saving in same format.
            if current_file is not None:
                if current_file.format == format:
                    subtitle_file.header = current_file.header

        shows  = []
        hides  = []
        texts  = []
        if subtitle_file.mode == Mode.TIME:
            times = self.times
            for i in range(len(times)):
                shows.append(times[i][SHOW])
                hides.append(times[i][HIDE])
                texts.append(new_texts[i])
        elif subtitle_file.mode == Mode.FRAME:
            frames = self.frames
            for i in range(len(frames)):
                shows.append(frames[i][SHOW])
                hides.append(frames[i][HIDE])
                texts.append(new_texts[i])

        # If the file to be written already exists, a temporary backup copy of
        # it is made in case writing fails. If the file does not exist and
        # writing fails, the resulting file (usually empty) is removed.
        file_existed = os.path.isfile(path)

        # Create backup.
        if file_existed:
            bak_path = tempfile.mkstemp('.bak', 'gaupol.')[1]
            bak_success = self._create_backup_file(path, bak_path)

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
                self._remove_backup_file(bak_path)

        # After successful writing, instance variables can be set.
        if keep_changes:
            if document == Document.MAIN:
                self.main_file = subtitle_file
                self.main_texts = new_texts
            elif document == Document.TRAN:
                self.tran_file = subtitle_file
                self.tran_texts = new_texts

    def save_main_file(self, keep_changes=True, properties=None):
        """
        Save main file.

        properties: path, format, encoding, newlines
        Raise IOError if reading fails.
        Raise UnicodeError if encoding fails.
        """
        self._save_file(Document.MAIN, keep_changes, properties)
        if keep_changes:
            self.main_changed = 0

    def save_translation_file(self, keep_changes=True, properties=None):
        """
        Save translation file.

        properties: path, format, encoding, newlines
        Raise IOError if reading fails.
        Raise UnicodeError if encoding fails.
        """
        self._save_file(Document.TRAN, keep_changes, properties)
        if keep_changes:
            self.tran_active  = True
            self.tran_changed = 0


if __name__ == '__main__':

    from gaupol.base.cons import Newlines
    from gaupol.test      import Test

    class TestFileSaveDelegate(Test):

        def test_save_files(self):

            project = self.get_project()

            project.save_main_file()
            project.save_translation_file()

            properties = [
                project.main_file.path,
                Format.MPL2,
                'utf_8',
                Newlines.UNIX
            ]
            project.save_main_file(properties=properties)
            properties[1] = Format.MICRODVD
            project.save_main_file(properties=properties)
            properties[1] = Format.SUBVIEWER2
            project.save_main_file(properties=properties)

            project.insert_subtitles([0])
            project.save_main_file(keep_changes=False)
            assert project.main_changed
            project.save_main_file(keep_changes=True)
            assert not project.main_changed

    TestFileSaveDelegate().run()
