# Copyright (C) 2005-2007 Osmo Salomaa
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

from gaupol import cons
from gaupol.base import Delegate
from gaupol.converter import TagConverter
from gaupol.files import *
from .index import SHOW, HIDE, DURN


def _create_backup(path, bak_path):
    """Create a temporary backup file.

    Return success (True or False).
    """
    try:
        shutil.copyfile(path, bak_path)
        return True
    except IOError, (no, message):
        print "Failed to create temporary backup file '%s': %s." % (
            bak_path, message)
        return False

def _remove_backup(bak_path):
    """Remove the temporary backup file.

    Return success (True or False).
    """
    try:
        os.remove(bak_path)
        return True
    except OSError, (no, message):
        print "Failed to remove temporary backup file '%s': %s." % (
            bak_path, message)
        return False

def _remove_failed(path):
    """Remove the empty file after failing to write it.

    Return success (True or False).
    """
    try:
        os.remove(path)
        return True
    except OSError, (no, message):
        print "Failed to remove file '%s' after failing to write it: %s." % (
            path, message)
        return False

def _restore_original(path, bak_path):
    """Restore the file from the temporary backup after failing writing.

    Return success (True or False).
    """
    try:
        shutil.move(bak_path, path)
        return True
    except (IOError, OSError), (no, message):
        print "Failed to restore file '%s' from temporary backup file '%s' " \
            "after failing to write it: %s." % (path, bak_path, message)
        return False


class SaveAgent(Delegate):

    """Saving subtitle files."""

    # pylint: disable-msg=E0203,W0201

    def _write_file(self, file, texts):
        """Write subtitle file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        positions = self.get_positions(file.mode)
        shows = list(positions[i][SHOW] for i in range(len(positions)))
        hides = list(positions[i][HIDE] for i in range(len(positions)))

        file_existed = os.path.isfile(file.path)
        if file_existed:
            bak_path = tempfile.mkstemp(suffix=".bak", prefix="gaupol.")[1]
            bak_success = _create_backup(file.path, bak_path)
        try:
            write_success = False
            file.write(shows, hides, texts)
            write_success = True
        finally:
            if write_success:
                if file_existed and bak_success:
                    _remove_backup(bak_path)
            elif not file_existed:
                _remove_failed(file.path)
            elif bak_success:
                _restore_original(file.path, bak_path)

    def save(self, doc, props=None, keep_changes=True):
        """Save subtitle file.

        props should be a sequence of path, format, encoding, newline.
        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        file = self.get_file(doc)
        path, format, encoding, newline = props or [None] * 4

        # Convert tags if saving in different format.
        updated_rows = []
        texts = self.get_texts(doc)[:]
        if file is not None and format is not None:
            if file.format != format:
                converter = TagConverter(file.format, format)
                for i, text in enumerate(texts):
                    new = converter.convert(text)
                    if new != text:
                        texts[i] = new
                        updated_rows.append(i)

        # Create file if needed.
        if not None in (path, format, encoding, newline):
            new_file = eval(format.class_name)(path, encoding, newline)
            if file is not None and file.format == format:
                # Copy header and mode to new file.
                new_file.header = file.header
                if format == cons.FORMAT.MPSUB:
                    new_file.mode = file.mode
            file = new_file

        self._write_file(file, texts)

        if keep_changes:
            if doc == cons.DOCUMENT.MAIN:
                self.main_file = file
                self.main_texts = texts
                self.main_changed = 0
                self.emit("main-texts-changed", updated_rows)
            elif doc == cons.DOCUMENT.TRAN:
                self.tran_file = file
                self.tran_texts = texts
                self.tran_changed = 0
                self.tran_active = True
                self.emit("translation-texts-changed", updated_rows)

        signal = ("main-file-saved", "translation-file-saved")[doc]
        self.emit(signal, file)
