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


from gaupol.unittest import TestCase


class TestOpenAgent(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = self.project.open_main.im_self

    def test__sort(self):

        sort = self.delegate._sort

        shows = [ 1 ,  2 ,  3 ]
        hides = [ 2 ,  3 ,  4 ]
        texts = ["1", "2", "3"]
        shows, hides, texts = sort(shows, hides, texts)
        assert shows == [ 1 ,  2 ,  3 ]
        assert hides == [ 2 ,  3 ,  4 ]
        assert texts == ["1", "2", "3"]
        assert self.delegate._sort_count == 0

        shows = [ 2 ,  3 ,  1 ]
        hides = [ 3 ,  4 ,  2 ]
        texts = ["2", "3", "1"]
        shows, hides, texts = sort(shows, hides, texts)
        assert shows == [ 1 ,  2 ,  3 ]
        assert hides == [ 2 ,  3 ,  4 ]
        assert texts == ["1", "2", "3"]
        assert self.delegate._sort_count > 0

    def test_open_main_file(self):

        for path in (self.get_subrip_path(), self.get_microdvd_path()):
            self.project.remove_subtitles([0])
            assert self.project.open_main(path, "ascii") == 0
            assert self.project.times
            assert self.project.frames
            assert self.project.main_texts
            assert self.project.tran_texts
            assert self.project.main_file is not None
            assert self.project.main_changed == 0
            assert self.project.tran_changed == 0
            assert self.project.tran_active == False

    def test_open_translation_file_smart(self):

        for path in (self.get_subrip_path(), self.get_microdvd_path()):
            self.project.remove_subtitles([0])
            assert self.project.open_translation(path, "ascii", True) == 0
            assert self.project.tran_texts
            assert len(self.project.tran_texts) == len(self.project.main_texts)
            for i, main_text in enumerate(self.project.main_texts):
                assert main_text or self.project.tran_texts[i]
            assert self.project.tran_file is not None
            assert self.project.tran_changed == 0
            assert self.project.tran_active == True

    def test_open_translation_file_stupid(self):

        for path in (self.get_subrip_path(), self.get_microdvd_path()):
            self.project.remove_subtitles([0])
            assert self.project.open_translation(path, "ascii", False) == 0
            assert self.project.tran_texts
            assert len(self.project.tran_texts) == len(self.project.main_texts)
            for i, main_text in enumerate(self.project.main_texts):
                assert main_text or self.project.tran_texts[i]
            assert self.project.tran_file is not None
            assert self.project.tran_changed == 0
            assert self.project.tran_active == True
