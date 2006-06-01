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


"""Advanced Sub Station Alpha file."""


from gaupol.base          import cons
from gaupol.base.file.ssa import SubStationAlpha


class AdvancedSubStationAlpha(SubStationAlpha):

    """Advanced Sub Station Alpha file."""

    format     = cons.Format.ASS
    identifier = r'^ScriptType: v4.00\+\s*$', 0

    header_template = \
'''[Script Info]
Title:
Original Script:
Original Translation:
Original Editing:
Original Timing:
Synch Point:
Script Updated By:
Update Details:
ScriptType: v4.00+
Collisions: Normal
PlayResY:
PlayResX:
PlayDepth:
Timer: 100.0000
WrapStyle:

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,18,&H00ffffff,&H0000ffff,&H00000000,&H00000000,0,0,0,0,100,100,0,0.00,1,2,2,2,30,30,10,0'''

    event_fields = (
        'Layer',
        'Start',
        'End',
        'Style',
        'Name',
        'MarginL',
        'MarginR',
        'MarginV',
        'Effect',
        'Text'
    )
