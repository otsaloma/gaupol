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


from gaupol.base                 import cons
from gaupol.base.icons           import *
from gaupol.base.delegate.action import RevertableAction
from gaupol.base.delegate.action import RevertableActionDelegate
from gaupol.base.delegate.action import RevertableActionGroup
from gaupol.test                 import Test


class TestRevertableAction(Test):

    def test_revert(self):

        def revert_method(arg, kwarg, register):
            assert arg == 'argument'
            assert kwarg == 'keyword'
            assert register == cons.Action.UNDO

        RevertableAction(
            cons.Action.DO,
            docs=[MAIN],
            description='test',
            revert_method=revert_method,
            revert_args=['argument'],
            revert_kwargs={'kwarg': 'keyword'},
        ).revert()


class TestRevertableActionGroup(Test):

    def test_init(self):

        RevertableActionGroup([], 'test')


class TestRevertableActionDelegate(Test):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = RevertableActionDelegate(self.project)

    def test_emit_notification(self):

        def on_action_done(action):
            assert isinstance(action, RevertableAction)

        self.project.clear_texts([0], MAIN)
        self.project.clear_texts([1], MAIN)
        self.project.connect('action_done', on_action_done)
        actions = reversed(self.project.undoables)
        self.delegate._emit_notification(actions, cons.Action.DO)

    def test_get_destination_stack(self):

        stacks = (
            (cons.Action.DO           , self.project.undoables),
            (cons.Action.UNDO         , self.project.redoables),
            (cons.Action.REDO         , self.project.undoables),
            (cons.Action.DO_MULTIPLE  , self.project.undoables),
            (cons.Action.UNDO_MULTIPLE, self.project.redoables),
            (cons.Action.REDO_MULTIPLE, self.project.undoables),
        )
        for register, stack in stacks:
            assert self.delegate._get_destination_stack(register) == stack

    def test_get_notification_action_insert(self):

        self.project.clear_texts([0], MAIN)
        self.project.insert_subtitles([0, 3])
        self.project.clear_texts([2], MAIN)

        actions = reversed(self.project.undoables)
        action = self.delegate._get_notification_action(actions, False)
        assert action.inserted_rows == [0, 3]
        assert action.removed_rows == []
        assert action.updated_main_texts == [1, 2]

        actions = self.project.undoables
        action = self.delegate._get_notification_action(actions, True)
        assert action.inserted_rows == []
        assert action.removed_rows == [0, 3]
        assert action.updated_main_texts == [0, 1]

    def test_get_notification_action_remove(self):

        self.project.clear_texts([0], MAIN)
        self.project.remove_subtitles([0, 3])
        self.project.clear_texts([3], MAIN)

        actions = reversed(self.project.undoables)
        action = self.delegate._get_notification_action(actions, False)
        assert action.inserted_rows == []
        assert action.removed_rows == [0, 3]
        assert action.updated_main_texts == [3]

        actions = self.project.undoables
        action = self.delegate._get_notification_action(actions, True)
        assert action.inserted_rows == [0, 3]
        assert action.removed_rows == []
        assert action.updated_main_texts == [0, 5]

    def test_get_source_stack(self):

        stacks = (
            (cons.Action.UNDO         , self.project.undoables),
            (cons.Action.REDO         , self.project.redoables),
            (cons.Action.UNDO_MULTIPLE, self.project.undoables),
            (cons.Action.REDO_MULTIPLE, self.project.redoables),
        )

        for register, stack in stacks:
            assert self.delegate._get_source_stack(register) == stack

    def test_revert_multiple_insert(self):

        def on_action_undone(action):
            assert action.updated_main_texts == [0, 2]

        self.project.connect('action_undone', on_action_undone)
        self.project.clear_texts([0], MAIN)
        self.project.insert_subtitles([1])
        self.project.clear_texts([1], MAIN)
        self.project.clear_texts([3], MAIN)
        self.project.undo(4)

    def test_revert_multiple_remove(self):

        def on_action_undone(action):
            assert action.updated_main_texts == [1, 2, 3]

        self.project.connect('action_undone', on_action_undone)
        self.project.clear_texts([1], MAIN)
        self.project.remove_subtitles([1])
        self.project.clear_texts([1], MAIN)
        self.project.clear_texts([2], MAIN)
        self.project.undo(4)

    def test_can_redo_and_undo(self):

        assert self.project.can_undo() is False
        assert self.project.can_redo() is False

        self.project.clear_texts([0], MAIN)
        assert self.project.can_undo() is True
        assert self.project.can_redo() is False

        self.project.undo()
        assert self.project.can_undo() is False
        assert self.project.can_redo() is True

    def test_get_signal(self):

        signals = (
            (cons.Action.DO           , 'action_done'  ),
            (cons.Action.UNDO         , 'action_undone'),
            (cons.Action.REDO         , 'action_redone'),
            (cons.Action.DO_MULTIPLE  , 'action_done'  ),
            (cons.Action.UNDO_MULTIPLE, 'action_undone'),
            (cons.Action.REDO_MULTIPLE, 'action_redone'),
        )
        for register, signal in signals:
            assert self.project.get_signal(register) == signal

    def test_group_and_break_actions(self):

        self.project.clear_texts([0], MAIN)
        self.project.clear_texts([1], MAIN)
        self.project.clear_texts([2], MAIN)

        self.project.group_actions(cons.Action.DO, 2, 'test')
        assert len(self.project.undoables) == 2
        assert self.project.undoables[0].description == 'test'
        assert len(self.project.undoables[0].actions) == 2

        self.delegate._break_action_group(self.project.undoables)
        assert len(self.project.undoables) == 3
        self.project.group_actions(cons.Action.DO, 2, 'test')

        self.project.undo()
        assert len(self.project.undoables) == 1
        assert len(self.project.redoables) == 1
        assert self.project.redoables[0].description == 'test'
        assert len(self.project.redoables[0].actions) == 2

        self.project.redo()
        assert len(self.project.undoables) == 2
        assert len(self.project.redoables) == 0
        assert self.project.undoables[0].description == 'test'
        assert len(self.project.undoables[0].actions) == 2

        self.project.undo(2)
        assert len(self.project.undoables) == 0
        assert len(self.project.redoables) == 2
        assert self.project.redoables[1].description == 'test'
        assert len(self.project.redoables[1].actions) == 2

    def test_redo_and_undo(self):

        self.project.clear_texts([0], MAIN)
        self.project.clear_texts([1], MAIN)
        assert len(self.project.undoables) == 2
        assert self.project.main_changed == 2

        self.project.undo()
        assert self.project.main_texts[1] != ''
        assert len(self.project.undoables) == 1
        assert len(self.project.redoables) == 1
        assert self.project.main_changed == 1

        self.project.redo()
        assert self.project.main_texts[0] == ''
        assert len(self.project.undoables) == 2
        assert len(self.project.redoables) == 0
        assert self.project.main_changed == 2

        self.project.undo(2)
        assert self.project.main_texts[0] != ''
        assert self.project.main_texts[1] != ''
        assert len(self.project.undoables) == 0
        assert len(self.project.redoables) == 2
        assert self.project.main_changed == 0

        self.project.redo(2)
        assert self.project.main_texts[0] == ''
        assert self.project.main_texts[1] == ''
        assert len(self.project.undoables) == 2
        assert len(self.project.redoables) == 0
        assert self.project.main_changed == 2

    def test_set_action_description(self):

        self.project.clear_texts([0], MAIN)
        self.project.set_action_description(cons.Action.DO, 'test')
        assert self.project.undoables[0].description == 'test'
