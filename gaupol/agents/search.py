# Copyright (C) 2005-2008 Osmo Salomaa
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

import gaupol
_ = gaupol.i18n._


class SearchAgent(gaupol.Delegate):

    """Searching for and replacing text.

    Instance variables:
     * _docs: Sequence of the target document enumerations
     * _finder: Instance of Finder used
     * _match_doc: Document enumeration of the last match
     * _match_passed: True if the position of last match has been passed
     * _match_index: The index of the last match
     * _match_span: The start and end positions of the last match
     * _indices: Sequence of the target indices or None for all
     * _wrap: True to wrap search, False to stop at the last index

    Searching is done with the help of an instance of Finder. This agent
    provides for looping over the subtitles and their texts feeding those texts
    to the finder and raising StopIteration when no more matches are found.
    """

    __metaclass__ = gaupol.Contractual

    def __init__(self, master):
        """Initialize a SearchAgent object."""

        gaupol.Delegate.__init__(self, master)
        self._docs = None
        self._finder = gaupol.Finder()
        self._indices = None
        self._match_doc = None
        self._match_index = None
        self._match_passed = None
        self._match_span = None
        self._wrap = None

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
        indices = self._indices or range(len(self.subtitles))
        while True:
            try:
                # Return match in document after position.
                return find(index, doc, pos)
            except ValueError:
                pass
            # Proceed to the next document or raise StopIteration.
            self._match_passed = True
            doc = self._get_document(doc, next)
            index = (min(indices) if next else max(indices))
            pos = None

    def _get_document(self, doc, next):
        """Return the document to proceed to.

        next should be True to find next, False to find previous.
        Raise StopIteration if nowhere to proceed.
        """
        if len(self._docs) == 1:
            if self._wrap:
                return doc
            raise StopIteration
        if next and (doc == gaupol.documents.MAIN):
            return gaupol.documents.TRAN
        if next and (doc == gaupol.documents.TRAN):
            if self._wrap:
                return gaupol.documents.MAIN
            raise StopIteration
        if (not next) and (doc == gaupol.documents.MAIN):
            if self._wrap:
                return gaupol.documents.TRAN
            raise StopIteration
        if (not next) and (doc == gaupol.documents.TRAN):
            return gaupol.documents.MAIN
        raise ValueError("Invalid document: %s or invalid next: %s" % (
            repr(doc), repr(next)))

    def _invariant(self):
        for index in self._indices or []:
            assert 0 <= index < len(self.subtitles)

    def _next_in_document(self, index, doc, pos=None):
        """Find the next match in document starting from position.

        pos can be None to start from beginning.
        Raise StopIteration if no matches at all anywhere.
        Raise ValueError if no match in this document after position.
        Return tuple of index, document, match span.
        """
        indices = self._indices or range(len(self.subtitles))
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
        raise ValueError("No more matches in document: %s" % repr(doc))

    def _previous_in_document(self, index, doc, pos=None):
        """Find the previous match in document starting from position.

        pos can be None to start from end.
        Raise StopIteration if no matches at all anywhere.
        Raise ValueError if no match in this document before position.
        Return tuple of index, document, match span.
        """
        indices = self._indices or range(len(self.subtitles))
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
        raise ValueError("No more matches in document: %s" % repr(doc))

    def find_next_require(self, index=None, doc=None, pos=None):
        assert 0 <= (index or 0) < len(self.subtitles)

    def find_next_ensure(self, value, index=None, doc=None, pos=None):
        index, doc, match_span = value
        assert 0 <= index < len(self.subtitles)
        text = self.subtitles[index].get_text(doc)
        assert 0 <= match_span[0] <= len(text)
        assert 0 <= match_span[1] <= len(text)
        assert self._docs

    def find_next(self, index=None, doc=None, pos=None):
        """Find the next match starting from position.

        index, doc and pos can be None to start from beginning.
        Raise StopIteration if no matches exist.
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

    def find_previous(self, index=None, doc=None, pos=None):
        """Find the previous match starting from position.

        index, doc and pos can be None to start from end.
        Raise StopIteration if no matches exist.
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

    @gaupol.deco.revertable
    def replace(self, register=-1):
        """Replace the current match of pattern.

        Raise re.error if bad replacement.
        """
        orig_text = self._finder.text
        self._finder.replace()
        index = self._match_index
        doc = self._match_doc
        text = self._finder.text
        if text == orig_text: return
        self.set_text(index, doc, text, register=register)
        self.set_action_description(register, _("Replacing"))

    @gaupol.deco.revertable
    def replace_all(self, register=-1):
        """Replace all matches of pattern and return amount.

        Raise re.error if bad replacement.
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
                args = (new_indices, doc, new_texts)
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

    def set_search_target_require(self, indices=None, docs=None, wrap=True):
        for index in indices or []:
            assert 0 <= index < len(self.subtitles)

    def set_search_target(self, indices=None, docs=None, wrap=True):
        """Set the targets to search in.

        indices can be None to target all subtitles.
        docs can be None to target all documents.
        """
        self._indices = (tuple(indices) if indices else None)
        self._docs = tuple(docs or gaupol.documents)
        self._wrap = wrap
