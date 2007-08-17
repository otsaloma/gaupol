# Copyright (C) 2007 Osmo Salomaa
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

"""Automatic correcting of texts."""

import gaupol
import re
_ = gaupol.i18n._


class TextAgent(gaupol.Delegate):

    """Automatic correcting of texts."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = gaupol.Contractual
    _re_alphanum = re.compile(r"\w", re.UNICODE)

#     def _capitalize_after(self, parser, cap_next):
#         """Capitalize all texts following matches of pattern."""

#         try:
#             z = parser.next()[1]
#         except StopIteration:
#             return cap_next
#         match = self._re_alphanum.search(parser.text[z:])
#         if match is not None:
#             z = z + match.start()
#             prefix = parser.text[:z]
#             text = parser.text[z:z + 1].capitalize()
#             suffix = parser.text[z + 1:]
#             parser.text = prefix + text + suffix
#             return self._capitalize_after(parser, cap_next)
#         return True

#     def _capitalize_next(self, parser, cap_next):
#         """Capitalize the next alphanumeric character."""

#         match = self._re_alphanum.search(parser.text)
#         if match is not None:
#             a = match.start()
#             prefix = parser.text[:a]
#             text = parser.text[a:a + 1].capitalize()
#             suffix = parser.text[a + 1:]
#             parser.text = prefix + text + suffix
#             cap_next = False
#         return cap_next

    def _get_subtitutions(self, patterns):
        """Get a list of tuples of pattern, flags, replacement."""

        re_patterns = []
        for pattern in (x for x in patterns if x.enabled):
            string = pattern.get_field("Pattern")
            flags = pattern.get_flags()
            replacement = pattern.get_field("Replacement")
            re_patterns.append((string, flags, replacement))
        return re_patterns

    def _remove_leftover_spaces(self, texts, parser):
        """Remove excess whitespace in texts."""

        def substitute(pattern, replacement):
            parser.set_regex(pattern)
            parser.replacement = replacement
            parser.replace_all()

        texts = texts[:]
        for i, text in enumerate(texts):
            parser.set_text(text)
            substitute(r"(^\s+|\s+$)", "")
            substitute(r" {2,}", " ")
            substitute(r"^\W*$", "")
            substitute(r"(^\n|\n$)", "")
            substitute(r"^-(\S)", r"- \1")
            substitute(r"^- (.*?^[^-])", r"\1")
            substitute(r"\A- ([^\n]*)\Z", r"\1")
            texts[i] = parser.get_text()
        return texts

#     def capitalize_require(self, indexes, doc, pattern, register=-1):
#         for index in (indexes or []):
#             assert 0 <= index < len(self.subtitles)

#     @gaupol.util.revertable
#     def capitalize(self, indexes, doc, pattern, register=-1):
#         """Capitalize texts following matches of pattern.

#         indexes can be None to process all subtitles.
#         Raise re.error if bad pattern.
#         Return changed indexes.
#         """
#         new_indexes = []
#         new_texts = []
#         parser = self.get_parser(doc)
#         parser.set_regex(pattern)
#         indexes = indexes or range(len(self.subtitles))
#         for indexes in gaupol.util.get_ranges(indexes):
#             cap_next = False
#             for index in indexes:
#                 orig_text = self.subtitles[index].get_text(doc)
#                 parser.set_text(orig_text)
#                 if cap_next or (index == 0):
#                     cap_next = self._capitalize_next(parser, cap_next)
#                 cap_next = self._capitalize_after(parser, cap_next)
#                 text = parser.get_text()
#                 if text != orig_text:
#                     new_indexes.append(index)
#                     new_texts.append(text)

#         if new_indexes:
#             self.replace_texts(new_indexes, doc, new_texts, register=register)
#             self.set_action_description(register, _("Capitalizing texts"))
#         return new_indexes

    def correct_common_errors_require(self, indexes, *args, **kwargs):
        for index in (indexes or []):
            assert 0 <= index < len(self.subtitles)

    @gaupol.util.revertable
    @gaupol.util.asserted_return
    def correct_common_errors(self, indexes, doc, patterns, register=-1):
        """Correct common human and OCR errors  in texts.

        indexes can be None to process all subtitles.
        Raise re.error if bad pattern or replacement.
        """
        new_indexes = []
        new_texts = []
        parser = self.get_parser(doc)
        re_patterns = self._get_subtitutions(patterns)
        repeats = [x.get_field_boolean("Repeat") for x in patterns]
        indexes = indexes or range(len(self.subtitles))
        for index in indexes:
            subtitle = self.subtitles[index]
            parser.set_text(subtitle.get_text(doc))
            for i, (string, flags, replacement) in enumerate(re_patterns):
                parser.set_regex(string, flags, 0)
                parser.replacement = replacement
                count = parser.replace_all()
                while repeats[i] and count:
                    count = parser.replace_all()
            text = parser.get_text()
            if text != subtitle.get_text(doc):
                new_indexes.append(index)
                new_texts.append(text)
        assert new_indexes
        self.replace_texts(new_indexes, doc, new_texts, register=register)
        description = _("Correcting common errors")
        self.set_action_description(register, description)

