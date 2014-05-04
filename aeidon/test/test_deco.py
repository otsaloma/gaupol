# -*- coding: utf-8 -*-

# Copyright (C) 2006 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import aeidon
import os
import sys


class TestModule(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()

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

    def test_silent(self):
        function = lambda: [].remove(None)
        aeidon.deco.silent(ValueError)(function)()
        aeidon.deco.silent(Exception)(function)()
