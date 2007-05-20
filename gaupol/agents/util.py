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


"""Miscellaneous methods for use with subtitle data editing."""


from gaupol import const, files, tags, util
from gaupol.base import Contractual, Delegate
from gaupol.parser import Parser
from gaupol.reversion import RevertableAction
from gaupol.subtitle import Subtitle


class UtilityAgent(Delegate):

    """Miscellaneous methods for subtitle data editing."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = Contractual

    def _get_format_class_name(self, doc):
        """Get the class name of document's file format or None."""

        if doc == const.DOCUMENT.MAIN:
            if self.main_file is not None:
                return self.main_file.format.class_name
            return None
        if doc == const.DOCUMENT.TRAN:
            if self.tran_file is not None:
                return self.tran_file.format.class_name
            return self.get_format_class_name(const.DOCUMENT.MAIN)
        raise ValueError

    def get_changed(self, doc):
        """Get the changed value corresponding to document."""

        if doc == const.DOCUMENT.MAIN:
            return self.main_changed
        if doc == const.DOCUMENT.TRAN:
            return self.tran_changed
        raise ValueError

    def get_file(self, doc):
        """Get the file corresponding to document."""

        if doc == const.DOCUMENT.MAIN:
            return self.main_file
        if doc == const.DOCUMENT.TRAN:
            return self.tran_file
        raise ValueError

    @util.asserted_return
    def get_file_class(self, doc):
        """Get document's file class or None."""

        class_name = self._get_format_class_name(doc)
        assert class_name is not None
        return getattr(files, class_name)

    def get_line_lengths_require(self, index, doc):
        assert 0 <= index < len(self.subtitles)

    def get_line_lengths(self, index, doc):
        """Get a list of line lengths in text without tags."""

        text = self.subtitles[index].get_text(doc)
        re_tag = self.get_tag_regex(doc)
        if re_tag is not None:
            text = re_tag.sub("", text)
        return [len(x) for x in text.split("\n")]

    def get_mode(self):
        """Get the mode of the main file or default."""

        if self.main_file is not None:
            return self.main_file.mode
        return const.MODE.TIME

    def get_parser(self, doc):
        """Get parser with proper properties."""

        return Parser(self.get_tag_regex(doc))

    def get_revertable_action(self, register):
        """Get a new revertable action with proper properties."""

        action = RevertableAction()
        action.register = register
        return action

    def get_subtitle(self):
        """Get a new subtitle with proper properties."""

        subtitle = Subtitle()
        subtitle.mode = self.get_mode()
        subtitle.framerate = self.framerate
        return subtitle

    @util.asserted_return
    def get_tag_library(self, doc):
        """Get document's tag library instance or None."""

        class_name = self._get_format_class_name(doc)
        assert class_name is not None
        return getattr(tags, class_name)()

    @util.asserted_return
    def get_tag_regex(self, doc):
        """Get the regular expression for a tag in document or None."""

        class_name = self._get_format_class_name(doc)
        assert class_name is not None
        return getattr(tags, class_name)().tag

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

        if doc == const.DOCUMENT.MAIN:
            return "main-texts-changed"
        if doc == const.DOCUMENT.TRAN:
            return "translation-texts-changed"
        raise ValueError
