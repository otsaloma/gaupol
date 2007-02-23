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


from gaupol.unittest import TestCase
from .. import cons


class TestSection(TestCase):

    def setup_method(self, method):

        # pylint: disable-msg=C0103
        self.SECTION = cons.Section()
        self.SECTION.BOO = cons.Member()
        self.SECTION.BOO.value = 0
        self.SECTION.HOO = cons.Member()
        self.SECTION.HOO.value = 1
        self.SECTION.finalize()

    def test_attributes(self):

        assert self.SECTION.BOO == 0
        assert self.SECTION.BOO.name == "BOO"
        assert self.SECTION.BOO.value == 0
        assert self.SECTION.members[0] == self.SECTION.BOO
        assert self.SECTION.names[0] == "BOO"
        assert self.SECTION.values[0] == 0

        assert self.SECTION.HOO == 1
        assert self.SECTION.HOO.name == "HOO"
        assert self.SECTION.HOO.value == 1
        assert self.SECTION.members[1] == self.SECTION.HOO
        assert self.SECTION.names[1] == "HOO"
        assert self.SECTION.values[1] == 1
