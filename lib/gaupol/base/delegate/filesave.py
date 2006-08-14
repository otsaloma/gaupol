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


"""Saving subtitle files."""


import os
import shutil
import tempfile

from gaupol.base                import cons
from gaupol.base.icons          import *
from gaupol.base.delegate       import Delegate
from gaupol.base.file.classes   import *
from gaupol.base.tags.converter import TagConverter


def _create_backup(path, bak_path):
    """
    Create a temporary backup file.

    Return success (True or False).
    """
    try:
        shutil.copyfile(path, bak_path)
        return True
    except IOError, (no, message):
        print 'Failed to create temporary backup file "%s": %s.' % (
            bak_path, message)
        return False

def _remove_backup(bak_path):
    """Remove temporary backup file."""

    try:
        os.remove(bak_path)
    except OSError, (no, message):
        print 'Failed to remove temporary backup file "%s": %s.' % (
            bak_path, message)

def _remove_failed(path):
    """Remove empty file after failing to write it."""

    try:
        os.remove(path)
    except OSError, (no, message):
        print 'Failed to remove file "%s" after failing to write it: %s.' % (
            path, message)

def _restore_original(path, bak_path):
    """Restore file from temporary backup after failing writing."""

    try:
        shutil.move(bak_path, path)
    except (IOError, OSError), (no, message):
        print 'Failed to restore file "%s" from temporary backup file "%s" ' \
              'after failing to write it: %s.' % (path, bak_path, message)


class FileSaveDelegate(Delegate):

    """Saving subtitle files."""

    def _save_file(self, doc, props, keep_changes):
        """
        Save subtitle file.

        props: path, format, encoding, newlines
        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        file_ = (self.main_file, self.tran_file)[doc]
        path, format, encoding, newlines = props or [None] * 4

        # Convert tags if saving in different format.
        texts = (self.main_texts, self.tran_texts)[doc]
        if file_ is not None and format is not None:
            if file_.format != format:
                conv = TagConverter(file_.format, format)
                texts = list(conv.convert(x) for x in texts)

        # Create file if needed.
        if not None in (path, format, encoding, newlines):
            format_name = cons.Format.class_names[format]
            new_file = eval(format_name)(path, encoding, newlines)
            if file_ is not None:
                if file_.format == format:
                    new_file.header = file_.header
                if file_.format == cons.Format.MPSUB:
                    if format == cons.Format.MPSUB:
                        new_file.mode = file_.mode
            file_ = new_file

        self._write_file(file_, texts)

        if keep_changes:
            if doc == MAIN:
                self.main_file = file_
                self.main_texts = texts
            elif doc == TRAN:
                self.tran_file = file_
                self.tran_texts = texts

    def _write_file(self, file_, texts):
        """
        Write subtitle file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        sources = {cons.Mode.TIME: self.times, cons.Mode.FRAME: self.frames}
        source = sources[file_.mode]
        shows = list(source[i][SHOW] for i in range(len(source)))
        hides = list(source[i][HIDE] for i in range(len(source)))

        file_existed = os.path.isfile(file_.path)
        if file_existed:
            bak_path = tempfile.mkstemp('.bak', 'gaupol.')[1]
            bak_success = _create_backup(file_.path, bak_path)
        try:
            write_success = False
            file_.write(shows, hides, texts)
            write_success = True
        finally:
            if write_success:
                if file_existed and bak_success:
                    _remove_backup(bak_path)
            else:
                if file_existed:
                    if bak_success:
                        _restore_original(file_.path, bak_path)
                elif not write_success:
                    _remove_failed(file_.path)

    def save_main_file(self, props=None, keep_changes=True):
        """
        Save main file.

        props: path, format, encoding, newlines
        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        self._save_file(MAIN, props, keep_changes)
        if keep_changes:
            self.main_changed = 0

    def save_translation_file(self, props=None, keep_changes=True):
        """
        Save translation file.

        props: path, format, encoding, newlines
        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        self._save_file(TRAN, props, keep_changes)
        if keep_changes:
            self.tran_active = True
            self.tran_changed = 0
