# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Decorators for testing methods and functions."""

import functools
import time


def _dump(subtitles):
    """Get a list of the essential attributes of subtitles."""

    values = []
    for subtitle in subtitles:
        values.append((
            subtitle._start,
            subtitle._end,
            subtitle._main_text,
            subtitle._tran_text,
            subtitle._framerate,))
    return values

def benchmark(function):
    """Decorator for benchmarking functions and methods."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        a = time.time()
        value = function(*args, **kwargs)
        z = time.time()
        print "%.3f %s" % (z - a, function.__name__)
        return value

    return wrapper

def reversion_test(function):
    """Decorator for testing reversions of one action."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        project = args[0].project
        original = _dump(project.subtitles)
        value = function(*args, **kwargs)
        changed = _dump(project.subtitles)
        assert changed != original
        for i in range(2):
            project.undo()
            current = _dump(project.subtitles)
            assert current == original
            project.redo()
            current = _dump(project.subtitles)
            assert current == changed
        return value

    return wrapper
