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


from gaupol import const
from gaupol.unittest import TestCase
from ..register import RevertableAction, RevertableActionGroup


class TestModule(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()

    def test_revertable(self):

        self.project.undo_limit = 2
        self.project.clear_texts([0], const.DOCUMENT.MAIN)
        self.project.clear_texts([1], const.DOCUMENT.MAIN)
        self.project.clear_texts([2], const.DOCUMENT.TRAN)
        assert self.project.main_changed == 2
        assert self.project.tran_changed == 1
        assert len(self.project.undoables) == 2


class TestRevertableAction(TestCase):

    def setup_method(self, method):

        def revert(register=-1):
            assert register in const.REGISTER.members

        self.action = RevertableAction(
            register=const.REGISTER.DO,
            docs=[const.DOCUMENT.MAIN],
            description="",
            revert_method=revert,
            revert_args=[],
            revert_kwargs={},)

    def test_revert(self):

        self.action.revert()


class TestRevertableActionGroup(TestCase):

    def test___init__(self):

        RevertableActionGroup([], "")


class TestRegisterAgent(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = self.project.undo.im_self

    def test__break_action_group(self):

        self.project.clear_texts([0], const.DOCUMENT.MAIN)
        self.project.clear_texts([1], const.DOCUMENT.MAIN)
        self.project.clear_texts([2], const.DOCUMENT.MAIN)
        self.project.group_actions(const.REGISTER.DO, 3, "test")
        self.delegate._break_action_group(self.project.undoables)
        assert len(self.project.undoables) == 3

    def test__get_destination_stack(self):

        stacks = (
            (const.REGISTER.DO           , self.project.undoables),
            (const.REGISTER.UNDO         , self.project.redoables),
            (const.REGISTER.REDO         , self.project.undoables),
            (const.REGISTER.DO_MULTIPLE  , self.project.undoables),
            (const.REGISTER.UNDO_MULTIPLE, self.project.redoables),
            (const.REGISTER.REDO_MULTIPLE, self.project.undoables),)
        for register, stack in stacks:
            assert self.delegate._get_destination_stack(register) == stack

    def test__get_source_stack(self):

        stacks = (
            (const.REGISTER.UNDO         , self.project.undoables),
            (const.REGISTER.REDO         , self.project.redoables),
            (const.REGISTER.UNDO_MULTIPLE, self.project.undoables),
            (const.REGISTER.REDO_MULTIPLE, self.project.redoables),)
        for register, stack in stacks:
            assert self.delegate._get_source_stack(register) == stack

    def test__on_notify_undo_limit(self):

        self.project.clear_texts([0], const.DOCUMENT.MAIN)
        self.project.clear_texts([1], const.DOCUMENT.MAIN)
        assert len(self.project.undoables) == 2
        self.project.undo_limit = 1
        assert len(self.project.undoables) == 1

    def test__revert_multiple(self):

        for i in range(6):
            self.project.clear_texts([i], const.DOCUMENT.MAIN)
        self.project.group_actions(const.REGISTER.DO, 3, "")
        self.project.remove_subtitles([3, 4])
        self.project.insert_blank_subtitles([3])
        self.project.undo(6)
        self.project.redo(6)

    def test__shift_changed_value(self):

        self.project.clear_texts([0], const.DOCUMENT.MAIN)
        self.project.clear_texts([1], const.DOCUMENT.TRAN)
        assert self.project.main_changed == 1
        assert self.project.tran_changed == 1
        assert self.project.tran_active

    def test_can_redo(self):

        assert not self.project.can_redo()
        self.project.clear_texts([0], const.DOCUMENT.MAIN)
        assert not self.project.can_redo()
        self.project.undo()
        assert self.project.can_redo()

    def test_can_undo(self):

        assert not self.project.can_undo()
        self.project.clear_texts([0], const.DOCUMENT.MAIN)
        assert self.project.can_undo()
        self.project.undo()
        assert not self.project.can_undo()

    def test_cut_reversion_stacks(self):

        self.project.clear_texts([0], const.DOCUMENT.MAIN)
        self.project.clear_texts([1], const.DOCUMENT.MAIN)
        self.project.cut_reversion_stacks()
        self.project.undo_limit = 1
        self.project.cut_reversion_stacks()

    def test_emit_action_signal(self):

        def on_action_done(project, action):
            assert isinstance(action, RevertableAction)
        self.project.clear_texts([0], const.DOCUMENT.MAIN)
        self.project.clear_texts([1], const.DOCUMENT.MAIN)
        self.project.connect("action-done", on_action_done)
        self.delegate.emit_action_signal(const.REGISTER.DO, 1)
        self.delegate.emit_action_signal(const.REGISTER.DO, 2)

    def test_group_actions(self):

        self.project.clear_texts([0], const.DOCUMENT.MAIN)
        self.project.clear_texts([1], const.DOCUMENT.MAIN)
        self.project.clear_texts([2], const.DOCUMENT.MAIN)
        self.project.group_actions(const.REGISTER.DO, 2, "test")
        assert len(self.project.undoables) == 2
        assert self.project.undoables[0].description == "test"
        assert len(self.project.undoables[0].actions) == 2

    def test_redo(self):

        self.project.clear_texts([0], const.DOCUMENT.MAIN)
        self.project.clear_texts([1], const.DOCUMENT.MAIN)
        self.project.clear_texts([2], const.DOCUMENT.MAIN)
        self.project.undo(3)
        self.project.redo(1)
        self.project.redo(2)

    def test_register_action(self):

        self.project.clear_texts([0], const.DOCUMENT.TRAN)
        self.project.clear_texts([1], const.DOCUMENT.MAIN)
        self.project.clear_texts([2], const.DOCUMENT.MAIN)
        self.project.undo(3)
        self.project.redo(2)
        assert len(self.project.undoables) == 2
        assert len(self.project.redoables) == 1
        assert self.project.main_changed == 1
        assert self.project.tran_changed == 1
        assert self.project.tran_active

    def test_set_action_description(self):

        self.project.clear_texts([0], const.DOCUMENT.MAIN)
        self.project.set_action_description(const.REGISTER.DO, "test")
        assert self.project.undoables[0].description == "test"

    def test_undo(self):

        self.project.clear_texts([0], const.DOCUMENT.MAIN)
        self.project.clear_texts([1], const.DOCUMENT.MAIN)
        self.project.clear_texts([2], const.DOCUMENT.MAIN)
        self.project.undo(1)
        self.project.undo(2)
        self.project.redo(3)
