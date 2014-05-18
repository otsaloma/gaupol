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
import copy


class PuppetMaster:

    def __init__(self):
        self.count = 0

    def notify(self, name):
        self.count += 1


class _TestObservable(aeidon.TestCase):

    def edit_obs(self):
        raise NotImplementedError

    def setup_method(self, method):
        self.master = PuppetMaster()
        self.obs = None

    def teardown_method(self, method):
        if method.__name__ in self.__class__.__dict__:
            assert self.master.count == 1

    def test___copy__(self):
        obs_copy = copy.copy(self.obs)
        assert obs_copy == self.obs
        assert obs_copy.master is self.obs.master
        self.edit_obs()
        assert obs_copy != self.obs
        assert obs_copy.master is self.obs.master

    def test___deepcopy__(self):
        obs_copy = copy.deepcopy(self.obs)
        assert obs_copy == self.obs
        assert obs_copy.master is self.obs.master
        self.edit_obs()
        assert obs_copy != self.obs
        assert obs_copy.master is self.obs.master


class TestObservableDict(_TestObservable):

    def edit_obs(self):
        del self.obs[1]

    def setup_method(self, method):
        _TestObservable.setup_method(self, method)
        self.obs = aeidon.ObservableDict({1:1, 2:2}, self.master, "")

    def test___delitem__(self):
        del self.obs[1]

    def test___setitem__(self):
        self.obs[1] = 2

    def test_clear(self):
        self.obs.clear()

    def test_pop(self):
        self.obs.pop(1)

    def test_popitem(self):
        self.obs.popitem()

    def test_setdefault(self):
        self.obs.setdefault(1, 2)

    def test_update(self):
        self.obs.update({1:2, 3:3})


class TestObservableList(_TestObservable):

    def edit_obs(self):
        self.obs.pop()

    def setup_method(self, method):
        _TestObservable.setup_method(self, method)
        self.obs = aeidon.ObservableList((1, 2, 3), self.master, "")

    def test___delitem__(self):
        del self.obs[0]

    def test___iadd__(self):
        self.obs += (4, 5)

    def test___imul__(self):
        self.obs *= 2

    def test___setitem__(self):
        self.obs[0] = 2

    def test_append(self):
        self.obs.append(4)

    def test_extend(self):
        self.obs.extend((4, 5))

    def test_insert(self):
        self.obs.insert(0, 0)

    def test_pop(self):
        self.obs.pop()

    def test_remove(self):
        self.obs.remove(1)

    def test_reverse(self):
        self.obs.reverse()

    def test_sort(self):
        self.obs.sort()


class TestObservableSet(_TestObservable):

    def edit_obs(self):
        self.obs.pop()

    def setup_method(self, method):
        _TestObservable.setup_method(self, method)
        self.obs = aeidon.ObservableSet((1, 2, 3), self.master, "")

    def test___iand__(self):
        self.obs &= set((1, 2))

    def test___ior__(self):
        self.obs |= set((1, 2))

    def test___isub__(self):
        self.obs -= set((1, 2))

    def test___ixor__(self):
        self.obs ^= set((1, 2))

    def test_add(self):
        self.obs.add(4)

    def test_clear(self):
        self.obs.clear()

    def test_difference_update(self):
        self.obs.difference_update(set((1, 2)))

    def test_discard(self):
        self.obs.discard(1)

    def test_intersection_update(self):
        self.obs.intersection_update(set((1, 2)))

    def test_pop(self):
        self.obs.pop()

    def test_remove(self):
        self.obs.remove(1)

    def test_symmetric_difference_update(self):
        self.obs.symmetric_difference_update(set((1, 2)))

    def test_update(self):
        self.obs.update(set((4, 5)))
