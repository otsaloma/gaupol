# Copyright (C) 2007-2009 Osmo Salomaa
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

import aeidon


class PuppetBaseClass(object):

    __metaclass__ = aeidon.Contractual

    def _invariant(self):
        assert True

    def do_require(self):
        assert True

    def do_ensure(self, value):
        assert value is None

    def do(self):
        return None


class PuppetClassImplemented(PuppetBaseClass):

    def _invariant(self):
        assert True

    def do_require(self):
        assert True

    def do_ensure(self, value):
        assert value is None

    def do(self):
        return None


class PuppetClassNotImplemented(PuppetBaseClass):

    def do(self):
        return None


class TestContractual(aeidon.TestCase):

    def setup_method(self, method):
        self.contractual = PuppetClassImplemented()

    def test___new____implemented(self):
        self.contractual = PuppetClassImplemented()
        self.contractual.do()

    def test___new____not_implemented(self):
        self.contractual = PuppetClassNotImplemented()
        self.contractual.do()
