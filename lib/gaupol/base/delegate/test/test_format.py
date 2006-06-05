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
from gaupol.base.delegate.format import FormatDelegate
from gaupol.test                 import Test


MAIN = cons.Document.MAIN
TRAN = cons.Document.TRAN


class TestFormatDelegate(Test):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = FormatDelegate(self.project)

        for i in range(len(self.project.main_texts)):
            self.project.main_texts[i] = 'test\ntest'
            self.project.tran_texts[i] = 'test\ntest'

    def test_change_case(self):

        self.project.change_case([1, 3], MAIN, 'upper')
        assert self.project.main_texts[1] == 'TEST\nTEST'
        assert self.project.main_texts[3] == 'TEST\nTEST'

        self.project.undo()
        assert self.project.main_texts[1] == 'test\ntest'
        assert self.project.main_texts[3] == 'test\ntest'

        self.project.redo()
        assert self.project.main_texts[1] == 'TEST\nTEST'
        assert self.project.main_texts[3] == 'TEST\nTEST'

    def test_get_format_class_name(self):

        name = self.delegate._get_format_class_name(MAIN)
        assert name in cons.Format.class_names

    def test_get_tag_regex(self):

        regex = self.project.get_tag_regex(MAIN)
        assert hasattr(regex, 'match')

    def test_toggle_dialog_lines(self):

        self.project.toggle_dialog_lines([3, 4], MAIN)
        assert self.project.main_texts[3] == '- test\n- test'
        assert self.project.main_texts[4] == '- test\n- test'
        self.project.toggle_dialog_lines([3], MAIN)
        assert self.project.main_texts[3] == 'test\ntest'
        self.project.toggle_dialog_lines([3, 4], MAIN)
        assert self.project.main_texts[3] == '- test\n- test'
        assert self.project.main_texts[4] == '- test\n- test'

        self.project.undo(3)
        assert self.project.main_texts[3] == 'test\ntest'
        assert self.project.main_texts[4] == 'test\ntest'

        self.project.redo(3)
        assert self.project.main_texts[3] == '- test\n- test'
        assert self.project.main_texts[4] == '- test\n- test'

    def test_toggle_italicization(self):

        self.project.toggle_italicization([3, 4], MAIN)
        assert self.project.main_texts[3] == '<i>test\ntest</i>'
        assert self.project.main_texts[4] == '<i>test\ntest</i>'
        self.project.toggle_italicization([3], MAIN)
        assert self.project.main_texts[3] == 'test\ntest'
        self.project.toggle_italicization([3, 4], MAIN)
        assert self.project.main_texts[3] == '<i>test\ntest</i>'
        assert self.project.main_texts[4] == '<i>test\ntest</i>'

        self.project.undo(3)
        assert self.project.main_texts[3] == 'test\ntest'
        assert self.project.main_texts[4] == 'test\ntest'

        self.project.redo(3)
        assert self.project.main_texts[3] == '<i>test\ntest</i>'
        assert self.project.main_texts[4] == '<i>test\ntest</i>'
