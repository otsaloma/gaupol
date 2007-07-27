# Copyright (C) 2005-2007 Osmo Salomaa
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

"""Saving subtitle files."""

import gaupol
import os
import shutil
import sys
import tempfile


class SaveAgent(gaupol.Delegate):

    """Saving subtitle files."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = gaupol.Contractual

    def _convert_tags(self, texts, from_format, to_format):
        """Convert tags in texts and return changed indexes."""

        changed_indexes = []
        converter = gaupol.TagConverter(from_format, to_format)
        for i, text in enumerate(texts):
            new_text = converter.convert(text)
            if new_text != text:
                texts[i] = new_text
                changed_indexes.append(i)
        return changed_indexes

    def _copy_file_ensure(self, value, source, destination):
        assert (not value) or os.path.isfile(destination)

    def _copy_file(self, source, destination):
        """Copy source file to destination and return success."""

        try:
            shutil.copyfile(source, destination)
            return True
        except IOError:
            gaupol.util.handle_write_io(sys.exc_info(), destination)
        return False

    def _move_file_ensure(self, value, source, destination):
        assert (not value) or os.path.isfile(destination)

    def _move_file(self, source, destination):
        """Move source file to destination and return success."""

        try:
            shutil.move(source, destination)
            return True
        except (IOError, OSError):
            gaupol.util.handle_write_io(sys.exc_info(), destination)
        return False

    def _remove_file_ensure(self, value, path):
        assert (not value) or (not os.path.isfile(path))

    def _remove_file(self, path):
        """Remove file and return success."""

        try:
            os.remove(path)
            return True
        except OSError:
            gaupol.util.handle_remove_os(sys.exc_info(), path)
        return False

    def _save(self, doc, props, keep_changes):
        """Save subtitle file.

        props should be a sequence of path, format, encoding, newline.
        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        Return file, texts, changed indexes.
        """
        file = self.get_file(doc)
        path, format, encoding, newline = props or ([None] * 4)
        texts = [x.get_text(doc) for x in self.subtitles]

        changed_indexes = []
        # Convert tags if saving in different format.
        if (not None in (file, format)) and (file.format != format):
            args = (texts, file.format, format)
            changed_indexes = self._convert_tags(*args)

        # Create new file if needed.
        if not None in (path, format, encoding, newline):
            cls = gaupol.files.get_class(format)
            new_file = cls(path, encoding, newline)
            if (file is not None) and (file.format == format):
                new_file.copy_from(file)
            file = new_file

        self._write_file(file, texts)
        return file, texts, changed_indexes

    def _write_file_ensure(self, value, file, texts):
        assert os.path.isfile(file.path)

    def _write_file(self, file, texts):
        """Write subtitle file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        starts = [x.get_start(file.mode) for x in self.subtitles]
        ends = [x.get_end(file.mode) for x in self.subtitles]
        file_existed = os.path.isfile(file.path)
        if file_existed:
            backup_path = tempfile.mkstemp(".bak", "gaupol.")[1]
            backup_success = self._copy_file(file.path, backup_path)
        try:
            write_success = False
            file.write(starts, ends, texts)
            write_success = True
        finally:
            if write_success and file_existed and backup_success:
                self._remove_file(backup_path)
            elif (not write_success) and (not file_existed):
                self._remove_file(file.path)
            elif (not write_success) and file_existed and backup_success:
                self._move_file(backup_path, file.path)

    @gaupol.util.asserted_return
    def _update_mode(self, props, keep_changes, new_main_file):
        """Update the mode of subtitles if main file's format has changed.

        props should be a sequence of path, format, encoding, newline.
        """
        assert keep_changes
        assert props is not None
        assert len(props) >= 2
        format = props[1]
        assert format is not None
        assert format != self.main_file.format
        for i, subtitle in enumerate(self.subtitles):
            subtitle.mode = new_main_file.mode
        self.emit("positions-changed", range(len(self.subtitles)))

    def save(self, doc, props, keep_changes=True):
        """Save document's subtitle file.

        props should be a sequence of path, format, encoding, newline.
        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        if doc == gaupol.DOCUMENT.MAIN:
            return self.save_main(props, keep_changes)
        if doc == gaupol.DOCUMENT.TRAN:
            return self.save_translation(props, keep_changes)
        raise ValueError

    def save_main_ensure(self, value, props=None, keep_changes=True):
        assert self.main_file is not None
        assert (not keep_changes) or (self.main_changed == 0)

    def save_main(self, props, keep_changes=True):
        """Save the main subtitle file.

        props should be a sequence of path, format, encoding, newline.
        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        args = (gaupol.DOCUMENT.MAIN, props, keep_changes)
        main_file, texts, changed_indexes = self._save(*args)
        self._update_mode(props, keep_changes, main_file)
        if keep_changes:
            self.main_file = main_file
            for i, text in enumerate(texts):
                self.subtitles[i].main_text = text
            self.main_changed = 0
            self.emit("main-texts-changed", changed_indexes)
        self.emit("main-file-saved", self.main_file)

    def save_translation_ensure(self, value, props=None, keep_changes=True):
        assert self.tran_file is not None
        assert (not keep_changes) or (self.tran_changed == 0)

    def save_translation(self, props, keep_changes=True):
        """Save the translation subtitle file.

        props should be a sequence of path, format, encoding, newline.
        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        args = (gaupol.DOCUMENT.TRAN, props, keep_changes)
        tran_file, texts, changed_indexes = self._save(*args)
        if keep_changes:
            self.tran_file = tran_file
            for i, text in enumerate(texts):
                self.subtitles[i].tran_text = text
            self.tran_changed = 0
            self.emit("translation-texts-changed", changed_indexes)
        self.emit("translation-file-saved", self.tran_file)
