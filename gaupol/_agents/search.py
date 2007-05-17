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
from gaupol.base import Contractual, Delegate
from gaupol.finder import Finder
from gaupol.i18n import _
from gaupol.reversion import revertable


class SearchAgent(Delegate):

    """Searching for and replacing text.

    Instance variables:

        _docs:         List of the target DOCUMENT constants
        _finder:       Instance of Finder used
        _match_doc:    DOCUMENT constant of the last match
        _match_passed: True if the position of last match has been passed
        _match_index:  The index of the last match
        _match_span:   The start and end positions of the last match
        _indexes:      List of the target indexes or None for all
        _wrap:         True to wrap search, False to stop at the last index

    Searching is done with the help of an instance of Finder. This agent
    provides for looping over the subtitles and their texts feeding those texts
    to the finder and raising StopIteration when no more matches found.
    """

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = Contractual

    def __init__(self, master):

        Delegate.__init__(self, master)

        self._docs         = None
        self._finder       = Finder()
        self._indexes      = None
        self._match_doc    = None
        self._match_index  = None
        self._match_passed = None
        self._match_span   = None
        self._wrap         = None

        # Set targets to defaults.
        self.set_search_target()

    def _find(self, index, doc, pos, next):
        """Find pattern starting from position.

        pos can be None for beginning or end.
        next should be True to find next, False to find previous.
        Raise StopIteration if no match.
        Return tuple of index, document, match span.
        """
        find = (self._previous_in_document, self._next_in_document)[next]
        self._match_index = index
        self._match_doc = doc
        self._match_passed = False
        indexes = self._indexes or range(len(self.subtitles))
        while True:
            try:
                # Return match in document after position.
                return find(index, doc, pos)
            except ValueError:
                pass
            # Proceed to the next document or raise StopIteration.
            self._match_passed = True
            doc = self._get_document(doc, next)
            index = (min(indexes) if next else max(indexes))
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
        if next and (doc == const.DOCUMENT.MAIN):
            return const.DOCUMENT.TRAN
        if next and (doc == const.DOCUMENT.TRAN):
            if self._wrap:
                return const.DOCUMENT.MAIN
            raise StopIteration
        if (not next) and (doc == const.DOCUMENT.MAIN):
            if self._wrap:
                return const.DOCUMENT.TRAN
            raise StopIteration
        if (not next) and (doc == const.DOCUMENT.TRAN):
            return const.DOCUMENT.MAIN
        raise ValueError

    def _invariant(self):
        for index in self._indexes or []:
            assert 0 <= index < len(self.subtitles)

    def _next_in_document(self, index, doc, pos=None):
        """Find the next match in document starting from position.

        pos can be None to start from beginning.
        Raise StopIteration if no matches at all anywhere.
        Raise ValueError if no match in this document after position.
        Return tuple of index, document, match span.
        """
        indexes = self._indexes or range(len(self.subtitles))
        for index in range(index, max(indexes) + 1):
            text = self.subtitles[index].get_text(doc)
            # Avoid resetting finder's match span.
            if text != self._finder.text:
                self._finder.set_text(text)
            self._finder.pos = 0
            if pos is not None:
                self._finder.pos = pos
            try:
                match_span = self._finder.next()
            except StopIteration:
                # Raise StopIteration if a full loop around all target
                # documents and indexes has been made with no matches.
                if doc == self._match_doc:
                    if index == self._match_index:
                        if self._match_passed:
                            raise StopIteration
                pos = None
                continue
            self._match_index = index
            self._match_doc = doc
            self._match_span = match_span
            self._match_passed = False
            return index, doc, match_span
        # Raise ValueError if no match found in this document after position.
        raise ValueError

    def _previous_in_document(self, index, doc, pos=None):
        """Find the previous match in document starting from position.

        pos can be None to start from end.
        Raise StopIteration if no matches at all anywhere.
        Raise ValueError if no match in this document before position.
        Return tuple of index, document, match span.
        """
        indexes = self._indexes or range(len(self.subtitles))
        for index in reversed(range(min(indexes), index + 1)):
            text = self.subtitles[index].get_text(doc)
            # Avoid resetting finder's match span.
            if text != self._finder.text:
                self._finder.set_text(text)
            self._finder.pos = len(self._finder.text)
            if pos is not None:
                self._finder.pos = pos
            try:
                match_span = self._finder.previous()
            except StopIteration:
                # Raise StopIteration if a full loop around all target
                # documents and indexes has been made with no matches.
                if doc == self._match_doc:
                    if index == self._match_index:
                        if self._match_passed:
                            raise StopIteration
                pos = None
                continue
            self._match_index = index
            self._match_doc = doc
            self._match_span = match_span
            self._match_passed = False
            return index, doc, match_span
        # Raise ValueError if no match found in this document after position.
        raise ValueError

    def find_next_require(self, index=None, doc=None, pos=None):
        assert 0 <= (index or 0) < len(self.subtitles)
        text = self.subtitles[index or 0].get_text(doc)
        assert 0 <= (pos or 0) <= len(text)

    def find_next_ensure(self, value, index=None, doc=None, pos=None):
        index, doc, match_span = value
        assert 0 <= index < len(self.subtitles)
        text = self.subtitles[index].get_text(doc)
        assert 0 <= match_span[0] <= len(text)
        assert 0 <= match_span[1] <= len(text)

    def find_next(self, index=None, doc=None, pos=None):
        """Find the next match starting from position.

        index, doc and pos can be None to start from beginning.
        Raise StopIteration if no matches exist.
        Return tuple of index, document, match span.
        """
        index = (0 if index is None else index)
        doc = (const.DOCUMENT.MAIN if doc is None else doc)
        return self._find(index, doc, pos, True)

    def find_previous_require(self, index=None, doc=None, pos=None):
        assert 0 <= (index or 0) < len(self.subtitles)
        text = self.subtitles[index or 0].get_text(doc)
        assert 0 <= (pos or 0) <= len(text)

    def find_previous_ensure(self, value, index=None, doc=None, pos=None):
        index, doc, match_span = value
        assert 0 <= index < len(self.subtitles)
        text = self.subtitles[index].get_text(doc)
        assert 0 <= match_span[0] <= len(text)
        assert 0 <= match_span[1] <= len(text)

    def find_previous(self, index=None, doc=None, pos=None):
        """Find the previous match starting from position.

        index, doc and pos can be None to start from end.
        Raise StopIteration if no matches exist.
        Return tuple of index, document, match span.
        """
        index = (len(self.subtitles) - 1 if index is None else index)
        doc = (const.DOCUMENT.TRAN if doc is None else doc)
        return self._find(index, doc, pos, False)

    def replace_require(self, register=-1):
        assert 0 <= self._match_index < len(self.subtitles)
        subtitle = self.subtitles[self._match_index]
        text = subtitle.get_text(self._match_doc)
        assert 0 <= self._match_span[0] <= len(text)
        assert 0 <= self._match_span[1] <= len(text)

    @revertable
    def replace(self, register=-1):
        """Replace the current match."""

        self._finder.replace()
        index = self._match_index
        doc = self._match_doc
        text = self._finder.text
        self.set_text(index, doc, text, register=register)
        self.set_action_description(register, _("Replacing"))

    @revertable
    def replace_all(self, register=-1):
        """Replace all matches of pattern and return amount."""

        counts = {}
        for doc in self._docs:
            counts[doc] = 0
            new_indexes = []
            new_texts = []
            for index, subtitle in enumerate(self.subtitles):
                text = subtitle.get_text(doc)
                self._finder.set_text(text)
                sub_count = self._finder.replace_all()
                if sub_count > 0:
                    new_indexes.append(index)
                    new_texts.append(self._finder.text)
                    counts[doc] += sub_count
            if new_indexes:
                args = (new_indexes, doc, new_texts)
                kwargs = {"register": register}
                self.replace_texts(*args, **kwargs)
                self.set_action_description(register, _("Replacing all"))
        if (len(counts.keys()) == 2) and all(counts.values()):
            self.group_actions(register, 2, _("Replacing all"))
        return sum(counts.values())

    def set_search_regex(self, pattern, flags=0):
        """Set the regular expression pattern to find.

        DOTALL, MULTILINE and UNICODE are automatically added to flags.
        Raise re.error if bad pattern.
        """
        self._finder.set_regex(unicode(pattern), flags)

    def set_search_replacement(self, replacement):
        """Set the replacement string."""

        self._finder.replacement = unicode(replacement)

    def set_search_string(self, pattern, ignore_case=False):
        """Set string pattern to find."""

        self._finder.pattern = unicode(pattern)
        self._finder.ignore_case = ignore_case
        self._finder.is_regex = False

    def set_search_target_require(self, indexes=None, docs=None, wrap=True):
        for index in indexes or []:
            assert 0 <= index < len(self.subtitles)

    def set_search_target(self, indexes=None, docs=None, wrap=True):
        """Set the targets to search in.

        indexes can be None to target all subtitles.
        docs can be None to target all documents.
        """
        self._indexes = indexes
        self._docs = docs or const.DOCUMENT.members
        self._wrap = wrap
