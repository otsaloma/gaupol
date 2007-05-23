# Copyright (C) 2005-2007 Osmo Salomaa
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


"""Tags of all formats.

Imported names:
 * AdvSubStationAlpha (ass)
 * MicroDVD (microdvd)
 * MPL2 (mpl2)
 * MPsub (mpsub)
 * SubStationAlpha (ssa)
 * SubRip (subrip)
 * SubViewer2 (subviewer2)
 * TMPlayer (tmplayer)
"""


from .ass        import AdvSubStationAlpha
from .microdvd   import MicroDVD
from .mpl2       import MPL2
from .mpsub      import MPsub
from .ssa        import SubStationAlpha
from .subrip     import SubRip
from .subviewer2 import SubViewer2
from .tmplayer   import TMPlayer

from gaupol import const
__all__ = const.FORMAT.class_names
