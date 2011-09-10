# Copyright (C) 2005-2009 Osmo Salomaa
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

import aeidon

MAIN = aeidon.documents.MAIN
TRAN = aeidon.documents.TRAN


class TestRegisterAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()
        self.delegate = self.project.undo.__self__

    def test__on_notify_undo_limit(self):
        self.project.clear_texts((0,), MAIN)
        self.project.clear_texts((1,), MAIN)
        assert len(self.project.undoables) == 2
        self.project.undo_limit = 1
        assert len(self.project.undoables) == 1

    def test_can_redo(self):
        assert not self.project.can_redo()
        self.project.clear_texts((0,), MAIN)
        assert not self.project.can_redo()
        self.project.undo()
        assert self.project.can_redo()

    def test_can_undo(self):
        assert not self.project.can_undo()
        self.project.clear_texts((0,), MAIN)
        assert self.project.can_undo()
        self.project.undo()
        assert not self.project.can_undo()

    def test_cut_reversion_stacks(self):
        self.project.clear_texts((0,), MAIN)
        self.project.clear_texts((1,), MAIN)
        self.project.cut_reversion_stacks()
        self.project.undo_limit = 1
        self.project.cut_reversion_stacks()

    def test_emit_action_signal(self):
        self.project.clear_texts((0,), MAIN)
        self.project.emit_action_signal(aeidon.registers.DO)

    def test_group_actions(self):
        self.project.clear_texts((0,), MAIN)
        self.project.clear_texts((1,), MAIN)
        self.project.clear_texts((2,), MAIN)
        self.project.group_actions(aeidon.registers.DO, 2, "")
        assert len(self.project.undoables) == 2
        assert self.project.undoables[0].description == ""
        assert len(self.project.undoables[0].actions) == 2

    def test_redo(self):
        self.project.clear_texts((0,), MAIN)
        self.project.clear_texts((1,), MAIN)
        self.project.clear_texts((2,), MAIN)
        self.project.undo(3)
        self.project.redo(1)
        self.project.redo(2)

    def test_redo__multiple(self):
        for i in range(6):
            self.project.clear_texts([i], MAIN)
        self.project.group_actions(aeidon.registers.DO, 3, "")
        self.project.remove_subtitles((3, 4))
        self.project.insert_subtitles((3,))
        self.project.undo(6)
        self.project.redo(6)

    def test_register_action(self):
        self.project.clear_texts((0,), TRAN)
        self.project.clear_texts((1,), MAIN)
        self.project.clear_texts((2,), MAIN)
        self.project.undo(3)
        self.project.redo(2)
        assert len(self.project.undoables) == 2
        assert len(self.project.redoables) == 1

    def test_register_action__activate_translation(self):
        path = self.new_subrip_file()
        self.project.open_main(path, "ascii")
        assert self.project.tran_changed is None
        self.project.clear_texts((1,), TRAN)
        assert self.project.tran_changed == 1

    def test_set_action_description(self):
        self.project.clear_texts((0,), MAIN)
        self.project.set_action_description(aeidon.registers.DO, "")
        assert self.project.undoables[0].description == ""

    def test_undo(self):
        self.project.clear_texts((0,), MAIN)
        self.project.clear_texts((1,), MAIN)
        self.project.clear_texts((2,), MAIN)
        self.project.undo(1)
        self.project.undo(2)
        self.project.redo(3)

    def test_undo__multiple(self):
        for i in range(6):
            self.project.clear_texts([i], MAIN)
        self.project.group_actions(aeidon.registers.DO, 3, "")
        self.project.remove_subtitles((3, 4))
        self.project.insert_subtitles((3,))
        self.project.undo(6)
        self.project.redo(6)