#     def format_lines_require(self, indexes, *args, **kwargs):
#         for index in (indexes or []):
#             assert 0 <= index < len(self.subtitles)

#     @gaupol.util.revertable
#     def format_lines(self, indexes, doc, dialogue_pattern, clause_pattern,
#         ok_dialogue, ok_clauses, max_length, length_func, legal_length=None,
#         legal_lines=None, require_reduction=False, register=-1):
#         """Split or merge lines based on line length and count rules.

#         ok_dialogue is an acceptable line count if all lines are dialogue,
#         ok_clauses similarly for lines that are clauses. These are used for to
#         prefer elegance over compactness. Subtitles that do not violate
#         legal_length and legal_lines are skipped entirely to preserve an
#         assumed existing elegant line split. require_reduction should be True
#         to make changes in case of line count violations only when the line
#         count can be reduced.

#         indexes can be None to process all subtitles.
#         Raise re.error if bad pattern.
#         Return changed indexes.
#         """
#         def reduction_ok(check_reduction, text, lines):
#             if check_reduction and require_reduction:
#                 return len(text.split("\n")) < len(lines)
#             return True

#         new_indexes = []
#         new_texts = []
#         liner = gaupol.Liner(self.get_tag_regex(doc))
#         liner.re_dialogue = re.compile(dialogue_pattern, re.UNICODE)
#         liner.re_clause = re.compile(clause_pattern, re.UNICODE)
#         liner.ok_dialogue = ok_dialogue
#         liner.ok_clauses = ok_clauses
#         liner.max_length = max_length
#         liner.set_length_func(length_func)
#         indexes = indexes or range(len(self.subtitles))
#         for index in indexes:
#             orig_text = self.subtitles[index].get_text(doc)
#             lines = orig_text.split("\n")
#             format = not any((legal_length, legal_lines))
#             check_reduction = False
#             if (not format) and (legal_length is not None):
#                 lengths = [length_func(x) for x in lines]
#                 format = any([x > legal_length for x in lengths])
#             if (not format) and (legal_lines is not None):
#                 format = len(lines) > legal_lines
#                 check_reduction = True
#             if format:
#                 liner.set_text(orig_text)
#                 text = liner.format()
#                 if reduction_ok(check_reduction, text, lines):
#                     if text != orig_text:
#                         new_indexes.append(index)
#                         new_texts.append(text)

#         if new_indexes:
#             self.replace_texts(new_indexes, doc, new_texts, register=register)
#             self.set_action_description(register, _("Formatting lines"))
#         return new_indexes

    def remove_hearing_impaired_require(self, indexes, *args, **kwargs):
        for index in (indexes or []):
            assert 0 <= index < len(self.subtitles)

    @gaupol.util.revertable
    @gaupol.util.asserted_return
    def remove_hearing_impaired(self, indexes, doc, patterns, register=-1):
        """Remove hearing impaired parts from subtitles.

        indexes can be None to process all subtitles.
        Raise re.error if bad pattern or replacement.
        """
        new_indexes = []
        new_texts = []
        parser = self.get_parser(doc)
        re_patterns = self._get_subtitutions(patterns)
        indexes = indexes or range(len(self.subtitles))
        for index in indexes:
            subtitle = self.subtitles[index]
            parser.set_text(subtitle.get_text(doc))
            for string, flags, replacement in re_patterns:
                parser.set_regex(string, flags, 0)
                parser.replacement = replacement
                parser.replace_all()
            text = parser.get_text()
            if text != subtitle.get_text(doc):
                new_indexes.append(index)
                new_texts.append(text)
        new_texts = self._remove_leftover_spaces(new_texts, parser)
        assert new_indexes
        self.replace_texts(new_indexes, doc, new_texts, register=register)
        description = _("Removing hearing impaired texts")
        self.set_action_description(register, description)
        remove_indexes = []
        for i, text in (x for x in enumerate(new_texts) if not x[1]):
            remove_indexes.append(new_indexes[i])
        assert remove_indexes
        self.remove_subtitles(remove_indexes, register=register)
        self.group_actions(register, 2, description)
