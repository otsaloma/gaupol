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
from gaupol.base.delegate    import Delegate
from gaupol.base.text.finder import Finder


class FindDelegate(Delegate):

    """Finding and replacing text."""

    def __init__(self, *args, **kwargs):

        Delegate.__init__(self, *args, **kwargs)

        self._finder = Finder()

        self._rows = None
        self._docs = [cons.Document.MAIN, cons.Document.TRAN]
        self._wrap = True

        self._last_match_row = None
        self._last_match_doc = None
        self._last_match_passed = False

    def _find(self, row, doc, pos, next):
        """
        Find pattern starting from position.

        next: True to find next, False to find previous.
        Raise StopIteration if no matches exist.
        Return three-tuple: row, document, match span.
        """
        if next:
            find_in_document = self._find_next_in_document
        else:
            find_in_document = self._find_previous_in_document
        self._last_match_row = row
        self._last_match_doc = doc
        self._last_match_passed = False
        rows = self._rows or range(len(self.times))

        while True:
            try:
                return find_in_document(row, doc, pos)
            except ValueError:
                pass
            if doc == max(self._docs) and not self._wrap:
                raise StopIteration
            try:
                doc = self._get_other_document(doc)
            except ValueError:
                pass
            row = min(rows)
            pos = None

    def find_next(self, row, doc, pos=0):
        """
        Find next pattern starting from position.

        Raise StopIteration if no matches exist.
        Return three-tuple: row, document, match span.
        """
        return self._find(row, doc, pos, True)

    def _find_next_in_document(self, row, doc, pos):
        """
        Find next pattern in document starting from position.

        Raise ValueError if no matches after position.
        Raise StopIteration if no matches at all.
        Return three-tuple: row, document, match span.
        """
        rows = self._rows or range(len(self.times))
        texts = (self.main_texts, self.tran_texts)[doc]
        for row in range(row, max(rows)):
            self._finder.text = texts[row]
            self._finder.pos = pos or 0
            try:
                match_span = self._finder.next()
            except StopIteration:
                pos = None
                if doc == self._last_match_doc:
                    if row == self._last_match_row:
                        if self._last_match_passed:
                            raise StopIteration
                        self._last_match_passed = True
            else:
                self._last_match_row = row
                self._last_match_doc = doc
                self._last_match_passed = False
                return row, doc, match_span
        raise ValueError

    def find_previous(self, row, doc, pos=0):
        """
        Find previous pattern starting from position.

        Raise StopIteration if no matches exist.
        Return three-tuple: row, document, match span.
        """
        return self._find(row, doc, pos, False)

    def _find_previous_in_document(self, row, doc, pos):
        """
        Find previous pattern in document starting from position.

        Raise ValueError if no matches after position.
        Raise StopIteration if no matches at all.
        Return three-tuple: row, document, match span.
        """
        rows = self._rows or range(len(self.times))
        texts = (self.main_texts, self.tran_texts)[doc]
        for row in reversed(range(min(rows), row + 1)):
            self._finder.text = texts[row]
            self._finder.pos = pos or len(self._finder.text)
            try:
                match_span = self._finder.previous()
            except StopIteration:
                pos = None
                if doc == self._last_match_doc:
                    if row == self._last_match_row:
                        if self._last_match_passed:
                            raise StopIteration
                        self._last_match_passed = True
            else:
                self._last_match_row = row
                self._last_match_doc = doc
                self._last_match_passed = False
                return row, doc, match_span
        raise ValueError

    def _get_other_document(self, doc):
        """
        Get other document included in target.

        Raise ValueError if no other document.
        """
        for candidate in self._docs:
            if candidate != doc:
                return candidate
        raise ValueError

    def replace(self, register=cons.Action.DO):
        """Replace current match."""

        row = self._last_match_row
        doc = self._last_match_doc
        self._finder.replace()
        self.set_text(row, doc, self._finder.text, register)
        self.set_action_description(register, _('Replacing'))

    def replace_all(self, register=cons.Action.DO):
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
                self._finder.text = text
                this_count = self._finder.replace_all()
                if this_count > 0:
                    new_rows[doc].append(row)
                    new_texts[doc].append(self._finder.text)
                    count += this_count
        if count == 0:
            return count
        self.replace_both_texts(new_rows, new_texts, register)
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

        Use None in rows and docs for all.
        """
        self._rows = rows
        self._docs = docs or [cons.Document.MAIN, cons.Document.TRAN]
        self._wrap = wrap
