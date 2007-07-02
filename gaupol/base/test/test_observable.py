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

# pylint: disable-msg=E1101


from gaupol import unittest
from .. import observable


class Observable(observable.Observable):

    _signals = ["do"]

    def __init__(self):

        observable.Observable.__init__(self)
        self.variable = 0


class _TestObservable(unittest.TestCase):

    def on_notify_variable(self, obj, value):

        assert obj is self.obs
        assert value == self.obs.variable
        self.notify_count += 1

    def on_do(self, obj):

        assert obj is self.obs
        self.do_count += 1

    def setup_method(self, method):

        self.obs = Observable()
        self.notify_count = 0
        self.do_count = 0
        self.obs.connect("do", self.on_do)
        self.obs.connect("notify::variable", self.on_notify_variable)


class TestObservable(_TestObservable):

    def test__add_signal(self):

        self.obs._add_signal("undo")
        self.obs.emit("undo")

    def test__validate(self):

        for value in ([], {}, set()):
            assert self.obs._validate("", value) == value
            assert self.obs._validate("", value) is not value
        for value in (True, "", 1, 1.0, (), frozenset()):
            assert self.obs._validate("", value) == value
            assert self.obs._validate("", value) is value

    def test_block(self):

        assert self.obs.block("do")
        assert not self.obs.block("do")
        self.obs.emit("do")
        assert self.do_count == 0

    def test_block_all(self):

        assert self.obs.block_all()
        assert not self.obs.block_all()
        self.obs.emit("do")
        assert self.do_count == 0
        self.obs.notify("variable")
        assert self.notify_count == 0

    def test_disconnect(self):

        self.obs.disconnect("do", self.on_do)
        self.obs.emit("do")
        assert self.do_count == 0

    def test_emit(self):

        self.obs.variable = 1
        assert self.notify_count == 1
        self.obs.emit("do")
        assert self.do_count == 1

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

        self.obs.block("do")
        assert self.obs.unblock("do")
        assert not self.obs.unblock("do")
        self.obs.emit("do")
        assert self.do_count == 1

    def test_unblock_all(self):

        self.obs.block_all()
        assert self.obs.unblock_all()
        assert not self.obs.unblock_all()
        self.obs.emit("do")
        assert self.do_count == 1
        self.obs.notify("variable")
        assert self.notify_count == 1
