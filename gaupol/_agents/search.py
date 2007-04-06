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


"""Searching for and replacing text."""


from gaupol import const
from gaupol.base import Delegate
from gaupol.finder import Finder
from gaupol.i18n import _
from .register import revertable


class SearchAgent(Delegate):

    """Finding and replacing text.

    Instance variables:

        _docs:         List of the target documents
        _finder:       Finder
        _match_doc:    Document of the last match
        _match_passed: True if the position of last match has been passed
        _match_row:    The row of the last match
        _match_span:   The start and end positions of the last match
        _rows:         The target rows
        _wrap:         True to wrap search
    """

    # pylint: disable-msg=E0203,W0201

    def __init__(self, master):

        Delegate.__init__(self, master)

        self._docs         = [const.DOCUMENT.MAIN, const.DOCUMENT.TRAN]
        self._finder       = Finder()
        self._match_doc    = None
        self._match_passed = False
        self._match_row    = None
        self._match_span   = None
        self._rows         = None
        self._wrap         = True

    def _find(self, row, doc, pos, next):
        """Find pattern starting from position.

        pos can be None for beginning or end.
        next should be True to find next, False to find previous.
        Raise StopIteration if no match.
        Return tuple of row, document, match span.
        """
        find = (self._next_in_document if next else self._previous_in_document)
        self._match_row = row
        self._match_doc = doc
        self._match_passed = False
        rows = self._rows or range(len(self.times))
        while True:
            try:
                # Return match in document after position.
                return find(row, doc, pos)
            except ValueError:
                pass
            # Proceed to next document or raise StopIteration.
            self._match_passed = True
            doc = self._get_document(doc, next)
            row = (min(rows) if next else max(rows))
            pos = None

    def _get_document(self, doc, next):
        """Get the document to proceed to.

        next should be True to find next, False to find previous.
        Raise StopIteration if nowhere to proceed.
        """
        if len(self._docs) == 1:
            if self._wrap:
                return doc
            raise StopIteration
        if next and doc == const.DOCUMENT.MAIN:
            return const.DOCUMENT.TRAN
        if next and doc == const.DOCUMENT.TRAN:
            if self._wrap:
                return const.DOCUMENT.MAIN
            raise StopIteration
        if not next and doc == const.DOCUMENT.MAIN:
            if self._wrap:
                return const.DOCUMENT.TRAN
            raise StopIteration
        if not next and doc == const.DOCUMENT.TRAN:
            return const.DOCUMENT.MAIN
        raise ValueError

    def _next_in_document(self, row, doc, pos=None):
        """Find the next match in document starting from position.

        pos can be None to start from beginning.
        Raise StopIteration if no matches at all anywhere.
        Raise ValueError if no match in this document after position.
        Return tuple of row, document, match span.
        """
        rows = self._rows or range(len(self.times))
        texts = self.get_texts(doc)
        for row in range(row, max(rows) + 1):
            # Avoid resetting finder's match span.
            if texts[row] != self._finder.text:
                self._finder.set_text(texts[row])
            self._finder.pos = 0
            if pos is not None:
                self._finder.pos = pos
            try:
                match_span = self._finder.next()
            except StopIteration:
                # Raise StopIteration if a full loop around all target
                # documents and rows has been made with no matches.
                if doc == self._match_doc:
                    if row == self._match_row:
                        if self._match_passed:
                            raise StopIteration
                pos = None
                continue
            self._match_row = row
            self._match_doc = doc
            self._match_span = match_span
            self._match_passed = False
            return row, doc, match_span
        # Raise ValueError if no match found in this document after position.
        raise ValueError

    def _previous_in_document(self, row, doc, pos=None):
        """Find the previous match in document starting from position.

        pos can be None to start from end.
        Raise StopIteration if no matches at all anywhere.
        Raise ValueError if no match in this document before position.
        Return tuple of row, document, match span.
        """
        rows = self._rows or range(len(self.times))
        texts = self.get_texts(doc)
        for row in reversed(range(min(rows), row + 1)):
            # Avoid resetting finder's match span.
            if texts[row] != self._finder.text:
                self._finder.set_text(texts[row])
            self._finder.pos = len(self._finder.text)
            if pos is not None:
                self._finder.pos = pos
            try:
                match_span = self._finder.previous()
            except StopIteration:
                # Raise StopIteration if a full loop around all target
                # documents and rows has been made with no matches.
                if doc == self._match_doc:
                    if row == self._match_row:
                        if self._match_passed:
                            raise StopIteration
                pos = None
                continue
            self._match_row = row
            self._match_doc = doc
            self._match_span = match_span
            self._match_passed = False
            return row, doc, match_span
        # Raise ValueError if no match found in this document after position.
        raise ValueError

    def find_next(self, row=None, doc=None, pos=None):
        """Find the next match starting from position.

        row, doc and pos can be None to start from beginning.
        Raise StopIteration if no matches exist.
        Return tuple of row, document, match span.
        """
        if row is None:
            row = 0
        if doc is None:
            doc = const.DOCUMENT.MAIN
        return self._find(row, doc, pos, True)

    def find_previous(self, row=None, doc=None, pos=None):
        """Find the previous match starting from position.

        row, doc and pos can be None to start from end.
        Raise StopIteration if no matches exist.
        Return tuple of row, document, match span.
        """
        if row is None:
            row = len(self.times) - 1
        if doc is None:
            doc = const.DOCUMENT.TRAN
        return self._find(row, doc, pos, False)

    @revertable
    def replace(self, register=-1):
        """Replace the current match."""

        row = self._match_row
        doc = self._match_doc
        self._finder.replace()
        self.set_text(row, doc, self._finder.text, register=register)
        self.set_action_description(register, _("Replacing"))

    @revertable
    def replace_all(self, register=-1):
        """Replace all matches of pattern.

        Return the amount of substitutions made.
        """
        new_rows = [[], []]
        new_texts = [[], []]
        count = 0
        for doc in self._docs:
            texts = self.get_texts(doc)
            for row, text in enumerate(texts):
                self._finder.set_text(text)
                sub_count = self._finder.replace_all()
                if sub_count > 0:
                    new_rows[doc].append(row)
                    new_texts[doc].append(self._finder.text)
                    count += sub_count
        if count > 0:
            self.replace_both_texts(new_rows, new_texts, register=register)
            self.set_action_description(register, _("Replacing all"))
        return count

    def set_search_regex(self, pattern, flags=0):
        """Set the regular expression pattern to find.

        DOTALL, MULTILINE and UNICODE are automatically added to flags.
        Raise re.error if pattern sucks.
        """
        self._finder.set_regex(unicode(pattern), flags)

    def set_search_replacement(self, replacement):
        """Set the replacement."""

        self._finder.replacement = unicode(replacement)

    def set_search_string(self, pattern, ignore_case=False):
        """Set string pattern to find."""

        self._finder.pattern = unicode(pattern)
        self._finder.ignore_case = ignore_case
        self._finder.is_regex = False

    def set_search_target(self, rows=None, docs=None, wrap=True):
        """Set the target to find in.

        rows can be None to target all rows.
        docs can be None to target all documents.
        """
        self._rows = rows or []
        self._docs = docs or [const.DOCUMENT.MAIN, const.DOCUMENT.TRAN]
        self._wrap = wrap
