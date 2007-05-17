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


"""Decorator for revertable methods."""


import functools

from gaupol import const


def revertable(function):
    """Decorator for revertable methods."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        project = args[0]
        main_changed = project.main_changed
        tran_changed = project.tran_changed
        kwargs.setdefault("register", const.REGISTER.DO)
        register = kwargs["register"]
        if register is None:
            return function(*args, **kwargs)
        blocked = project.block(register.signal)
        value = function(*args, **kwargs)
        if not blocked:
            return value
        project.cut_reversion_stacks()
        project.unblock(register.signal)
        if (project.main_changed != main_changed) or \
           (project.tran_changed != tran_changed):
            project.emit_action_signal(register)
        return value

    return wrapper
