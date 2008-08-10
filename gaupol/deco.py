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

"""Miscellaneous decorators for functions and methods."""

import cPickle
import functools
import gaupol
import time


def _dump_subtitles(subtitles):
    """Return a tuple of the essential attributes of subtitles."""

    values = []
    for subtitle in subtitles:
        values.append((
            subtitle._start,
            subtitle._end,
            subtitle._main_text,
            subtitle._tran_text,
            subtitle._framerate,))
    return tuple(values)

def _is_method(function, args):
    """Return True if function to be decorated is a method.

    Decorator is required to have set an 'original' attribute on the wrapped
    method pointing to the original unwrapped function.
    """
    try:
        method = getattr(args[0], function.__name__)
        return (method.original is function)
    except (IndexError, AttributeError):
        return False

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

def contractual(function):
    """Decorator for module level functions with pre- and/or postconditions.

    function call will be wrapped around 'FUNCTION_NAME_require' and
    'FUNCTION_NAME_ensure' calls if such functions exist. The require function
    receives the same arguments as function, the ensure function will in
    addition receive function's return value as its first argument.
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if not gaupol.check_contracts:
            return function(*args, **kwargs)
        name = "%s_require" % function.__name__
        if name in function.func_globals:
            function.func_globals[name](*args, **kwargs)
        value = function(*args, **kwargs)
        name = "%s_ensure" % function.__name__
        if name in function.func_globals:
            function.func_globals[name](value, *args, **kwargs)
        return value

    return wrapper

def memoize(function):
    """Decorator for functions that cache their return values."""

    cache = {}
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        params = (args, kwargs)
        if _is_method(function, args):
            params = (id(args[0]), args[1:], kwargs)
        key = cPickle.dumps(params)
        if not key in cache:
            cache[key] = function(*args, **kwargs)
        return cache[key]

    wrapper.original = function
    return wrapper

def notify_frozen(function):
    """Decorator for methods to be run in notify frozen state."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        frozen = args[0].freeze_notify()
        try: value = function(*args, **kwargs)
        finally: args[0].thaw_notify(frozen)
        return value

    return wrapper

def once(function):
    """Decorator for functions that cache their only return value."""

    cache = []
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if not cache:
            cache.append(function(*args, **kwargs))
        return cache[0]

    return wrapper

def reversion_test(function):
    """Decorator for unit testing reversions of one action."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        project = args[0].project
        original = _dump_subtitles(project.subtitles)
        value = function(*args, **kwargs)
        changed = _dump_subtitles(project.subtitles)
        assert changed != original
        for i in range(2):
            project.undo()
            current = _dump_subtitles(project.subtitles)
            assert current == original
            project.redo()
            current = _dump_subtitles(project.subtitles)
            assert current == changed
        return value

    return wrapper

def revertable(function):
    """Decorator for revertable project methods."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):

        project = args[0]
        main_changed = project.main_changed
        tran_changed = project.tran_changed
        kwargs.setdefault("register", gaupol.registers.DO)
        register = kwargs["register"]
        if register is None:
            # Execute plain function for special-case actions
            # that are not to be pushed to the undo stack.
            return function(*args, **kwargs)
        blocked = project.block(register.signal)
        if not blocked:
            # Execute plain function for nested function calls
            # that are part of another revertable action.
            return function(*args, **kwargs)
        try: value = function(*args, **kwargs)
        finally: project.unblock(register.signal)
        project.cut_reversion_stacks()
        if (project.main_changed != main_changed) or \
           (project.tran_changed != tran_changed):
            project.emit_action_signal(register)
        return value

    return wrapper

def silent(*exceptions):
    """Decorator for ignoring exceptions raised  by function.

    If no exceptions specified, ignore Exception.
    Return None if an exception encountered.
    """
    if not exceptions:
        exceptions = (Exception,)

    def outer_wrapper(function):
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            try: return function(*args, **kwargs)
            except exceptions: return None
        return inner_wrapper

    return outer_wrapper
