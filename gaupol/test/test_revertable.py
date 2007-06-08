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


import gaupol

from gaupol import unittest
from .. import revertable


class TestRevertableAction(unittest.TestCase):

    def setup_method(self, method):

        def revert(register=-1):
            assert register in gaupol.REGISTER.members
        self.action = revertable.RevertableAction()
        self.action.register=gaupol.REGISTER.DO
        self.action.docs=[gaupol.DOCUMENT.MAIN]
        self.action.description=""
        self.action.revert_method=revert

    def test__get_reversion_register(self):

        register = self.action._get_reversion_register()
        assert register == gaupol.REGISTER.UNDO

    def test_revert(self):

        self.action.revert()


class TestRevertableActionGroup(unittest.TestCase):

    def test___init__(self):

        action_group = revertable.RevertableActionGroup()
        action_group.actions = []
        action_group.description = ""
