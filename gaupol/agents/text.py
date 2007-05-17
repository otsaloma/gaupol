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


"""Automatic correcting of texts."""


import re

from gaupol import util
from gaupol.base import Contractual, Delegate
from gaupol.i18n import _
from gaupol.liner import Liner
from gaupol.reversion import revertable


class TextAgent(Delegate):

    """Automatic correcting of texts."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = Contractual
    _re_alphanum = re.compile(r"\w", re.UNICODE)

    def _capitalize_after(self, parser, cap_next):
        """Capitalize all texts following matches of pattern."""

        try:
            z = parser.next()[1]
        except StopIteration:
            return cap_next
        match = self._re_alphanum.search(parser.text[z:])
        if match is not None:
            z = z + match.start()
            prefix = parser.text[:z]
            text = parser.text[z:].capitalize()
            parser.text = prefix + text
            return self._capitalize_after(parser, cap_next)
        return True

    def _capitalize_next(self, parser, cap_next):
        """Capitalize the next alphanumeric character."""

        match = self._re_alphanum.search(parser.text)
        if match is not None:
            a = match.start()
            prefix = parser.text[:a]
            text = parser.text[a:].capitalize()
            parser.text = prefix + text
            cap_next = False
        return cap_next

    def capitalize_require(self, indexes, doc, pattern, register=-1):
        for index in (indexes or []):
            assert 0 <= index < len(self.subtitles)

    @revertable
    def capitalize(self, indexes, doc, pattern, register=-1):
        """Capitalize texts following matches of pattern.

        indexes can be None to process all subtitles.
        Raise re.error if bad pattern.
        Return changed indexes.
        """
        new_indexes = []
        new_texts = []
        parser = self.get_parser(doc)
        parser.set_regex(pattern)
        indexes = indexes or range(len(self.subtitles))
        for indexes in util.get_ranges(indexes):
            cap_next = False
            for index in indexes:
                orig_text = self.subtitles[index].get_text(doc)
                parser.set_text(orig_text)
                if cap_next or (index == 0):
                    cap_next = self._capitalize_next(parser, cap_next)
                cap_next = self._capitalize_after(parser, cap_next)
                text = parser.get_text()
                if text != orig_text:
                    new_indexes.append(index)
                    new_texts.append(text)

        if new_indexes:
            self.replace_texts(new_indexes, doc, new_texts, register=register)
            self.set_action_description(register, _("Capitalizing texts"))
        return new_indexes

    def format_lines_require(self, indexes, *args, **kwargs):
        for index in (indexes or []):
            assert 0 <= index < len(self.subtitles)

    @revertable
    def format_lines(self, indexes, doc, dialogue_pattern, clause_pattern,
        ok_dialogue, ok_clauses, max_length, length_func, legal_length=None,
        legal_lines=None, require_reduction=False, register=-1):
        """Split or merge lines based on line length and count rules.

        ok_dialogue is an acceptable line count if all lines are dialogue,
        ok_clauses similarly for lines that are clauses. These are used for to
        prefer elegance over compactness. Subtitles that do not violate
        legal_length and legal_lines are skipped entirely to preserve an
        assumed existing elegant line split. require_reduction should be True
        to make changes in case of line count violations only when the line
        count can be reduced.

        indexes can be None to process all subtitles.
        Raise re.error if bad pattern.
        Return changed indexes.
        """
        def reduction_ok(check_reduction, text, lines):
            if check_reduction and require_reduction:
                return len(text.split("\n")) < len(lines)
            return True

        new_indexes = []
        new_texts = []
        liner = Liner(self.get_tag_regex(doc))
        liner.re_dialogue = re.compile(dialogue_pattern, re.UNICODE)
        liner.re_clause = re.compile(clause_pattern, re.UNICODE)
        liner.ok_dialogue = ok_dialogue
        liner.ok_clauses = ok_clauses
        liner.max_length = max_length
        liner.set_length_func(length_func)
        indexes = indexes or range(len(self.subtitles))
        for index in indexes:
            orig_text = self.subtitles[index].get_text(doc)
            lines = orig_text.split("\n")
            format = not any((legal_length, legal_lines))
            check_reduction = False
            if (not format) and (legal_length is not None):
                lengths = [length_func(x) for x in lines]
                format = any([x > legal_length for x in lengths])
            if (not format) and (legal_lines is not None):
                format = len(lines) > legal_lines
                check_reduction = True
            if format:
                liner.set_text(orig_text)
                text = liner.format()
                if reduction_ok(check_reduction, text, lines):
                    if text != orig_text:
                        new_indexes.append(index)
                        new_texts.append(text)

        if new_indexes:
            self.replace_texts(new_indexes, doc, new_texts, register=register)
            self.set_action_description(register, _("Formatting lines"))
        return new_indexes
