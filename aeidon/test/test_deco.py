# Copyright (C) 2006-2009 Osmo Salomaa
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
import os
import sys


class TestModule(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()

    def test_benchmark(self):
        function = aeidon.deco.benchmark(lambda x: x ** 2)
        assert function(2) == 4
        assert function(2) == 4

    @aeidon.deco.monkey_patch(aeidon, "debug")
    def test_contractual__check(self):
        aeidon.debug = True
        reload(aeidon.util)
        aeidon.util.get_ranges((1, 2, 3))

    @aeidon.deco.monkey_patch(aeidon, "debug")
    def test_contractual__skip(self):
        aeidon.debug = False
        reload(aeidon.util)
        aeidon.util.get_ranges((1, 2, 3))

    def test_export(self):
        function = aeidon.deco.export(lambda x: x ** 2)
        assert function.export is True

    def test_memoize(self):
        function = aeidon.deco.memoize(lambda x: x ** 2)
        assert function(2) == 4
        assert function(2) == 4

    def test_monkey_patch__no_attribute(self):
        @aeidon.deco.monkey_patch(sys, "aeidon")
        def modify_aeidon():
            sys.aeidon = True
        modify_aeidon()
        assert not hasattr(sys, "aeidon")

    def test_monkey_patch__os_environ(self):
        @aeidon.deco.monkey_patch(os, "environ")
        def modify_environment():
            os.environ["AEIDON_TEST"] = "1"
        modify_environment()
        assert not "AEIDON_TEST" in os.environ

    def test_monkey_patch__sys_platform(self):
        platform = sys.platform
        @aeidon.deco.monkey_patch(sys, "platform")
        def modify_platform():
            sys.platform = "commodore_64"
        modify_platform()
        assert sys.platform == platform

    def test_notify_frozen(self):
        self.project.insert_subtitles((0,))
        assert not self.project.thaw_notify(True)

    def test_once(self):
        function = aeidon.deco.once(lambda: 5)
        assert function() == 5
        assert function() == 5

    @aeidon.deco.reversion_test
    def test_reversion_test(self):
        self.project.remove_subtitles((0,))

    def test_revertable(self):
        project = self.project
        project.remove_subtitles((0,), register=None)
        assert len(project.undoables) == 0
        assert len(project.redoables) == 0
        project.clear_texts((0,), aeidon.documents.MAIN)
        assert len(project.undoables) == 1
        assert len(project.redoables) == 0
        project.remove_subtitles((0,))
        assert len(project.undoables) == 2
        assert len(project.redoables) == 0

    def test_silent(self):
        function = lambda: [].remove(None)
        aeidon.deco.silent(ValueError)(function)()
        aeidon.deco.silent(Exception)(function)()
        aeidon.deco.silent()(function)()
