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


"""Formatting text."""


import re
from gettext import gettext as _

from gaupol.base import Delegate
from gaupol.parser import Parser
from gaupol.tags import *
from .register import revertable


class FormatAgent(Delegate):

    """Formatting text."""

    # pylint: disable-msg=E0203,W0201

    @revertable
    def change_case(self, rows, doc, method, register=-1):
        """Change the case of text.

        method should be 'title', 'capitalize', 'upper' or 'lower'.
        """
        new_texts = []
        parser = Parser(self.get_tag_regex(doc))
        texts = self.get_texts(doc)
        for row in rows:
            parser.set_text(texts[row])
            parser.text = getattr(parser.text, method)()
            new_texts.append(parser.get_text())

        self.replace_texts(rows, doc, new_texts, register=register)
        self.set_action_description(register, _("Changing case"))

    @revertable
    def toggle_dialogue_lines(self, rows, doc, register=-1):
        """Toggle dialogue lines on text."""

        re_tag = self.get_tag_regex(doc)
        parser = Parser(re_tag)
        texts = self.get_texts(doc)
        dialoguize = False
        for row in rows:
            for line in texts[row].split("\n"):
                # Strip all tags from line.
                # If leftover doesn't start with "-",
                # dialogue lines should be added.
                if re_tag is not None:
                    line = re_tag.sub("", line)
                if not line.startswith("-"):
                    dialoguize = True
                    break

        new_texts = []
        for row in rows:
            parser.set_text(texts[row])
            parser.set_regex(r"^-\s*")
            parser.replacement = ""
            parser.replace_all()
            if dialoguize:
                parser.set_regex(r"^")
                parser.replacement = r"- "
                parser.replace_all()
            new_texts.append(parser.get_text())

        self.replace_texts(rows, doc, new_texts, register=register)
        self.set_action_description(register, _("Toggling dialogue lines"))

    @revertable
    def toggle_italicization(self, rows, doc, register=-1):
        """Toggle the italicization of text."""

        re_tag = self.get_tag_regex(doc)
        format = eval(self.get_format_class_name(doc))
        re_italic_tag = re.compile(*format.italic_tag)
        texts = self.get_texts(doc)
        italicize = False
        for row in rows:
            # Remove tags from the start of the text,
            # ending after all tags are removed
            # or when an italic tag is found.
            text = texts[row][:]
            if re_tag is not None:
                while re_tag.match(text) is not None:
                    if re_italic_tag.match(text) is not None:
                        break
                    text = re_tag.sub("", text, 1)
            # If there is no italic tag at the start of the text,
            # texts should be italicized.
            if re_italic_tag.match(text) is None:
                italicize = True
                break

        new_texts = []
        for row in rows:
            text = re_italic_tag.sub("", texts[row])
            if italicize:
                text = format.italicize(text)
            new_texts.append(text)

        self.replace_texts(rows, doc, new_texts, register=register)
        self.set_action_description(register, _("Toggling italicization"))
