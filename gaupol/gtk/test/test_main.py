# Copyright (C) 2006-2007 Osmo Salomaa
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


from gaupol.gtk.unittest import TestCase
from .. import main


class TestModule(TestCase):

    def test_check_dependencies(self):

        main._check_dependencies()

    def test_list_encodings(self):

        main._list_encodings()

    def test_move_eggs(self):

        main._move_eggs()

    def test_prepare_ui(self):

        main._prepare_ui()

    def test_show_version(self):

        main._show_version()
