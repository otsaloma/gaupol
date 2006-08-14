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


import copy

from gaupol.base              import cons
from gaupol.base.icons        import *
from gaupol.base.delegate.set import SetDelegate
from gaupol.test              import Test


class TestSetDelegate(Test):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = SetDelegate(self.project)

        for i in range(len(self.project.main_texts)):
            self.project.main_texts[i] = 'test'
            self.project.tran_texts[i] = 'test'

    def test_sort_data(self):

        last = len(self.project.times) - 1
        orig_times = copy.deepcopy(self.project.times)
        self.project.main_texts[0] = 'first'
        self.project.set_frame(0, SHOW, 999999999999)
        assert self.project.times[:last] == orig_times[1:]
        assert self.project.main_texts[last] == 'first'

        self.project.undo()
        assert self.project.times[1:] == orig_times[1:]
        assert self.project.main_texts[0] == 'first'

        self.project.redo()
        assert self.project.times[:last] == orig_times[1:]
        assert self.project.main_texts[last] == 'first'

    def test_needs_resort(self):

        assert self.project.needs_resort(0, '99:59:59.999') is True
        assert self.project.needs_resort(0, '00:00:00.000') is False

    def test_set_frame(self):

        orig_hide_frame = self.project.frames[3][HIDE]
        orig_durn_frame = self.project.frames[3][DURN]
        orig_hide_time  = self.project.times[3][HIDE]
        orig_durn_time  = self.project.times[3][DURN]

        self.project.set_frame(3, HIDE, 999999)
        assert self.project.frames[3][HIDE] == 999999
        assert self.project.frames[3][DURN] >  orig_durn_frame
        assert self.project.times[3][HIDE]  >  orig_hide_time
        assert self.project.times[3][DURN]  >  orig_durn_time

        self.project.undo()
        assert self.project.frames[3][HIDE] == orig_hide_frame
        assert self.project.frames[3][DURN] == orig_durn_frame
        assert self.project.times[3][HIDE]  == orig_hide_time
        assert self.project.times[3][DURN]  == orig_durn_time

        self.project.redo()
        assert self.project.frames[3][HIDE] == 999999
        assert self.project.frames[3][DURN] >  orig_durn_frame
        assert self.project.times[3][HIDE]  >  orig_hide_time
        assert self.project.times[3][DURN]  >  orig_durn_time

    def test_set_text(self):

        self.project.set_text(2, MAIN, 's')
        assert self.project.main_texts[2] == 's'

        self.project.undo()
        assert self.project.main_texts[2] == 'test'

        self.project.redo()
        assert self.project.main_texts[2] == 's'

    def test_set_time(self):

        orig_hide_time  = self.project.times[3][HIDE]
        orig_durn_time  = self.project.times[3][DURN]
        orig_hide_frame = self.project.frames[3][HIDE]
        orig_durn_frame = self.project.frames[3][DURN]

        self.project.set_time(3, DURN, '33:33:33.333')
        assert self.project.times[3][HIDE]  >  orig_hide_time
        assert self.project.times[3][DURN]  == '33:33:33.333'
        assert self.project.frames[3][HIDE] >  orig_hide_frame
        assert self.project.frames[3][DURN] >  orig_durn_frame

        self.project.undo()
        assert self.project.times[3][HIDE]  == orig_hide_time
        assert self.project.times[3][DURN]  == orig_durn_time
        assert self.project.frames[3][HIDE] == orig_hide_frame
        assert self.project.frames[3][DURN] == orig_durn_frame

        self.project.redo()
        assert self.project.times[3][HIDE]  >  orig_hide_time
        assert self.project.times[3][DURN]  == '33:33:33.333'
        assert self.project.frames[3][HIDE] >  orig_hide_frame
        assert self.project.frames[3][DURN] >  orig_durn_frame
