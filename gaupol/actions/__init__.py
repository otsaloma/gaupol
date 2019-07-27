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

"""User-activatable actions for :class:`gaupol.Application`."""

from gaupol.actions.audio    import * # noqa
from gaupol.actions.edit     import * # noqa
from gaupol.actions.file     import * # noqa
from gaupol.actions.help     import * # noqa
from gaupol.actions.projects import * # noqa
from gaupol.actions.text     import * # noqa
from gaupol.actions.tools    import * # noqa
from gaupol.actions.video    import * # noqa
from gaupol.actions.view     import * # noqa

__all__ = tuple(x for x in dir() if x.endswith("Action"))
