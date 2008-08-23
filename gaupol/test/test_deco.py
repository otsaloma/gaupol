# Copyright (C) 2006-2008 Osmo Salomaa
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


class TestModule(gaupol.TestCase):

    def setup_method(self, method):

        self.project = self.get_project()

    def test_benchmark(self):

        function = gaupol.deco.benchmark(lambda x: x ** 2)
        assert function(2) == 4
        assert function(2) == 4

    def test_contractual__check(self):

        debug = gaupol.debug
        gaupol.debug = True
        reload(gaupol.util)
        gaupol.util.get_ranges([1, 2, 3])
        gaupol.debug = debug

    def test_contractual__skip(self):

        debug = gaupol.debug
        gaupol.debug = False
        reload(gaupol.util)
        gaupol.util.get_ranges([1, 2, 3])
        gaupol.debug = debug

    def test_memoize(self):

        function = gaupol.deco.memoize(lambda x: x ** 2)
        assert function(2) == 4
        assert function(2) == 4

    def test_notify_frozen(self):

        self.project.insert_blank_subtitles((0,))
        assert not self.project.thaw_notify(True)

    def test_once(self):

        function = gaupol.deco.once(lambda: 5)
        assert function() == 5
        assert function() == 5

    @gaupol.deco.reversion_test
    def test_reversion_test(self):

        self.project.remove_subtitles((0,))

    def test_revertable(self):

        project = self.project
        project.remove_subtitles((0,), register=None)
        assert len(project.undoables) == 0
        assert len(project.redoables) == 0
        project.clear_texts((0,), gaupol.documents.MAIN)
        assert len(project.undoables) == 1
        assert len(project.redoables) == 0
        project.remove_subtitles((0,))
        assert len(project.undoables) == 2
        assert len(project.redoables) == 0

    def test_silent(self):

        function = lambda: [].remove(None)
        gaupol.deco.silent(ValueError)(function)()
        gaupol.deco.silent(Exception)(function)()
        gaupol.deco.silent()(function)()
