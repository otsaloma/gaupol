# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""
Managing revertable actions.

To hook some method up with the undo-redo system the following needs to be done
(1) The last argument to the function should be a keyword argument "register"
with a default value of Action.DO.
(2) At the end of the method, method "register_action" should be called with
keyword arguments specified in RevertableAction.__init__.

To do some action without possibility of reverting, None can be given as a
value to the "register" keyword argument.

During the "register_action" method, a signal will be emitted notifying that
an action was done. Any possible UI can hook up to that signal and use it to
refresh the data display.

When grouping actions, only one signal should be sent. For example

    self.register_action(..., emit_signal=False)
    self.register_action(..., emit_signal=False)
    self.group_actions(Action.DO, 2, description)

Alternatively methods self.block(signal) and self.unblock(signal) can be used
directly to avoid sending unwanted signals.
"""


try:
    from psyco.classes import *
except ImportError:
    pass

import bisect

from gaupol.base.delegates import Delegate
from gaupol.base.util      import listlib
from gaupol.constants      import Action, Document


class RevertableAction(object):

    """An action that can be reverted (undone or redone)."""

    def __init__(
        self,
        register,
        documents,
        description,
        revert_method,
        revert_method_args=[],
        revert_method_kwargs={},
        rows_inserted=[],
        rows_removed=[],
        rows_updated=[],
        timeframe_rows_updated=[],
        main_text_rows_updated=[],
        tran_text_rows_updated=[],
        emit_signal=True,
    ):
        """
        Initialize a RevertableAction object.

        register: Action.* constant
        documents: list of Document.* constants
        description: Short one line description of action
        emit_signal: True if signal is to be sent on do, undo and redo events

        *_updated arguments should preferably be called without duplication.
        *_updated are all sorted on initialization.
        """
        self.register               = register
        self.documents              = documents
        self.description            = description
        self._revert_method         = revert_method
        self._revert_method_args    = revert_method_args
        self._revert_method_kwargs  = revert_method_kwargs
        self.rows_inserted          = rows_inserted
        self.rows_removed           = rows_removed
        self.rows_updated           = rows_updated
        self.timeframe_rows_updated = timeframe_rows_updated
        self.main_text_rows_updated = main_text_rows_updated
        self.tran_text_rows_updated = tran_text_rows_updated
        self.emit_signal            = emit_signal

        self._validate_input()

    def revert(self):
        """Revert action."""

        args   = self._revert_method_args
        kwargs = self._revert_method_kwargs

        # Get register attribute for revert action.
        if self.register in (Action.DO, Action.REDO):
            kwargs['register'] = Action.UNDO
        elif self.register == Action.UNDO:
            kwargs['register'] = Action.REDO

        self._revert_method(*args, **kwargs)

    def _validate_input(self):
        """
        Validate given attribute values.

        Raise ValueError if values of attributes are incorrect.
        """
        registers = (
            Action.DO,
            Action.UNDO,
            Action.REDO,
            Action.DO_MULTIPLE,
            Action.UNDO_MULTIPLE,
            Action.REDO_MULTIPLE,
        )

        if self.register not in registers:
            message = 'Incorrect register: "%s".' % self.register
            raise ValueError(message)

        main_in = Document.MAIN in self.documents
        tran_in = Document.TRAN in self.documents
        if not main_in and not tran_in:
            message = 'Incorrect documents: "%s".' % self.documents
            raise ValueError(message)

        self.rows_inserted.sort()
        self.rows_removed.sort()
        self.rows_updated.sort()
        self.timeframe_rows_updated.sort()
        self.main_text_rows_updated.sort()
        self.tran_text_rows_updated.sort()


class ActionGroup(object):

    """Group of revertable actions."""

    def __init__(self, actions, description):

        self.actions     = actions
        self.description = description


class ActionDelegate(Delegate):

    """Managing revertable actions."""

    def break_action_group(self, stack, index=0):
        """
        Break action group in stack into individual actions.

        Return amount of actions broken into.
        """
        action_group = stack.pop(index)
        for action in reversed(action_group.actions):
            stack.insert(0, action)

        return len(action_group.actions)

    def can_redo(self):
        """Return True if there's something that can be redone."""

        return bool(self.redoables)

    def can_undo(self):
        """Return True if there's something that can be undone."""

        return bool(self.undoables)

    def _emit_notification(self, actions, register):
        """Emit signal with a notification action."""

        action = self._get_notification_action(actions, register)
        signal = self.get_signal(register)
        self.emit(signal, action)

    def _get_destination_stack(self, register):
        """Get stack where registered action will be placed."""

        if register in (Action.DO, Action.DO_MULTIPLE):
            return self.undoables
        if register in (Action.UNDO, Action.UNDO_MULTIPLE):
            return self.redoables
        if register in (Action.REDO, Action.REDO_MULTIPLE):
            return self.undoables

    def _get_source_stack(self, register):
        """Get stack where action to register is."""

        if register in (Action.UNDO, Action.UNDO_MULTIPLE):
            return self.undoables
        if register in (Action.REDO, Action.REDO_MULTIPLE):
            return self.redoables

    def _get_notification_action(self, actions, register):
        """
        Get an action to notify of changes made by actions.

        Get an action that lists all changes that would be made if actions were
        registered (done or reverted) in the order given.
        """
        revert = False
        if register != Action.DO:
            revert = True

        rows_inserted          = []
        rows_removed           = []
        rows_updated           = []
        timeframe_rows_updated = []
        main_text_rows_updated = []
        tran_text_rows_updated = []

        all_updated_rows = [
            rows_updated,
            timeframe_rows_updated,
            main_text_rows_updated,
            tran_text_rows_updated
        ]

        for action in actions:

            if revert:
                inserted = action.rows_removed
                removed  = action.rows_inserted
            else:
                inserted = action.rows_inserted
                removed  = action.rows_removed

            # Adjust previous updates due to rows being removed.
            if removed:
                first_removed_row = min(removed)
                for i in range(len(all_updated_rows)):
                    for k in reversed(range(len(all_updated_rows[i]))):
                        updated_row = all_updated_rows[i][k]
                        # Remove updates to rows being removed.
                        if updated_row in removed:
                            all_updated_rows[i].pop(k)
                        # Shift updates to rows being moved.
                        elif updated_row > first_removed_row:
                            args = removed, updated_row
                            rows_above = bisect.bisect_left(*args)
                            all_updated_rows[i][k] -= rows_above

            # Adjust previous updates due to rows being inserted.
            for inserted_row in inserted:
                for i in range(len(all_updated_rows)):
                    # Shift updates to rows being moved.
                    for k, updated_row in enumerate(all_updated_rows[i]):
                        if updated_row >= inserted_row:
                            all_updated_rows[i][k] += 1

            rows_inserted          += inserted
            rows_removed           += removed
            rows_updated           += action.rows_updated
            timeframe_rows_updated += action.timeframe_rows_updated
            main_text_rows_updated += action.main_text_rows_updated
            tran_text_rows_updated += action.tran_text_rows_updated

        clean_up = listlib.sort_and_remove_duplicates

        return RevertableAction(
            register=register,
            documents=[Document.MAIN, Document.TRAN],
            description='',
            revert_method=None,
            rows_inserted=clean_up(rows_inserted),
            rows_removed=clean_up(rows_removed),
            rows_updated=clean_up(rows_updated),
            timeframe_rows_updated=clean_up(timeframe_rows_updated),
            main_text_rows_updated=clean_up(main_text_rows_updated),
            tran_text_rows_updated=clean_up(tran_text_rows_updated),
        )

    def get_signal(self, register):
        """Get signal matching register."""

        if register in (Action.DO, Action.DO_MULTIPLE):
            return 'action_done'
        if register in (Action.UNDO, Action.UNDO_MULTIPLE):
            return 'action_undone'
        if register in (Action.REDO, Action.REDO_MULTIPLE):
            return 'action_redone'

    def group_actions(self, register, amount, description, emit_signal=True):
        """Group amount of registered actions as one entity."""

        stack  = self._get_destination_stack(register)
        signal = self.get_signal(register)

        actions = []
        for i in range(amount):
            actions.append(stack.pop(0))
        action_group = ActionGroup(actions, description)
        stack.insert(0, action_group)

        if emit_signal:
            self._emit_notification(reversed(actions), register)

    def modify_action_description(self, register, description):
        """Modify the description of the most recent action."""

        if register is None:
            return

        stack = self._get_destination_stack(register)
        stack[0].description = description

    def redo(self, amount=1):
        """Redo actions."""

        if amount == 1:
            if not isinstance(self.redoables[0], ActionGroup):
                self.redoables[0].revert()
                self.redoables.pop(0)
                return

        self._revert_multiple(amount, Action.REDO_MULTIPLE)

    def register_action(self, *args, **kwargs):
        """
        Register action done, undone or redone.

        See RevertableAction.__init__ for arguments as they're passed directly
        for the action instantiation.
        """
        if kwargs['register'] is None:
            return

        action = RevertableAction(*args, **kwargs)

        # Restore action's original "DO" description if reverting.
        if action.register == Action.DO:
            self._register_action_done(action)
        elif action.register == Action.UNDO:
            action.description = self.undoables[0].description
            self._register_action_undone(action)
        elif action.register == Action.REDO:
            action.description = self.redoables[0].description
            self._register_action_redone(action)

    def _register_action_done(self, action):
        """Register action done."""

        self.undoables.insert(0, action)

        # Remove oldest undo action if level limit is exceeded.
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

        # Remove oldest undo action if level limit is exceeded.
        if self.undo_limit is not None:
            while len(self.undoables) > self.undo_limit:
                self.undoables.pop()

        self._shift_changed_value(action, 1)
        if action.emit_signal:
            self.emit('action_redone', action)

    def _register_action_undone(self, action):
        """Register action undone."""

        self.redoables.insert(0, action)

        # Remove oldest redo action if level limit is exceeded.
        if self.undo_limit is not None:
            while len(self.redoables) > self.undo_limit:
                self.redoables.pop()

        self._shift_changed_value(action, -1)
        if action.emit_signal:
            self.emit('action_undone', action)

    def _revert_multiple(self, amount, register):
        """Revert multiple actions."""

        signal = self.get_signal(register)
        stack  = self._get_source_stack(register)

        self.block(signal)
        actions = []
        for i in range(amount):
            sub_amount = 1
            if isinstance(stack[0], ActionGroup):
                description = stack[0].description
                sub_amount  = self.break_action_group(stack)
            for k in range(sub_amount):
                action = stack[0]
                actions.append(action)
                action.revert()
                stack.pop(0)
            if sub_amount > 1:
                self.group_actions(register, sub_amount, description, False)
        self.unblock(signal)

        self._emit_notification(actions, register)

    def _shift_changed_value(self, action, shift):
        """Shift value(s) of project's changed attributes."""

        if Document.MAIN in action.documents:
            self.main_changed += shift
        if Document.TRAN in action.documents:
            self.tran_changed += shift
        if action.documents == [Document.TRAN]:
            self.tran_active = True

    def undo(self, amount=1):
        """Undo actions."""

        if amount == 1:
            if not isinstance(self.undoables[0], ActionGroup):
                self.undoables[0].revert()
                self.undoables.pop(0)
                return

        self._revert_multiple(amount, Action.UNDO_MULTIPLE)


