# Copyright (C) 2005-2006 Osmo Salomaa
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


"""
Managing revertable actions.

To hook a method up with the undo/redo system, three things need to be done:

(1) The last argument to the method must be keyword argument 'register' with a
    default value of -1. This argument indicates which of doing, undoing or
    redoing is in process.

(2) At the end of the method, self.register_action(...) needs to be called with
    keyword arguments specified in Action.__init__, where they're directly
    passed to. Calling this method takes care of the management of undo and
    redo stacks.

(3) The method should be marked with the 'revertablemethod' decorator from
    gaupol.base.delegate. This decorator takes care of emitting a signal with a
    real action or a notification action to state that something has been done,
    undone or redone and defaults the 'register' keyword argument to
    cons.Action.DO, which means that if the decorator is left out, an error is
    raised as -1 is not a valid register value.

Each method marked as revertable should match exactly one action in the undo
and redo stacks. Hence, if the method is a multipart method, that calls other
revertable methods, the resulting action needs to be grouped as one using
self.group_actions(...).

If a revertable method needs to be performed without the possibility of
reverting, the 'register' keyword argument can be given value of None. This way
it will not be in any way processed by the undo/redo system.

If the signal emitting is in some more complicated situation considered
premature, it can be blocked with self.block(signal), unblocked with
self.unblock(signal) and a custom signal can be sent, easiest with
self.emit_notification(...).
"""


import bisect

from gaupol.base          import cons
from gaupol.base.icons    import *
from gaupol.base.delegate import Delegate
from gaupol.base.util     import listlib


class Action(object):

    """
    Action that can be reverted (undone or redone).

    Instance variables:

        description:        Short one line description
        docs:               List of Document constants
        inserted_rows:      List of rows inserted
        register:           Action constant
        removed_rows:       List of rows removed
        revert_args:        Arguments passed to revert method
        revert_kwargs:      Keyword arguments passed to revert method
        revert_method:      Method called to revert action
        updated_main_texts: List of rows with main texts updated
        updated_positions:  List of rows with positions updated
        updated_rows:       List of rows updated
        updated_tran_texts: List of rows with translation texts updated

    """

    def __init__(
        self,
        register,
        docs,
        description,
        revert_method,
        revert_args=[],
        revert_kwargs={},
        inserted_rows=[],
        removed_rows=[],
        updated_rows=[],
        updated_positions=[],
        updated_main_texts=[],
        updated_tran_texts=[],
    ):

        self.description        = description
        self.docs               = docs
        self.inserted_rows      = sorted(inserted_rows)
        self.register           = register
        self.removed_rows       = sorted(removed_rows)
        self.revert_args        = revert_args
        self.revert_kwargs      = revert_kwargs
        self.revert_method      = revert_method
        self.updated_main_texts = sorted(updated_main_texts)
        self.updated_positions  = sorted(updated_positions)
        self.updated_rows       = sorted(updated_rows)
        self.updated_tran_texts = sorted(updated_tran_texts)

    def revert(self):
        """Revert action."""

        # Get register constant for revert action.
        if self.register in (cons.Action.DO, cons.Action.REDO):
            self.revert_kwargs['register'] = cons.Action.UNDO
        elif self.register == cons.Action.UNDO:
            self.revert_kwargs['register'] = cons.Action.REDO

        self.revert_method(*self.revert_args, **self.revert_kwargs)


class ActionGroup(object):

    """
    Group of revertable actions.

    Instance variables:

        actions:     Stack of Actions
        description: Short one line description

    """

    def __init__(self, actions, description):

        self.actions     = actions
        self.description = description


