# -*- coding: utf-8 -*-

# Copyright (C) 2007 Osmo Salomaa
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

"""Extension delegates of of :class:`gaupol.Application`."""

from .close    import CloseAgent # noqa
from .edit     import EditAgent # noqa
from .format   import FormatAgent # noqa
from .help     import HelpAgent # noqa
from .menu     import MenuAgent # noqa
from .open     import OpenAgent # noqa
from .preview  import PreviewAgent # noqa
from .save     import SaveAgent # noqa
from .search   import SearchAgent # noqa
from .tools    import ToolsAgent # noqa
from .update   import UpdateAgent # noqa
from .util     import UtilityAgent # noqa
from .video    import VideoAgent # noqa
from .view     import ViewAgent # noqa

__all__ = tuple(x for x in dir() if x.endswith("Agent"))
