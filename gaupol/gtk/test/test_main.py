# Copyright (C) 2006-2008 Osmo Salomaa
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

import gaupol.gtk


class TestModule(gaupol.gtk.TestCase):

    def test__check_dependencies(self):

        gaupol.gtk.main._check_dependencies()

    def test__init_application(self):

        opts = type("", (object,), {})
        opts.encoding = "ascii"
        opts.translation_file = self.get_subrip_path()
        opts.adapt_translation = True
        opts.video_file = self.get_subrip_path()
        args = [self.get_subrip_path(), "+3"]
        gaupol.gtk.main._init_application(opts, args)

    def test__init_configuration(self):

        path = self.get_subrip_path()
        open(path, "w").write("\n")
        gaupol.gtk.main._init_configuration(path)

    def test__init_debugging(self):

        gaupol.gtk.main._init_debugging(True)
        gaupol.gtk.main._init_debugging(False)

    def test__list_encodings(self):

        gaupol.gtk.main._list_encodings()

    def test__move_eggs(self):

        gaupol.gtk.main._move_eggs()

    def test__parse_args(self):

        gaupol.gtk.main._parse_args([])

    def test__show_version(self):

        gaupol.gtk.main._show_version()
