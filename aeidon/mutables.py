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

"""Observable versions of built-in mutable objects."""

import copy
import functools

__all__ = ("ObservableDict", "ObservableList", "ObservableSet",)


def _mutation(function):
    """Decorator for sending a notification after mutating object."""
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        value = function(*args, **kwargs)
        args[0].master.notify(args[0].name)
        return value
    return wrapper


class ObservableDict(dict):

    """
    Observable version of ``dict``.

    :ivar master: Master instance with a ``notify`` method
    :ivar name: Argument passed when calling :attr:`master`'s ``notify`` method
    """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args[:-2], **kwargs)
        self.master = args[-2]
        self.name = args[-1]

    def __copy__(self):
        dic = dict(copy.copy(x) for  x in self.items())
        return self.__class__(dic, self.master, self.name)

    def __deepcopy__(self, memo):
        dic = dict(copy.deepcopy(x) for  x in self.items())
        return self.__class__(dic, self.master, self.name)

    @_mutation
    def __delitem__(self, *args, **kwargs):
        return dict.__delitem__(self, *args, **kwargs)

    @_mutation
    def __setitem__(self, *args, **kwargs):
        return dict.__setitem__(self, *args, **kwargs)

    @_mutation
    def clear(self, *args, **kwargs):
        return dict.clear(self, *args, **kwargs)

    @_mutation
    def pop(self, *args, **kwargs):
        return dict.pop(self, *args, **kwargs)

    @_mutation
    def popitem(self, *args, **kwargs):
        return dict.popitem(self, *args, **kwargs)

    @_mutation
    def setdefault(self, *args, **kwargs):
        return dict.setdefault(self, *args, **kwargs)

    @_mutation
    def update(self, *args, **kwargs):
        return dict.update(self, *args, **kwargs)


class ObservableList(list):

    """
    Observable version of ``list``.

    :ivar master: Master instance with a ``notify`` method
    :ivar name: Argument passed when calling :attr:`master`'s ``notify`` method
    """

    def __init__(self, *args, **kwargs):
        list.__init__(self, *args[:-2], **kwargs)
        self.master = args[-2]
        self.name = args[-1]

    def __copy__(self):
        lst = list(copy.copy(x) for x in self)
        return self.__class__(lst, self.master, self.name)

    def __deepcopy__(self, memo):
        lst = [copy.deepcopy(x) for x in self]
        return self.__class__(lst, self.master, self.name)

    @_mutation
    def __delitem__(self, *args, **kwargs):
        return list.__delitem__(self, *args, **kwargs)

    @_mutation
    def __iadd__(self, *args, **kwargs):
        return list.__iadd__(self, *args, **kwargs)

    @_mutation
    def __imul__(self, *args, **kwargs):
        return list.__imul__(self, *args, **kwargs)

    @_mutation
    def __setitem__(self, *args, **kwargs):
        return list.__setitem__(self, *args, **kwargs)

    @_mutation
    def append(self, *args, **kwargs):
        return list.append(self, *args, **kwargs)

    @_mutation
    def extend(self, *args, **kwargs):
        return list.extend(self, *args, **kwargs)

    @_mutation
    def insert(self, *args, **kwargs):
        return list.insert(self, *args, **kwargs)

    @_mutation
    def pop(self, *args, **kwargs):
        return list.pop(self, *args, **kwargs)

    @_mutation
    def remove(self, *args, **kwargs):
        return list.remove(self, *args, **kwargs)

    @_mutation
    def reverse(self, *args, **kwargs):
        return list.reverse(self, *args, **kwargs)

    @_mutation
    def sort(self, *args, **kwargs):
        return list.sort(self, *args, **kwargs)


class ObservableSet(set):

    """
    Observable version of ``set``.

    :ivar master: Master instance with a ``notify`` method
    :ivar name: Argument passed when calling :attr:`master`'s ``notify`` method
    """

    def __init__(self, *args, **kwargs):
        set.__init__(self, *args[:-2], **kwargs)
        self.master = args[-2]
        self.name = args[-1]

    def __copy__(self):
        zet = set(copy.copy(x) for x in self)
        return self.__class__(zet, self.master, self.name)

    def __deepcopy__(self, memo):
        zet = set(copy.deepcopy(x) for x in self)
        return self.__class__(zet, self.master, self.name)

    @_mutation
    def __iand__(self, *args, **kwargs):
        return set.__iand__(self, *args, **kwargs)

    @_mutation
    def __ior__(self, *args, **kwargs):
        return set.__ior__(self, *args, **kwargs)

    @_mutation
    def __isub__(self, *args, **kwargs):
        return set.__isub__(self, *args, **kwargs)

    @_mutation
    def __ixor__(self, *args, **kwargs):
        return set.__ixor__(self, *args, **kwargs)

    @_mutation
    def add(self, *args, **kwargs):
        return set.add(self, *args, **kwargs)

    @_mutation
    def clear(self, *args, **kwargs):
        return set.clear(self, *args, **kwargs)

    @_mutation
    def difference_update(self, *args, **kwargs):
        return set.difference_update(self, *args, **kwargs)

    @_mutation
    def discard(self, *args, **kwargs):
        return set.discard(self, *args, **kwargs)

    @_mutation
    def intersection_update(self, *args, **kwargs):
        return set.intersection_update(self, *args, **kwargs)

    @_mutation
    def pop(self, *args, **kwargs):
        return set.pop(self, *args, **kwargs)

    @_mutation
    def remove(self, *args, **kwargs):
        return set.remove(self, *args, **kwargs)

    @_mutation
    def symmetric_difference_update(self, *args, **kwargs):
        return set.symmetric_difference_update(self, *args, **kwargs)

    @_mutation
    def update(self, *args, **kwargs):
        return set.update(self, *args, **kwargs)
