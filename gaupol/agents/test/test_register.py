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


import gaupol
from gaupol import unittest


class TestRegisterAgent(unittest.TestCase):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = self.project.undo.im_self

    def test__break_action_group(self):

        self.project.clear_texts([0], gaupol.DOCUMENT.MAIN)
        self.project.clear_texts([1], gaupol.DOCUMENT.MAIN)
        self.project.clear_texts([2], gaupol.DOCUMENT.MAIN)
        self.project.group_actions(gaupol.REGISTER.DO, 3, "")
        self.delegate._break_action_group(self.project.undoables)
        assert len(self.project.undoables) == 3

    def test__get_destination_stack(self):

        stack = self.delegate._get_destination_stack(gaupol.REGISTER.DO)
        assert stack is self.project.undoables
        stack = self.delegate._get_destination_stack(gaupol.REGISTER.UNDO)
        assert stack is self.project.redoables
        stack = self.delegate._get_destination_stack(gaupol.REGISTER.REDO)
        assert stack is self.project.undoables

    def test__get_source_stack(self):

        stack = self.delegate._get_source_stack(gaupol.REGISTER.UNDO)
        assert stack is self.project.undoables
        stack = self.delegate._get_source_stack(gaupol.REGISTER.REDO)
        assert stack is self.project.redoables

    def test__on_notify_undo_limit(self):

        self.project.clear_texts([0], gaupol.DOCUMENT.MAIN)
        self.project.clear_texts([1], gaupol.DOCUMENT.MAIN)
        assert len(self.project.undoables) == 2
        self.project.undo_limit = 1
        assert len(self.project.undoables) == 1

    def test__revert_multiple(self):

        for i in range(6):
            self.project.clear_texts([i], gaupol.DOCUMENT.MAIN)
        self.project.group_actions(gaupol.REGISTER.DO, 3, "")
        self.project.remove_subtitles([3, 4])
        self.project.insert_blank_subtitles([3])
        self.project.undo(6)
        self.project.redo(6)

    def test__shift_changed_value(self):

        self.project.clear_texts([0], gaupol.DOCUMENT.MAIN)
        assert self.project.main_changed == 1
        self.project.clear_texts([1], gaupol.DOCUMENT.TRAN)
        assert self.project.tran_changed == 1

    def test_can_redo(self):

        assert not self.project.can_redo()
        self.project.clear_texts([0], gaupol.DOCUMENT.MAIN)
        assert not self.project.can_redo()
        self.project.undo()
        assert self.project.can_redo()

    def test_can_undo(self):

        assert not self.project.can_undo()
        self.project.clear_texts([0], gaupol.DOCUMENT.MAIN)
        assert self.project.can_undo()
        self.project.undo()
        assert not self.project.can_undo()

    def test_cut_reversion_stacks(self):

        self.project.clear_texts([0], gaupol.DOCUMENT.MAIN)
        self.project.clear_texts([1], gaupol.DOCUMENT.MAIN)
        self.project.cut_reversion_stacks()
        self.project.undo_limit = 1
        self.project.cut_reversion_stacks()

    def test_emit_action_signal(self):

        self.project.clear_texts([0], gaupol.DOCUMENT.MAIN)
        self.delegate.emit_action_signal(gaupol.REGISTER.DO)

    def test_group_actions(self):

        self.project.clear_texts([0], gaupol.DOCUMENT.MAIN)
        self.project.clear_texts([1], gaupol.DOCUMENT.MAIN)
        self.project.clear_texts([2], gaupol.DOCUMENT.MAIN)
        self.project.group_actions(gaupol.REGISTER.DO, 2, "")
        assert len(self.project.undoables) == 2
        assert self.project.undoables[0].description == ""
        assert len(self.project.undoables[0].actions) == 2

    def test_redo(self):

        self.project.clear_texts([0], gaupol.DOCUMENT.MAIN)
        self.project.clear_texts([1], gaupol.DOCUMENT.MAIN)
        self.project.clear_texts([2], gaupol.DOCUMENT.MAIN)
        self.project.undo(3)
        self.project.redo(1)
        self.project.redo(2)

    def test_register_action(self):

        self.project.clear_texts([0], gaupol.DOCUMENT.TRAN)
        self.project.clear_texts([1], gaupol.DOCUMENT.MAIN)
        self.project.clear_texts([2], gaupol.DOCUMENT.MAIN)
        self.project.undo(3)
        self.project.redo(2)
        assert len(self.project.undoables) == 2
        assert len(self.project.redoables) == 1

    def test_set_action_description(self):

        self.project.clear_texts([0], gaupol.DOCUMENT.MAIN)
        self.project.set_action_description(gaupol.REGISTER.DO, "")
        assert self.project.undoables[0].description == ""

    def test_undo(self):

        self.project.clear_texts([0], gaupol.DOCUMENT.MAIN)
        self.project.clear_texts([1], gaupol.DOCUMENT.MAIN)
        self.project.clear_texts([2], gaupol.DOCUMENT.MAIN)
        self.project.undo(1)
        self.project.undo(2)
        self.project.redo(3)
