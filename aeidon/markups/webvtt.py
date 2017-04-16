# -*- coding: utf-8 -*-

# Copyright (C) 2017 Osmo Salomaa
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

"""Text markup for the WebVTT format."""

import aeidon

__all__ = ("WebVTT",)


class WebVTT(aeidon.markups.SubRip):

    """
    Text markup for the WebVTT format.

    WebVTT is very similar to the SubRip format, except it doesn't support the
    <font> tag and it includes a few other tags, such as the class tag <c>,
    which we cannot support for conversions.

    https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API
    """

    format = aeidon.formats.WEBVTT

    def colorize(self, text, color, bounds=None):
        """Return `text` colorized to hexadecimal value."""
        raise NotImplementedError

    def _main_decode(self, text):
        """Return `text` with decodable markup decoded."""
        text = self._decode_b(text, r"<b>(.*?)</b>", 1)
        text = self._decode_i(text, r"<i>(.*?)</i>", 1)
        return self._decode_u(text, r"<u>(.*?)</u>", 1)

    def _post_decode(self, text):
        """Return `text` with markup finalized after decoding."""
        # Remove all unsupported markup tags.
        text = self._substitute(text, r"</?[^biu]>", "")
        return self._substitute(text, r"</?[^/>]{2,}>", "")
