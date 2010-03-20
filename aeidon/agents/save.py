# Copyright (C) 2005-2009 Osmo Salomaa
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

"""Writing subtitle data to file."""

import aeidon
import os
import shutil
import sys


class SaveAgent(aeidon.Delegate):

    """Writing subtitle data to file."""

    # pylint: disable-msg=E0203,E1101,W0201

    __metaclass__ = aeidon.Contractual

    def _convert_markup(self, doc, from_format, to_format):
        """Convert markup in texts and return changed indices."""
        indices = []
        converter = aeidon.MarkupConverter(from_format, to_format)
        for i, subtitle in enumerate(self.subtitles):
            text = subtitle.get_text(doc)
            new_text = converter.convert(text)
            if new_text == text: continue
            subtitle.set_text(doc, new_text)
            indices.append(i)
        return indices

    def _copy_file_ensure(self, value, source, destination):
        assert (not value) or os.path.isfile(destination)

    def _copy_file(self, source, destination):
        """Copy source file to destination and return success."""
        try:
            shutil.copyfile(source, destination)
            return True
        except IOError:
            aeidon.util.print_write_io(sys.exc_info(), destination)
        return False

    def _ensure_mode(self, mode):
        """Update mode of subtitles if necessary."""
        if self.main_file is None: return
        if mode == self.main_file.mode: return
        for i, subtitle in enumerate(self.subtitles):
            subtitle.mode = mode
        self.emit("positions-changed", self.get_all_indices())

    def _move_file_ensure(self, value, source, destination):
        assert (not value) or os.path.isfile(destination)

    def _move_file(self, source, destination):
        """Move source file to destination and return success."""
        try:
            shutil.move(source, destination)
            return True
        except (IOError, OSError):
            aeidon.util.print_write_io(sys.exc_info(), destination)
        return False

    def _remove_file_ensure(self, value, path):
        assert (not value) or (not os.path.isfile(path))

    def _remove_file(self, path):
        """Remove file and return success."""
        try:
            os.remove(path)
            return True
        except OSError:
            aeidon.util.print_remove_os(sys.exc_info(), path)
        return False

    def _save(self, doc, sfile, keep_changes):
        """Write subtitle data from `doc` to `sfile`.

        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        Return indices of texts changed due to markup conversion.
        """
        current_file = self.get_file(doc)
        current_format = self.get_format(doc)
        orig_texts = [x.get_text(doc) for x in self.subtitles]
        indices = []
        if sfile.format != current_format:
            indices = self._convert_markup(doc, current_format, sfile.format)
        self._write_file(sfile, self.subtitles, doc)
        if keep_changes: return indices
        for i, subtitle in enumerate(self.subtitles):
            subtitle.set_text(doc, orig_texts[i])
        return []

    def _write_file_ensure(self, value, sfile, subtitles, doc):
        assert os.path.isfile(sfile.path)

    def _write_file(self, sfile, subtitles, doc):
        """Write subtitle data to `sfile`.

        Raise :exc.`IOError` if writing fails.
        Raise :exc.`UnicodeError` if encoding fails.
        """
        file_existed = os.path.isfile(sfile.path)
        if os.path.isfile(sfile.path):
            # Create a backup of existing file in case writing
            # new data to that file fails.
            backup_path = aeidon.temp.create(".bak")
            aeidon.temp.close(backup_path)
            backup_success = self._copy_file(sfile.path, backup_path)
        try: sfile.write(subtitles, doc)
        except (IOError, UnicodeError):
            if file_existed and backup_success:
                # If overwriting existing file fails,
                # restore old file from backup.
                self._move_file(backup_path, sfile.path)
            if not file_existed:
                # If writing new file fails, remove failed attempt,
                # which is a blank or an incomplete file.
                self._remove_file(sfile.path)
            raise # (IOError, UnicodeError)
        if file_existed and backup_success:
            aeidon.temp.remove(backup_path)

    @aeidon.deco.export
    def save(self, doc, sfile=None, keep_changes=True):
        """Write subtitle data from `doc` to `sfile`.

        `sfile` can be ``None`` to use existing file, i.e. :attr:`main_file`
        or :attr:`tran_file`.
        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        if doc == aeidon.documents.MAIN:
            return self.save_main(sfile, keep_changes)
        if doc == aeidon.documents.TRAN:
            return self.save_translation(sfile, keep_changes)
        raise ValueError("Invalid document: %s" % repr(doc))

    def save_main_ensure(self, value, sfile=None, keep_changes=True):
        assert self.main_file is not None
        assert (not keep_changes) or (self.main_changed == 0)

    @aeidon.deco.export
    def save_main(self, sfile=None, keep_changes=True):
        """Write subtitle data from main document to `sfile`.

        `sfile` can be ``None`` to use :attr:`main_file`.
        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        sfile = sfile or self.main_file
        indices = self._save(aeidon.documents.MAIN, sfile, keep_changes)
        if keep_changes:
            self._ensure_mode(sfile.mode)
            self.main_file = sfile
            self.main_changed = 0
            self.emit("main-texts-changed", indices)
        self.emit("main-file-saved", sfile)

    def save_translation_ensure(self, value, sfile=None, keep_changes=True):
        assert self.tran_file is not None
        assert (not keep_changes) or (self.tran_changed == 0)

    @aeidon.deco.export
    def save_translation(self, sfile=None, keep_changes=True):
        """Write subtitle data from translation document to `sfile`.

        `sfile` can be ``None`` to use :attr:`tran_file`.
        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        sfile = sfile or self.tran_file
        indices = self._save(aeidon.documents.TRAN, sfile, keep_changes)
        if keep_changes:
            self.tran_file = sfile
            self.tran_changed = 0
            self.emit("translation-texts-changed", indices)
        self.emit("translation-file-saved", sfile)
