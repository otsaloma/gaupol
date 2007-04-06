# Copyright (C) 2007 Osmo Salomaa
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


"""Text corrections."""


import re

from gaupol import util
from gaupol.base import Delegate
from gaupol.i18n import _
from gaupol.liner import Liner
from gaupol.parser import Parser
from .register import revertable


class TextAgent(Delegate):

    """Text corrections."""

    # pylint: disable-msg=E0203,W0201

    @revertable
    def capitalize(self, rows, doc, pattern, register=-1):
        """Capitalize texts following match of pattern.

        rows can be None to process all rows.
        Raise re.error if pattern sucks.
        Return changed rows.
        """
        parser = Parser(self.get_tag_regex(doc))
        parser.set_regex(pattern)
        re_alphanum = re.compile(r"\w", re.UNICODE)

        new_rows = []
        new_texts = []
        rows = rows or range(len(self.times))
        texts = self.get_texts(doc)
        for rows in util.get_ranges(rows):
            cap_next = False
            for row in rows:
                parser.set_text(texts[row])
                if cap_next or row == 0:
                    match = re_alphanum.search(parser.text)
                    if match is not None:
                        a = match.start()
                        prefix = parser.text[:a]
                        text = parser.text[a:].capitalize()
                        parser.text = prefix + text
                    cap_next = False
                while True:
                    try:
                        z = parser.next()[1]
                    except StopIteration:
                        break
                    match = re_alphanum.search(parser.text[z:])
                    if match is not None:
                        z = z + match.start()
                        prefix = parser.text[:z]
                        text = parser.text[z:].capitalize()
                        parser.text = prefix + text
                        continue
                    cap_next = True
                    break
                text = parser.get_text()
                if text != texts[row]:
                    new_rows.append(row)
                    new_texts.append(text)

        if new_rows:
            self.replace_texts(new_rows, doc, new_texts, register=register)
            self.set_action_description(register, _("Capitalizing texts"))
        return new_rows

    @revertable
    def format_lines(self, rows, doc, dialogue_pattern, clause_pattern,
        ok_dialogue, ok_clauses, max_length, length_func, legal_length=None,
        legal_lines=None, require_reduction=False, register=-1):
        """Split or merge lines.

        rows can be None to process all rows.
        ok_* are line counts that are not attempted to be reduced.
        legal_length is the maximum line length of skipped subtitles.
        legal_lines is the maximum line count of skipped subtitles.
        require_reduction should be True to skip unreducible line counts.
        Raise re.error if pattern sucks.
        Return changed rows.
        """
        liner = Liner(self.get_tag_regex(doc))
        liner.re_dialogue = re.compile(dialogue_pattern, re.UNICODE)
        liner.re_clause = re.compile(clause_pattern, re.UNICODE)
        liner.ok_dialogue = ok_dialogue
        liner.ok_clauses = ok_clauses
        liner.max_length = max_length
        liner.set_length_function(length_func)

        new_rows = []
        new_texts = []
        rows = rows or range(len(self.times))
        texts = self.get_texts(doc)
        for row in rows:
            text = texts[row]
            lines = text.split("\n")
            if legal_length is None and legal_lines is None:
                liner.set_text(text)
                text = liner.format()
            elif legal_length is not None:
                if any([length_func(x) > legal_length for x in lines]):
                    liner.set_text(text)
                    text = liner.format()
                elif legal_lines is not None:
                    if len(lines) > legal_lines:
                        liner.set_text(text)
                        text = liner.format()
                        if require_reduction:
                            if not len(text.split("\n")) < len(lines):
                                continue
            elif legal_lines is not None:
                if len(lines) > legal_lines:
                    liner.set_text(text)
                    text = liner.format()
                    if require_reduction:
                        if not len(text.split("\n")) < len(lines):
                            continue
            if text != texts[row]:
                new_rows.append(row)
                new_texts.append(text)

        if new_rows:
            self.replace_texts(new_rows, doc, new_texts, register=register)
            self.set_action_description(register, _("Formatting lines"))
        return new_rows
