# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""MicroDVD tag library."""

import gaupol
import re

from .taglib import TagLibrary


class MicroDVD(TagLibrary):

    """MicroDVD tag library."""

    format = gaupol.FORMAT.MICRODVD

    @property
    @gaupol.util.once
    def italic_tag(self):
        """Regular expression for an italic tag."""

        return re.compile(r"\{y:i\}", re.IGNORECASE)

    @property
    @gaupol.util.once
    def tag(self):
        """Regular expression for any tag."""

        return re.compile(r"\{[a-z]:[^{]*?\}", re.IGNORECASE)

    @gaupol.util.once
    def _get_decode_tags(self):
        """Get list of tuples of regular expression, replacement, count."""

        FLAGS = re.MULTILINE | re.DOTALL

        tags = [
            # Style x3 (single line)
            (r"\{y:(b|i|u)[^\}]*?(b|i|u)[^\}]*?(b|i|u)\}(.*?)$", FLAGS,
                r"<\1><\2><\3>\4</\3></\2></\1>", 1),
            # Style x2 (single line)
            (r"\{y:(b|i|u)[^\}]*?(b|i|u)\}(.*?)$", FLAGS,
                r"<\1><\2>\3</\2></\1>", 2),
            # Style x1 (single line)
            (r"\{y:(b|i|u)\}(.*?)$", FLAGS,
                r"<\1>\2</\1>", 3),
            # Style x3 (whole subtitle)
            (r"\{Y:(b|i|u)[^\}]*?(b|i|u)[^\}]*?(b|i|u)\}(.*?)\Z", FLAGS,
                r"<\1><\2><\3>\4</\3></\2></\1>", 1),
            # Style x2 (whole subtitle)
            (r"\{Y:(b|i|u)[^\}]*?(b|i|u)\}(.*?)\Z", FLAGS,
                r"<\1><\2>\3</\2></\1>", 2),
            # Style x1 (whole subtitle)
            (r"\{Y:(b|i|u)\}(.*?)\Z", FLAGS,
                r"<\1>\2</\1>", 3),
            # Color (single line)
            (r"\{c:\$([a-zA-Z0-9]{6})\}(.*?)$", FLAGS,
                r'<color="#\1">\2</color>', 1),
            # Color (whole subtitle)
            (r"\{C:\$([a-zA-Z0-9]{6})\}(.*?)\Z", FLAGS,
                r'<color="#\1">\2</color>', 1),
            # Font (single line)
            (r"\{f:([^{]*?)\}(.*?)$", FLAGS,
                r'<font="\1">\2</font>', 1),
            # Font (whole subtitle)
            (r"\{F:([^{]*?)\}(.*?)\Z", FLAGS,
                r'<font="\1">\2</font>', 1),
            # Size (single line)
            (r"\{s:(\d+)\}(.*?)$", FLAGS,
                r'<size="\1">\2</size>', 1),
            # Size (whole subtitle)
            (r"\{S:(\d+)\}(.*?)\Z", FLAGS,
                r'<size="\1">\2</size>', 1),
            # Remove all other tags.
            (r"\{.:[^{]*?\}", re.IGNORECASE,
                r"", 1),]

        for i, (pattern, flags, replacement, count) in enumerate(tags):
            tags[i] = (re.compile(pattern, flags), replacement, count)
        return tags

    @gaupol.util.once
    def _get_encode_tags(self):
        """Get list of tuples of regular expression, replacement, count."""

        FLAGS = re.MULTILINE | re.DOTALL

        tags = [
            # Remove duplicate style tags (e.g. <b>test</b><b>test</b>).
            (r"</(b|i|u)>(\n?)<\1>", FLAGS,
                r"\2", 3),
            # Remove other duplicate tags.
            (r"<([^<]*?)=([^<]*?)>(.*?)</\1>(\n?)<\1=\2>", FLAGS,
                r"<\1=\2>\3\4", 3),
            # Style (affecting a single line subtitle fully)
            (r"\A<(b|i|u)>(.*?)</\1>\Z", re.MULTILINE,
                r"{Y:\1}\2", 3),
            # Style (affecting only one line)
            (r"<(b|i|u)>(.*?)</\1>", re.MULTILINE,
                r"{y:\1}\2", 3),
            # Style (affecting whole subtitle)
            (r"<(b|i|u)>(.*?)</\1>", FLAGS,
                r"{Y:\1}\2", 3),
            # Color (affecting a single line subtitle fully)
            (r'\A<color="#(.{6})">(.*?)</color>\Z', re.MULTILINE,
                r"{C:$\1}\2", 1),
            # Color (affecting only one line)
            (r'<color="#(.{6})">(.*?)</color>', re.MULTILINE,
                r"{c:$\1}\2", 1),
            # Color (affecting whole subtitle)
            (r'<color="#(.{6})">(.*?)</color>', FLAGS,
                r"{C:$\1}\2", 1),
            # Font (affecting a single line subtitle fully)
            (r'\A<font="([^<]*?)">(.*?)</font>\Z', re.MULTILINE,
                r"{F:\1}\2", 1),
            # Font (affecting only one line)
            (r'<font="([^<]*?)">(.*?)</font>', re.MULTILINE,
                r"{f:\1}\2", 1),
            # Font (affecting whole subtitle)
            (r'<font="([^<]*?)">(.*?)</font>', FLAGS,
                r"{F:\1}\2", 1),
            # Size (affecting a single line subtitle fully)
            (r'\A<size="([^<]*?)">(.*?)</size>\Z', re.MULTILINE,
                r"{S:\1}\2", 1),
            # Size (affecting only one line)
            (r'<size="([^<]*?)">(.*?)</size>', re.MULTILINE,
                r"{s:\1}\2", 1),
            # Size (affecting whole subtitle)
            (r'<size="([^<]*?)">(.*?)</size>', FLAGS,
                r"{S:\1}\2", 1),]

        for i, (pattern, flags, replacement, count) in enumerate(tags):
            tags[i] = (re.compile(pattern, flags), replacement, count)
        return tags

    def decode(self, text):
        """Return text with tags converted from this to internal format."""

        for regex, replacement, count in self._get_decode_tags():
            for i in range(count):
                # pylint: disable-msg=E1101
                text = regex.sub(replacement, text)
        return text

    def encode(self, text):
        """Return text with tags converted from internal to this format."""

        for regex, replacement, count in self._get_encode_tags():
            for i in range(count):
                # pylint: disable-msg=E1101
                text = regex.sub(replacement, text)
        return text

    def italicize(self, text):
        """Return italicized text."""

        return u"{Y:i}%s" % text
