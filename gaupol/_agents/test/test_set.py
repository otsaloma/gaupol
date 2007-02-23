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


from gaupol import cons
from gaupol.unittest import TestCase, reversion_test
from ..index import SHOW, HIDE, DURN


class TestSetAgent(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()

    def test_needs_resort(self):

        assert self.project.needs_resort(0, "99:59:59.999")
        assert self.project.needs_resort(0, 999999)
        assert not self.project.needs_resort(0, "00:00:00.000")
        assert not self.project.needs_resort(0, 0)

    @reversion_test
    def test_set_position_frame_durn(self):

        time = self.project.times[3][:]
        frame = self.project.frames[3][:]
        self.project.set_position(3, DURN, 0)
        assert self.project.times[3][SHOW] == time[SHOW]
        assert self.project.times[3][HIDE] == time[SHOW]
        assert self.project.times[3][DURN] == "00:00:00.000"
        assert self.project.frames[3][SHOW] == frame[SHOW]
        assert self.project.frames[3][HIDE] == frame[SHOW]
        assert self.project.frames[3][DURN] == 0

    @reversion_test
    def test_set_position_frame_hide(self):

        time = self.project.times[3][:]
        frame = self.project.frames[3][:]
        self.project.set_position(3, HIDE, 999999)
        assert self.project.times[3][SHOW] == time[SHOW]
        assert self.project.times[3][HIDE] != time[HIDE]
        assert self.project.times[3][DURN] != time[DURN]
        assert self.project.frames[3][SHOW] == frame[SHOW]
        assert self.project.frames[3][HIDE] == 999999
        assert self.project.frames[3][DURN] != frame[DURN]

    @reversion_test
    def test_set_position_frame_show(self):

        time = self.project.times[3][:]
        frame = self.project.frames[3][:]
        main_text = self.project.main_texts[3][:]
        tran_text = self.project.tran_texts[3][:]
        self.project.set_position(3, SHOW, 0)
        assert self.project.times[0][SHOW] == "00:00:00.000"
        assert self.project.times[0][HIDE] == time[HIDE]
        assert self.project.times[0][DURN] != time[DURN]
        assert self.project.frames[0][SHOW] == 0
        assert self.project.frames[0][HIDE] == frame[HIDE]
        assert self.project.frames[0][DURN] != frame[DURN]
        assert self.project.main_texts[0] == main_text
        assert self.project.tran_texts[0] == tran_text

    @reversion_test
    def test_set_position_time_durn(self):

        time = self.project.times[3][:]
        frame = self.project.frames[3][:]
        self.project.set_position(3, DURN, "00:00:00.000")
        assert self.project.times[3][SHOW] == time[SHOW]
        assert self.project.times[3][HIDE] == time[SHOW]
        assert self.project.times[3][DURN] == "00:00:00.000"
        assert self.project.frames[3][SHOW] == frame[SHOW]
        assert self.project.frames[3][HIDE] == frame[SHOW]
        assert self.project.frames[3][DURN] == 0

    @reversion_test
    def test_set_position_time_hide(self):

        time = self.project.times[3][:]
        frame = self.project.frames[3][:]
        self.project.set_position(3, HIDE, "99:59:59.999")
        assert self.project.times[3][SHOW] == time[SHOW]
        assert self.project.times[3][HIDE] == "99:59:59.999"
        assert self.project.times[3][DURN] != time[DURN]
        assert self.project.frames[3][SHOW] == frame[SHOW]
        assert self.project.frames[3][HIDE] != frame[SHOW]
        assert self.project.frames[3][DURN] != frame[DURN]

    @reversion_test
    def test_set_position_time_show(self):

        time = self.project.times[3][:]
        frame = self.project.frames[3][:]
        main_text = self.project.main_texts[3][:]
        tran_text = self.project.tran_texts[3][:]
        self.project.set_position(3, SHOW, "00:00:00.000")
        assert self.project.times[0][SHOW] == "00:00:00.000"
        assert self.project.times[0][HIDE] == time[HIDE]
        assert self.project.times[0][DURN] != time[DURN]
        assert self.project.frames[0][SHOW] == 0
        assert self.project.frames[0][HIDE] == frame[HIDE]
        assert self.project.frames[0][DURN] != frame[DURN]
        assert self.project.main_texts[0] == main_text
        assert self.project.tran_texts[0] == tran_text

    @reversion_test
    def test_set_text_main(self):

        self.project.set_text(2, cons.DOCUMENT.MAIN, "")
        assert self.project.main_texts[2] == ""

    @reversion_test
    def test_set_text_tran(self):

        self.project.set_text(2, cons.DOCUMENT.TRAN, "")
        assert self.project.tran_texts[2] == ""
