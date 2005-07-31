# Copyright (C) 2005 Osmo Salomaa
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


"""Handling of tags of different subtitle formats."""


import re

try:
    from psyco.classes import *
except ImportError:
    pass


COMMON = re.MULTILINE|re.DOTALL


class MicroDVD(object):

    """MicroDVD tags."""

    # Documentation:
    # http://netti.nic.fi/~temp/easydivx/help/mdvddoc/#step5
    
    TAG = r'\{[a-z]:.*?\}', re.IGNORECASE

    DECODE_TAGS = (
        (    
            # Style x3 (single line)
            r'\{y:(b|i|u).*?(b|i|u).*?(b|i|u)\}(.*?)$', COMMON,
            r'<\1><\2><\3>\4</\1></\2></\3>'
        ), (
            # Style x2 (single line)
            r'\{y:(b|i|u).*?(b|i|u)\}(.*?)$', COMMON,
            r'<\1><\2></\1></\2>'
        ), (
            # Style x1 (single line)
            r'\{y:(b|i|u)\}(.*?)$', COMMON,
            r'<\1>\2</\1>'
        ), (
            # Style x3 (whole subtitle unit)
            r'\{Y:(b|i|u).*?(b|i|u).*?(b|i|u)\}(.*?)\Z', COMMON,
            r'<\1><\2><\3>\4</\1></\2></\3>'
        ), (
            # Style x2 (whole subtitle unit)
            r'\{Y:(b|i|u).*?(b|i|u)\}(.*?)\Z', COMMON,
            r'<\1><\2></\1></\2>'
        ), (
            # Style x1 (whole subtitle unit)
            r'\{Y:(b|i|u)\}(.*?)\Z', COMMON,
            r'<\1>\2</\1>'
        ), (
            # Color (single line)
            r'\{c:\$([a-zA-Z0-9]{6})\}(.*?)$', COMMON,
            r'<color="#\1">\2</color>'
        ), (
            # Color (whole subtitle unit)
            r'\{C:\$([a-zA-Z0-9]{6})\}(.*?)\Z', COMMON,
            r'<color="#\1">\2</color>'
        ), (
            # Font (single line)
            r'\{f:(.*?)\}(.*?)$', COMMON,
            r'<font="\1">\2</font>'
        ), (
            # Font (whole subtitle unit)
            r'\{F:(.*?)\}(.*?)\Z', COMMON,
            r'<font="\1">\2</font>'
        ), (
            # Size (single line)
            r'\{s:(\d+)\}(.*?)$', COMMON,
            r'<size="\1">\2</size>'
        ), (
            # Size (whole subtitle unit)
            r'\{S:(\d+)\}(.*?)\Z', COMMON,
            r'<size="\1">\2</size>'
        ), (
            # Remove all other tags. Includes at least position and coordinate
            # tags.
            r'\{[a-z]:.*?\}', re.IGNORECASE,
            r''
        )
    )

    ENCODE_TAGS = (
        (
            # Remove duplicate style tags (e.g. <b>foo</b><b>bar</b>).
            r'</(b|i|u)>(\n?)<\1>', COMMON,
            r'\2'
        ), (
            # Remove other duplicate tags.
            r'<(.*?)=(.*?)>(.*?)</\1>(\n?)<\1=\2>', COMMON,
            r'<\1=\2>\3\4'
        ), (
            # Style (affecting a single line subtitle fully)
            r'\A<(b|i|u)>(.*?)</\1>\Z', re.MULTILINE,
            r'{Y:\1}\2'
        ), (
            # Style (affecting only one line)
            r'<(b|i|u)>(.*?)</\1>', re.MULTILINE,
            r'{y:\1}\2'
        ), (
            # Style (affecting whole subtitle unit)
            r'<(b|i|u)>(.*?)</\1>', COMMON,
            r'{Y:\1}\2'
        ), (
            # Color (affecting a single line subtitle fully)
            r'\A<color="#(.{6})">(.*?)</color>\Z', re.MULTILINE,
            r'{C:$\1}\2'
        ), (
            # Color (affecting only one line)
            r'<color="#(.{6})">(.*?)</color>', re.MULTILINE,
            r'{c:$\1}\2'
        ), (
            # Color (affecting whole subtitle unit)
            r'<color="#(.{6})">(.*?)</color>', COMMON,
            r'{C:$\1}\2'
        ), (
            # Font (affecting a single line subtitle fully)
            r'\A<font="(.*?)">(.*?)</font>\Z', re.MULTILINE,
            r'{F:\1}\2'
        ), (
            # Font (affecting only one line)
            r'<font="(.*?)">(.*?)</font>', re.MULTILINE,
            r'{f:\1}\2'
        ), (
            # Font (affecting whole subtitle unit)
            r'<font="(.*?)">(.*?)</font>', COMMON,
            r'{F:\1}\2'
        ), (
            # Size (affecting a single line subtitle fully)
            r'\A<size="(.*?)">(.*?)</size>\Z', re.MULTILINE,
            r'{S:\1}\2'
        ), (
            # Size (affecting only one line)
            r'<size="(.*?)">(.*?)</size>', re.MULTILINE,
            r'{s:\1}\2'
        ), (
            # Size (affecting whole subtitle unit)
            r'<size="(.*?)">(.*?)</size>', COMMON,
            r'{S:\1}\2'
        )
    )

    def toggle_italicization(texts):
        """Toggle italicization of texts."""
        
        re_italic_tag = re.compile('\{y:i\}', re.IGNORECASE)

        turn_into_italics = _get_italicize(re_italic_tag, texts)
            
        for i in range(len(texts)):
            texts[i] = re_italic_tag.sub('', texts[i])
            if turn_into_italics:
                texts[i] = '{Y:i}%s' % texts[i]
        
        return texts

    toggle_italicization = staticmethod(toggle_italicization)
    
    
