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

import aeidon


class TestRevertableAction(aeidon.TestCase):

    def setup_method(self, method):
        self.revert_action_call_count = 0
        self.revert_action_register = None
        def revert_action(x, y, z=None, register=-1):
            self.revert_action_call_count += 1
            self.revert_action_register = register
            assert (x, y, z) == (0, 1, 2)
        self.action = aeidon.RevertableAction(description="")
        self.action.register = aeidon.registers.DO
        self.action.docs = (aeidon.documents.MAIN,)
        self.action.revert_args = (0, 1)
        self.action.revert_kwargs = {"z": 2}
        self.action.revert_function = revert_action

    def test_revert__do(self):
        self.action.register = aeidon.registers.DO
        self.action.revert()
        assert self.revert_action_call_count == 1
        register = self.revert_action_register
        assert register == aeidon.registers.UNDO

    def test_revert__redo(self):
        self.action.register = aeidon.registers.REDO
        self.action.revert()
        assert self.revert_action_call_count == 1
        register = self.revert_action_register
        assert register == aeidon.registers.UNDO

    def test_revert__undo(self):
        self.action.register = aeidon.registers.UNDO
        self.action.revert()
        assert self.revert_action_call_count == 1
        register = self.revert_action_register
        assert register == aeidon.registers.REDO


class TestRevertableActionGroup(aeidon.TestCase):

    def setup_method(self, method):
        self.action_group = aeidon.RevertableActionGroup(actions=())
        self.action_group.description = ""
