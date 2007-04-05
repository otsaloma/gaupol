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


import gtk

from gaupol.gtk import const
from gaupol.gtk.unittest import TestCase
from .. import frconvert


class TestFramerateConvertDialog(TestCase):

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.application = self.get_application()
        parent = self.application.window
        self.dialog = frconvert.FramerateConvertDialog(
            parent, self.application)
        self.dialog.show()

    def test__convert(self):

        self.dialog._convert()

    def test__get_target(self):

        target = self.dialog._get_target()
        assert target in (const.TARGET.SELECTED, const.TARGET.CURRENT)

    def test__get_target_pages(self):

        pages = self.dialog._get_target_pages()
        assert isinstance(pages, list)

    def test__on_correct_combo_changed(self):

        for framerate in const.FRAMERATE.members:
            self.dialog._correct_combo.set_active(framerate)

    def test__on_current_combo_changed(self):

        for framerate in const.FRAMERATE.members:
            self.dialog._current_combo.set_active(framerate)

    def test__on_response(self):

        self.dialog.response(gtk.RESPONSE_OK)
