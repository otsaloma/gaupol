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


"""Managing revertable actions.

To hook a method up with the undo/redo system, the following need to be done:

(1) The last argument to the method must be keyword argument 'register' with a
    default value of -1. This argument indicates which of doing, undoing or
    redoing is in process.

(2) At the end of the method, 'self.register_action' needs to be called with an
    instance of 'RevertableAction'. Calling this method takes care of the
    management of undo and redo stacks.

(3) The method should be marked with the 'revertable' decorator. This decorator
    takes care of emitting an action signal once the method has been run, cuts
    the undo and redo stacks if needed and defaults the 'register' keyword
    argument to 'const.REGISTER.DO'.

Each method marked as revertable should match exactly one action in the undo
and redo stacks. Hence, if the method calls other revertable methods, the
resulting action needs to be grouped as one using 'self.group_actions'.

If a revertable method needs to be performed without the possibility of
reverting, the 'register' keyword argument should be given a value of 'None'.
This way it will not be in any way processed by the undo/redo system.
"""


from gaupol import const, util
from gaupol.base import Contractual, Delegate
from gaupol.reversion import RevertableActionGroup


class RegisterAgent(Delegate):

    """Managing revertable actions.

    Instance variables:

        _do_description: The original description of the reverted action
    """

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = Contractual

    def __init__(self, master):

        Delegate.__init__(self, master)
        self._do_description = None
        util.connect(self, self, "notify::undo_limit")

    def _break_action_group_require(self, stack, index=0):
        assert 0 <= index < len(stack)

    def _break_action_group(self, stack, index=0):
        """Break the action group in stack into individual actions.

        Return the amount of actions broken into.
        """
        action_group = stack.pop(index)
        for action in reversed(action_group.actions):
            stack.insert(index, action)
        return len(action_group.actions)

    def _get_destination_stack(self, register):
        """Get the stack where the registered action will be placed."""

        if register.shift == 1:
            return self.undoables
        if register.shift == -1:
            return self.redoables
        raise ValueError

    def _get_source_stack(self, register):
        """Get the stack where the action to register is taken from."""

        if register.shift == 1:
            return self.redoables
        if register.shift == -1:
            return self.undoables
        raise ValueError

    @util.silent(AssertionError)
    def _on_notify_undo_limit(self, *args):
        """Cut reversion stacks if limit set."""

        assert self.undo_limit is not None
        self.cut_reversion_stacks()

    def _revert_multiple_require(self, count, register):
        stack = self._get_source_stack(register)
        assert len(stack) >= count

    def _revert_multiple(self, count, register):
        """Revert multiple actions."""

        self.block(register.signal)
        stack = self._get_source_stack(register)
        for i in range(count):
            sub_count = 1
            if isinstance(stack[0], RevertableActionGroup):
                description = stack[0].description
                sub_count = self._break_action_group(stack)
            for j in range(sub_count):
                self._do_description = stack[0].description
                stack.pop(0).revert()
            if sub_count > 1:
                self.group_actions(register, sub_count, description)
        self.unblock(register.signal)
        self.cut_reversion_stacks()
        self.emit_action_signal(register)

    def _shift_changed_value(self, action, shift):
        """Shift the values of the changed attributes."""

        if const.DOCUMENT.MAIN in action.docs:
            self.main_changed += shift
        if action.docs == [const.DOCUMENT.TRAN]:
            if self.tran_changed is None:
                self.tran_active = 0
        if const.DOCUMENT.TRAN in action.docs:
            if self.tran_changed is not None:
                self.tran_changed += shift

    def can_redo(self):
        """Return True if something can be redone."""

        return bool(self.redoables)

    def can_undo(self):
        """Return True if something can be undone."""

        return bool(self.undoables)

    @util.silent(AssertionError)
    def cut_reversion_stacks(self):
        """Cut the undo and redo stacks to their maximum lengths."""

        assert self.undo_limit is not None
        del self.redoables[self.undo_limit:]
        del self.undoables[self.undo_limit:]

    def emit_action_signal_require(self, register):
        assert self._get_destination_stack(register)

    @util.silent(AssertionError)
    def emit_action_signal(self, register):
        """Emit an action signal for the most recent registered action."""

        assert register is not None
        action = self._get_destination_stack(register)[0]
        self.emit(register.signal, action)

    def group_actions_require(self, register, count, description):
        if register is not None:
            stack = self._get_destination_stack(register)
            assert len(stack) >= count

    def group_actions_ensure(self, value, register, count, description):
        if register is not None:
            stack = self._get_destination_stack(register)
            assert isinstance(stack[0], RevertableActionGroup)

    @util.silent(AssertionError)
    def group_actions(self, register, count, description):
        """Group the registered actions as one item in the stack."""

        assert register is not None
        actions = []
        stack = self._get_destination_stack(register)
        for i in range(count):
            actions.append(stack.pop(0))
        action_group = RevertableActionGroup()
        action_group.actions = actions
        action_group.description = description
        stack.insert(0, action_group)

    def redo_require(self, count=1):
        assert len(self.redoables) >= count

    def redo(self, count=1):
        """Redo actions."""

        if count > 1 or isinstance(self.redoables[0], RevertableActionGroup):
            return self._revert_multiple(count, const.REGISTER.REDO)
        self._do_description = self.redoables[0].description
        self.redoables.pop(0).revert()

    @util.silent(AssertionError)
    def register_action(self, action):
        """Register action done, undone or redone."""

        assert action.register is not None
        if action.register == const.REGISTER.DO:
            self.undoables.insert(0, action)
            self.redoables = []
        elif action.register == const.REGISTER.UNDO:
            self.redoables.insert(0, action)
            action.description = self._do_description
        elif action.register == const.REGISTER.REDO:
            self.undoables.insert(0, action)
            action.description = self._do_description
        self._shift_changed_value(action, action.register.shift)

    def set_action_description_require(self, register, description):
        assert self._get_destination_stack(register)

    @util.silent(AssertionError)
    def set_action_description(self, register, description):
        """Set the description of the most recent action."""

        assert register is not None
        stack = self._get_destination_stack(register)
        stack[0].description = description

    def undo_require(self, count=1):
        assert len(self.undoables) >= count

    def undo(self, count=1):
        """Undo actions."""

        if count > 1 or isinstance(self.undoables[0], RevertableActionGroup):
            return self._revert_multiple(count, const.REGISTER.UNDO)
        self._do_description = self.undoables[0].description
        self.undoables.pop(0).revert()
