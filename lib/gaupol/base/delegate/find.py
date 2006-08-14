# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Finding and replacing text."""


from gettext import gettext as _

from gaupol.base             import cons
from gaupol.base.icons       import *
from gaupol.base.delegate    import Delegate, revertablemethod
from gaupol.base.text.finder import Finder


class FindDelegate(Delegate):

    """
    Finding and replacing text.

    Instance variables:

        _docs:              List of target documents
        _finder:            Finder
        _last_match_doc:    Document of last match
        _last_match_passed: True if passed position of last match
        _last_match_row:    Row of last match
        _rows:              Target rows
        _wrap:              True to wrap search

    """

    def __init__(self, *args, **kwargs):

        Delegate.__init__(self, *args, **kwargs)

        self._docs              = [MAIN, TRAN]
        self._finder            = Finder()
        self._last_match_doc    = None
        self._last_match_passed = False
        self._last_match_row    = None
        self._rows              = None
        self._wrap              = True

    def _find(self, row, doc, pos, next):
        """
        Find pattern starting from position.

        pos: None for beginning or end
        next: True to find next, False to find previous
        Raise StopIteration if no matches exist.
        Return three-tuple: row, document, match span.
        """
        if next:
            find_in_document = self._next_in_document
        else:
            find_in_document = self._previous_in_document
        self._last_match_row = row
        self._last_match_doc = doc
        self._last_match_passed = False
        rows = self._rows or range(len(self.times))

        while True:
            try:
                return find_in_document(row, doc, pos)
            except ValueError:
                pass
            if not self._wrap:
                if next and doc == max(self._docs):
                    raise StopIteration
                if not next and doc == min(self._docs):
                    raise StopIteration
            if next:
                row = min(rows)
            else:
                row = max(rows)
            try:
                doc = self._get_other_document(doc)
            except ValueError:
                pass
            pos = None

    def _get_other_document(self, doc):
        """
        Get other document included in target.

        Raise ValueError if no other document.
        """
        for candidate in self._docs:
            if candidate != doc:
                return candidate
        raise ValueError

    def _next_in_document(self, row, doc, pos=None):
        """
        Find next pattern in document starting from position.

        pos: None to start from beginning
        Raise ValueError if no matches after position.
        Raise StopIteration if no matches at all.
        Return three-tuple: row, document, match span.
        """
        rows = self._rows or range(len(self.times))
        texts = (self.main_texts, self.tran_texts)[doc]
        for row in range(row, max(rows) + 1):
            if texts[row] != self._finder.text:
                self._finder.set_text(texts[row])
            self._finder.pos = pos or 0
            if pos is not None:
                self._finder.pos = pos
            else:
                self._finder.pos = 0
            try:
                match_span = self._finder.next()
            except StopIteration:
                pos = None
                if doc == self._last_match_doc:
                    if row == self._last_match_row:
                        if self._last_match_passed:
                            raise StopIteration
                        self._last_match_passed = True
                if row == max(rows):
                    raise ValueError
            else:
                self._last_match_row = row
                self._last_match_doc = doc
                self._last_match_passed = False
                return row, doc, match_span

    def _previous_in_document(self, row, doc, pos=None):
        """
        Find previous pattern in document starting from position.

        pos: None to start from end
        Raise ValueError if no matches before position.
        Raise StopIteration if no matches at all.
        Return three-tuple: row, document, match span.
        """
        rows = self._rows or range(len(self.times))
        texts = (self.main_texts, self.tran_texts)[doc]
        for row in reversed(range(min(rows), row + 1)):
            if texts[row] != self._finder.text:
                self._finder.set_text(texts[row])
            if pos is not None:
                self._finder.pos = pos
            else:
                self._finder.pos = len(self._finder.text)
            try:
                match_span = self._finder.previous()
            except StopIteration:
                pos = None
                if doc == self._last_match_doc:
                    if row == self._last_match_row:
                        if self._last_match_passed:
                            raise StopIteration
                        self._last_match_passed = True
                if row == min(rows):
                    raise ValueError
            else:
                self._last_match_row = row
                self._last_match_doc = doc
                self._last_match_passed = False
                return row, doc, match_span

    def find_next(self, row, doc, pos=None):
        """
        Find next pattern starting from position.

        pos: None for beginning
        Raise StopIteration if no matches exist.
        Return three-tuple: row, document, match span.
        """
        return self._find(row, doc, pos, True)

    def find_previous(self, row, doc, pos=None):
        """
        Find previous pattern starting from position.

        pos: None for end
        Raise StopIteration if no matches exist.
        Return three-tuple: row, document, match span.
        """
        return self._find(row, doc, pos, False)

    @revertablemethod
    def replace(self, register=-1):
        """Replace current match."""

        row = self._last_match_row
        doc = self._last_match_doc
        self._finder.replace()
        self.set_text(row, doc, self._finder.text, register=register)
        self.set_action_description(register, _('Replacing'))

    @revertablemethod
    def replace_all(self, register=-1):
        """
        Replace all matches.

        Return amount of substitutions made.
        """
        new_rows  = [[], []]
        new_texts = [[], []]
        count = 0
        for doc in self._docs:
            texts = (self.main_texts, self.tran_texts)[doc]
            for row, text in enumerate(texts):
                self._finder.set_text(text)
                this_count = self._finder.replace_all()
                if this_count > 0:
                    new_rows[doc].append(row)
                    new_texts[doc].append(self._finder.text)
                    count += this_count
        if count == 0:
            return count
        self.replace_both_texts(new_rows, new_texts, register=register)
        self.set_action_description(register, _('Replacing all'))
        return count

    def set_find_regex(self, pattern, flags=0):
        """Set regular expression pattern to find."""

        self._finder.set_regex(pattern, flags)

    def set_find_replacement(self, replacement):
        """Set replacement."""

        self._finder.replacement = replacement

    def set_find_string(self, pattern, ignore_case=False):
        """Set string pattern to find."""

        self._finder.pattern = pattern
        self._finder.ignore_case = ignore_case
        self._finder.is_regex = False

    def set_find_target(self, rows=None, docs=None, wrap=True):
        """
        Set target to find in.

        rows: None for all rows
        docs: None for all documents
        """
        self._rows = rows
        self._docs = docs or [MAIN, TRAN]
        self._wrap = wrap
