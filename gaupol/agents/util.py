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

"""Miscellaneous methods for use with subtitle data editing."""

import gaupol


class UtilityAgent(gaupol.Delegate):

    """Miscellaneous methods for subtitle data editing."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = gaupol.Contractual

    def _get_format(self, doc):
        """Get the format of document's file or None."""

        if doc == gaupol.DOCUMENT.MAIN:
            if self.main_file is not None:
                return self.main_file.format
            return None
        if doc == gaupol.DOCUMENT.TRAN:
            if self.tran_file is not None:
                return self.tran_file.format
            return self._get_format(gaupol.DOCUMENT.MAIN)
        raise ValueError

    def get_changed(self, doc):
        """Get the changed value corresponding to document."""

        if doc == gaupol.DOCUMENT.MAIN:
            return self.main_changed
        if doc == gaupol.DOCUMENT.TRAN:
            return self.tran_changed
        raise ValueError

    def get_file(self, doc):
        """Get the file corresponding to document."""

        if doc == gaupol.DOCUMENT.MAIN:
            return self.main_file
        if doc == gaupol.DOCUMENT.TRAN:
            return self.tran_file
        raise ValueError

    @gaupol.util.asserted_return
    def get_file_class(self, doc):
        """Get document's file class or None."""

        format = self._get_format(doc)
        assert format is not None
        return gaupol.files.get_class(format)

    def get_line_lengths_require(self, index, doc):
        assert 0 <= index < len(self.subtitles)

    def get_line_lengths(self, index, doc):
        """Get a list of line lengths in text without tags."""

        text = self.subtitles[index].get_text(doc)
        re_tag = self.get_tag_regex(doc)
        if re_tag is not None:
            text = re_tag.sub("", text)
        return [len(x) for x in text.split("\n")]

    def get_liner(self, doc):
        """Get liner with proper properties."""

        re_tag = self.get_tag_regex(doc)
        clean_func = self.get_tag_clean_func(doc)
        return gaupol.Liner(re_tag, clean_func)

    def get_mode(self):
        """Get the mode of the main file or default."""

        if self.main_file is not None:
            return self.main_file.mode
        return gaupol.MODE.TIME

    def get_parser(self, doc):
        """Get parser with proper properties."""

        re_tag = self.get_tag_regex(doc)
        clean_func = self.get_tag_clean_func(doc)
        return gaupol.Parser(re_tag, clean_func)

    def get_revertable_action(self, register):
        """Get a new revertable action with proper properties."""

        action = gaupol.RevertableAction()
        action.register = register
        return action

    def get_subtitle(self):
        """Get a new subtitle with proper properties."""

        subtitle = gaupol.Subtitle()
        subtitle.mode = self.get_mode()
        subtitle.framerate = self.framerate
        return subtitle

    @gaupol.util.asserted_return
    def get_tag_clean_func(self, doc):
        """Get the function to clean tags or None."""

        format = self._get_format(doc)
        assert format is not None
        return gaupol.tags.get_class(format)().clean

    @gaupol.util.asserted_return
    def get_tag_library(self, doc):
        """Get document's tag library instance or None."""

        format = self._get_format(doc)
        assert format is not None
        return gaupol.tags.get_class(format)()

    @gaupol.util.asserted_return
    def get_tag_regex(self, doc):
        """Get the regular expression for a tag in document or None."""

        format = self._get_format(doc)
        assert format is not None
        return gaupol.tags.get_class(format)().tag

    def get_text_length_require(self, index, doc):
        assert 0 <= index < len(self.subtitles)

    def get_text_length(self, index, doc):
        """Get the length of text without tags."""

        text = self.subtitles[index].get_text(doc)
        re_tag = self.get_tag_regex(doc)
        if re_tag is not None:
            text = re_tag.sub("", text)
        return len(text)

    def get_text_signal(self, doc):
        """Get the 'texts-changed' signal corresponding to document."""

        if doc == gaupol.DOCUMENT.MAIN:
            return "main-texts-changed"
        if doc == gaupol.DOCUMENT.TRAN:
            return "translation-texts-changed"
        raise ValueError
