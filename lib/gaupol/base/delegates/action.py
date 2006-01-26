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
Managing actions.

To hook some method up with the undo-redo system the following needs to be done
(1) The last argument to the function should be a keyword argument "register"
with a default value of Action.DO.
(2) At the end of the method, method "register_action" should be called with
keyword arguments specified in RevertableAction.__init__.

To do some action without possibility of reverting, None can be given as a
value to the "register" keyword argument.

All data-changing methods need to come in pairs as each action needs to be
revertable. For example insert_subtitles and remove_subtitles form a pair.

During the "register_action" method, a signal will be emitted notifying that
an action was done. Any possible UI can hook up to that signal and use it to
refresh the data display.

Currently, there is no ability to group actions. This makes it impossible to,
for example, insert new rows while pasting if clipboard contents don't fit in
the existing rows.
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
        timing_rows_updated=[],
        main_text_rows_updated=[],
        tran_text_rows_updated=[]
    ):
        """
        Initialize a RevertableAction object.

        register: Action.DO, Action.UNDO or Action.REDO
        documents: list of document constants (Document.MAIN, Document.TRAN)
        description: Short one line description of action
        revert_method: Method called to revert action

        *_updated arguments should preferably be called without duplication.
        *_updated are all in sorted order.
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
        self.timing_rows_updated    = timing_rows_updated
        self.main_text_rows_updated = main_text_rows_updated
        self.tran_text_rows_updated = tran_text_rows_updated

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
            Action.UNDO_MULTIPLE,
            Action.REDO_MULTIPLE,
        )

        if self.register not in registers:
            message = 'Incorrect register: "%s".' % self.register
            raise ValueError(message)

        if Document.MAIN not in self.documents and \
           Document.TRAN not in self.documents:
               message = 'Incorrect documents: "%s".' % self.documents
               raise ValueError(message)

        # Sort all row data.
        self.rows_inserted.sort()
        self.rows_removed.sort()
        self.rows_updated.sort()
        self.timing_rows_updated.sort()
        self.main_text_rows_updated.sort()
        self.tran_text_rows_updated.sort()


class ActionDelegate(Delegate):

    """Managing actions."""

    def can_redo(self):
        """Return True if there's something that can be redone."""

        return bool(self.redoables)

    def can_undo(self):
        """Return True if there's something that can be undone."""

        return bool(self.undoables)

    def modify_action_description(self, register, description):
        """Modify the description of the most recent action."""

        if register in (Action.DO, Action.REDO):
            self.undoables[0].description = description
        if register == Action.UNDO:
            self.redoables[0].description = description

    def redo(self, amount=1):
        """Redo actions."""

        if amount == 1:
            self.redoables[0].revert()
            self.redoables.pop(0)
        elif amount > 1:
            self._revert_multiple(amount, Action.REDO_MULTIPLE)

    def register_action(self, *args, **kwargs):
        """
        Register action done, undone or redone.

        See RevertableAction.__init__ for arguments as they're passed directly
        for there for the action instatiation.
        """
        if kwargs['register'] is None:
            return

        action = RevertableAction(*args, **kwargs)

        # Restore action's original "DO" description.
        if action.register == Action.UNDO:
            action.description = self.undoables[0].description
        elif action.register == Action.REDO:
            action.description = self.redoables[0].description

        # Register action.
        if action.register == Action.DO:
            self._register_action_done(action)
        elif action.register == Action.UNDO:
            self._register_action_undone(action)
        elif action.register == Action.REDO:
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
        self.emit('action_done', action)

    def _register_action_redone(self, action):
        """Register action redone."""

        self.undoables.insert(0, action)

        # Remove oldest undo action if level limit is exceeded.
        if self.undo_limit is not None:
            while len(self.undoables) > self.undo_limit:
                self.undoables.pop()

        self._shift_changed_value(action, 1)
        self.emit('action_redone', action)

    def _register_action_undone(self, action):
        """Register action undone."""

        self.redoables.insert(0, action)

        # Remove oldest redo action if level limit is exceeded.
        if self.undo_limit is not None:
            while len(self.redoables) > self.undo_limit:
                self.redoables.pop()

        self._shift_changed_value(action, -1)
        self.emit('action_undone', action)

    def _revert_multiple(self, amount, register):
        """Revert multiple actions."""

        if register == Action.UNDO_MULTIPLE:
            signal = 'action_undone'
            stack  = self.undoables
        elif register == Action.REDO_MULTIPLE:
            signal = 'action_redone'
            stack  = self.redoables

        # For simplicity log updates only for full rows.
        rows_inserted = []
        rows_removed  = []
        rows_updated  = []

        # Block signals of individual actions.
        self.block(signal)

        for i in range(amount):

            action = stack[0]
            action.revert()

            # Adjust previous updates to rows now being removed.
            if action.rows_inserted:
                first_row = min(action.rows_inserted)
                for i in reversed(range(len(rows_updated))):

                    # Remove updates to rows that will no longer exist.
                    if rows_updated[i] in action.rows_inserted:
                        rows_updated.pop(i)

                    # Shift updates according to new row count.
                    elif rows_updated[i] > first_row:
                        lst = action.rows_inserted
                        rows_above = bisect.bisect_left(lst, rows_updated[i])
                        rows_updated[i] -= rows_above

            # Adjust previous updates to rows now being inserted.
            for row in action.rows_removed:
                for i in range(len(rows_updated)):
                    if rows_updated[i] >= row:
                        rows_updated[i] += 1

            rows_inserted += action.rows_inserted
            rows_removed  += action.rows_removed
            rows_updated  += action.rows_updated
            rows_updated  += action.timing_rows_updated
            rows_updated  += action.main_text_rows_updated
            rows_updated  += action.tran_text_rows_updated

            stack.pop(0)

        self.unblock(signal)

        # Sort and remove duplicates from lists of updates.
        for data in (rows_inserted, rows_removed, rows_updated):
            data = listlib.sort_and_remove_duplicates(data)

        # Create an action to deliver information of reverting.
        action = RevertableAction(
            register=register,
            documents=[Document.MAIN, Document.TRAN],
            description='',
            revert_method=None,
            rows_inserted=rows_inserted,
            rows_removed=rows_removed,
            rows_updated=rows_updated,
        )

        self.emit(signal, action)

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
            self.undoables[0].revert()
            self.undoables.pop(0)
        elif amount > 1:
            self._revert_multiple(amount, Action.UNDO_MULTIPLE)
            return


