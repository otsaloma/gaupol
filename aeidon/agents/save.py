# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Writing subtitle data to file."""

import aeidon


class SaveAgent(aeidon.Delegate):

    """Writing subtitle data to file."""

    def _save(self, doc, file, keep_changes):
        """
        Write subtitle data from `doc` to `file`.

        Return indices of texts changed due to markup conversion.
        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        current_format = self.get_format(doc)
        orig_texts = [x.get_text(doc) for x in self.subtitles]
        indices = []
        if current_format is not None and file.format != current_format:
            # Convert markup if saving in different format.
            converter = aeidon.MarkupConverter(current_format, file.format)
            for i, subtitle in enumerate(self.subtitles):
                text = subtitle.get_text(doc)
                new_text = converter.convert(text)
                if new_text == text: continue
                subtitle.set_text(doc, new_text)
                indices.append(i)
        file.write(self.subtitles, doc)
        if keep_changes: return indices
        for i, subtitle in enumerate(self.subtitles):
            subtitle.set_text(doc, orig_texts[i])
        return []

    @aeidon.deco.export
    def save(self, doc, file=None, keep_changes=True):
        """
        Write subtitle data from `doc` to `file`.

        `file` can be ``None`` to use existing file.
        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        if doc == aeidon.documents.MAIN:
            return self.save_main(file, keep_changes)
        if doc == aeidon.documents.TRAN:
            return self.save_translation(file, keep_changes)
        raise ValueError("Invalid document: {!r}".format(doc))

    @aeidon.deco.export
    def save_main(self, file=None, keep_changes=True):
        """
        Write subtitle data from main document to `file`.

        `file` can be ``None`` to use :attr:`main_file`.
        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        file = file or self.main_file
        if file is not None and self.main_file is not None:
            file.copy_from(self.main_file)
        indices = self._save(aeidon.documents.MAIN, file, keep_changes)
        if keep_changes:
            if (self.main_file is not None and
                file.mode != self.main_file.mode):
                # Apply possibly changed mode (times vs. frames).
                for i, subtitle in enumerate(self.subtitles):
                    subtitle.mode = file.mode
                self.emit("positions-changed", self.get_all_indices())
            self.main_file = file
            self.main_changed = 0
            self.emit("main-texts-changed", indices)
        self.emit("main-file-saved", file)

    @aeidon.deco.export
    def save_translation(self, file=None, keep_changes=True):
        """
        Write subtitle data from translation document to `file`.

        `file` can be ``None`` to use :attr:`tran_file`.
        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        file = file or self.tran_file
        if file is not None and self.tran_file is not None:
            file.copy_from(self.tran_file)
        indices = self._save(aeidon.documents.TRAN, file, keep_changes)
        if keep_changes:
            self.tran_file = file
            self.tran_changed = 0
            self.emit("translation-texts-changed", indices)
        self.emit("translation-file-saved", file)
