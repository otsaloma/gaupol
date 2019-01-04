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

"""
Managing revertable actions.

To hook a method up with the undo/redo system, the following need to be done:

(1) The last argument to the method must be a keyword argument `register` with
    a default value of -1. This argument indicates which of doing, undoing or
    redoing is in process.

(2) At the end of the method, :meth:`register_action` needs to be called with
    an instance of :class:`aeidon.RevertableAction`. Calling this method takes
    care of the management of undo and redo stacks.

(3) The method should be marked with the :func:`aeidon.deco.revertable`
    decorator. This decorator takes care of emitting an action signal once
    the method has been run, cuts the undo and redo stacks if needed and
    defaults the `register` keyword argument to :attr:`aeidon.registers.DO`.

Each method marked as revertable should match exactly one action in the undo
and redo stacks. Hence, if a method calls other revertable methods, the
resulting action needs to be grouped as one using :meth:`group_actions`.

If a revertable method needs to be performed without the possibility of
reverting, the `register` keyword argument should be given a value of ``None``.
This way it will not be in any way processed by the undo/redo system.
"""

import aeidon


class RegisterAgent(aeidon.Delegate):

    """
    Managing revertable actions.

    :ivar _do_description: Original description of the action
    """

    def __init__(self, master):
        """Initialize a :class:`RegisterAgent` instance."""
        aeidon.Delegate.__init__(self, master)
        self._do_description = None
        aeidon.util.connect(self, self, "notify::undo_limit")

    def _break_action_group(self, stack, index=0):
        """Break the action group in `stack` and return amount broken into."""
        action_group = stack.pop(index)
        for action in reversed(action_group.actions):
            stack.insert(index, action)
        return len(action_group.actions)

    @aeidon.deco.export
    def can_redo(self, count=1):
        """Return ``True`` if one or more actions can be redone."""
        return len(self.redoables) >= count

    @aeidon.deco.export
    def can_undo(self, count=1):
        """Return ``True`` if one or more actions can be undone."""
        return len(self.undoables) >= count

    @aeidon.deco.export
    def cut_reversion_stacks(self):
        """Cut undo and redo stacks to their maximum lengths."""
        if self.undo_limit is not None:
            del self.redoables[self.undo_limit:]
            del self.undoables[self.undo_limit:]

    @aeidon.deco.export
    def emit_action_signal(self, register):
        """Emit an action signal for the most recent registered action."""
        if register is not None:
            self.emit(register.signal,
                      self._get_destination_stack(register)[0])

    def _get_destination_stack(self, register):
        """Return the stack where the registered action will be placed."""
        if register.shift == 1:
            return self.undoables
        if register.shift == -1:
            return self.redoables
        raise ValueError("Invalid register: {!r}"
                         .format(register))

    def _get_source_stack(self, register):
        """Return the stack where the action to register is taken from."""
        if register.shift == 1:
            return self.redoables
        if register.shift == -1:
            return self.undoables
        raise ValueError("Invalid register: {!r}"
                         .format(register))

    @aeidon.deco.export
    def group_actions(self, register, count, description):
        """Group the registered actions as one item in the stack."""
        if register is None: return
        action_group = aeidon.RevertableActionGroup()
        action_group.actions = []
        action_group.description = description
        stack = self._get_destination_stack(register)
        for i in range(count):
            action = stack.pop(0)
            if isinstance(action, aeidon.RevertableActionGroup):
                action_group.actions.extend(action.actions)
            else: # Single action
                action_group.actions.append(action)
        stack.insert(0, action_group)

    def _on_notify_undo_limit(self, *args):
        """Cut reversion stacks if limit set."""
        if self.undo_limit is not None:
            self.cut_reversion_stacks()

    @aeidon.deco.export
    def redo(self, count=1):
        """Redo `count` amount of actions from the redoable stack."""
        group = aeidon.RevertableActionGroup
        if count > 1 or isinstance(self.redoables[0], group):
            return self._revert_multiple(count, aeidon.registers.REDO)
        self._do_description = self.redoables[0].description
        self.redoables.pop(0).revert()

    @aeidon.deco.export
    def register_action(self, action):
        """Register `action` as done, undone or redone."""
        if action.register == aeidon.registers.DO:
            self.undoables.insert(0, action)
            self.redoables = []
            self._shift_changed_value(action, action.register.shift)
        if action.register == aeidon.registers.UNDO:
            self.redoables.insert(0, action)
            action.description = self._do_description
            self._shift_changed_value(action, action.register.shift)
        if action.register == aeidon.registers.REDO:
            self.undoables.insert(0, action)
            action.description = self._do_description
            self._shift_changed_value(action, action.register.shift)

    def _revert_multiple(self, count, register):
        """Revert multiple actions."""
        self.block(register.signal)
        stack = self._get_source_stack(register)
        for i in range(count):
            part_count = 1
            if isinstance(stack[0], aeidon.RevertableActionGroup):
                description = stack[0].description
                part_count = self._break_action_group(stack)
            for j in range(part_count):
                self._do_description = stack[0].description
                stack.pop(0).revert()
            if part_count > 1:
                self.group_actions(register, part_count, description)
        self.unblock(register.signal)
        self.cut_reversion_stacks()
        self.emit_action_signal(register)

    @aeidon.deco.export
    def set_action_description(self, register, description):
        """Set the description of the most recent registered action."""
        if register is None: return
        stack = self._get_destination_stack(register)
        stack[0].description = description

    def _shift_changed_value(self, action, shift):
        """Shift the values of changed attributes."""
        if aeidon.documents.MAIN in action.docs:
            self.main_changed += shift
        if tuple(action.docs) == (aeidon.documents.TRAN,):
            # Make translation document active.
            if self.tran_changed is None:
                self.tran_changed = 0
        if aeidon.documents.TRAN in action.docs:
            if self.tran_changed is not None:
                self.tran_changed += shift

    @aeidon.deco.export
    def undo(self, count=1):
        """Undo `count` amount of actions from the undoable stack."""
        group = aeidon.RevertableActionGroup
        if count > 1 or isinstance(self.undoables[0], group):
            return self._revert_multiple(count, aeidon.registers.UNDO)
        self._do_description = self.undoables[0].description
        self.undoables.pop(0).revert()
