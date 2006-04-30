# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Finding and replacing text."""


from gettext import gettext as _

from gaupol.base.delegates import Delegate
from gaupol.constants      import Action, Document


class FindDelegate(Delegate):

    """Finding and replacing text."""

    def __init__(self, *args, **kwargs):

        Delegate.__init__(self, *args, **kwargs)

        self.__last_match_row = None
        self.__last_match_doc = None
        self.__last_match_passed = False

        self.__wrap = False

    def _find(self, row, doc, docs, pos, next):
        """
        Find pattern starting from given position.

        next: True to find next, False to find previous.
        Raise StopIteration if no matches exist.
        Return three-tuple: row, doc, match span.
        """
        find_in_document = (
            self._find_previous_in_document,
            self._find_next_in_document,
        )[int(next)]

        self.__last_match_row = row
        self.__last_match_doc = doc
        self.__last_match_passed = False

        while True:
            try:
                return find_in_document(row, doc, pos)
            except ValueError:
                pass
            if doc == Document.TRAN and not self.__wrap:
                raise StopIteration
            row = 0
            try:
                doc = self._get_other_document(doc, docs)
            except ValueError:
                pass
            pos = None

    def find_next(self, row, doc, docs, pos=0):
        """
        Find next pattern starting from given position.

        Raise StopIteration if no matches exist.
        Return three-tuple: row, doc, match span.
        """
        return self._find(row, doc, docs, pos, True)

    def _find_next_in_document(self, row, doc, pos):
        """
        Find next pattern in given document starting from given position.

        Raise StopIteration if no matches exist.
        Return three-tuple: row, doc, match span.
        """
        texts = (self.main_texts, self.tran_texts)[doc]
        for row in range(row, len(texts)):
            self.finder.text = texts[row]
            self.finder.position = pos or 0
            try:
                match_span = self.finder.next()
            except StopIteration:
                pos = None
                if doc == self.__last_match_doc:
                    if row == self.__last_match_row:
                        if self.__last_match_passed:
                            raise StopIteration
                        self.__last_match_passed = True
            else:
                self.__last_match_row = row
                self.__last_match_doc = doc
                self.__last_match_passed = False
                return row, doc, match_span
        raise ValueError

    def find_previous(self, row, doc, docs, pos=0):
        """
        Find previous pattern starting from given position.

        Raise StopIteration if no matches exist.
        Return three-tuple: row, doc, match span.
        """
        return self._find(row, doc, docs, pos, False)

    def _find_previous_in_document(self, row, doc, pos):
        """
        Find previous pattern in given document starting from given position.

        Raise StopIteration if no matches exist.
        Return three-tuple: row, doc, match span.
        """
        texts = (self.main_texts, self.tran_texts)[doc]
        for row in reversed(range(0, row + 1)):
            self.finder.text = texts[row]
            self.finder.position = pos or len(self.finder.text)
            try:
                match_span = self.finder.previous()
            except StopIteration:
                pos = None
                if doc == self.__last_match_doc:
                    if row == self.__last_match_row:
                        if self.__last_match_passed:
                            raise StopIteration
                        self.__last_match_passed = True
            else:
                self.__last_match_row = row
                self.__last_match_doc = doc
                self.__last_match_passed = False
                return row, doc, match_span
        raise ValueError

    def _get_other_document(self, doc, docs):
        """
        Get other document included in docs.

        Raise ValueError if no other document.
        """
        if doc == Document.MAIN:
            if Document.TRAN in docs:
                return Document.TRAN
        if doc == Document.TRAN:
            if Document.MAIN in docs:
                return Document.MAIN

        raise ValueError

    def replace(self, register=Action.DO):
        """Replace current match."""

        doc = self.__last_match_doc
        row = self.__last_match_row
        self.finder.replace()
        self.set_text(row, doc, self.finder.text, register)
        self.modify_action_description(register, _('Replacing'))

    def replace_all(self, docs, register=Action.DO):
        """
        Replace all matches.

        Return amount of substitutions made.
        """
        MAIN = Document.MAIN
        TRAN = Document.TRAN
        new_rows = [[], []]
        new_texts = [[], []]
        count = 0

        for doc in (MAIN, TRAN):
            if doc not in docs:
                continue
            texts = (self.main_texts, self.tran_texts)[doc]
            for row, text in enumerate(texts):
                self.finder.text = text
                single_count = self.finder.replace_all()
                if single_count > 0:
                    new_rows[doc].append(row)
                    new_texts[doc].append(self.finder.text)
                    count += single_count

        if count == 0:
            return count

        if not new_rows[MAIN]:
            self.replace_texts(new_rows[TRAN], TRAN, new_texts[TRAN], register)
        elif not new_rows[TRAN]:
            self.replace_texts(new_rows[MAIN], TRAN, new_texts[MAIN], register)
        else:
            self.replace_both_texts(new_rows, new_texts, register)
        self.modify_action_description(register, _('Replacing all'))
        return count

    def set_find_regex(self, pattern, flags=0):
        """Set regular expression pattern to find."""

        self.finder.set_regex(pattern, flags)

    def set_find_replacement(self, replacement):
        """Set replacement."""

        self.finder.replacement = replacement

    def set_find_string(self, pattern, ignore_case=False):
        """Set string pattern to find."""

        self.finder.pattern = pattern
        self.finder.ignore_case = ignore_case
        self.finder.is_regex = False

    def set_find_wrap(self, wrap):

        self.__wrap = wrap


