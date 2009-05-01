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

"""Miscellaneous methods for use with subtitle data editing."""

import gaupol


class UtilityAgent(gaupol.Delegate):

    """Miscellaneous methods for subtitle data editing."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = gaupol.Contractual

    def _get_format(self, doc):
        """Return the format of document's file or None."""

        if doc == gaupol.documents.MAIN:
            if self.main_file is not None:
                return self.main_file.format
            return None
        if doc == gaupol.documents.TRAN:
            if self.tran_file is not None:
                return self.tran_file.format
            return self._get_format(gaupol.documents.MAIN)
        raise ValueError("Invalid document: %s" % repr(doc))

    def get_changed(self, doc):
        """Return the changed value corresponding to document."""

        if doc == gaupol.documents.MAIN:
            return self.main_changed
        if doc == gaupol.documents.TRAN:
            return self.tran_changed
        raise ValueError("Invalid document: %s" % repr(doc))

    def get_file(self, doc):
        """Return the file corresponding to document."""

        if doc == gaupol.documents.MAIN:
            return self.main_file
        if doc == gaupol.documents.TRAN:
            return self.tran_file
        raise ValueError("Invalid document: %s" % repr(doc))

    def get_liner(self, doc):
        """Return liner with proper properties."""

        re_tag = self.get_markup_tag_regex(doc)
        clean_func = self.get_markup_clean_func(doc)
        return gaupol.Liner(re_tag, clean_func)

    def get_markup(self, doc):
        """Return document's markup instance or None."""

        format = self._get_format(doc)
        if format is None: return None
        return gaupol.tags.new(format)

    def get_markup_clean_func(self, doc):
        """Return the function to clean markup or None."""

        format = self._get_format(doc)
        if format is None: return None
        return gaupol.tags.new(format).clean

    def get_markup_tag_regex(self, doc):
        """Return the regular expression for a markup tag or None."""

        format = self._get_format(doc)
        if format is None: return None
        return gaupol.tags.new(format).tag

    def get_mode(self):
        """Return the mode of the main file or default."""

        if self.main_file is not None:
            return self.main_file.mode
        return gaupol.modes.TIME

    def get_parser(self, doc):
        """Return parser with proper properties."""

        re_tag = self.get_markup_tag_regex(doc)
        clean_func = self.get_markup_clean_func(doc)
        return gaupol.Parser(re_tag, clean_func)

    def get_revertable_action(self, register):
        """Return a new revertable action with proper properties."""

        action = gaupol.RevertableAction()
        action.register = register
        return action

    def get_subtitle(self):
        """Return a new subtitle with proper properties."""

        return gaupol.Subtitle(self.get_mode(), self.framerate)

    def get_text_length_require(self, index, doc):
        assert 0 <= index < len(self.subtitles)

    def get_text_length(self, index, doc):
        """Return the amount of characters in text excluding markup."""

        text = self.subtitles[index].get_text(doc)
        re_tag = self.get_markup_tag_regex(doc)
        if re_tag is not None:
            text = re_tag.sub("", text)
        return len(text)

    def get_text_signal(self, doc):
        """Return the 'texts-changed' signal corresponding to document."""

        if doc == gaupol.documents.MAIN:
            return "main-texts-changed"
        if doc == gaupol.documents.TRAN:
            return "translation-texts-changed"
        raise ValueError("Invalid document: %s" % repr(doc))
