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


import re

from gaupol.base              import cons
from gaupol.base.tags         import TagLibrary
from gaupol.base.tags.classes import *
from gaupol.test              import Test


class TestTagLibrary(Test):

    def test_attributes(self):

        for name in cons.Format.class_names:
            cls = eval(name)
            re.compile(*cls.tag)
            re.compile(*cls.italic_tag)
            for lst in (cls.decode_tags, cls.encode_tags):
                for entry in lst:
                    re.compile(entry[0], entry[1])
                    assert isinstance(entry[2], basestring)
                    if len(entry) == 4:
                        assert isinstance(entry[3], int)

    def test_italicize(self):

        for name in cons.Format.class_names:
            cls = eval(name)
            text = cls.italicize('test')
            assert isinstance(text, basestring)

    def test_post_decode(self):

        for name in cons.Format.class_names:
            cls = eval(name)
            text = cls.post_decode('test')
            assert isinstance(text, basestring)

    def test_post_encode(self):

        for name in cons.Format.class_names:
            cls = eval(name)
            text = cls.post_encode('test')
            assert isinstance(text, basestring)

    def test_pre_decode(self):

        for name in cons.Format.class_names:
            cls = eval(name)
            text = cls.pre_decode('test')
            assert isinstance(text, basestring)

    def test_pre_encode(self):

        for name in cons.Format.class_names:
            cls = eval(name)
            text = cls.pre_encode('test')
            assert isinstance(text, basestring)
