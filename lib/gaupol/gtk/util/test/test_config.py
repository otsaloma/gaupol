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


import ConfigParser

from gaupol.base.cons import *
from gaupol.gtk.cons  import *
from gaupol.gtk.util  import config
from gaupol.test      import Test


class TestType(Test):

    def test_is_list(self):

        for i in range(0, 4):
            assert config.Type.is_list(i) is False
        for i in range(5, 8):
            assert config.Type.is_list(i) is True


class TestModule(Test):

    def test_get_boolean(self):

        assert config._get_boolean(True)    == 'true'
        assert config._get_boolean(False)   == 'false'
        assert config._get_boolean('true')  is True
        assert config._get_boolean('false') is False

    def test_get_constant(self):

        assert config._get_constant('editor', 'mode', 'time') == Mode.TIME
        assert config._get_constant('editor', 'mode', Mode.TIME) == 'time'

    def test_get_options(self):

        assert config.sections
        for section in config.sections:
            options = config.get_options(section)
            assert options
            for option in options:
                assert isinstance(option, basestring)

    def test_read_and_write(self):

        config.read()
        config.write()
        config.read()
        config.write()
        config.read()

    def test_sections(self):

        assert config.sections
        for section in config.sections:
            cls = getattr(config, section)
            assert issubclass(cls, config.Section)
            assert hasattr(cls, 'types')
            assert hasattr(cls, 'classes')
            assert hasattr(cls, 'run_time_only')

    def test_set_config_option(self):

        config.read()
        config.write()
        parser = ConfigParser.RawConfigParser()
        parser.read([config.CONFIG_FILE])
        LIST_SEP = config.LIST_SEP

        # String
        parser.set('editor', 'font', 'test')
        config._set_config_option(parser, 'editor', 'font')
        assert config.editor.font == 'test'

        # Integer
        parser.set('editor', 'undo_levels', 99)
        config._set_config_option(parser, 'editor', 'undo_levels')
        assert config.editor.undo_levels == 99

        # Boolean
        parser.set('app_window', 'maximized', 'true')
        config._set_config_option(parser, 'app_window', 'maximized')
        assert config.app_window.maximized is True

        # Constant
        parser.set('editor', 'framerate', '25')
        config._set_config_option(parser, 'editor', 'framerate')
        assert config.editor.framerate == Framerate.FR_25

        # String list
        parser.set('encoding', 'fallbacks', 'test%stset' % LIST_SEP)
        config._set_config_option(parser, 'encoding', 'fallbacks')
        assert config.encoding.fallbacks == ['test', 'tset']

        # Integer list
        parser.set('app_window', 'position', '3%s4' % LIST_SEP)
        config._set_config_option(parser, 'app_window', 'position')
        assert config.app_window.position == [3, 4]

        # Constant list
        parser.set('editor', 'visible_cols', 'show%shide' % LIST_SEP)
        config._set_config_option(parser, 'editor', 'visible_cols')
        assert config.editor.visible_cols == [SHOW, HIDE]

    def test_set_parser_option(self):

        config.read()
        config.write()
        parser = ConfigParser.RawConfigParser()
        parser.read([config.CONFIG_FILE])
        LIST_SEP = config.LIST_SEP

        # String
        config.editor.font = 'test'
        config._set_parser_option(parser, 'editor', 'font')
        value = parser.get('editor', 'font')
        assert value == 'test'

        # Integer
        config.editor.undo_levels = 99
        config._set_parser_option(parser, 'editor', 'undo_levels')
        value = parser.get('editor', 'undo_levels')
        assert value == '99'

        # Boolean
        config.app_window.maximized = True
        config._set_parser_option(parser, 'app_window', 'maximized')
        value = parser.get('app_window', 'maximized')
        assert value == 'true'

        # Constant
        config.editor.framerate = Framerate.FR_25
        config._set_parser_option(parser, 'editor', 'framerate')
        value = parser.get('editor', 'framerate')
        assert value == '25'

        # String list
        config.encoding.fallbacks = ['test', 'tset']
        config._set_parser_option(parser, 'encoding', 'fallbacks')
        value = parser.get('encoding', 'fallbacks')
        assert value == 'test%stset' % LIST_SEP

        # Integer list
        config.app_window.position = [3, 4]
        config._set_parser_option(parser, 'app_window', 'position')
        value = parser.get('app_window', 'position')
        assert value == '3%s4' % LIST_SEP

        # Constant list
        config.editor.visible_cols = [SHOW, HIDE]
        config._set_parser_option(parser, 'editor', 'visible_cols')
        value = parser.get('editor', 'visible_cols')
        assert value == 'show%shide' % LIST_SEP
