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


import os

import gtk

from gaupol.gtk.unittest import TestCase


class TestToolsAgent(TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.preview.im_self

        def respond(*args):
            return gtk.RESPONSE_DELETE_EVENT
        self.delegate.flash_dialog = respond
        self.delegate.run_dialog = respond

    def test__clean(self):

        path = self.get_subrip_path()
        self.delegate._clean(path, None)
        assert not os.path.isfile(path)

    def test__post_process(self):

        data = (self.get_subrip_path(), self.get_subrip_path())
        self.delegate._post_process(None, 0, data)
        data = (self.get_subrip_path(), self.get_subrip_path())
        self.delegate._post_process(None, 1, data)

    def test__show_encoding_error_dialog(self):

        self.delegate._show_encoding_error_dialog()

    def test__show_io_error_dialog(self):

        self.delegate._show_io_error_dialog("test")
