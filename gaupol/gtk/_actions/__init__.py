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


"""UI manager actions."""

# pylint: disable-msg=W0612,W0621


def _get_actions():
    """Get all UIMAction classes."""

    from gaupol.gtk import util
    from ._action import UIMAction
    actions = []
    for module in _get_modules():
        names = list(x for x in dir(module) if not x.startswith("_"))
        while "UIMAction" in names:
            names.remove("UIMAction")
        values = list(getattr(module, x) for x in names)
        values = list(x for x in values if isinstance(x, type))
        values = list(x for x in values if issubclass(x, UIMAction))
        for value in values:
            globals()[value.__name__] = value
            actions.append(value.__name__)
    return util.get_sorted_unique(actions)

def _get_modules():
    """Get all modules that define UIMActions."""

    from . import edit
    from . import file
    from . import help
    from . import projects
    from . import text
    from . import tools
    from . import view
    return tuple(eval(x) for x in dir())

__all__ = ACTIONS = _get_actions()
