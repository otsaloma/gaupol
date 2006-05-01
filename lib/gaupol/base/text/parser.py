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


"""Text parser that allows text editing while keeping tags intact."""


# TODO:
# This parser is experimental and needs more testing. Possible problems with
# the "replace" and "substitute" methods after shifting tags include at least:
#   * Tags might overlap
#   * Tags that were in the middle of a match might end up in the wrong place
#   * Tags might be shifted further than the text length


try:
    from psyco.classes import *
except ImportError:
    pass


STR, POS = 0, 1


class TextParser(object):

    """
    Text parser that allows text editing while keeping tags intact.

    Parser can be used by first setting text to it, then performing operations
    on the pure text and finally getting the full text back.
    """

    def __init__(self, re_tag=None):

        # Regular expression for any tag
        self.re_tag = re_tag

        # Tagless text
        self.text = None

        # List of lists [tag, position]
        self.tags = None

    def get_text(self):
        """Reassemble text and return it."""

        text = self.text[:]

        for entry in self.tags:
            tag, start = entry
            text = text[:start] + tag + text[start:]

        return text

    def replace(self, pattern, replacement):
        """
        Perform simple string replacement on text.

        Beware of infinite recursion caused by replacement matching pattern.
        """
        while True:

            start = self.text.find(pattern)
            if start == -1:
                break

            # Perform replace.
            len_before = len(self.text)
            self.text = self.text.replace(pattern, replacement)
            shift = len(self.text) - len_before

            # Shift tags.
            self._shift_tags(start, shift)

    def set_text(self, text):
        """Set text and parse it for tags."""

        self.tags = []

        if self.re_tag is None:
            self.text = text
            return

        for match in self.re_tag.finditer(text):
            start, end = match.span()
            self.tags.append([text[start:end], start])

        self.text = self.re_tag.sub('', text)

    def _shift_tags(self, start, shift):
        """
        Shift tags.

        All tags that are positioned after start in tagless text are shifted
        shift amount either forward or backward.
        """
        # Get length of tags before start.
        len_tags = 0
        start_with_tags = start
        for tag, position in self.tags:
            if position <= start_with_tags:
                len_tags += len(tag)
                start_with_tags += len(tag)

        # Shift tags.
        for i in range(len(self.tags)):
            if self.tags[i][POS] > start + len_tags:
                self.tags[i][POS] += shift
                if self.tags[i][POS] < 0:
                    self.tags[i][POS] = 0

    def substitute(self, regex, replacement):
        """
        Perform a regular expression substitution on text.

        Beware of infinite recursion caused by replacement matching pattern.
        """
        while True:

            match = regex.search(self.text)
            if match is None:
                break

            start = match.span()[0]

            # Perform substitution.
            len_before = len(self.text)
            self.text = regex.sub(replacement, self.text, 1)
            shift = len(self.text) - len_before

            # Shift tags.
            self._shift_tags(start, shift)


if __name__ == '__main__':

    import re
    from gaupol.test import Test

    re_tag = re.compile(r'<.*?>')

    class TestTextParser(Test):

        def __init__(self):

            Test.__init__(self)
            self.parser = TextParser(re_tag)

        def test_replace(self):

            text = '<i>He changed shifts.</i>\n' \
                   'Didn\'t <i>he</i> tell you?'
            self.parser.set_text(text)
            self.parser.replace('i', '*')
            text = self.parser.get_text()
            assert text == '<i>He changed sh*fts.</i>\n' \
                           'D*dn\'t <i>he</i> tell you?'

        def test_substitute(self):

            text = '<i>He changed shifts.</i>\n' \
                   'Didn\'t <i>he</i> tell you?'
            self.parser.set_text(text)
            self.parser.substitute(re.compile(r'[hHi]'), '*')
            text = self.parser.get_text()
            assert text == '<i>*e c*anged s**fts.</i>\n' \
                           'D*dn\'t <i>*e</i> tell you?'

    TestTextParser().run()