class ActionDelegate(Delegate):

    """Managing revertable actions."""

    def __init__(self, *args, **kwargs):

        Delegate.__init__(self, *args, **kwargs)

        self._revert_desc = None

    def _break_action_group(self, stack, index=0):
        """
        Break action group in stack into individual actions.

        Return amount of actions broken into.
        """
        action_group = stack.pop(index)
        for action in reversed(action_group.actions):
            stack.insert(index, action)
        return len(action_group.actions)

    def _get_destination_stack(self, register):
        """Get stack where registered action will be placed."""

        if register in (cons.Action.DO, cons.Action.DO_MULTIPLE):
            return self.undoables
        if register in (cons.Action.UNDO, cons.Action.UNDO_MULTIPLE):
            return self.redoables
        if register in (cons.Action.REDO, cons.Action.REDO_MULTIPLE):
            return self.undoables
        raise ValueError

    def _get_notification_action(self, register, count=1):
        """Get dummy action to notify of changes."""

        inserted_rows      = []
        removed_rows       = []
        updated_rows       = []
        updated_positions  = []
        updated_main_texts = []
        updated_tran_texts = []
        all_updated = [
            updated_rows,
            updated_positions,
            updated_main_texts,
            updated_tran_texts
        ]

        actions = []
        stack = self._get_destination_stack(register)
        for action in reversed(stack[0:count]):
            if isinstance(action, ActionGroup):
                actions.extend(reversed(action.actions))
            elif isinstance(action, Action):
                actions.append(action)
        for action in actions:

            # Adjust previous updates due to rows being removed.
            if action.removed_rows:
                first_removed_row = min(action.removed_rows)
                for i in range(len(all_updated)):
                    for j in reversed(range(len(all_updated[i]))):
                        updated_row = all_updated[i][j]
                        # Remove updates to rows being removed.
                        if updated_row in action.removed_rows:
                            all_updated[i].pop(j)
                        # Shift updates to rows being moved.
                        elif updated_row > first_removed_row:
                            rows_above = bisect.bisect_left(
                                action.removed_rows, updated_row)
                            all_updated[i][j] -= rows_above

            # Adjust previous updates due to rows being inserted.
            for inserted_row in action.inserted_rows:
                for i in range(len(all_updated)):
                    for j, updated_row in enumerate(all_updated[i]):
                        # Shift updates to rows being moved.
                        if updated_row >= inserted_row:
                            all_updated[i][j] += 1

            inserted_rows.extend(action.inserted_rows)
            removed_rows.extend(action.removed_rows)
            updated_rows.extend(action.updated_rows)
            updated_positions.extend(action.updated_positions)
            updated_main_texts.extend(action.updated_main_texts)
            updated_tran_texts.extend(action.updated_tran_texts)

        return Action(
            register=register,
            docs=[MAIN, TRAN],
            description='',
            revert_method=None,
            inserted_rows=listlib.sorted_unique(inserted_rows),
            removed_rows=listlib.sorted_unique(removed_rows),
            updated_rows=listlib.sorted_unique(updated_rows),
            updated_positions=listlib.sorted_unique(updated_positions),
            updated_main_texts=listlib.sorted_unique(updated_main_texts),
            updated_tran_texts=listlib.sorted_unique(updated_tran_texts),
        )

    def _get_source_stack(self, register):
        """Get stack where action to register is."""

        if register in (cons.Action.UNDO, cons.Action.UNDO_MULTIPLE):
            return self.undoables
        if register in (cons.Action.REDO, cons.Action.REDO_MULTIPLE):
            return self.redoables
        raise ValueError

    def _register_action_done(self, action):
        """Register action done."""

        self.undoables.insert(0, action)
        if self.undo_limit is not None:
            while len(self.undoables) > self.undo_limit:
                self.undoables.pop()
        self.redoables = []
        self._shift_changed_value(action, 1)

    def _register_action_redone(self, action):
        """Register action redone."""

        self.undoables.insert(0, action)
        if self.undo_limit is not None:
            while len(self.undoables) > self.undo_limit:
                self.undoables.pop()
        self._shift_changed_value(action, 1)

    def _register_action_undone(self, action):
        """Register action undone."""

        self.redoables.insert(0, action)
        if self.undo_limit is not None:
            while len(self.redoables) > self.undo_limit:
                self.redoables.pop()
        self._shift_changed_value(action, -1)

    def _revert_multiple(self, count, register):
        """Revert multiple actions."""

        signal = cons.Action.signals[register]
        self.block(signal)
        stack = self._get_source_stack(register)
        for i in range(count):
            sub_count = 1
            if isinstance(stack[0], ActionGroup):
                description = stack[0].description
                sub_count = self._break_action_group(stack)
            for j in range(sub_count):
                self._revert_desc = stack[0].description
                stack.pop(0).revert()
            if sub_count > 1:
                self.group_actions(register, sub_count, description)
        self.unblock(signal)
        self.emit_notification(register, count)

    def _shift_changed_value(self, action, shift):
        """Shift values of changed attributes."""

        if MAIN in action.docs:
            self.main_changed += shift
        if TRAN in action.docs:
            self.tran_changed += shift
        if action.docs == [TRAN]:
            self.tran_active = True

    def can_redo(self):
        """Return True if something can be redone."""

        return bool(self.redoables)

    def can_undo(self):
        """Return True if something can be undone."""

        return bool(self.undoables)

    def emit_notification(self, register, count=1):
        """Emit signal of registered actions."""

        stack = self._get_destination_stack(register)
        action = stack[0]
        if count > 1 or isinstance(action, ActionGroup):
            action = self._get_notification_action(register, count)
        signal = cons.Action.signals[register]
        self.emit(signal, action)

    def group_actions(self, register, count, description):
        """Group registered actions as one entity."""

        stack = self._get_destination_stack(register)
        actions = []
        for i in range(count):
            actions.append(stack.pop(0))
            action_group = ActionGroup(actions, description)
        stack.insert(0, action_group)

    def redo(self, count=1):
        """Redo actions."""

        if count > 1 or isinstance(self.redoables[0], ActionGroup):
            return self._revert_multiple(count, cons.Action.REDO_MULTIPLE)
        self._revert_desc = self.redoables[0].description
        self.redoables.pop(0).revert()

    def register_action(self, *args, **kwargs):
        """
        Register action done, undone or redone.

        See Action.__init__ for arguments.
        """
        if kwargs['register'] is None:
            return

        action = Action(*args, **kwargs)

        # Restore action's original 'DO' description if reverting.
        if action.register == cons.Action.DO:
            return self._register_action_done(action)
        elif action.register == cons.Action.UNDO:
            action.description = self._revert_desc
            return self._register_action_undone(action)
        elif action.register == cons.Action.REDO:
            action.description = self._revert_desc
            return self._register_action_redone(action)
        raise ValueError

    def set_action_description(self, register, description):
        """Set description of the most recent action."""

        if register is None:
            return
        stack = self._get_destination_stack(register)
        stack[0].description = description

    def undo(self, count=1):
        """Undo actions."""

        if count > 1 or isinstance(self.undoables[0], ActionGroup):
            return self._revert_multiple(count, cons.Action.UNDO_MULTIPLE)
        self._revert_desc = self.undoables[0].description
        self.undoables.pop(0).revert()
