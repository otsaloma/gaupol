# Copyright (C) 2005-2008 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Saving subtitle files."""

import gaupol
import os
import shutil
import sys


class SaveAgent(gaupol.Delegate):

    """Saving subtitle files."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = gaupol.Contractual

    def _convert_tags(self, subtitles, doc, from_format, to_format):
        """Convert tags in texts and return changed indices."""

        changed_indices = []
        converter = gaupol.MarkupConverter(from_format, to_format)
        for i, subtitle in enumerate(subtitles):
            text = subtitle.get_text(doc)
            new_text = converter.convert(text)
            if new_text != text:
                subtitle.set_text(doc, new_text)
                changed_indices.append(i)
        return changed_indices

    def _copy_file_ensure(self, value, source, destination):
        assert (not value) or os.path.isfile(destination)

    def _copy_file(self, source, destination):
        """Copy source file to destination and return success."""

        try:
            shutil.copyfile(source, destination)
            return True
        except IOError:
            gaupol.util.print_write_io(sys.exc_info(), destination)
        return False

    def _move_file_ensure(self, value, source, destination):
        assert (not value) or os.path.isfile(destination)

    def _move_file(self, source, destination):
        """Move source file to destination and return success."""

        try:
            shutil.move(source, destination)
            return True
        except (IOError, OSError):
            gaupol.util.print_write_io(sys.exc_info(), destination)
        return False

    def _remove_file_ensure(self, value, path):
        assert (not value) or (not os.path.isfile(path))

    def _remove_file(self, path):
        """Remove file and return success."""

        try:
            os.remove(path)
            return True
        except OSError:
            gaupol.util.print_remove_os(sys.exc_info(), path)
        return False

    def _save(self, doc, props, keep_changes):
        """Save subtitle file.

        props should be a sequence of path, format, encoding, newline.
        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        Return file, changed indices.
        """
        file = self.get_file(doc)
        path, format, encoding, newline = props or ([None] * 4)
        orig_texts = [x.get_text(doc) for x in self.subtitles]
        changed_indices = []
        if (not None in (file, format)) and (file.format != format):
            args = (self.subtitles, doc, file.format, format)
            changed_indices = self._convert_tags(*args)
        if not None in (path, format, encoding, newline):
            new_file = gaupol.files.new(format, path, encoding, newline)
            if (file is not None):
                new_file.copy_from(file)
            file = new_file
        self._write_file(file, self.subtitles, doc)
        if not keep_changes:
            for i in changed_indices:
                self.subtitles[i].set_text(doc, orig_texts[i])
            changed_indices = []
        return file, changed_indices

    def _update_mode(self, new_main_file):
        """Update the mode of subtitles if main file's format has changed.

        props should be a sequence of path, format, encoding, newline.
        """
        if self.main_file is None: return
        if new_main_file.mode == self.main_file.mode: return
        for i, subtitle in enumerate(self.subtitles):
            subtitle.mode = new_main_file.mode
        self.emit("positions-changed", range(len(self.subtitles)))

    def _write_file_ensure(self, value, file, subtitles, doc):
        assert os.path.isfile(file.path)

    def _write_file(self, file, subtitles, doc):
        """Write subtitle file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        file_existed = os.path.isfile(file.path)
        if os.path.isfile(file.path):
            backup_path = gaupol.temp.create(".bak")
            gaupol.temp.close(backup_path)
            backup_success = self._copy_file(file.path, backup_path)
        try:
            file.write(subtitles, doc)
        except (IOError, UnicodeError):
            if file_existed and backup_success:
                self._move_file(backup_path, file.path)
            elif (not file_existed):
                self._remove_file(file.path)
            raise
        if file_existed and backup_success:
            self._remove_file(backup_path)

    def save(self, doc, props, keep_changes=True):
        """Save document's subtitle file.

        props should be a sequence of path, format, encoding, newline.
        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        if doc == gaupol.documents.MAIN:
            return self.save_main(props, keep_changes)
        if doc == gaupol.documents.TRAN:
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
        args = (gaupol.documents.MAIN, props, keep_changes)
        main_file, changed_indices = self._save(*args)
        if keep_changes:
            self._update_mode(main_file)
            self.main_file = main_file
            self.main_changed = 0
            self.emit("main-texts-changed", changed_indices)
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
        args = (gaupol.documents.TRAN, props, keep_changes)
        tran_file, changed_indices = self._save(*args)
        if keep_changes:
            self.tran_file = tran_file
            self.tran_changed = 0
            self.emit("translation-texts-changed", changed_indices)
        self.emit("translation-file-saved", self.tran_file)
