# Copyright (C) 2005-2009 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Enumerations for subtitle file format types.

Mime-types of subtitle file formats conform to those defined in
freedesktop.org's shared-mime-info package [1]. For all formats not included in
shared-mime-info, 'text/plain' is used as the mime-type.

 [1] http://freedesktop.org/wiki/Software/shared-mime-info
"""

import gaupol

__all__ = ("formats",)


class AdvSubStationAlpha(gaupol.EnumerationItem):

    container = "ssa"
    extension = ".ass"
    has_header = True
    identifier = r"^ScriptType:\s*[vV]4.00\+\s*$"
    label = "Advanced Sub Station Alpha"
    mime_type = "text/x-ssa"


class MicroDVD(gaupol.EnumerationItem):

    container = None
    extension = ".sub"
    has_header = True
    identifier = r"^\{-?\d+\}\{-?\d+\}"
    label = "MicroDVD"
    mime_type = "text/x-microdvd"


class MPL2(gaupol.EnumerationItem):

    container = None
    extension = ".txt"
    has_header = False
    identifier = r"^\[-?\d+\]\[-?\d+\]"
    label = "MPL2"
    mime_type = "text/plain"


class MPsub(gaupol.EnumerationItem):

    container = None
    extension = ".sub"
    has_header = True
    identifier = r"^FORMAT=(TIME|[\d.]+)\s*$"
    label = "MPsub"
    mime_type = "text/x-mpsub"


class SubRip(gaupol.EnumerationItem):

    container = "subrip"
    extension = ".srt"
    has_header = False
    identifier = (
        r"^-?\d\d:\d\d:\d\d,\d\d\d -->"
        r" -?\d\d:\d\d:\d\d,\d\d\d"
        r"(  X1:\d+ X2:\d+ Y1:\d+ Y2:\d+)?\s*$")
    label = "SubRip"
    mime_type = "application/x-subrip"


class SubStationAlpha(gaupol.EnumerationItem):

    container = "ssa"
    extension = ".ssa"
    has_header = True
    identifier = r"^ScriptType:\s*[vV]4.00\s*$"
    label = "Sub Station Alpha"
    mime_type = "text/x-ssa"


class SubViewer2(gaupol.EnumerationItem):

    container = None
    extension = ".sub"
    has_header = True
    identifier = (
        r"^-?\d\d:\d\d:\d\d\.\d\d"
        r",-?\d\d:\d\d:\d\d\.\d\d\s*$")
    label = "SubViewer 2.0"
    mime_type = "text/x-subviewer"


class TMPlayer(gaupol.EnumerationItem):

    container = None
    extension = ".txt"
    has_header = False
    identifier = r"^-?\d\d:\d\d:\d\d:"
    label = "TMPlayer"
    mime_type = "text/plain"


formats = gaupol.Enumeration()
formats.ASS = AdvSubStationAlpha()
formats.MICRODVD = MicroDVD()
formats.MPL2 = MPL2()
formats.MPSUB = MPsub()
formats.SUBRIP = SubRip()
formats.SSA = SubStationAlpha()
formats.SUBVIEWER2 = SubViewer2()
formats.TMPLAYER = TMPlayer()