if __name__ == '__main__':

    from gaupol.test import Test

    class TestRevertableAction(Test):

        def test_revert(self):

            def revert_method(arg, kwarg, register):
                assert arg      == 'foo'
                assert kwarg    == 'bar'
                assert register == Action.UNDO

            RevertableAction(
                Action.DO,
                documents=[Document.MAIN],
                description='foo',
                revert_method=revert_method,
                revert_method_args=['foo'],
                revert_method_kwargs={'kwarg': 'bar'},
            ).revert()

    class TestActionDelegate(Test):

        def test_modify_action_description(self):

            project = self.get_project()
            project.clear_texts([0], Document.MAIN)
            project.modify_action_description(Action.DO, 'foo')
            assert project.undoables[0].description == 'foo'

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

        def test_revert_multiple(self):

            def on_action_undone_1(action):
                assert action.rows_updated == [0, 2]

            project = self.get_project()
            project.connect('action_undone', on_action_undone_1)

            project.clear_texts([0], Document.MAIN)
            project.insert_subtitles([1])
            project.clear_texts([1], Document.MAIN)
            project.clear_texts([3], Document.MAIN)
            project.undo(4)

            def on_action_undone_2(action):
                assert action.rows_updated == [1, 2, 3]

            project = self.get_project()
            project.connect('action_undone', on_action_undone_2)

            project.clear_texts([1], Document.MAIN)
            project.remove_subtitles([1])
            project.clear_texts([1], Document.MAIN)
            project.clear_texts([2], Document.MAIN)
            project.undo(4)

    TestRevertableAction().run()
    TestActionDelegate().run()
