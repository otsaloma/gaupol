# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if falset, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


from gaupol.base.cons import Action
from gaupol.base.cons import Column
from gaupol.base.cons import Document
from gaupol.base.cons import Format
from gaupol.base.cons import Framerate
from gaupol.base.cons import Mode
from gaupol.base.cons import Newlines
from gaupol.base.cons import VideoPlayer
from gaupol.test      import Test


classes = [
    Action,
    Column,
    Document,
    Format,
    Framerate,
    Mode,
    Newlines,
    VideoPlayer,
]


class TestSection(Test):

    def test_get_names(self):

        for cls in classes:
            names = cls.get_names()
            assert names
            for i, name in enumerate(names):
                assert getattr(cls, name) == i
                assert cls.get_name(i) == name
