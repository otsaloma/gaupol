# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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

"""Base class for text markup."""

import aeidon
import re

__all__ = ("Markup",)


class Markup(aeidon.Singleton):

    """
    Base class for text markup.

    Markup conversions between different formats are done via an internal
    format, which has the following BBcode-style tags with angle brackets.
    Conversions are best done via the ``_decode_*`` and ``_encode_*`` methods
    rather than hard-coding internal tags in regular expression substitutions.

     * ``<b>...................</b>``
     * ``<i>...................</i>``
     * ``<u>...................</u>``
     * ``<color=#RRGGBB>...</color>``
     * ``<font=NAME>........</font>``
     * ``<size=POINTS>......</size>``

    :class:`Markup` is effectively equivalent to a format with no markup and
    can therefore be merely subclassed with a ``pass``-statement by formats
    that do not implement any markup. The caller of any tagging methods, e.g.
    :meth:`bolden`, must be prepared to handle :exc:`NotImplementedError`.
    """

    _flags = re.DOTALL | re.MULTILINE
    format = aeidon.formats.NONE

    def bolden(self, text, bounds=None):
        """Return bolded `text`."""
        raise NotImplementedError

    def clean(self, text):
        """
        Return `text` with less ugly markup.

        Subclasses can implement this to, for example, remove redundant markup,
        finetune tag positioning or to join or split tags; in general, whatever
        that changes the style of the markup but not that of the text.
        """
        return text

    def colorize(self, text, color, bounds=None):
        """Return `text` colorized to hexadecimal value."""
        raise NotImplementedError

    def decode(self, text):
        """Return `text` with markup converted from this to internal format."""
        text = self._pre_decode(text)
        text = self._main_decode(text)
        return self._post_decode(text)

    def _decode_apply(self, text, regex, replacement, groups):
        """
        Return `text` with all matches of `regex` replaced.

        `replacement` may contain one or more of ``{}``, which are replaced
        with parts of the match as defined by `groups`, a ``tuple`` of numbers.
        """
        orig_text = text
        match = regex.search(text)
        if match is None: return text
        a, z = match.span()
        new = replacement.format(*tuple(map(match.group, groups)))
        text = "".join((text[:a], new, text[z:]))
        if text == orig_text: return text
        return self._decode_apply(text, regex, replacement, groups)

    def _decode_b(self, text, pattern, target, flags=0):
        """Return `text` with bold markup converted to internal format."""
        regex = self._get_regex(pattern, flags)
        replacement = "<b>{}</b>"
        return self._decode_apply(text, regex, replacement, (target,))

    def _decode_c(self, text, pattern, value, target, flags=0):
        """Return `text` with color markup converted to internal format."""
        regex = self._get_regex(pattern, flags)
        replacement = "<color=#{}>{}</color>"
        return self._decode_apply(text, regex, replacement, (value, target))

    def _decode_f(self, text, pattern, value, target, flags=0):
        """Return `text` with font markup converted to internal format."""
        regex = self._get_regex(pattern, flags)
        replacement = "<font={}>{}</font>"
        return self._decode_apply(text, regex, replacement, (value, target))

    def _decode_i(self, text, pattern, target, flags=0):
        """Return `text` with italic markup converted to internal format."""
        regex = self._get_regex(pattern, flags)
        replacement = "<i>{}</i>"
        return self._decode_apply(text, regex, replacement, (target,))

    def _decode_s(self, text, pattern, value, target, flags=0):
        """Return `text` with size markup converted to internal format."""
        regex = self._get_regex(pattern, flags)
        replacement = "<size={}>{}</size>"
        return self._decode_apply(text, regex, replacement, (value, target))

    def _decode_u(self, text, pattern, target, flags=0):
        """Return `text` with underline markup converted to internal format."""
        regex = self._get_regex(pattern, flags)
        replacement = "<u>{}</u>"
        return self._decode_apply(text, regex, replacement, (target,))

    def encode(self, text):
        """Return `text` with markup converted from internal to this format."""
        text = self._encode_b(text)
        text = self._encode_c(text)
        text = self._encode_f(text)
        text = self._encode_i(text)
        text = self._encode_s(text)
        return self._encode_u(text)

    def _encode_apply(self, text, regex, method, target, value=None):
        """
        Return `text` with internal tags removed and `method` applied.

        `method` should be one the tagging methods, e.g. meth:`bolden`.
        `target` and `value` should be group numbers in `regex`.
        """
        orig_text = text
        match = regex.search(text)
        if match is None: return text
        text = regex.sub(r"\{}".format(target), text, 1)
        a = match.start()
        z = a + len(match.group(target))
        args = (text, (a, z))
        if value is not None:
            args = (text, match.group(value), (a, z))
        with aeidon.util.silent(NotImplementedError):
            text = method(*args)
        if text == orig_text: return text
        return self._encode_apply(text, regex, method, target, value)

    def _encode_b(self, text):
        """Return `text` with bold markup converted to this format."""
        regex = self._get_regex(r"<b>(.*?)</b>")
        return self._encode_apply(text, regex, self.bolden, 1)

    def _encode_c(self, text):
        """Return `text` with color markup converted to this format."""
        regex = self._get_regex(r"<color=#([a-fA-F0-9]{6})>(.*?)</color>")
        return self._encode_apply(text, regex, self.colorize, 2, 1)

    def _encode_f(self, text):
        """Return `text` with font markup converted to this format."""
        regex = self._get_regex(r"<font=(.+?)>(.*?)</font>")
        return self._encode_apply(text, regex, self.fontify, 2, 1)

    def _encode_i(self, text):
        """Return `text` with italic markup converted to this format."""
        regex = self._get_regex(r"<i>(.*?)</i>")
        return self._encode_apply(text, regex, self.italicize, 1)

    def _encode_s(self, text):
        """Return `text` with size markup converted to this format."""
        regex = self._get_regex(r"<size=(\d+)>(.*?)</size>")
        return self._encode_apply(text, regex, self.scale, 2, 1)

    def _encode_u(self, text):
        """Return `text` with underline markup converted to this format."""
        regex = self._get_regex(r"<u>(.*?)</u>")
        return self._encode_apply(text, regex, self.underline, 1)

    def fontify(self, text, font, bounds=None):
        """Return `text` changed to `font`."""
        raise NotImplementedError

    @aeidon.deco.memoize(100)
    def _get_regex(self, pattern, flags=0):
        """Return compiled regular expression from cache."""
        flags = self._flags | flags
        return re.compile(pattern, flags)

    @property
    def italic_tag(self):
        """Regular expression for an italic markup tag or ``None``."""
        return None

    def italicize(self, text, bounds=None):
        """Return italicized `text`."""
        raise NotImplementedError

    def _main_decode(self, text):
        """Return `text` with decodable markup decoded."""
        return text

    def _post_decode(self, text):
        """Return `text` with markup finalized after decoding."""
        return text

    def _pre_decode(self, text):
        """Return `text` with markup prepared for decoding."""
        return text

    def scale(self, text, size, bounds=None):
        """Return `text` scaled to `size`."""
        raise NotImplementedError

    def _substitute(self, text, pattern, replacement, flags=0):
        """Return `text` with matches of `pattern` replaced."""
        regex = self._get_regex(pattern, flags)
        return regex.sub(replacement, text)

    @property
    def tag(self):
        """Regular expression for any markup tag or ``None``."""
        return None

    def underline(self, text, bounds=None):
        """Return underlined `text`."""
        raise NotImplementedError
