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

To hook some method up with the undo/redo system, the last argument to the
method should be a keyword argument "register" with a default value of
Action.DO. At the end of the method, self.register_action(...) should be called
with keyword arguments specified in RevertableAction.__init__.

To do some revertable action without the possibility of reverting, None can be
given as a value to the "register" keyword argument.

During the "register_action" method, a signal will be emitted notifying that an
action was done. Any possible UI can hook up to that signal and use it to
refresh the data display.

When grouping actions, only one signal should be sent. For example

    self.register_action(..., emit_signal=False)
    self.register_action(..., emit_signal=False)
    self.group_actions(Action.DO, 2, description)

Alternatively methods self.block(signal) and self.unblock(signal) can be used
directly to avoid sending unwanted signals.
"""


import bisect

from gaupol.base          import cons
from gaupol.base.delegate import Delegate
from gaupol.base.util     import listlib


class RevertableAction(object):

    """Action that can be reverted (undone or redone)."""

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
        emit_signal=True,
    ):
        """
        Initialize a RevertableAction object.

        register: Action constant
        documents: List of Document constants
        description: Short one line description of action
        """
        self.register           = register
        self.docs               = docs
        self.description        = description
        self.revert_method      = revert_method
        self.revert_args        = revert_args
        self.revert_kwargs      = revert_kwargs
        self.inserted_rows      = inserted_rows
        self.removed_rows       = removed_rows
        self.updated_rows       = updated_rows
        self.updated_positions  = updated_positions
        self.updated_main_texts = updated_main_texts
        self.updated_tran_texts = updated_tran_texts
        self.emit_signal        = emit_signal

        self._validate_input()

    def revert(self):
        """Revert action."""

        # Get register constant for revert action.
        if self.register in (cons.Action.DO, cons.Action.REDO):
            self.revert_kwargs['register'] = cons.Action.UNDO
        elif self.register == cons.Action.UNDO:
            self.revert_kwargs['register'] = cons.Action.REDO

        self.revert_method(*self.revert_args, **self.revert_kwargs)

    def _validate_input(self):
        """
        Validate given attribute values.

        Raise ValueError if values of attributes are incorrect.
        """
        if not self.register in (
            cons.Action.DO,
            cons.Action.UNDO,
            cons.Action.REDO,
            cons.Action.DO_MULTIPLE,
            cons.Action.UNDO_MULTIPLE,
            cons.Action.REDO_MULTIPLE,
        ):
            raise ValueError

        main_in = cons.Document.MAIN in self.docs
        tran_in = cons.Document.TRAN in self.docs
        if not main_in and not tran_in:
            raise ValueError

        self.inserted_rows.sort()
        self.removed_rows.sort()
        self.updated_rows.sort()
        self.updated_positions.sort()
        self.updated_main_texts.sort()
        self.updated_tran_texts.sort()


class RevertableActionGroup(object):

    """Group of revertable actions."""

    def __init__(self, actions, description):

        self.actions = actions
        self.description = description


class RevertableActionDelegate(Delegate):

    """Managing revertable actions."""

    def _break_action_group(self, stack, index=0):
        """
        Break action group in stack into individual actions.

        Return amount of actions broken into.
        """
        action_group = stack.pop(index)
        for action in reversed(action_group.actions):
            stack.insert(index, action)

        return len(action_group.actions)

    def can_redo(self):
        """Return True if something can be redone."""

        return bool(self.redoables)

    def can_undo(self):
        """Return True if something can be undone."""

        return bool(self.undoables)

    def _emit_notification(self, actions, register):
        """Emit signal with a notification action."""

        action = self._get_notification_action(actions, register)
        signal = self.get_signal(register)
        self.emit(signal, action)

    def _get_destination_stack(self, register):
        """Get stack where registered action will be placed."""

        if register in (cons.Action.DO, cons.Action.DO_MULTIPLE):
            return self.undoables
        if register in (cons.Action.UNDO, cons.Action.UNDO_MULTIPLE):
            return self.redoables
        if register in (cons.Action.REDO, cons.Action.REDO_MULTIPLE):
            return self.undoables

        raise ValueError

    def _get_notification_action(self, actions, register):
        """
        Get a dummy action to notify of changes.

        Return a RevertableAction that lists all changes that would be made if
        actions were registered (done or reverted) in the order given.
        """
        revert = bool(register != cons.Action.DO)

        inserted_rows = []
        removed_rows  = []
        updated_rows  = []
        updated_positions  = []
        updated_main_texts = []
        updated_tran_texts = []
        all_updated_rows = [
            updated_rows,
            updated_positions,
            updated_main_texts,
            updated_tran_texts
        ]

        for action in actions:
            if revert:
                inserted = action.removed_rows
                removed  = action.inserted_rows
            else:
                inserted = action.inserted_rows
                removed  = action.removed_rows

            # Adjust previous updates due to rows being removed.
            if removed:
                first_removed_row = min(removed)
                for i in range(len(all_updated_rows)):
                    for j in reversed(range(len(all_updated_rows[i]))):
                        updated_row = all_updated_rows[i][j]
                        # Remove updates to rows being removed.
                        if updated_row in removed:
                            all_updated_rows[i].pop(j)
                        # Shift updates to rows being moved.
                        elif updated_row > first_removed_row:
                            rows_above = bisect.bisect_left(
                                removed, updated_row)
                            all_updated_rows[i][j] -= rows_above

            # Adjust previous updates due to rows being inserted.
            for inserted_row in inserted:
                for i in range(len(all_updated_rows)):
                    # Shift updates to rows being moved.
                    for j, updated_row in enumerate(all_updated_rows[i]):
                        if updated_row >= inserted_row:
                            all_updated_rows[i][j] += 1

            inserted_rows += inserted
            removed_rows  += removed
            updated_rows  += action.updated_rows
            updated_positions  += action.updated_positions
            updated_main_texts += action.updated_main_texts
            updated_tran_texts += action.updated_tran_texts

        return RevertableAction(
            register=register,
            docs=[cons.Document.MAIN, cons.Document.TRAN],
            description='',
            revert_method=None,
            inserted_rows=listlib.sorted_unique(inserted_rows),
            removed_rows=listlib.sorted_unique(removed_rows),
            updated_rows=listlib.sorted_unique(updated_rows),
            updated_positions=listlib.sorted_unique(updated_positions),
            updated_main_texts=listlib.sorted_unique(updated_main_texts),
            updated_tran_texts=listlib.sorted_unique(updated_tran_texts),
        )

    def get_signal(self, register):
        """Get signal matching register."""

        if register in (cons.Action.DO, cons.Action.DO_MULTIPLE):
            return 'action_done'
        if register in (cons.Action.UNDO, cons.Action.UNDO_MULTIPLE):
            return 'action_undone'
        if register in (cons.Action.REDO, cons.Action.REDO_MULTIPLE):
            return 'action_redone'

    def _get_source_stack(self, register):
        """Get stack where action to register is."""

        if register in (cons.Action.UNDO, cons.Action.UNDO_MULTIPLE):
            return self.undoables
        if register in (cons.Action.REDO, cons.Action.REDO_MULTIPLE):
            return self.redoables

        raise ValueError

    def group_actions(self, register, amount, description, emit_signal=True):
        """Group registered actions as one entity."""

        stack = self._get_destination_stack(register)
        actions = []
        for i in range(amount):
            actions.append(stack.pop(0))
            action_group = RevertableActionGroup(actions, description)
        stack.insert(0, action_group)

        if emit_signal:
            self._emit_notification(reversed(actions), register)

    def redo(self, amount=1):
        """Redo actions."""

        if amount == 1:
            if not isinstance(self.redoables[0], RevertableActionGroup):
                self.redoables[0].revert()
                self.redoables.pop(0)
                return

        self._revert_multiple(amount, cons.Action.REDO_MULTIPLE)

    def register_action(self, *args, **kwargs):
        """
        Register action done, undone or redone.

        See RevertableAction.__init__ for arguments as they're passed directly
        for the RevertableAction initialization.
        """
        if kwargs['register'] is None:
            return

        action = RevertableAction(*args, **kwargs)

        # Restore action's original "DO" description if reverting.
        if action.register == cons.Action.DO:
            self._register_action_done(action)
        elif action.register == cons.Action.UNDO:
            action.description = self.undoables[0].description
            self._register_action_undone(action)
        elif action.register == cons.Action.REDO:
            action.description = self.redoables[0].description
            self._register_action_redone(action)

    def _register_action_done(self, action):
        """Register action done."""

        self.undoables.insert(0, action)
        if self.undo_limit is not None:
            while len(self.undoables) > self.undo_limit:
                self.undoables.pop()

        self.redoables = []
        self._shift_changed_value(action, 1)
        if action.emit_signal:
            self.emit('action_done', action)

    def _register_action_redone(self, action):
        """Register action redone."""

        self.undoables.insert(0, action)
        if self.undo_limit is not None:
            while len(self.undoables) > self.undo_limit:
                self.undoables.pop()

        self._shift_changed_value(action, 1)
        if action.emit_signal:
            self.emit('action_redone', action)

    def _register_action_undone(self, action):
        """Register action undone."""

        self.redoables.insert(0, action)
        if self.undo_limit is not None:
            while len(self.redoables) > self.undo_limit:
                self.redoables.pop()

        self._shift_changed_value(action, -1)
        if action.emit_signal:
            self.emit('action_undone', action)

    def _revert_multiple(self, amount, register):
        """Revert multiple actions."""

        signal = self.get_signal(register)
        stack = self._get_source_stack(register)

        self.block(signal)
        actions = []
        for i in range(amount):
            sub_amount = 1
            if isinstance(stack[0], RevertableActionGroup):
                description = stack[0].description
                sub_amount = self._break_action_group(stack)
            for j in range(sub_amount):
                action = stack[0]
                actions.append(action)
                action.revert()
                stack.pop(0)
            if sub_amount > 1:
                self.group_actions(register, sub_amount, description, False)
        self.unblock(signal)
        self._emit_notification(actions, register)

    def set_action_description(self, register, description):
        """Set description of the most recent action."""

        if register is None:
            return
        stack = self._get_destination_stack(register)
        stack[0].description = description

    def _shift_changed_value(self, action, shift):
        """Shift values of changed attributes."""

        if cons.Document.MAIN in action.docs:
            self.main_changed += shift
        if cons.Document.TRAN in action.docs:
            self.tran_changed += shift
        if action.docs == [cons.Document.TRAN]:
            self.tran_active = True

    def undo(self, amount=1):
        """Undo actions."""

        if amount == 1:
            if not isinstance(self.undoables[0], RevertableActionGroup):
                self.undoables[0].revert()
                self.undoables.pop(0)
                return

        self._revert_multiple(amount, cons.Action.UNDO_MULTIPLE)
