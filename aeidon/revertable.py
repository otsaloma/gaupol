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

"""Actions that can be reverted, i.e. undone and redone."""

import aeidon

__all__ = ("RevertableAction", "RevertableActionGroup",)


class RevertableAction:

    """
    Action that can be reverted, i.e. undone and redone.

    :ivar description: Short one line description
    :ivar docs: Sequence of :attr:`aeidon.documents` items affected
    :ivar register: :attr:`aeidon.registers` item for action taken
    :ivar revert_args: Arguments passed to the revert method
    :ivar revert_function: Method called to revert this action
    :ivar revert_kwargs: Keyword arguments passed to the revert method
    """

    def __init__(self, **kwargs):
        """
        Initialize a :class:`RevertableAction` instance.

        `kwargs` can contain any of the names of public instance variables,
        of which :attr:`description`, :attr:`docs`, :attr:`register` and
        :attr:`revert_function` are required to be set eventually, either with
        `kwargs` or direct assignment later.
        """
        self.description = None
        self.docs = None
        self.register = None
        self.revert_args = ()
        self.revert_function = None
        self.revert_kwargs = {}
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _get_reversion_register(self):
        """Return the :attr:`aeidon.registers` item for reversion."""
        if self.register.shift == 1:
            return aeidon.registers.UNDO
        if self.register.shift == -1:
            return aeidon.registers.REDO
        raise ValueError("Invalid register: {!r}"
                         .format(self.register))

    def revert(self):
        """Call the reversion function."""
        kwargs = self.revert_kwargs.copy()
        kwargs["register"] = self._get_reversion_register()
        return self.revert_function(*self.revert_args, **kwargs)


class RevertableActionGroup:

    """
    Group of :class:`RevertableAction`.

    :ivar actions: Sequence of :class:`RevertableAction` in group
    :ivar description: Short one line description
    """

    def __init__(self, **kwargs):
        """
        Initialize a :class:`RevertableAction` instance.

        `kwargs` can contain any of the names of public instance variables,
        of which :attr:`actions` and :attr:`description` are required to be
        set eventually, either with `kwargs` or direct assignment later.
        """
        self.actions = None
        self.description = None
        for key, value in kwargs.items():
            setattr(self, key, value)
