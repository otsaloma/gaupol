# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009 Osmo Salomaa
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

"""Searching for and replacing text."""

import aeidon
_ = aeidon.i18n._


class SearchAgent(aeidon.Delegate, metaclass=aeidon.Contractual):

    """
    Searching for and replacing text.

    :ivar _docs: Sequence of :attr:`aeidon.documents` items
    :ivar _finder: Instance of :class:`aeidon.Finder` used
    :ivar _match_doc: :attr:`aeidon.documents` item of the last match
    :ivar _match_passed: ``True`` if the position of last match has been passed
    :ivar _match_index: Index of the last match
    :ivar _match_span: Start and end positions of the last match
    :ivar _indices: Sequence of target indices or ``None`` for all
    :ivar _wrap: ``True`` to wrap search, ``False`` to stop at the last index

    Searching is done with the help of an instance of :class:`aeidon.Finder`.
    This agent provides for looping over the subtitles and their texts, feeding
    those texts to the finder and raising :exc:`StopIteration` when no more
    matches are found.
    """

    def __init__(self, master):
        """Initialize a :class:`SearchAgent` object."""
        aeidon.Delegate.__init__(self, master)
        self._docs = None
        self._finder = aeidon.Finder()
        self._indices = None
        self._match_doc = None
        self._match_index = None
        self._match_passed = None
        self._match_span = None
        self._wrap = None
        # Set targets to defaults.
        self.set_search_target()

    def _find(self, index, doc, pos, next):
        """
        Find pattern starting from given location.

        `pos` can be ``None`` for beginning or end.
        `next` should be ``True`` to find next, ``False`` to find previous.
        Raise :exc:`StopIteration` if no match.
        Return tuple of index, document, match span.
        """
        find = (self._next_in_document if next
                else self._previous_in_document)

        self._match_index = index
        self._match_doc = doc
        self._match_passed = False
        indices = self._indices or self.get_all_indices()
        while True:
            try:
                # Return match in document after location.
                return find(index, doc, pos)
            except ValueError:
                pass
            # Proceed to the next document or raise StopIteration.
            self._match_passed = True
            doc = self._get_document(doc, next)
            index = (min(indices) if next else max(indices))
            pos = None

    def _get_document(self, doc, next):
        """
        Return the document to proceed to.

        `next` should be ``True`` to find next, ``False`` to find previous.
        Raise :exc:`StopIteration` if nowhere to proceed.
        """
        if len(self._docs) == 1:
            if self._wrap:
                return doc
            raise StopIteration
        if next and (doc == aeidon.documents.MAIN):
            return aeidon.documents.TRAN
        if next and (doc == aeidon.documents.TRAN):
            if self._wrap:
                return aeidon.documents.MAIN
            raise StopIteration
        if (not next) and (doc == aeidon.documents.MAIN):
            if self._wrap:
                return aeidon.documents.TRAN
            raise StopIteration
        if (not next) and (doc == aeidon.documents.TRAN):
            return aeidon.documents.MAIN
        raise ValueError("Invalid document: {} or invalid next: {}"
                         .format(repr(doc), repr(next)))

    def _invariant(self):
        for index in self._indices or ():
            assert 0 <= index < len(self.subtitles)

    def _next_in_document(self, index, doc, pos=None):
        """
        Find the next match in `doc` starting from `pos`.

        `pos` can be ``None`` to start from beginning.
        Raise :exc:`StopIteration` if no matches at all anywhere.
        Raise :exc:`ValueError` if no match in this `doc` after `pos`.
        Return tuple of index, document, match span.
        """
        indices = self._indices or self.get_all_indices()
        for index in range(index, max(indices) + 1):
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
                # documents and indices has been made with no matches.
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
        raise ValueError("No more matches in document: {}"
                         .format(repr(doc)))

    def _previous_in_document(self, index, doc, pos=None):
        """
        Find the previous match in `doc` starting from `pos`.

        `pos` can be ``None`` to start from end.
        Raise :exc:`StopIteration` if no matches at all anywhere.
        Raise :exc:`ValueError` if no match in this `doc` before `pos`.
        Return tuple of index, document, match span.
        """
        indices = self._indices or self.get_all_indices()
        for index in reversed(range(min(indices), index + 1)):
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
                # documents and indices has been made with no matches.
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
        raise ValueError("No more matches in document: {}"
                         .format(repr(doc)))

    def find_next_require(self, index=None, doc=None, pos=None):
        assert 0 <= (index or 0) < len(self.subtitles)

    def find_next_ensure(self, value, index=None, doc=None, pos=None):
        index, doc, match_span = value
        assert 0 <= index < len(self.subtitles)
        text = self.subtitles[index].get_text(doc)
        assert 0 <= match_span[0] <= len(text)
        assert 0 <= match_span[1] <= len(text)
        assert self._docs

    @aeidon.deco.export
    def find_next(self, index=None, doc=None, pos=None):
        """
        Find the next match starting from given location.

        `index`, `doc` and `pos` can be ``None`` to start from beginning.
        Raise :exc:`StopIteration` if no matches exist.
        Return tuple of index, document, match span.
        """
        index = (0 if index is None else index)
        doc = (self._docs[0] if doc is None else doc)
        return self._find(index, doc, pos, True)

    def find_previous_require(self, index=None, doc=None, pos=None):
        assert 0 <= (index or 0) < len(self.subtitles)
        if doc is not None:
            text = self.subtitles[index or 0].get_text(doc)
            assert 0 <= (pos or 0) <= len(text)

    def find_previous_ensure(self, value, index=None, doc=None, pos=None):
        index, doc, match_span = value
        assert 0 <= index < len(self.subtitles)
        text = self.subtitles[index].get_text(doc)
        assert 0 <= match_span[0] <= len(text)
        assert 0 <= match_span[1] <= len(text)
        assert self._docs

    @aeidon.deco.export
    def find_previous(self, index=None, doc=None, pos=None):
        """
        Find the previous match starting from given location.

        `index`, `doc` and `pos` can be ``None`` to start from end.
        Raise :exc:`StopIteration` if no matches exist.
        Return tuple of index, document, match span.
        """
        index = (len(self.subtitles) - 1 if index is None else index)
        doc = (self._docs[-1] if doc is None else doc)
        return self._find(index, doc, pos, False)

    def replace_require(self, register=-1):
        assert 0 <= self._match_index < len(self.subtitles)
        subtitle = self.subtitles[self._match_index]
        text = subtitle.get_text(self._match_doc)
        assert 0 <= self._match_span[0] <= len(text)
        assert 0 <= self._match_span[1] <= len(text)

    @aeidon.deco.export
    @aeidon.deco.revertable
    def replace(self, register=-1):
        """
        Replace the current match of pattern.

        Raise :exc:`re.error` if bad replacement.
        """
        orig_text = self._finder.text
        self._finder.replace()
        if self._finder.text == orig_text: return
        self.set_text(self._match_index,
                      self._match_doc,
                      self._finder.text,
                      register=register)

        self.set_action_description(register, _("Replacing"))

    @aeidon.deco.export
    @aeidon.deco.revertable
    def replace_all(self, register=-1):
        """
        Replace all matches of pattern and return amount.

        Raise :exc:`re.error` if bad replacement.
        """
        counts = {}
        for doc in self._docs:
            counts[doc] = 0
            new_indices = []
            new_texts = []
            for index, subtitle in enumerate(self.subtitles):
                text = subtitle.get_text(doc)
                self._finder.set_text(text)
                sub_count = self._finder.replace_all()
                if sub_count > 0:
                    new_indices.append(index)
                    new_texts.append(self._finder.text)
                    counts[doc] += sub_count
            if new_indices:
                self.replace_texts(new_indices,
                                   doc,
                                   new_texts,
                                   register=register)

                self.set_action_description(register, _("Replacing all"))
        if (len(list(counts.keys())) == 2) and all(counts.values()):
            self.group_actions(register, 2, _("Replacing all"))
        return sum(counts.values())

    @aeidon.deco.export
    def set_search_regex(self, pattern, flags=0):
        """
        Set the regular expression pattern to find.

        ``DOTALL``, ``MULTILINE`` and ``UNICODE`` are automatically added to
        flags. Raise :exc:`re.error` if bad pattern.
        """
        self._finder.set_regex(pattern, flags)

    @aeidon.deco.export
    def set_search_replacement(self, replacement):
        """Set the replacement string."""
        self._finder.replacement = replacement

    @aeidon.deco.export
    def set_search_string(self, pattern, ignore_case=False):
        """Set the string pattern to find."""
        self._finder.pattern = pattern
        self._finder.ignore_case = ignore_case

    def set_search_target_require(self, indices=None, docs=None, wrap=True):
        for index in indices or ():
            assert 0 <= index < len(self.subtitles)

    @aeidon.deco.export
    def set_search_target(self, indices=None, docs=None, wrap=True):
        """
        Set the targets to search in.

        `indices` can be ``None`` to target all subtitles.
        `docs` can be ``None`` to target all documents.
        """
        self._indices = (tuple(indices) if indices else None)
        self._docs = tuple(docs or aeidon.documents)
        self._wrap = wrap
