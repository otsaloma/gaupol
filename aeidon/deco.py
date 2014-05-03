# -*- coding: utf-8 -*-

# Copyright (C) 2006-2009,2011-2012 Osmo Salomaa
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

"""Miscellaneous decorators for functions and methods."""

import aeidon
import collections
import copy
import functools
import pickle
import time

# Python decorators normally do not preserve the signature of the original
# function. We, however, absolutely need those function signatures kept to able
# to autogenerate useful API documentation with sphinx. Let's use the
# 'decorator' module [1] designed to solve this problem, but only if running
# sphinx in order to avoid an unnecessary dependency and to avoid an additional
# layer of code with its own runtime speed penalty and potential bugs.
# Specifically, let's use the 'decorator_apply' function as instructed [2] to
# avoid rewriting our standard-form decorators.
#
#  [1] http://pypi.python.org/pypi/decorator/
#  [2] http://micheles.googlecode.com/hg/decorator/documentation.html


def _dump_subtitles(subtitles):
    """Return a tuple of essential attributes of subtitles."""
    return tuple((subtitle._start,
                  subtitle._end,
                  subtitle._main_text,
                  subtitle._tran_text,
                  subtitle._framerate) for subtitle in subtitles)

def _hasattr_def(obj, name):
    """Return ``True`` if `obj` has attribute `name` defined."""
    if hasattr(obj, "__dict__"):
        return name in obj.__dict__
    return hasattr(obj, name)

def _is_method(function, args):
    """
    Return ``True`` if `function` to be decorated is a method.

    Decorator is required to have set an `original` attribute on the wrapped
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
        start = time.time()
        value = function(*args, **kwargs)
        duration = time.time() - start
        print("{:7.3f} {}".format(duration, function.__name__))
        return value
    return wrapper

if aeidon.RUNNING_SPHINX:
    _benchmark = benchmark
    def benchmark(function):
        return decorator_apply(_benchmark, function)
    benchmark.__doc__ = _benchmark.__doc__

def decorator_apply(dec, fun):
    """Rewrap `dec` to preserve function signature."""
    import decorator
    return decorator.FunctionMaker.create(
        fun, 'return decorated(%(signature)s)',
        dict(decorated=dec(fun)), __wrapped__=fun)

def export(function):
    """Decorator for delegate functions that are exported to master."""
    function.export = True
    return function

if aeidon.RUNNING_SPHINX:
    _export = export
    def export(function):
        return decorator_apply(_export, function)
    export.__doc__ = _export.__doc__

def memoize(limit=100):
    """
    Decorator for functions that cache their return values.

    Use ``None`` for `limit` for a boundless cache.
    """
    def outer_wrapper(function):
        cache = collections.OrderedDict()
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            params = (args, kwargs)
            if _is_method(function, args):
                params = (id(args[0]), args[1:], kwargs)
            key = pickle.dumps(params)
            try:
                return cache[key]
            except KeyError:
                pass
            cache[key] = function(*args, **kwargs)
            if limit is not None:
                while len(cache) > limit:
                    cache.popitem(last=False)
            return cache[key]
        inner_wrapper.original = function
        return inner_wrapper
    if aeidon.RUNNING_SPHINX:
        _outer_wrapper = outer_wrapper
        def outer_wrapper(function):
            return decorator_apply(_outer_wrapper, function)
    return outer_wrapper

def monkey_patch(obj, name):
    """
    Decorator for functions that change `obj`'s `name` attribute.

    Any changes done will be reverted after the function is run, i.e. `name`
    attribute is either restored to its original value or deleted, if it didn't
    originally exist. The attribute in question must be able to correctly
    handle a :func:`copy.deepcopy` operation.

    Typical use would be unit testing code under legitimately unachievable
    conditions, e.g. pseudo-testing behaviour on Windows, while not actually
    using Windows::

        @aeidon.deco.monkey_patch(sys, "platform")
        def test_do_something():
            sys.platform = "win32"
            do_something()

    """
    def outer_wrapper(function):
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            if _hasattr_def(obj, name):
                attr = getattr(obj, name)
                setattr(obj, name, copy.deepcopy(attr))
                try:
                    return function(*args, **kwargs)
                finally:
                    setattr(obj, name, attr)
                    assert getattr(obj, name) == attr
                    assert getattr(obj, name) is attr
            else: # Attribute not defined.
                try:
                    return function(*args, **kwargs)
                finally:
                    delattr(obj, name)
                    assert not _hasattr_def(obj, name)
        return inner_wrapper
    if aeidon.RUNNING_SPHINX:
        _outer_wrapper = outer_wrapper
        def outer_wrapper(function):
            return decorator_apply(_outer_wrapper, function)
    return outer_wrapper

def notify_frozen(function):
    """Decorator for methods to be run in notify frozen state."""
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        frozen = args[0].freeze_notify()
        try:
            return function(*args, **kwargs)
        finally:
            args[0].thaw_notify(frozen)
    return wrapper

if aeidon.RUNNING_SPHINX:
    _notify_frozen = notify_frozen
    def notify_frozen(function):
        return decorator_apply(_notify_frozen, function)
    notify_frozen.__doc__ = _notify_frozen.__doc__

def once(function):
    """Decorator for functions that cache their only return value."""
    cache = []
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return cache[0]
        except IndexError:
            pass
        cache.append(function(*args, **kwargs))
        return cache[0]
    return wrapper

if aeidon.RUNNING_SPHINX:
    _once = once
    def once(function):
        return decorator_apply(_once, function)
    once.__doc__ = _once.__doc__

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

if aeidon.RUNNING_SPHINX:
    _reversion_test = reversion_test
    def reversion_test(function):
        return decorator_apply(_reversion_test, function)
    reversion_test.__doc__ = _reversion_test.__doc__

def revertable(function):
    """Decorator for revertable methods of :class:`aeidon.Project`."""
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        project = args[0]
        main_changed = project.main_changed
        tran_changed = project.tran_changed
        kwargs.setdefault("register", aeidon.registers.DO)
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
        try:
            value = function(*args, **kwargs)
        finally:
            project.unblock(register.signal)
        project.cut_reversion_stacks()
        if (project.main_changed != main_changed or
            project.tran_changed != tran_changed):
            project.emit_action_signal(register)
        return value
    return wrapper

if aeidon.RUNNING_SPHINX:
    _revertable = revertable
    def revertable(function):
        return decorator_apply(_revertable, function)
    revertable.__doc__ = _revertable.__doc__

def silent(*exceptions):
    """
    Decorator for ignoring `exceptions` raised  by function.

    If no exceptions specified, ignore :exc:`Exception`.
    Return ``None`` if an exception encountered.
    """
    if not exceptions:
        exceptions = (Exception,)
    def outer_wrapper(function):
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except exceptions:
                return None
        return inner_wrapper
    if aeidon.RUNNING_SPHINX:
        _outer_wrapper = outer_wrapper
        def outer_wrapper(function):
            return decorator_apply(_outer_wrapper, function)
    return outer_wrapper
