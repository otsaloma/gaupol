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

from gaupol.gtk         import cons
from gaupol.gtk.colcons import *
from gaupol.gtk.util    import config
from gaupol.test        import Test


class TestSection(Test):

    def test_attributes(self):

        for section in config._get_sections():
            cls = getattr(config, section)
            assert hasattr(cls, 'types')
            assert hasattr(cls, 'classes')
            assert hasattr(cls, 'run_time_only')
            options = cls.get_options()
            assert isinstance(options, list)
            assert options
            for option in options:
                assert isinstance(option, basestring)

class TestModule(Test):

    def test_get_boolean(self):

        assert config._get_boolean(True)    == 'true'
        assert config._get_boolean(False)   == 'false'
        assert config._get_boolean('true')  is True
        assert config._get_boolean('false') is False

    def test_get_constant(self):

        assert config._get_constant('Editor', 'mode', 'TIME') == cons.Mode.TIME
        assert config._get_constant('Editor', 'mode', cons.Mode.TIME) == 'time'

    def test_get_sections(self):

        sections = config._get_sections()
        assert isinstance(sections, list)
        assert sections
        for section in sections:
            assert hasattr(config, section)

    def test_read_and_write(self):

        config.read()
        config.write()
        config.read()
        config.write()
        config.read()

    def test_set_config_option(self):

        config.read()
        config.write()
        parser = ConfigParser.RawConfigParser()
        parser.read([config.CONFIG_FILE])

        # String
        parser.set('Editor', 'font', 'test')
        config._set_config_option(parser, 'Editor', 'font')
        assert config.Editor.font == 'test'

        # Integer
        parser.set('Editor', 'undo_levels', 99)
        config._set_config_option(parser, 'Editor', 'undo_levels')
        assert config.Editor.undo_levels == 99

        # Boolean
        parser.set('AppWindow', 'maximized', 'true')
        config._set_config_option(parser, 'AppWindow', 'maximized')
        assert config.AppWindow.maximized is True

        # Constant
        parser.set('Editor', 'framerate', 'fr_25')
        config._set_config_option(parser, 'Editor', 'framerate')
        assert config.Editor.framerate == cons.Framerate.FR_25

        # String list
        parser.set('Encoding', 'fallback', '[test,tset]')
        config._set_config_option(parser, 'Encoding', 'fallback')
        assert config.Encoding.fallback == ['test', 'tset']

        # Integer list
        parser.set('AppWindow', 'position', '[3,4]')
        config._set_config_option(parser, 'AppWindow', 'position')
        assert config.AppWindow.position == [3, 4]

        # Constant list
        parser.set('Editor', 'visible_cols', '[show,hide]')
        config._set_config_option(parser, 'Editor', 'visible_cols')
        assert config.Editor.visible_cols == [SHOW, HIDE]

    def test_set_parser_option(self):

        config.read()
        config.write()
        parser = ConfigParser.RawConfigParser()
        parser.read([config.CONFIG_FILE])

        # String
        config.Editor.font = 'test'
        config._set_parser_option(parser, 'Editor', 'font')
        value = parser.get('Editor', 'font')
        assert value == 'test'

        # Integer
        config.Editor.undo_levels = 99
        config._set_parser_option(parser, 'Editor', 'undo_levels')
        value = parser.get('Editor', 'undo_levels')
        assert value == '99'

        # Boolean
        config.AppWindow.maximized = True
        config._set_parser_option(parser, 'AppWindow', 'maximized')
        value = parser.get('AppWindow', 'maximized')
        assert value == 'true'

        # Constant
        config.Editor.framerate = cons.Framerate.FR_25
        config._set_parser_option(parser, 'Editor', 'framerate')
        value = parser.get('Editor', 'framerate')
        assert value == 'fr_25'

        # String list
        config.Encoding.fallback = ['test', 'tset']
        config._set_parser_option(parser, 'Encoding', 'fallback')
        value = parser.get('Encoding', 'fallback')
        assert value == '[test,tset]'

        # Integer list
        config.AppWindow.position = [3, 4]
        config._set_parser_option(parser, 'AppWindow', 'position')
        value = parser.get('AppWindow', 'position')
        assert value == '[3,4]'

        # Constant list
        config.Editor.visible_cols = [SHOW, HIDE]
        config._set_parser_option(parser, 'Editor', 'visible_cols')
        value = parser.get('Editor', 'visible_cols')
        assert value == '[show,hide]'
