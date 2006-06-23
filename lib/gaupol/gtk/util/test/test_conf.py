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


import ConfigParser

from gaupol.gtk       import cons
from gaupol.gtk.icons import *
from gaupol.gtk.util  import conf
from gaupol.test      import Test


class TestSection(Test):

    def test_attributes(self):

        for section in conf._get_sections():
            cls = getattr(conf, section)
            assert hasattr(cls, 'constants')
            assert hasattr(cls, 'types')
            assert hasattr(cls, 'privates')
            options = cls.get_options()
            assert isinstance(options, list)
            assert options
            for option in options:
                assert isinstance(option, basestring)

class TestModule(Test):

    def test_get_boolean(self):

        assert conf._get_boolean(True)    == 'true'
        assert conf._get_boolean(False)   == 'false'
        assert conf._get_boolean('true')  is True
        assert conf._get_boolean('false') is False

    def test_get_constant(self):

        assert conf._get_constant('editor', 'mode', 'TIME') == cons.Mode.TIME
        assert conf._get_constant('editor', 'mode', cons.Mode.TIME) == 'time'

    def test_get_sections(self):

        sections = conf._get_sections()
        assert isinstance(sections, list)
        assert sections
        for section in sections:
            assert hasattr(conf, section)

    def test_set_conf_option(self):

        conf.read()
        conf.write()
        parser = ConfigParser.RawConfigParser()
        parser.read([conf._CONFIG_FILE])

        # String
        parser.set('editor', 'font', 'test')
        conf._set_conf_option(parser, 'editor', 'font')
        assert conf.editor.font == 'test'

        # Integer
        parser.set('editor', 'undo_levels', 99)
        conf._set_conf_option(parser, 'editor', 'undo_levels')
        assert conf.editor.undo_levels == 99

        # Boolean
        parser.set('application_window', 'maximized', 'true')
        conf._set_conf_option(parser, 'application_window', 'maximized')
        assert conf.application_window.maximized is True

        # Constant
        parser.set('editor', 'framerate', 'fr_25')
        conf._set_conf_option(parser, 'editor', 'framerate')
        assert conf.editor.framerate == cons.Framerate.FR_25

        # String list
        parser.set('encoding', 'fallbacks', '[test,rest]')
        conf._set_conf_option(parser, 'encoding', 'fallbacks')
        assert conf.encoding.fallbacks == ['test', 'rest']

        # Integer list
        parser.set('application_window', 'position', '[3,4]')
        conf._set_conf_option(parser, 'application_window', 'position')
        assert conf.application_window.position == [3, 4]

        # Constant list
        parser.set('editor', 'visible_cols', '[show,hide]')
        conf._set_conf_option(parser, 'editor', 'visible_cols')
        assert conf.editor.visible_cols == [SHOW, HIDE]

    def test_set_parser_option(self):

        conf.read()
        conf.write()
        parser = ConfigParser.RawConfigParser()
        parser.read([conf._CONFIG_FILE])

        # String
        conf.editor.font = 'test'
        conf._set_parser_option(parser, 'editor', 'font')
        value = parser.get('editor', 'font')
        assert value == 'test'

        # Integer
        conf.editor.undo_levels = 99
        conf._set_parser_option(parser, 'editor', 'undo_levels')
        value = parser.get('editor', 'undo_levels')
        assert value == '99'

        # Boolean
        conf.application_window.maximized = True
        conf._set_parser_option(parser, 'application_window', 'maximized')
        value = parser.get('application_window', 'maximized')
        assert value == 'true'

        # Constant
        conf.editor.framerate = cons.Framerate.FR_25
        conf._set_parser_option(parser, 'editor', 'framerate')
        value = parser.get('editor', 'framerate')
        assert value == 'fr_25'

        # String list
        conf.encoding.fallbacks = ['test', 'rest']
        conf._set_parser_option(parser, 'encoding', 'fallbacks')
        value = parser.get('encoding', 'fallbacks')
        assert value == '[test,rest]'

        # Integer list
        conf.application_window.position = [3, 4]
        conf._set_parser_option(parser, 'application_window', 'position')
        value = parser.get('application_window', 'position')
        assert value == '[3,4]'

        # Constant list
        conf.editor.visible_cols = [SHOW, HIDE]
        conf._set_parser_option(parser, 'editor', 'visible_cols')
        value = parser.get('editor', 'visible_cols')
        assert value == '[show,hide]'

    def test_read_and_write(self):

        conf.read()
        conf.write()
        conf.read()
        conf.write()
        conf.read()