class SubRip(object):

    """SubRip tags."""

    TAG = r'</?(b|i|u)>', re.IGNORECASE
    
    DECODE_TAGS = (
        (
            # Uppercase bold
            r'(</?)B>', None,
            r'\1b>'
        ), (
            # Uppercase italics
            r'(</?)I>', None,
            r'\1i>'
        ), (
            # Uppercase underline
            r'(</?)U>', None,
            r'\1u>'
        )
    )

    ENCODE_TAGS = (
        (
            # Color
            r'</?color.*?>', None,
            r''
        ), (
            # Font
            r'</?font.*?>', None,
            r''
        ), (
            # Size
            r'</?size.*?>', None,
            r''
        )
    )

    def toggle_italicization(texts):
        """Toggle italicization of texts."""
        
        re_italic_tag = re.compile('</?i>', re.IGNORECASE)

        turn_into_italics = _get_italicize(re_italic_tag, texts)
            
        for i in range(len(texts)):
            texts[i] = re_italic_tag.sub('', texts[i])
            if turn_into_italics:
                texts[i] = '<i>%s</i>' % texts[i]
        
        return texts

    toggle_italicization = staticmethod(toggle_italicization)


class TagConverter(object):
    
    """
    Conversions between tags of different subtitle formats.
    
    Tag conversions are done via an internal format, which has a HTML style
    syntax. All essential tags are converted and troublesome tags, such as
    position, and rare tags are removed.

    Internal tags:
    <b></b>
    <i></i>
    <u></u>
    <color="#rrggbb"></color>
    <font="name"></font>
    <size="int"></size>
    """
    
    def __init__(self, from_format, to_format):

        from_tags = eval(from_format).DECODE_TAGS
        to_tags   = eval(to_format).ENCODE_TAGS

        self._from_res = []
        self._to_res   = []

        PATTERN, FLAGS, REPL = 0, 1, 2

        for i in range(len(from_tags)):
            try:
                regex = re.compile(from_tags[i][PATTERN], from_tags[i][FLAGS])
            except TypeError:
                regex = re.compile(from_tags[i][PATTERN])
            self._from_res.append([regex, from_tags[i][REPL]])

        for i in range(len(to_tags)):
            try:
                regex = re.compile(to_tags[i][PATTERN], to_tags[i][FLAGS])
            except TypeError:
                regex = re.compile(to_tags[i][PATTERN])
            self._to_res.append([regex, to_tags[i][REPL]])

    def convert_tags(self, string):
        """Convert subtitle tags in string."""

        if not string:
            return string

        REGEX, REPL = 0, 1

        # Convert to internal format ("decode")
        for i in range(len(self._from_res)):
            string = self._from_res[i][REGEX].sub(self._from_res[i][REPL],
                                                  string)
        
        # Convert to desired format ("encode")
        for i in range(len(self._to_res)):
            string = self._to_res[i][REGEX].sub(self._to_res[i][REPL], string)

        return string


def _get_italicize(re_italic_tag, texts):
    """Return True if texts should italicized, otherwise return False."""
    
    for text in texts:
        if re_italic_tag.match(text) is None:
            return True
            
    return False

def get_tag_re(format):
    """Get regular expression for tag in format."""

    regex, flags = eval(format).TAG
    
    try:
        return re.compile(regex, flags)
    except TypeError:
        return re.compile(regex)
    
def toggle_italicization(format, texts):
    """Toggle italicization of texts in given format."""

    return eval(format).toggle_italicization(texts)
