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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Checking and correcting spelling."""

import aeidon
import contextlib
import os
import re
import traceback

with contextlib.suppress(Exception):
    from gi.repository import Spelling
    Spelling.init()

__all__ = ("SpellChecker", "SpellCheckNavigator", "SpellCheckTokenizer")


class SpellChecker:

    """Checking the spelling of an individual word."""

    def __init__(self, language):
        """Initialize a :class:`SpellChecker` instance."""
        provider = Spelling.Provider.get_default()
        if not provider.supports_language(language):
            raise aeidon.Error('Language "{}" not supported'.format(language))
        self.checker = Spelling.Checker.new(provider, language)
        self.language = language
        self.replacements = []
        self.session_words = set()
        self.read_replacements()

    def add_replacement(self, word, replacement):
        """Inform that `word` is to be replaced with `replacement`."""
        self.replacements.append((word, replacement))

    def add_to_personal(self, word):
        """Add `word` to personal word list."""
        self.checker.add_word(word)

    def add_to_session(self, word):
        """Add `word` to session word list."""
        # libspelling's ignore_word applies to a dictionary shared
        # between all checkers of the same language, so keep the
        # session word list per-checker here, like Gspell had it.
        self.session_words.add(word)

    @classmethod
    def available(cls):
        """Return ``True`` if spell-check is available."""
        return "Spelling" in globals()

    def check(self, word, leading_context="", trailing_context=""):
        """Return ``True`` if `word` is correct, ``False`` otherwise."""
        # Include special cases to deal with suboptimal tokenization
        # and informal spoken language common in subtitles.
        if self.language.startswith("en"):
            if word.endswith("in") and trailing_context.startswith("'"):
                # Also check word with formal "ing" ending.
                return self.check_any(word, word + "g")
            for suffix in ["'d", "'ll", "'re", "'s", "'ve"]:
                # Strip certain suffixes to also check just the main word.
                # https://en.wikipedia.org/wiki/English_possessive
                # https://en.wikipedia.org/wiki/Contraction_(grammar)#English
                if word.endswith(suffix):
                    return self.check_any(word, word[:-len(suffix)])
            if (re.match(r"^\d*?(?<!1)1st$", word) or
                re.match(r"^\d*?(?<!1)2nd$", word) or
                re.match(r"^\d*?(?<!1)3rd$", word) or
                re.match(r"^\d*?(?<=1)1th$", word) or
                re.match(r"^\d*?(?<=1)2th$", word) or
                re.match(r"^\d*?(?<=1)3th$", word) or
                re.match(r"^\d*?[0,4-9]th$", word)):
                # Accept ordinal numerals comprised of number and suffix.
                # https://en.wikipedia.org/wiki/English_numerals#Ordinal_numbers
                return True
        return self._check_word(word)

    def check_all(self, *words):
        """Return ``True`` if all of `words` are correct, ``False`` otherwise."""
        return all(self._check_word(x) for x in words)

    def check_any(self, *words):
        """Return ``True`` if any of `words` is correct, ``False`` otherwise."""
        return any(self._check_word(x) for x in words)

    def _check_word(self, word):
        """Return ``True`` if `word` is correct, ``False`` otherwise."""
        if word in self.session_words: return True
        return self.checker.check_word(word, -1)

    @classmethod
    def list_languages(cls):
        """Return a list of supported language codes."""
        languages = Spelling.Provider.get_default().list_languages()
        codes = [x.get_code() for x in languages]
        # Filter out odd Enchant entries, e.g. "en-variant_0" and
        # "en-w_accents", that are not valid locale codes.
        return sorted(filter(aeidon.locales.is_valid, codes))

    def read_replacements(self):
        """Read list of replacements from file."""
        if not os.path.isfile(self.replacement_file): return
        try:
            lines = aeidon.util.readlines(self.replacement_file)
            lines = aeidon.util.get_unique(lines)
            lines = list(filter(lambda x: x.strip(), lines))
            self.replacements = [tuple(x.strip().split("|", 1)) for x in lines]
        except OSError:
            traceback.print_exc()

    @property
    def replacement_file(self):
        """Return path to the replacement file."""
        directory = os.path.join(aeidon.CONFIG_HOME_DIR, "spell-check")
        return os.path.join(directory, "{}.repl".format(self.language))

    def suggest(self, word):
        """Return a list of suggestions for `word`."""
        custom = [y for x, y in self.replacements if x == word]
        if "I" in word:
            # Add the most common OCR replacement.
            replacement = word.replace("I", "l")
            if self.check(replacement):
                custom.append(replacement)
        if re.match(r"^\d+\D+$", word):
            # Add a common OCR fix of missing space between number and unit.
            replacement = re.sub(r"^(\d+)(\D+)$", r"\1 \2", word)
            if self.check_all(*replacement.split()):
                custom.append(replacement)
        suggestions = self.checker.list_corrections(word) or []
        return aeidon.util.get_unique(custom + suggestions)

    def write_replacements(self):
        """Write list of replacements to file."""
        if not self.replacements: return
        replacements = aeidon.util.get_unique(
            self.replacements, keep_last=True)[-10000:]
        text = "\n".join("|".join(x) for x in replacements) + "\n"
        try:
            aeidon.util.write(self.replacement_file, text)
        except OSError:
            traceback.print_exc()


class SpellCheckNavigator:

    """Iterating over spelling errors in a piece of text."""

    def __init__(self, language):
        """Return a :class:`SpellCheckNavigator` instance."""
        self.checker = SpellChecker(language)
        self.pos = 0
        self.replacements = {}
        self.text = None
        self.tokenizer = SpellCheckTokenizer("")
        self.word = None

    def __iter__(self):
        return self

    def __next__(self):
        """Iterate over spelling errors in text."""
        initial_pos = self.pos
        self.tokenizer.text = self.text[initial_pos:]
        for pos, word in self.tokenizer.tokenize():
            self.pos = initial_pos + pos
            self.word = word
            leading = self.leading_context(1)
            trailing = self.trailing_context(1)
            if self.checker.check(word, leading, trailing): continue
            if word in self.replacements:
                self.replace(self.replacements[word])
                return self.__next__()
            return self.pos, self.word
        raise StopIteration

    def add(self):
        """Add the current word to personal word list."""
        self.checker.add_to_personal(self.word)

    def _delete_at(self, i):
        """Delete character in text at index `i`."""
        self.text = self.text[:i] + self.text[i+1:]

    @property
    def endpos(self):
        """The end position of the current word."""
        return self.pos + len(self.word)

    def ignore(self):
        """Ignore the current word."""
        self.pos = self.endpos

    def ignore_all(self):
        """Ignore the current word and any subsequent instances."""
        self.checker.add_to_session(self.word)
        self.pos = self.endpos

    def join_with_next(self):
        """Join the current word with the next."""
        while self.trailing_context(1).isspace():
            self._delete_at(self.endpos)

    def join_with_previous(self):
        """Join the current word with the previous."""
        while self.leading_context(1).isspace():
            self._delete_at(self.pos - 1)
            self.pos -= 1
        # Rewind position to the start of the new compound word.
        while self.leading_context(1).isalnum():
            self.pos -= 1

    def leading_context(self, n):
        """Return `n` characters before the current word."""
        return self.text[:self.pos][-n:]

    def replace(self, replacement):
        """Replace the current word with `replacement`."""
        self.checker.add_replacement(self.word, replacement)
        self.text = self.text[:self.pos] + replacement + self.text[self.endpos:]
        self.pos += len(replacement)

    def replace_all(self, replacement):
        """Replace the current word and subsequent instances with `replacement`."""
        self.replacements[self.word] = replacement
        self.replace(replacement)

    def reset(self, text):
        """Clear the iteration state."""
        self.pos = 0
        self.text = text
        self.word = None

    def suggest(self):
        """Return a list of suggestions for the current word."""
        return self.checker.suggest(self.word)

    def trailing_context(self, n):
        """Return `n` characters after the current word."""
        return self.text[self.endpos:][:n]


class SpellCheckTokenizer:

    """Splitting text to words for spell-check."""

    # XXX: This is unlikely to work well for all languages.

    def __init__(self, text):
        """Initialize a :class:`SpellCheckTokenizer` instance."""
        self.text = text

    def tokenize(self):
        """Iterate over words in text."""
        i = 0
        while i < len(self.text):
            if self.text[i].isalnum():
                word = re.split(r"(?!')\W+", self.text[i:])[0]
                word = re.sub(r"\W+$", "", word)
                if len(word) > 1 and not word.isdigit():
                    yield (i, word)
                i += len(word)
            else:
                i += 1
