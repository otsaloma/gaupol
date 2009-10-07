# Copyright (C) 2005-2007 Osmo Salomaa
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

"""Actions that can be reverted, i.e. undone and redone."""

import gaupol

__all__ = ("RevertableAction", "RevertableActionGroup",)


class RevertableAction(object):

    """Action that can be reverted, i.e. undone and redone.

    Instance variables:
     * description: Short one line description
     * docs: Sequence of document enumerations affected
     * register: Register enumeration corresponding to the action taken
     * revert_args: Arguments passed to the revert method
     * revert_kwargs: Keyword arguments passed to the revert method
     * revert_method: Method called to revert this action

    'description', 'docs', 'register' and 'revert_method' are required to be
    set eventually, either upon instantiation or directly after.
    """

    __metaclass__ = gaupol.Contractual

    def __init__(self, **kwargs):
        """Initialize a RevertableAction object.

        kwargs can contain any of the names of public instance variables.
        """
        self.description = None
        self.docs = None
        self.register = None
        self.revert_args = ()
        self.revert_kwargs = {}
        self.revert_method = None

        for key, value in kwargs.items():
            setattr(self, key, value)

    def _get_reversion_register_require(self):
        assert self.register in gaupol.registers

    def _get_reversion_register(self):
        """Return the register enumeration corresponding to reversion."""

        if self.register.shift == 1:
            return gaupol.registers.UNDO
        if self.register.shift == -1:
            return gaupol.registers.REDO
        raise ValueError("Invalid register: %s" % repr(self.register))

    def revert_require(self):
        assert callable(self.revert_method)

    def revert(self):
        """Call the revert method."""

        kwargs = self.revert_kwargs.copy()
        kwargs["register"] = self._get_reversion_register()
        return self.revert_method(*self.revert_args, **kwargs)


class RevertableActionGroup(object):

    """Group of revertable actions.

    Instance variables:
     * actions: Sequence of actions in group
     * description: Short one line description

    Instance variables 'actions' and 'description' are required to be set
    eventually, either upon instantiation or directly after.
    """

    def __init__(self, **kwargs):
        """Initialize a RevertableAction object.

        kwargs can contain any of the names of public instance variables,
        """
        self.actions = None
        self.description = None

        for key, value in kwargs.items():
            setattr(self, key, value)
