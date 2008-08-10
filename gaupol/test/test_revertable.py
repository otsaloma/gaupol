# Copyright (C) 2005-2008 Osmo Salomaa
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

import gaupol


class TestRevertableAction(gaupol.TestCase):

    def setup_method(self, method):

        self.revert_action_call_count = 0
        self.revert_action_register = None
        def revert_action(x, y, z=None, register=-1):
            self.revert_action_call_count += 1
            self.revert_action_register = register
            assert (x, y, z) == (0, 1, 2)
        self.action = gaupol.RevertableAction(description="")
        self.action.register = gaupol.registers.DO
        self.action.docs = (gaupol.documents.MAIN,)
        self.action.revert_args = (0, 1)
        self.action.revert_kwargs = {"z": 2}
        self.action.revert_method = revert_action

    def test_revert__do(self):

        self.action.register = gaupol.registers.DO
        self.action.revert()
        assert self.revert_action_call_count == 1
        register = self.revert_action_register
        assert register== gaupol.registers.UNDO

    def test_revert__redo(self):

        self.action.register = gaupol.registers.REDO
        self.action.revert()
        assert self.revert_action_call_count == 1
        register = self.revert_action_register
        assert register== gaupol.registers.UNDO

    def test_revert__undo(self):

        self.action.register = gaupol.registers.UNDO
        self.action.revert()
        assert self.revert_action_call_count == 1
        register = self.revert_action_register
        assert register== gaupol.registers.REDO


class TestRevertableActionGroup(gaupol.TestCase):

    def setup_method(self, method):

        self.action_group = gaupol.RevertableActionGroup(actions=())
        self.action_group.description = ""
