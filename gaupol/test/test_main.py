# -*- coding: utf-8-unix -*-

# Copyright (C) 2006-2008,2010 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

import gaupol


class TestModule(gaupol.TestCase):

    def test__check_dependencies(self):
        gaupol.main._check_dependencies()

    def test__init_application(self):
        opts = type("", (object,), {})
        opts.encoding = "ascii"
        opts.translation_file = self.new_subrip_file()
        opts.align_method = "position"
        opts.video_file = self.new_subrip_file()
        args = [self.new_subrip_file(), "+3"]
        gaupol.main._init_application(opts, args)

    def test__init_configuration(self):
        path = self.new_subrip_file()
        open(path, "w").write("\n")
        gaupol.main._init_configuration(path)

    def test__on_parser_list_encodings(self):
        self.assert_raises(SystemExit, gaupol.main._on_parser_list_encodings)

    def test__on_parser_version(self):
        self.assert_raises(SystemExit, gaupol.main._on_parser_version)

    def test__parse_args(self):
        gaupol.main._parse_args([])
