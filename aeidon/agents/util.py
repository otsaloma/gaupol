# -*- coding: utf-8 -*-

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

"""Miscellaneous helper methods."""

import aeidon
import os


class UtilityAgent(aeidon.Delegate, metaclass=aeidon.Contractual):

    """Miscellaneous helper methods."""

    @aeidon.deco.export
    def get_all_indices(self):
        """Return a list of all indices of subtitles."""
        return list(range(len(self.subtitles)))

    @aeidon.deco.export
    def get_changed(self, doc):
        """Return the changed value corresponding to `doc`."""
        if doc == aeidon.documents.MAIN:
            return self.main_changed
        if doc == aeidon.documents.TRAN:
            return self.tran_changed
        raise ValueError("Invalid document: {}"
                         .format(repr(doc)))

    @aeidon.deco.export
    def get_file(self, doc):
        """Return the file corresponding to `doc`."""
        if doc == aeidon.documents.MAIN:
            return self.main_file
        if doc == aeidon.documents.TRAN:
            return self.tran_file
        raise ValueError("Invalid document: {}"
                         .format(repr(doc)))

    @aeidon.deco.export
    def get_format(self, doc):
        """
        Return format of the file corresponding to `doc`.

        For translation file that is ``None``, return format of main file.
        If main file is ``None``, return ``None``.
        """
        if doc == aeidon.documents.MAIN:
            if self.main_file is not None:
                return self.main_file.format
            return None
        if doc == aeidon.documents.TRAN:
            if self.tran_file is not None:
                return self.tran_file.format
            return self.get_format(aeidon.documents.MAIN)
        raise ValueError("Invalid document: {}"
                         .format(repr(doc)))

    @aeidon.deco.export
    def get_liner(self, doc):
        """Return a new :class:`aeidon.Liner` instance."""
        re_tag = self.get_markup_tag_regex(doc)
        clean_func = self.get_markup_clean_func(doc)
        return aeidon.Liner(re_tag, clean_func)

    @aeidon.deco.export
    def get_markup(self, doc):
        """Return `doc`'s markup instance or ``None``."""
        format = self.get_format(doc)
        if format is None: return None
        return aeidon.tags.new(format)

    @aeidon.deco.export
    def get_markup_clean_func(self, doc):
        """Return the function to clean markup or ``None``."""
        format = self.get_format(doc)
        if format is None: return None
        return aeidon.tags.new(format).clean

    @aeidon.deco.export
    def get_markup_tag_regex(self, doc):
        """Return the regular expression for a markup tag or ``None``."""
        format = self.get_format(doc)
        if format is None: return None
        return aeidon.tags.new(format).tag

    @aeidon.deco.export
    def get_mode(self):
        """Return mode of the main file or default."""
        if self.main_file is not None:
            return self.main_file.mode
        return aeidon.modes.TIME

    @aeidon.deco.export
    def get_parser(self, doc):
        """Return a new :class:`aeidon.Parser` instance."""
        re_tag = self.get_markup_tag_regex(doc)
        clean_func = self.get_markup_clean_func(doc)
        return aeidon.Parser(re_tag, clean_func)

    def get_text_length_require(self, index, doc):
        assert 0 <= index < len(self.subtitles)

    @aeidon.deco.export
    def get_text_length(self, index, doc):
        """Return the amount of characters in text excluding markup."""
        text = self.subtitles[index].get_text(doc)
        re_tag = self.get_markup_tag_regex(doc)
        if re_tag is not None:
            text = re_tag.sub("", text)
        return len(text)

    @aeidon.deco.export
    def get_text_signal(self, doc):
        """Return the ``texts-changed`` signal corresponding to `doc`."""
        if doc == aeidon.documents.MAIN:
            return "main-texts-changed"
        if doc == aeidon.documents.TRAN:
            return "translation-texts-changed"
        raise ValueError("Invalid document: {}"
                         .format(repr(doc)))

    @aeidon.deco.export
    def new_revertable_action(self, register):
        """Return a new :class:`aeidon.RevertableAction` instance."""
        action = aeidon.RevertableAction()
        action.register = register
        return action

    @aeidon.deco.export
    def new_subtitle(self):
        """Return a new :class:`aeidon.Subtitle` instance."""
        return aeidon.Subtitle(self.get_mode(), self.framerate)

    def new_temp_file_require(self, doc, encoding=None):
        assert self.get_file(doc) is not None
        if encoding is not None:
            assert aeidon.encodings.is_valid_code(encoding)

    def new_temp_file_ensure(self, value, doc, encoding=None):
        assert os.path.isfile(value)

    @aeidon.deco.export
    def new_temp_file(self, doc, encoding=None):
        """
        Return path to a new temporary file with subtitles from `doc`.

        Raise :exc:`IOError` if writing to temporary file fails.
        Raise :exc:`UnicodeError` if encoding temporary file fails.
        """
        file = self.get_file(doc)
        if file is None and doc == aeidon.documents.TRAN:
            # For an unsaved translation document,
            # fall back to main document's properties.
            file = self.get_file(aeidon.documents.MAIN)
        if file is not None:
            path = aeidon.temp.create(file.format.extension)
            encoding = encoding or file.encoding
            file = aeidon.files.new(file.format, path, encoding)
            file.copy_from(self.get_file(doc))
        else:
            # If no saved document to pull properties from,
            # fall back to SubRip format and UTF-8 encoding.
            path = aeidon.temp.create(aeidon.formats.SUBRIP.extension)
            encoding = encoding or "utf_8"
            file = aeidon.files.new(aeidon.formats.SUBRIP, path, encoding)
        self.save(doc, file, False)
        return file.path