if __name__ == '__main__':

    import re
    from gaupol.test import Test

    class TestFindDelegate(Test):

        def get_blank_project(self):

            project = self.get_project()
            rows = range(len(project.times))
            project.clear_texts(rows, Document.MAIN)
            project.clear_texts(rows, Document.TRAN)
            return project

        def get_uniform_project(self):

            project = self.get_project()
            text = \
                'Said he was wounded by a pin.\n' \
                'He\'s convalescing at home.'
            for texts in (project.main_texts, project.tran_texts):
                for i in range(len(texts)):
                    texts[i] = text
            return project

        def test_find_next(self):

            project = self.get_blank_project()
            project.set_find_string('test')
            docs = [Document.MAIN, Document.TRAN]
            try:
                project.find_next(0, docs[0], docs)
                raise AssertionError
            except StopIteration:
                pass

            project = self.get_uniform_project()
            project.set_find_regex(r'pin\.')
            docs = [Document.MAIN, Document.TRAN]
            args = 2, docs[1], [docs[1]], 40
            row, doc, match_span = project.find_next(*args)
            assert row == 3
            assert doc == Document.TRAN
            assert match_span == (25, 29)

            row = 0
            doc = Document.MAIN
            pos = 0
            for i in range(100):
                args = row, doc, docs, pos
                row, doc, match_span = project.find_next(*args)
                pos = match_span[1]
                assert match_span == (25, 29)
                assert pos == 29

        def test_find_previous(self):

            project = self.get_blank_project()
            project.set_find_string('test')
            docs = [Document.MAIN, Document.TRAN]
            try:
                project.find_previous(0, docs[0], docs)
                raise AssertionError
            except StopIteration:
                pass

            project = self.get_uniform_project()
            project.set_find_regex(r'pin\.')
            docs = [Document.MAIN, Document.TRAN]
            args = 2, docs[1], [docs[1]], 40
            row, doc, match_span = project.find_previous(*args)
            assert row == 2
            assert doc == Document.TRAN
            assert match_span == (25, 29)

            row = 0
            doc = Document.MAIN
            pos = 0
            for i in range(100):
                args = row, doc, docs, pos
                row, doc, match_span = project.find_previous(*args)
                pos = match_span[1]
                assert match_span == (25, 29)
                assert pos == 29

        def test_replace(self):

            def replace_and_assert(project):
                project.replace()
                assert project.main_texts[0] == \
                    'Said he xxx wounded by a pin.\n' \
                    'He\'s convalescing at home.'
                project.undo()
                assert project.main_texts[0] == \
                    'Said he was wounded by a pin.\n' \
                    'He\'s convalescing at home.'
                project.redo()
                assert project.main_texts[0] == \
                    'Said he xxx wounded by a pin.\n' \
                    'He\'s convalescing at home.'

            project = self.get_uniform_project()
            project.set_find_string('WAS', True)
            project.set_find_replacement('xxx')
            docs = [Document.MAIN, Document.TRAN]
            project.find_next(0, docs[0], docs)
            replace_and_assert(project)

            project = self.get_uniform_project()
            project.set_find_regex(r'\bwas\b', re.DOTALL)
            project.set_find_replacement('xxx')
            docs = [Document.MAIN, Document.TRAN]
            project.find_next(0, docs[0], docs)
            replace_and_assert(project)

        def test_replace_all(self):

            def replace_all_and_assert(project):
                project.replace_all(docs)
                for texts in (project.main_texts, project.tran_texts):
                    for text in texts:
                        assert text == \
                            'Said he xxx wounded by a pin.\n' \
                            'He\'s convalescing at home.'
                project.undo()
                for texts in (project.main_texts, project.tran_texts):
                    for text in texts:
                        assert text == \
                            'Said he was wounded by a pin.\n' \
                            'He\'s convalescing at home.'
                project.redo()
                for texts in (project.main_texts, project.tran_texts):
                    for text in texts:
                        assert text == \
                            'Said he xxx wounded by a pin.\n' \
                            'He\'s convalescing at home.'

            project = self.get_uniform_project()
            project.set_find_string('was')
            project.set_find_replacement('xxx')
            docs = [Document.MAIN, Document.TRAN]
            replace_all_and_assert(project)

            project = self.get_uniform_project()
            project.set_find_regex(r'\bwas\b', re.DOTALL)
            project.set_find_replacement('xxx')
            docs = [Document.MAIN, Document.TRAN]
            replace_all_and_assert(project)

        def test_set_find_regex(self):

            project = self.get_blank_project()
            project.set_find_regex(r'^test', re.DOTALL)
            assert project.finder.pattern == r'^test'
            assert project.finder.is_regex == True
            assert project.finder.regex.pattern == r'^test'
            assert project.finder.regex.flags == re.DOTALL|re.UNICODE

        def test_set_find_replacement(self):

            project = self.get_blank_project()
            project.set_find_replacement('test')
            assert project.finder.replacement == 'test'

        def test_set_find_string(self):

            project = self.get_blank_project()
            project.set_find_string('test')
            assert project.finder.pattern == 'test'

    TestFindDelegate().run()
