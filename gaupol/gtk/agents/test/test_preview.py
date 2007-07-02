# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.


import functools
import gaupol.gtk
import gtk

from gaupol.gtk import unittest


class TestPreviewAgent(unittest.TestCase):

    def run__show_encoding_error_dialog(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_encoding_error_dialog()

    def run__show_io_error_dialog(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_io_error_dialog("test")

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.preview.im_self
        respond = lambda *args: gtk.RESPONSE_DELETE_EVENT
        self.delegate.flash_dialog = respond

    def test__show_encoding_error_dialog(self):

        self.delegate._show_encoding_error_dialog()

    def test__show_io_error_dialog(self):

        self.delegate._show_io_error_dialog("test")
