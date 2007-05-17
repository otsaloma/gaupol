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
from gaupol.unittest import TestCase, reversion_test


class TestSetAgent(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()

    @reversion_test
    def test_set_duration__frame(self):

        subtitles = self.project.subtitles
        self.project.set_duration(0, 1)
        assert subtitles[0].duration_frame == 1

    @reversion_test
    def test_set_duration__seconds(self):

        subtitles = self.project.subtitles
        self.project.set_duration(0, 100.0)
        assert subtitles[0].duration_seconds == 100.0

    @reversion_test
    def test_set_duration__time(self):

        subtitles = self.project.subtitles
        self.project.set_duration(0, "00:01:11.111")
        assert subtitles[0].duration_time == "00:01:11.111"

    @reversion_test
    def test_set_end__frame(self):

        subtitles = self.project.subtitles
        self.project.set_end(0, 600000)
        assert subtitles[0].end_frame == 600000

    @reversion_test
    def test_set_end__seconds(self):

        subtitles = self.project.subtitles
        self.project.set_end(0, 500.0)
        assert subtitles[0].end_seconds == 500.0

    @reversion_test
    def test_set_end__time(self):

        subtitles = self.project.subtitles
        self.project.set_end(0, "00:22:00.000")
        assert subtitles[0].end_time == "00:22:00.000"

    @reversion_test
    def test_set_start__frame(self):

        subtitles = self.project.subtitles
        self.project.set_start(0, 1)
        assert subtitles[0].start_frame == 1

    @reversion_test
    def test_set_start__reorder(self):

        subtitles = self.project.subtitles
        text_0 = subtitles[0].main_text
        text_3 = subtitles[3].main_text
        self.project.set_start(3, 0)
        assert subtitles[0].start_frame == 0
        assert subtitles[0].main_text == text_3
        assert subtitles[1].main_text == text_0

    @reversion_test
    def test_set_start__seconds(self):

        subtitles = self.project.subtitles
        self.project.set_start(0, 1.0)
        assert subtitles[0].start_seconds == 1.0

    @reversion_test
    def test_set_start__time(self):

        subtitles = self.project.subtitles
        self.project.set_start(0, "00:00:00.001")
        assert subtitles[0].start_time == "00:00:00.001"

    @reversion_test
    def test_set_text__main(self):

        self.project.set_text(0, const.DOCUMENT.MAIN, "m")
        assert self.project.subtitles[0].main_text == "m"

    @reversion_test
    def test_set_text__translation(self):

        self.project.set_text(0, const.DOCUMENT.TRAN, "t")
        assert self.project.subtitles[0].tran_text == "t"
