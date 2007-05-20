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


"""Changing the appearance of texts."""


import re

from gaupol import util
from gaupol.base import Contractual, Delegate
from gaupol.i18n import _
from gaupol.reversion import revertable


class FormatAgent(Delegate):

    """Changing the appearance of texts."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = Contractual
    _re_alphanum = re.compile(r"\w", re.UNICODE)

    @util.asserted_return
    def _change_case_first(self, parser, method):
        """Change the case of the alphanumeric substring."""

        match = self._re_alphanum.search(parser.text)
        assert match is not None
        a = match.start()
        prefix = parser.text[:a]
        text = getattr(parser.text[a:], method)()
        parser.text = prefix + text

    def _should_dialoguize(self, indexes, doc):
        """Return True if dialogue lines should be added to texts."""

        re_tag = self.get_tag_regex(doc)
        for index in indexes:
            text = self.subtitles[index].get_text(doc)
            for line in text.split("\n"):
                # Strip all tags from line.
                # If leftover doesn't start with "-",
                # dialogue lines should be added.
                if re_tag is not None:
                    line = re_tag.sub("", line)
                if not line.startswith("-"):
                    return True
        return False

    def _should_italicize(self, indexes, doc):
        """Return True if texts should be italicized."""

        re_tag = self.get_tag_regex(doc)
        taglib = self.get_tag_library(doc)
        re_italic_tag = taglib.italic_tag
        for index in indexes:
            text = self.subtitles[index].get_text(doc)
            # Remove tags from the start of the text,
            # ending after all tags are removed
            # or when an italic tag is found.
            if re_tag is not None:
                while re_tag.match(text) is not None:
                    if re_italic_tag.match(text) is not None:
                        break
                    text = re_tag.sub("", text, 1)
            # If there is no italic tag at the start of the text,
            # all texts should be italicized.
            if re_italic_tag.match(text) is None:
                return True
        return False

    def change_case_require(self, indexes, doc, method, register=-1):
        for index in indexes:
            assert 0 <= index < len(self.subtitles)
        assert method in ("title", "capitalize", "upper", "lower")

    @revertable
    def change_case(self, indexes, doc, method, register=-1):
        """Change the case of texts with method.

        method should be 'title', 'capitalize', 'upper' or 'lower'.
        """
        new_texts = []
        parser = self.get_parser(doc)
        for index in indexes:
            subtitle = self.subtitles[index]
            parser.set_text(subtitle.get_text(doc))
            self._change_case_first(parser, method)
            new_texts.append(parser.get_text())

        self.replace_texts(indexes, doc, new_texts, register=register)
        self.set_action_description(register, _("Changing case"))

    def toggle_dialogue_lines_require(self, indexes, doc, register=-1):
        for index in indexes:
            assert 0 <= index < len(self.subtitles)

    @revertable
    def toggle_dialogue_lines(self, indexes, doc, register=-1):
        """Show or hide dialogue lines on texts."""

        new_texts = []
        parser = self.get_parser(doc)
        dialoguize = self._should_dialoguize(indexes, doc)
        for index in indexes:
            subtitle = self.subtitles[index]
            parser.set_text(subtitle.get_text(doc))
            parser.set_regex(r"^-\s*")
            parser.replacement = ""
            parser.replace_all()
            if dialoguize:
                parser.set_regex(r"^")
                parser.replacement = r"- "
                parser.replace_all()
            new_texts.append(parser.get_text())

        self.replace_texts(indexes, doc, new_texts, register=register)
        self.set_action_description(register, _("Toggling dialogue lines"))

    def toggle_italicization_require(self, indexes, doc, register=-1):
        for index in indexes:
            assert 0 <= index < len(self.subtitles)

    @revertable
    def toggle_italicization(self, indexes, doc, register=-1):
        """Italicize or normalize texts."""

        new_texts = []
        taglib = self.get_tag_library(doc)
        re_italic_tag = taglib.italic_tag
        italicize = self._should_italicize(indexes, doc)
        for index in indexes:
            text = self.subtitles[index].get_text(doc)
            text = re_italic_tag.sub("", text)
            if italicize:
                text = taglib.italicize(text)
            new_texts.append(text)

        self.replace_texts(indexes, doc, new_texts, register=register)
        self.set_action_description(register, _("Toggling italicization"))
