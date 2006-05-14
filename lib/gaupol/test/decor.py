# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Decorators for timing methods and functions."""


import time


def timefunction(function):
    """Decorator for timing functions."""

    def wrapper(*args, **kwargs):

        start = time.time()
        function(*args, **kwargs)
        end = time.time()

        print '%.3f %s' % (end - start, function.__name__)

    return wrapper

def timemethod(function):
    """Decorator for timing methods."""

    def wrapper(*args, **kwargs):

        start = time.time()
        function(*args, **kwargs)
        end = time.time()

        print '%.3f %s.%s.%s' % (
            end - start,
            args[0].__class__.__module__,
            args[0].__class__.__name__,
            function.__name__
        )

    return wrapper
