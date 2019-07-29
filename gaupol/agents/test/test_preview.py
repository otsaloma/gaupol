# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import gaupol


class TestPreviewAgent(gaupol.TestCase):

    def run__show_encoding_error_dialog(self):
        self.delegate._show_encoding_error_dialog()

    def run__show_io_error_dialog(self):
        self.delegate._show_io_error_dialog("test")

    def run__show_player_not_found_error_dialog(self):
        self.delegate._show_player_not_found_error_dialog()

    def run__show_process_error_dialog(self):
        self.delegate._show_process_error_dialog("test")

    def setup_method(self, method):
        self.application = self.new_application()
        self.delegate = self.application.preview.__self__
