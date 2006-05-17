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
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import re

from gaupol.base.text.parser import Parser
from gaupol.test             import Test


TEXT = '''\
<i>He changed shifts.</i>
Didn\'t <i>he</i> tell you?'''


class TestParser(Test):

    def test_init(self):

        Parser()
        Parser(re.compile(r'x'))

    def test_get_and_set_text(self):

        parser = Parser(re.compile(r'<.*?>'))
        parser.set_text(TEXT)
        assert parser.get_text() == TEXT

    def test_replace(self):

        def get_text(pattern, replacement):
            parser = Parser(re.compile(r'<.*?>'))
            parser.set_text(TEXT)
            parser.pattern = pattern
            parser.replacement = replacement
            parser.next()
            parser.replace()
            return parser.get_text()

        text = get_text('i', '_')
        assert text == \
            '<i>He changed sh_fts.</i>\n' \
            'Didn\'t <i>he</i> tell you?'

        text = get_text('e', '__')
        assert text == \
            '<i>H__ changed shifts.</i>\n' \
            'Didn\'t <i>he</i> tell you?'

        text = get_text('e', '')
        assert text == \
            '<i>H changed shifts.</i>\n' \
            'Didn\'t <i>he</i> tell you?'

        def get_text(pattern, flags, replacement):
            parser = Parser(re.compile(r'<.*?>'))
            parser.set_text(TEXT)
            parser.set_regex(pattern, flags)
            parser.replacement = replacement
            parser.next()
            parser.replace()
            return parser.get_text()

        text = get_text(r'[Hh]', 0, '_')
        assert text == \
            '<i>_e changed shifts.</i>\n' \
            'Didn\'t <i>he</i> tell you?'

        text = get_text(r'\W', 0, '__')
        assert text == \
            '<i>He__changed shifts.</i>\n' \
            'Didn\'t <i>he</i> tell you?'

        text = get_text(r'\s', 0, '')
        assert text == \
            '<i>Hechanged shifts.</i>\n' \
            'Didn\'t <i>he</i> tell you?'

    def test_replace_all(self):

        def get_text(pattern, replacement):
            parser = Parser(re.compile(r'<.*?>'))
            parser.set_text(TEXT)
            parser.pattern = pattern
            parser.replacement = replacement
            parser.replace_all()
            return parser.get_text()

        text = get_text('i', '_')
        assert text == \
            '<i>He changed sh_fts.</i>\n' \
            'D_dn\'t <i>he</i> tell you?'

        text = get_text('e', '__')
        assert text == \
            '<i>H__ chang__d shifts.</i>\n' \
            'Didn\'t <i>h__</i> t__ll you?'

        text = get_text('H', '')
        assert text == \
            '<i>e changed shifts.</i>\n' \
            'Didn\'t <i>he</i> tell you?'

        text = get_text('?', '__')
        assert text == \
            '<i>He changed shifts.</i>\n' \
            'Didn\'t <i>he</i> tell you__'

        text = get_text('?', '')
        assert text == \
            '<i>He changed shifts.</i>\n' \
            'Didn\'t <i>he</i> tell you'

        text = get_text('e', 'e')
        assert text == TEXT

        def get_text(pattern, flags, replacement):
            parser = Parser(re.compile(r'<.*?>'))
            parser.set_text(TEXT)
            parser.set_regex(pattern, flags)
            parser.replacement = replacement
            parser.replace_all()
            return parser.get_text()

        text = get_text(r'i', re.MULTILINE, '_')
        assert text == \
            '<i>He changed sh_fts.</i>\n' \
            'D_dn\'t <i>he</i> tell you?'

        text = get_text(r'[A-Za-z]', re.MULTILINE, '_')
        assert text == \
            '<i>__ _______ ______.</i>\n' \
            '____\'_ <i>__</i> ____ ___?'

        text = get_text(r'[Hh]', re.MULTILINE, '__')
        assert text == \
            '<i>__e c__anged s__ifts.</i>\n' \
            'Didn\'t <i>__e</i> tell you?'

        text = get_text(r'e', re.MULTILINE, '')
        assert text == \
            '<i>H changd shifts.</i>\n' \
            'Didn\'t <i>h</i> tll you?'

        text = get_text(r'\?', re.MULTILINE, '__')
        assert text == \
            '<i>He changed shifts.</i>\n' \
            'Didn\'t <i>he</i> tell you__'

        text = get_text(r'\?', re.MULTILINE, '')
        assert text == \
            '<i>He changed shifts.</i>\n' \
            'Didn\'t <i>he</i> tell you'

        text = get_text(r'\w', re.MULTILINE, 'x')
        assert text == \
            '<i>xx xxxxxxx xxxxxx.</i>\n' \
            'xxxx\'x <i>xx</i> xxxx xxx?'
