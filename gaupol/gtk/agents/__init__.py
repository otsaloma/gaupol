# Copyright (C) 2007 Osmo Salomaa
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


"""Extension delegates of Application."""


# FIX:
from .close      import CloseAgent
from .edit       import EditAgent
# from .format     import FormatAgent
from .help       import HelpAgent
# from .menu       import MenuAgent
from .open       import OpenAgent
# from .position   import PositionAgent
# from .preview    import PreviewAgent
from .save       import SaveAgent
# from .search     import SearchAgent
# from .spellcheck import SpellCheckAgent
from .update     import UpdateAgent
from .util       import UtilityAgent
from .view       import ViewAgent

__all__ = [x for x in dir() if x.endswith("Agent")]
