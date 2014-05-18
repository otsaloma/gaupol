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

"""Text markup for the MicroDVD format."""

import aeidon

__all__ = ("MicroDVD",)


class MicroDVD(aeidon.Markup):

    """
    Text markup for the MicroDVD format.

    The MicroDVD format contains a lot of markup tags, of which the following
    are of interest to us. Tags that start with a lower case letter end at the
    end of the line, upper case ones at the end of the subtitle.

     * ``{c:$BBGGRR}..., {C:$BBGGRR}...``
     * ``{f:NAME}......, {F:NAME}......``
     * ``{s:SIZE}......, {S:SIZE}......``
     * ``{y:STYLE}....., {Y:STYLE}.....``

    Note the reverse order of the color tag, ``BBGGRR`` instead of the normal
    ``RRGGBB``. ``STYLE`` in the ``y`` is a string containing one or more of
    the letters "b", "i" and "u" and any amount of any possible separators or
    other characters.
    """

    format = aeidon.formats.MICRODVD

    def bolden(self, text, bounds=None):
        """Return bolded `text`."""
        return self._style(text, "Y", "y", "b", bounds)

    def colorize(self, text, color, bounds=None):
        """Return `text` colorized to hexadecimal value."""
        # Reverse the color value from RRGGBB to BBGGRR.
        color = "${}{}{}".format(color[4:], color[2:4], color[:2])
        return self._style(text, "C", "c", color, bounds)

    def fontify(self, text, font, bounds=None):
        """Return `text` changed to `font`."""
        return self._style(text, "F", "f", font, bounds)

    @property
    def italic_tag(self):
        """Regular expression for an italic markup tag."""
        return self._get_regex(r"\{[Yy]:i\}")

    def italicize(self, text, bounds=None):
        """Return italicized `text`."""
        return self._style(text, "Y", "y", "i", bounds)

    def _main_decode(self, text):
        """Return `text` with decodable markup decoded."""
        text = self._decode_b(text, r"\{([Yy]:b)\}(.*?)\{/\1\}", 2)
        text = self._decode_c(text, r"\{([Cc]:#(.*?))\}(.*?)\{/\1\}", 2, 3)
        text = self._decode_f(text, r"\{([Ff]:(.*?))\}(.*?)\{/\1\}", 2, 3)
        text = self._decode_i(text, r"\{([Yy]:i)\}(.*?)\{/\1\}", 2)
        text = self._decode_s(text, r"\{([Ss]:(.*?))\}(.*?)\{/\1\}", 2, 3)
        text = self._decode_u(text, r"\{([Yy]:u)\}(.*?)\{/\1\}", 2)
        return text

    def _pre_decode(self, text):
        """Return `text` with markup prepared for decoding."""
        text = self._pre_decode_break(text)
        text = self._pre_decode_color(text)
        text = self._pre_decode_close(text)
        return text

    def _pre_decode_break(self, text):
        """
        Return `text` with combined markup tags separated.

        For example, ``{y:biu}`` is replaced with ``{y:b}{y:i}{y:u}``.
        """
        pattern = r"\{([Yy]):([^}]{2,})\}"
        regex = self._get_regex(pattern)
        match = regex.search(text)
        if match is None: return text
        y = match.group(1)
        replacement = ""
        for m in ("b", "i", "u"):
            if m in match.group(2):
                replacement += "{{{}:{}}}".format(y, m)
        text = regex.sub(replacement, text, 1)
        return self._pre_decode_break(text)

    def _pre_decode_close(self, text):
        """
        Return `text` with all markup tags closed.

        The artificial closing tags are of form ``{/X:VALUE}``.
        """
        # Add lower case closing tags to the end of each line.
        lines = text.split("\n")
        re_tag = self._get_regex(r"\{([cfsy]:.*?)\}")
        for i, line in enumerate(lines):
            matches = [x for x in re_tag.finditer(line)]
            for j in reversed(range(len(matches))):
                lines[i] += "{{/{}}}".format(matches[j].group(1))
        text = "\n".join(lines)
        # Add upper case closing tags to the end of the text.
        re_tag = self._get_regex(r"\{([CFSY]:.*?)\}")
        matches = [x for x in re_tag.finditer(text)]
        for j in reversed(range(len(matches))):
            text += "{{/{}}}".format(matches[j].group(1))
        return text

    def _pre_decode_color(self, text):
        """
        Return `text` with colors converted to standard hexadecimal form.

        Color tags are converted from ``{c:$BBGGRR}`` to ``{c:#RRGGBB}``.
        """
        regex = self._get_regex(r"\{([Cc]:)\$([0-9A-Fa-f]{6})\}")
        match = regex.search(text)
        if match is None: return text
        color = match.group(2)
        color = "{}{}{}".format(color[4:], color[2:4], color[:2])
        text = regex.sub(r"{{\1#{}}}".format(color), text, 1)
        return self._pre_decode_color(text)

    def scale(self, text, size, bounds=None):
        """Return `text` scaled to `size`."""
        return self._style(text, "S", "s", str(size), bounds)

    def _style(self, text, upper, lower, value, bounds=None):
        """Return `text` wrapped in ``upper`` or ``lower`` markup tag."""
        a, z = bounds or (0, len(text))
        prefix = text[:a].split("\n")[-1]
        suffix = text[z:].split("\n")[0]
        re_alpha = self._get_regex(r"\w")
        # Return plain text if bounds does not define an entire line or
        # subtitle and thus cannot be marked without side-effects.
        if re_alpha.search(prefix): return text
        if re_alpha.search(suffix): return text
        if (not "\n" in text) or ("\n" in text[a:z]):
            tag = "{{{}:{}}}".format(upper, value)
        else:
            tag = "{{{}:{}}}".format(lower, value)
        return "".join((text[:a], "{}{}".format(tag, text[a:])))

    @property
    def tag(self):
        """Regular expression for any markup tag."""
        return self._get_regex(r"\{[CFSYcfsy]:.*?\}")

    def underline(self, text, bounds=None):
        """Return underlined `text`."""
        return self._style(text, "Y", "y", "u", bounds)
