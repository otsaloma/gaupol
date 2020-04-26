# -*- coding: utf-8 -*-

# Copyright (C) 2019 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import aeidon


class TestSpellChecker(aeidon.TestCase):

    def setup_method(self, method):
        language = self.get_spell_check_language("en")
        self.checker = aeidon.SpellChecker(language)

    def test_add_replacement(self):
        self.checker.add_replacement("abc", "xyz")
        suggestions = self.checker.suggest("abc")
        assert suggestions and suggestions[0] == "xyz"

    def test_add_to_session(self):
        assert not self.checker.check("asdf")
        self.checker.add_to_session("asdf")
        assert self.checker.check("asdf")

    def test_available(self):
        assert aeidon.SpellChecker.available()

    def test_check(self):
        assert self.checker.check("subtitle")
        assert not self.checker.check("substitle")

    def test_list_languages(self):
        assert aeidon.SpellChecker.list_languages()

    def test_suggest(self):
        assert self.checker.suggest("substitle")


class TestSpellCheckNavigator(aeidon.TestCase):

    def setup_method(self, method):
        language = self.get_spell_check_language("en")
        self.navigator = aeidon.SpellCheckNavigator(language)
        self.navigator.text = "She knows the fighting\ntechniques of Panzr Kunst."

    def test_ignore(self):
        error = next(self.navigator)
        assert error == (37, "Panzr")
        self.navigator.ignore()
        error = next(self.navigator)
        assert error == (43, "Kunst")
        self.navigator.ignore()
        self.assert_raises(StopIteration, self.navigator.__next__)

    def test_ignore_all(self):
        error = next(self.navigator)
        assert error == (37, "Panzr")
        self.navigator.ignore_all()
        self.navigator.reset(self.navigator.text)
        error = next(self.navigator)
        assert error == (43, "Kunst")

    def test_join_with_next(self):
        error = next(self.navigator)
        assert error == (37, "Panzr")
        self.navigator.join_with_next()
        error = next(self.navigator)
        assert error == (37, "PanzrKunst")

    def test_join_with_previous(self):
        error = next(self.navigator)
        assert error == (37, "Panzr")
        self.navigator.ignore()
        error = next(self.navigator)
        assert error == (43, "Kunst")
        self.navigator.join_with_previous()
        error = next(self.navigator)
        assert error == (37, "PanzrKunst")

    def test_leading_context(self):
        error = next(self.navigator)
        assert error == (37, "Panzr")
        assert self.navigator.leading_context(3) == "of "

    def test_replace(self):
        text = self.navigator.text
        text = text.replace("Panzr", "Test")
        error = next(self.navigator)
        assert error == (37, "Panzr")
        self.navigator.replace("Test")
        assert self.navigator.text == text

    def test_replace_all(self):
        self.navigator.reset("abc abc abc")
        error = next(self.navigator)
        self.navigator.replace_all("xyz")
        for error in self.navigator: pass
        assert self.navigator.text == "xyz xyz xyz"

    def test_reset(self):
        error = next(self.navigator)
        self.navigator.reset(self.navigator.text)
        assert next(self.navigator) == error

    def test_suggest(self):
        error = next(self.navigator)
        assert error == (37, "Panzr")
        assert self.navigator.suggest()

    def test_trailing_context(self):
        error = next(self.navigator)
        assert error == (37, "Panzr")
        assert self.navigator.trailing_context(3) == " Ku"


class TestSpellCheckTokenizer(aeidon.TestCase):

    def setup_method(self, method):
        text = "- This is an URM ship?\n- Uh-huh."
        self.tokenizer = aeidon.SpellCheckTokenizer(text)

    def test_tokenize(self):
        assert list(self.tokenizer.tokenize()) == [
            ( 2, "This"),
            ( 7, "is"),
            (10, "an"),
            (13, "URM"),
            (17, "ship"),
            (25, "Uh"),
            (28, "huh"),
        ]
