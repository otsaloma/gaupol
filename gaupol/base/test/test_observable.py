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

# pylint: disable-msg=E1101


from gaupol.unittest import TestCase
from .. import observable


class Observable(observable.Observable):

    _signals = ["test"]

    def __init__(self):

        observable.Observable.__init__(self)
        self.variable = 0

    @observable.notify_frozen
    def do(self):

        self.variable = 1
        self.variable = 2
        self.variable = 3


class _TestObservable(TestCase):

    def on_notify_variable(self, obj, value):

        assert obj is self.obs
        assert value == self.obs.variable
        self.notify_count += 1

    def on_test(self, obj):

        assert obj is self.obs
        self.test_count += 1

    def setup_method(self, method):

        self.obs = Observable()
        self.notify_count = 0
        self.test_count = 0
        self.obs.connect("test", self.on_test)
        self.obs.connect("notify::variable", self.on_notify_variable)


class TestModule(_TestObservable):

    def _test_notify_frozen(self):

        self.obs.do()
        assert self.notify_count == 1


class TestObservable(_TestObservable):

    def test__add_signal(self):

        self.obs._add_signal("rest")
        self.obs.emit("rest")

    def test__validate(self):

        for value in ([], {}, set()):
            assert self.obs._validate("", value) == value
            assert self.obs._validate("", value) is not value
        for value in (True, "", 1, 1.0, (), frozenset()):
            assert self.obs._validate("", value) == value
            assert self.obs._validate("", value) is value

    def test_block(self):

        assert self.obs.block("test")
        assert not self.obs.block("test")
        self.obs.emit("test")
        assert self.test_count == 0

    def test_disconnect(self):

        self.obs.disconnect("test", self.on_test)
        self.obs.emit("test")
        assert self.test_count == 0

    def test_emit(self):

        self.obs.variable = 1
        assert self.notify_count == 1
        self.obs.emit("test")
        assert self.test_count == 1

    def test_freeze_notify(self):

        assert self.obs.freeze_notify()
        assert not self.obs.freeze_notify()
        self.obs.variable = 1
        assert self.notify_count == 0

    def test_notify(self):

        self.obs.notify("variable")
        assert self.notify_count == 1

    def test_thaw_notify(self):

        self.obs.freeze_notify()
        self.obs.variable = 1
        self.obs.variable = 2
        assert self.obs.thaw_notify()
        assert not self.obs.thaw_notify()
        assert self.notify_count == 1

    def test_unblock(self):

        self.obs.block("test")
        assert self.obs.unblock("test")
        assert not self.obs.unblock("test")
        self.obs.emit("test")
        assert self.test_count == 1
