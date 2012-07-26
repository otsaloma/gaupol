# -*- coding: utf-8-unix -*-

# Copyright (C) 2007,2009 Osmo Salomaa
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

"""
Metaclass for design-by-contract_ pre- and postcondition checks.

.. _design-by-contract:
   http://www.eiffel.com/developers/design_by_contract.html
"""

import aeidon
import functools

__all__ = ("Contractual",)


def _ensured(ensure_func):
    """Decorator for checking a postcondition."""
    def outer_wrapper(function):
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            value = function(*args, **kwargs)
            ensure_func(args[0], value, *args[1:], **kwargs)
            return value
        return inner_wrapper
    return outer_wrapper

def _invariated(invariant_func):
    """Decorator for checking a class invariant."""
    def outer_wrapper(function):
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            value = function(*args, **kwargs)
            invariant_func(args[0])
            return value
        return inner_wrapper
    return outer_wrapper

def _required(require_func):
    """Decorator for checking a precondition."""
    def outer_wrapper(function):
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            require_func(*args, **kwargs)
            return function(*args, **kwargs)
        return inner_wrapper
    return outer_wrapper


class Contractual(type):

    """
    Metaclass for design-by-contract_ pre- and postcondition checks.

    Method calls are automatically wrapped in ``METHOD_NAME_require``
    precondition call, ``METHOD_NAME_ensure`` postcondition call and public
    method calls in ``_invariant`` class invariant check call if such methods
    exist. The require method receives the same arguments as method, the ensure
    method will in addition receive method's return value as its first argument
    after self.

    Preconditions may be weakened; only the first precondition found in the
    inheritance tree is used. Postconditions and class invariants may be
    strengthened; all postconditions and class invariant checks found in the
    inheritance tree will be used.

    :class:`Contractual` is a debug metaclass that is in use only if
    :data:`aeidon.DEBUG` is ``True``.

    .. _design-by-contract:
       http://www.eiffel.com/developers/design_by_contract.html
    """

    def __new__(meta, class_name, bases, dic):
        """Return instance with method calls wrapped in condition calls."""
        new_dict = dic.copy()
        for name, attr in dic.items():
            if not callable(attr): continue
            require_name = "{}_require".format(name)
            if name.startswith("__"):
                require_name = "_{}{}".format(class_name, require_name)
            if require_name in dic:
                require_func = dic[require_name]
                attr = _required(require_func)(attr)
            elif not name.startswith("__"):
                # If a precondition is not defined in this class, look for
                # a precodition among ancestors and use the first one found.
                for base in bases:
                    if hasattr(base, require_name):
                        require_func = getattr(base, require_name)
                        attr = _required(require_func)(attr)
                        break
            ensure_name = "{}_ensure".format(name)
            if name.startswith("__"):
                ensure_name = "_{}{}".format(class_name, ensure_name)
            if ensure_name in dic:
                ensure_func = dic[ensure_name]
                attr = _ensured(ensure_func)(attr)
            if not name.startswith("__"):
                # Check all postconditions defined by ancestors.
                for base in bases:
                    if hasattr(base, ensure_name):
                        ensure_func = getattr(base, ensure_name)
                        attr = _ensured(ensure_func)(attr)
            invariant_name = "_invariant"
            if invariant_name in dic:
                invariant_func = dic[invariant_name]
                attr = _invariated(invariant_func)(attr)
            # Check all class invariants defined by ancestors.
            for base in bases:
                if hasattr(base, invariant_name):
                    invariant_func = getattr(base, invariant_name)
                    attr = _invariated(invariant_func)(attr)
            new_dict[name] = attr
        return type.__new__(meta, class_name, bases, new_dict)

    if not aeidon.DEBUG: del __new__
