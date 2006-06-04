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


from gaupol.base.delegates.fileopen import FileOpenDelegate
from gaupol.test                    import Test


class TestFileOpenDelegate(Test):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = FileOpenDelegate(self.project)

    def test_open_main_file(self):

        path = self.get_subrip_path()
        self.project.open_main_file(path, 'utf_8')
        assert self.project.times
        assert self.project.frames
        assert self.project.main_texts
        assert self.project.tran_texts

    def test_open_translation_file(self):

        self.project.remove_subtitles([0, 1])
        path = self.get_microdvd_path()
        self.project.open_translation_file(path, 'utf_8')
        assert self.project.tran_texts[0]

    def test_sort_data(self):

        sort = self.delegate._sort_data

        shows = [ 1 ,  2 ,  3 ]
        hides = [ 2 ,  3 ,  4 ]
        texts = ['1', '2', '3']
        shows, hides, texts, resorts = sort(shows, hides, texts)
        assert shows == [ 1 ,  2 ,  3 ]
        assert hides == [ 2 ,  3 ,  4 ]
        assert texts == ['1', '2', '3']
        assert resorts == 0

        shows = [ 2 ,  3 ,  1 ]
        hides = [ 3 ,  4 ,  2 ]
        texts = ['2', '3', '1']
        shows, hides, texts, resorts = sort(shows, hides, texts)
        assert shows == [ 1 ,  2 ,  3 ]
        assert hides == [ 2 ,  3 ,  4 ]
        assert texts == ['1', '2', '3']
        assert resorts > 0
