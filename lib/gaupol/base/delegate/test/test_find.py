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


import re

from gaupol.base import cons
from gaupol.test import Test


TEXT = \
'''Said he was wounded by a pin.
He\'s convalescing at home.'''

DOCS_ALL  = [cons.Document.MAIN, cons.Document.TRAN]
DOCS_MAIN = [cons.Document.MAIN]
DOCS_TRAN = [cons.Document.TRAN]


class TestFindDelegate(Test):

    def get_blank_project(self):

        project = self.get_project()
        rows = range(len(project.times))
        project.clear_texts(rows, cons.Document.MAIN)
        project.clear_texts(rows, cons.Document.TRAN)
        return project

    def get_uniform_project(self):

        project = self.get_project()
        for texts in (project.main_texts, project.tran_texts):
            for i in range(len(texts)):
                texts[i] = TEXT
        return project

    def test_find_next_match(self):

        project = self.get_uniform_project()
        project.set_find_regex(r'pin\.')
        row = 0
        doc = cons.Document.MAIN
        pos = 0
        for i in range(100):
            row, doc, match_span = project.find_next(row, doc, pos)
            pos = match_span[1]
            assert match_span == (25, 29)

    def test_find_next_match_docs(self):

        project = self.get_uniform_project()
        project.set_find_regex(r'pin\.')
        for docs in (DOCS_ALL, DOCS_MAIN, DOCS_TRAN):
            project.set_find_target(docs=docs)
            row = 0
            doc = docs[0]
            pos = 0
            docs_found = []
            for i in range(100):
                row, doc, match_span = project.find_next(row, doc, pos)
                if doc not in docs_found:
                    docs_found.append(doc)
                pos = match_span[1]
            assert docs_found == docs

    def test_find_next_match_rows(self):

        project = self.get_uniform_project()
        project.set_find_regex(r'pin\.')
        project.set_find_target(rows=[0, 1])
        row = 0
        doc = cons.Document.MAIN
        pos = 0
        for i in range(100):
            row, doc, match_span = project.find_next(row, doc, pos)
            assert row in [0, 1]
            pos = match_span[1]

    def test_find_next_match_wrap(self):

        project = self.get_uniform_project()
        project.set_find_regex(r'pin\.')
        project.set_find_target(wrap=False)
        row = 0
        doc = cons.Document.MAIN
        pos = 0
        try:
            for i in range(100):
                row, doc, match_span = project.find_next(row, doc, pos)
                pos = match_span[1]
            raise AssertionError
        except StopIteration:
            pass

    def test_find_next_none(self):

        project = self.get_blank_project()
        project.set_find_string('test')
        try:
            project.find_next(0, cons.Document.MAIN)
            raise AssertionError
        except StopIteration:
            pass

    def test_find_previous_match(self):

        project = self.get_uniform_project()
        project.set_find_regex(r'pin\.')
        row = 5
        doc = cons.Document.MAIN
        pos = 5
        for i in range(100):
            row, doc, match_span = project.find_previous(row, doc, pos)
            pos = match_span[0]
            assert match_span == (25, 29)

    def test_find_previous_match_docs(self):

        project = self.get_uniform_project()
        project.set_find_regex(r'pin\.')
        for docs in (DOCS_ALL, DOCS_MAIN, DOCS_TRAN):
            project.set_find_target(docs=docs)
            row = 5
            doc = docs[0]
            pos = 5
            docs_found = []
            for i in range(100):
                row, doc, match_span = project.find_previous(row, doc, pos)
                if doc not in docs_found:
                    docs_found.append(doc)
                pos = match_span[0]
            assert docs_found == docs

    def test_find_previous_match_rows(self):

        project = self.get_uniform_project()
        project.set_find_regex(r'pin\.')
        project.set_find_target(rows=[0, 1])
        row = 1
        doc = cons.Document.MAIN
        pos = 5
        for i in range(100):
            row, doc, match_span = project.find_previous(row, doc, pos)
            assert row in [0, 1]
            pos = match_span[0]

    def test_find_previous_match_wrap(self):

        project = self.get_uniform_project()
        project.set_find_regex(r'pin\.')
        project.set_find_target(wrap=False)
        row = 5
        doc = cons.Document.MAIN
        pos = 5
        try:
            for i in range(100):
                row, doc, match_span = project.find_previous(row, doc, pos)
                pos = match_span[0]
            raise AssertionError
        except StopIteration:
            pass

    def test_find_previous_none(self):

        project = self.get_blank_project()
        project.set_find_string('test')
        try:
            project.find_previous(5, cons.Document.TRAN)
            raise AssertionError
        except StopIteration:
            pass

    def test_replace(self):

        def replace_and_assert(project):
            new_text = \
                'Said he xxx wounded by a pin.\n' \
                'He\'s convalescing at home.'
            project.replace()
            assert project.main_texts[0] == new_text
            project.undo()
            assert project.main_texts[0] == TEXT
            project.redo()
            assert project.main_texts[0] == new_text

        project = self.get_uniform_project()
        project.set_find_string('WAS', True)
        project.set_find_replacement('xxx')
        project.find_next(0, cons.Document.MAIN)
        replace_and_assert(project)

        project = self.get_uniform_project()
        project.set_find_regex(r'\bwas\b', re.DOTALL)
        project.set_find_replacement('xxx')
        project.find_next(0, cons.Document.MAIN)
        replace_and_assert(project)

    def test_replace_all(self):

        def replace_all_and_assert(project):
            new_text = \
                'Said he xxx wounded by a pin.\n' \
                'He\'s convalescing at home.'
            project.replace_all()
            for texts in (project.main_texts, project.tran_texts):
                for text in texts:
                    assert text == new_text
            project.undo()
            for texts in (project.main_texts, project.tran_texts):
                for text in texts:
                    assert text == TEXT
            project.redo()
            for texts in (project.main_texts, project.tran_texts):
                for text in texts:
                    assert text == new_text

        project = self.get_uniform_project()
        project.set_find_string('was')
        project.set_find_replacement('xxx')
        replace_all_and_assert(project)

        project = self.get_uniform_project()
        project.set_find_regex(r'\bwas\b', re.DOTALL)
        project.set_find_replacement('xxx')
        replace_all_and_assert(project)

    def test_set_find_regex(self):

        project = self.get_blank_project()
        project.set_find_regex(r'test', re.DOTALL)

    def test_set_find_replacement(self):

        project = self.get_blank_project()
        project.set_find_replacement('test')

    def test_set_find_string(self):

        project = self.get_blank_project()
        project.set_find_string('test')

    def test_set_find_target(self):

        project = self.get_blank_project()
        project.set_find_target([1, 2], DOCS_ALL, True)