if __name__ == '__main__':

    from gaupol.test import Test

    class TestRevertableAction(Test):

        def test_revert(self):

            def revert_method(arg, kwarg, register):
                assert arg      == 'argument'
                assert kwarg    == 'keyword'
                assert register == Action.UNDO

            RevertableAction(
                Action.DO,
                documents=[Document.MAIN],
                description='test',
                revert_method=revert_method,
                revert_method_args=['argument'],
                revert_method_kwargs={'kwarg': 'keyword'},
            ).revert()

    class TestActionGroup(Test):

        def test_init(self):

            ActionGroup([], 'test')

    class TestActionDelegate(Test):

        def test_action_grouping(self):

            project = self.get_project()
            project.clear_texts([0], Document.MAIN)
            project.clear_texts([1], Document.MAIN)
            project.clear_texts([2], Document.MAIN)

            project.group_actions(Action.DO, 2, 'test')
            assert len(project.undoables) == 2
            assert project.undoables[0].description == 'test'
            assert len(project.undoables[0].actions) == 2

            project.break_action_group(project.undoables)
            assert len(project.undoables) == 3
            project.group_actions(Action.DO, 2, 'test')

            project.undo(1)
            assert len(project.undoables) == 1
            assert len(project.redoables) == 1
            assert project.redoables[0].description == 'test'
            assert len(project.redoables[0].actions) == 2

            project.redo(1)
            project.undo(2)

        def test_emit_notification(self):

            def on_action_done(action):
                assert isinstance(action, RevertableAction)

            project = self.get_project()
            delegate = ActionDelegate(project)
            project.clear_texts([0], Document.MAIN)
            project.clear_texts([1], Document.MAIN)
            project.connect('action_done', on_action_done)
            actions = reversed(project.undoables)
            delegate._emit_notification(actions, Action.DO)

        def test_get_notification_action(self):

            # 1
            project = self.get_project()
            delegate = ActionDelegate(project)
            project.clear_texts([0], Document.MAIN)
            project.insert_subtitles([0, 3])
            project.clear_texts([2], Document.MAIN)

            # Do
            actions = reversed(project.undoables)
            action = delegate._get_notification_action(actions, False)
            assert action.rows_inserted          == [0, 3]
            assert action.rows_removed           == []
            assert action.main_text_rows_updated == [1, 2]

            # Revert
            actions = project.undoables
            action = delegate._get_notification_action(actions, True)
            assert action.rows_inserted          == []
            assert action.rows_removed           == [0, 3]
            assert action.main_text_rows_updated == [0, 1]

            # 2
            project = self.get_project()
            delegate = ActionDelegate(project)
            project.clear_texts([0], Document.MAIN)
            project.remove_subtitles([0, 3])
            project.clear_texts([3], Document.MAIN)

            # Do
            actions = reversed(project.undoables)
            action = delegate._get_notification_action(actions, False)
            assert action.rows_inserted          == []
            assert action.rows_removed           == [0, 3]
            assert action.main_text_rows_updated == [3]

            # Revert
            actions = project.undoables
            action = delegate._get_notification_action(actions, True)
            assert action.rows_inserted          == [0, 3]
            assert action.rows_removed           == []
            assert action.main_text_rows_updated == [0, 5]

        def test_get_destination_stack(self):

            project = self.get_project()
            delegate = ActionDelegate(project)

            stacks = (
                (Action.DO           , project.undoables),
                (Action.UNDO         , project.redoables),
                (Action.REDO         , project.undoables),
                (Action.DO_MULTIPLE  , project.undoables),
                (Action.UNDO_MULTIPLE, project.redoables),
                (Action.REDO_MULTIPLE, project.undoables),
            )

            for register, stack in stacks:
                assert delegate._get_destination_stack(register) == stack

        def test_get_source_stack(self):

            project = self.get_project()
            delegate = ActionDelegate(project)

            stacks = (
                (Action.UNDO         , project.undoables),
                (Action.REDO         , project.redoables),
                (Action.UNDO_MULTIPLE, project.undoables),
                (Action.REDO_MULTIPLE, project.redoables),
            )

            for register, stack in stacks:
                assert delegate._get_source_stack(register) == stack

        def test_get_signal(self):

            project = self.get_project()

            signal = (
                (Action.DO           , 'action_done'  ),
                (Action.UNDO         , 'action_undone'),
                (Action.REDO         , 'action_redone'),
                (Action.DO_MULTIPLE  , 'action_done'  ),
                (Action.UNDO_MULTIPLE, 'action_undone'),
                (Action.REDO_MULTIPLE, 'action_redone'),
            )

            for register, signal in signal:
                assert project.get_signal(register) == signal

        def test_modify_action_description(self):

            project = self.get_project()
            project.clear_texts([0], Document.MAIN)
            project.modify_action_description(Action.DO, 'test')
            assert project.undoables[0].description == 'test'

        def test_revert_multiple(self):

            def on_action_undone_1(action):
                assert action.main_text_rows_updated == [0, 2]

            project = self.get_project()
            project.connect('action_undone', on_action_undone_1)

            project.clear_texts([0], Document.MAIN)
            project.insert_subtitles([1])
            project.clear_texts([1], Document.MAIN)
            project.clear_texts([3], Document.MAIN)
            project.undo(4)

            def on_action_undone_2(action):
                assert action.main_text_rows_updated == [1, 2, 3]

            project = self.get_project()
            project.connect('action_undone', on_action_undone_2)

            project.clear_texts([1], Document.MAIN)
            project.remove_subtitles([1])
            project.clear_texts([1], Document.MAIN)
            project.clear_texts([2], Document.MAIN)
            project.undo(4)

        def test_undo_and_redo(self):

            project = self.get_project()

            project.clear_texts([0], Document.MAIN)
            project.clear_texts([1], Document.MAIN)
            assert len(project.undoables) == 2
            assert project.main_changed == 2

            project.undo()
            assert project.main_texts[1] != ''
            assert len(project.undoables) == 1
            assert len(project.redoables) == 1
            assert project.main_changed == 1

            project.redo()
            assert project.main_texts[0] == ''
            assert len(project.undoables) == 2
            assert len(project.redoables) == 0
            assert project.main_changed == 2

            project.undo(2)
            assert project.main_texts[0] != ''
            assert project.main_texts[1] != ''
            assert len(project.undoables) == 0
            assert len(project.redoables) == 2
            assert project.main_changed == 0

            project.redo(2)
            assert project.main_texts[0] == ''
            assert project.main_texts[1] == ''
            assert len(project.undoables) == 2
            assert len(project.redoables) == 0
            assert project.main_changed == 2

    TestRevertableAction().run()
    TestActionGroup().run()
    TestActionDelegate().run()
