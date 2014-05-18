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

"""Advanced Sub Station Alpha file."""

import aeidon

__all__ = ("AdvSubStationAlpha",)


class AdvSubStationAlpha(aeidon.files.SubStationAlpha):

    """
    Advanced Sub Station Alpha file.

    :ivar event_fields: Tuple of field names for the ``[Events]`` section
    """

    format = aeidon.formats.ASS

    def __init__(self, path, encoding, newline=None):
        """Initialize an :class:`AdvSubStationAlpha` instance."""
        aeidon.files.SubStationAlpha.__init__(self, path, encoding, newline)
        self.event_fields = (
            "Layer", "Start", "End", "Style", "Name",
            "MarginL", "MarginR", "MarginV", "Effect", "Text")

    def _decode_field(self, field_name, value, subtitle):
        """Save `value` of field as a subtitle attribute."""
        if field_name == "Layer":
            return setattr(subtitle.ssa, "layer", int(value))
        decode = aeidon.files.SubStationAlpha._decode_field
        return decode(self, field_name, value, subtitle)

    def _encode_field(self, field_name, subtitle, doc):
        """Return value of field as string to be written to file."""
        if field_name == "Layer":
            return str(subtitle.ssa.layer)
        encode = aeidon.files.SubStationAlpha._encode_field
        return encode(self, field_name, subtitle, doc)
