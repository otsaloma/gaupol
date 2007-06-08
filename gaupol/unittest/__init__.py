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


"""Unit testing system.

All test module names should be prefixed with 'test_', class names with 'Test',
function and method names with 'test_'. Interactive GUI test method names
should be prefixed with 'run'. All test classes should inherit from TestCase.

Tests can be run with at least py.test [1] and nose [2]. All test code is to be
kept as independent as possible of the application used to run the tests.

[1] http://codespeak.net/py/dist/test.html
[2] http://somethingaboutorange.com/mrl/projects/nose/
"""


from .case import TestCase
from .deco import benchmark
from .deco import reversion_test

__all__ = ["TestCase", "benchmark", "reversion_test"]
