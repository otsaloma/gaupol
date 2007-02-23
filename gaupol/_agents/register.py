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

(2) At the end of the method, self.register_action(...) needs to be called with
    keyword arguments specified in RevertableAction.__init__, where they're
    directly passed to. Calling this method takes care of the management of
    undo and redo stacks.

(3) The method should be marked with the 'revertable' decorator. This decorator
    takes care of emitting an action signal once the method has been run, cuts
    the undo and redo stacks if needed and defaults the 'register' keyword
    argument to cons.REGISTER.DO.

Each method marked as revertable should match exactly one action in the undo
and redo stacks. Hence, if the method calls other revertable methods, the
resulting action needs to be grouped as one using self.group_actions(...).

If a revertable method needs to be performed without the possibility of
reverting, the 'register' keyword argument can be given a value of None. This
way it will not be in any way processed by the undo/redo system.
"""


import functools

from gaupol import cons, util
from gaupol.base import Delegate


def revertable(function):
    """Decorator to handle handle function with the action reversion system."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        project = args[0]
        main_changed = project.main_changed
        tran_changed = project.tran_changed
        if not "register" in kwargs:
            kwargs["register"] = cons.REGISTER.DO
        register = kwargs["register"]
        if register is None:
            return function(*args, **kwargs)
        blocked = project.block(register.signal)
        value = function(*args, **kwargs)
        if blocked:
            project.cut_reversion_stacks()
            project.unblock(register.signal)
            if project.main_changed != main_changed or \
               project.tran_changed != tran_changed:
                project.emit_action_signal(register)
        return value

    return wrapper


class RevertableAction(object):

    """Action that can be reverted (undone or redone).

    Instance variables:

        description:   Short one line description
        docs:          List of DOCUMENT constants
        register:      REGISTER constant
        revert_args:   Arguments passed to the revert method
        revert_kwargs: Keyword arguments passed to the revert method
        revert_method: Method called for reversion
    """

    def __init__(self, register, docs, description,
        revert_method, revert_args=None, revert_kwargs=None):

        revert_args = (revert_args if revert_args is not None else [])
        revert_kwargs = (revert_kwargs if revert_kwargs is not None else {})

        self.description   = description
        self.docs          = docs
        self.register      = register
        self.revert_args   = revert_args
        self.revert_kwargs = revert_kwargs
        self.revert_method = revert_method

    def revert(self):
        """Call the revert method."""

        register = None
        if self.register.shift == 1:
            register = cons.REGISTER.UNDO
        if self.register.shift == -1:
            register = cons.REGISTER.REDO
        self.revert_kwargs["register"] = register
        self.revert_method(*self.revert_args, **self.revert_kwargs)


class RevertableActionGroup(object):

    """Group of revertable actions.

    Instance variables:

        actions:     List of actions in group
        description: Short one line description
    """

    def __init__(self, actions, description):

        self.actions     = actions
        self.description = description


class RegisterAgent(Delegate):

    """Managing revertable actions.

    Instance variables:

        _do_description: The original description of the reverted action
    """

    # pylint: disable-msg=E0203,W0201

    def __init__(self, master):

        Delegate.__init__(self, master)

        self._do_description = None

        util.connect(self, self, "notify::undo_limit")

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
        """Get the stack where the action to register is."""

        if register.shift == 1:
            return self.redoables
        if register.shift == -1:
            return self.undoables
        raise ValueError

    def _on_notify_undo_limit(self, *args):
        """Cut reversion stacks if limit set."""

        if self.undo_limit is not None:
            self.cut_reversion_stacks()

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
        self.emit_action_signal(register, count)

    def _shift_changed_value(self, action, shift):
        """Shift the values of the changed attributes."""

        if cons.DOCUMENT.MAIN in action.docs:
            self.main_changed += shift
        if cons.DOCUMENT.TRAN in action.docs:
            self.tran_changed += shift

        if action.docs == [cons.DOCUMENT.TRAN]:
            self.tran_active = True

    def can_redo(self):
        """Return True if something can be redone."""

        return bool(self.redoables)

    def can_undo(self):
        """Return True if something can be undone."""

        return bool(self.undoables)

    def cut_reversion_stacks(self):
        """Cut the undo and redo stacks to their maximum lengths."""

        if self.undo_limit is not None:
            del self.redoables[self.undo_limit:]
            del self.undoables[self.undo_limit:]

    def emit_action_signal(self, register, count=1):
        """Emit an action signal for register."""

        if register is not None:
            action = self._get_destination_stack(register)[0]
            self.emit(register.signal, action)

    def group_actions(self, register, count, description):
        """Group the registered actions as one item in the stack."""

        if register is not None:
            actions = []
            stack = self._get_destination_stack(register)
            for i in range(count):
                actions.append(stack.pop(0))
            action_group = RevertableActionGroup(actions, description)
            stack.insert(0, action_group)

    def redo(self, count=1):
        """Redo actions."""

        if count > 1 or isinstance(self.redoables[0], RevertableActionGroup):
            return self._revert_multiple(count, cons.REGISTER.REDO_MULTIPLE)
        self._do_description = self.redoables[0].description
        self.redoables.pop(0).revert()

    def register_action(self, *args, **kwargs):
        """Register action done, undone or redone.

        See RevertableAction.__init__ for arguments.
        """
        action = RevertableAction(*args, **kwargs)
        if action.register is None:
            return
        if action.register == cons.REGISTER.DO:
            self.undoables.insert(0, action)
            self.redoables = []
        elif action.register == cons.REGISTER.UNDO:
            self.redoables.insert(0, action)
            action.description = self._do_description
        elif action.register == cons.REGISTER.REDO:
            self.undoables.insert(0, action)
            action.description = self._do_description
        self._shift_changed_value(action, action.register.shift)

    def set_action_description(self, register, description):
        """Set the description of the most recent action."""

        if register is not None:
            stack = self._get_destination_stack(register)
            stack[0].description = description

    def undo(self, count=1):
        """Undo actions."""

        if count > 1 or isinstance(self.undoables[0], RevertableActionGroup):
            return self._revert_multiple(count, cons.REGISTER.UNDO_MULTIPLE)
        self._do_description = self.undoables[0].description
        self.undoables.pop(0).revert()
