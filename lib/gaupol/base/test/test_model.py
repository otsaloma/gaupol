# Copyright (C) 2005-2006 Osmo Salomaa
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


from gaupol.base.model import Model
from gaupol.test       import Test


class TestModel(Test):

    def test_signals(self):

        class Count(object):
            test = 0
            rest = 0

        def on_test(arg):
            assert arg == 1
            Count.test += 1

        def on_rest(kwarg=None):
            assert kwarg == 2
            Count.rest += 1

        Model._signals = ['test', 'rest']
        model = Model()
        model.connect('test', on_test)
        model.connect('rest', on_rest)
        model.emit('test', 1)
        model.emit('rest', kwarg=2)
        model.block('test')
        model.block('rest')
        model.emit('test', 1)
        model.emit('rest', kwarg=2)
        model.unblock('test')
        model.unblock('rest')
        model.emit('test', 1)
        model.emit('rest', kwarg=2)

        assert Count.test == 2
        assert Count.rest == 2
