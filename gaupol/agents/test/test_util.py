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


import gaupol
from gaupol import unittest


class TestUtilityAgent(unittest.TestCase):

    def setup_method(self, method):

        self.project = self.get_project()

    def test_get_changed(self):

        changed = self.project.get_changed(gaupol.DOCUMENT.MAIN)
        assert changed == self.project.main_changed
        changed = self.project.get_changed(gaupol.DOCUMENT.TRAN)
        assert changed == self.project.tran_changed

    def test_get_file(self):

        file = self.project.get_file(gaupol.DOCUMENT.MAIN)
        assert file == self.project.main_file
        file = self.project.get_file(gaupol.DOCUMENT.TRAN)
        assert file == self.project.tran_file

    def test_get_file_class(self):

        cls = self.project.get_file_class(gaupol.DOCUMENT.MAIN)
        assert cls == self.project.main_file.__class__
        cls = self.project.get_file_class(gaupol.DOCUMENT.TRAN)
        assert cls == self.project.tran_file.__class__

    def test_get_line_lengths(self):

        self.project.subtitles[0].main_text = "<i>test\ntest.</i>"
        lengths = self.project.get_line_lengths(0, gaupol.DOCUMENT.MAIN)
        assert lengths == [4, 5]

    def test_get_mode(self):

        self.project.open_main(self.get_subrip_path(), "ascii")
        assert self.project.get_mode() == gaupol.MODE.TIME
        self.project.open_main(self.get_microdvd_path(), "ascii")
        assert self.project.get_mode() == gaupol.MODE.FRAME

    def test_get_parser(self):

        doc = gaupol.DOCUMENT.MAIN
        parser = self.project.get_parser(doc)
        assert parser.re_tag == self.project.get_tag_regex(doc)

    def test_get_revertable_action(self):

        register = gaupol.REGISTER.DO
        action = self.project.get_revertable_action(register)
        assert action.register == register

    def test_get_subtitle(self):

        subtitle = self.project.get_subtitle()
        assert subtitle.mode == self.project.main_file.mode
        assert subtitle.framerate == self.project.framerate

    def test_get_tag_library(self):

        taglib = self.project.get_tag_library(gaupol.DOCUMENT.MAIN)
        format = self.project.main_file.format
        assert taglib == gaupol.tags.get_class(format)()
        taglib = self.project.get_tag_library(gaupol.DOCUMENT.TRAN)
        format = self.project.tran_file.format
        assert taglib == gaupol.tags.get_class(format)()

    def test_get_tag_regex(self):

        re_tag = self.project.get_tag_regex(gaupol.DOCUMENT.MAIN)
        assert re_tag is not None
        self.project.main_file = None
        re_tag = self.project.get_tag_regex(gaupol.DOCUMENT.MAIN)
        assert re_tag is None

    def test_get_text_length(self):

        self.project.subtitles[0].main_text = "<i>test\ntest.</i>"
        length = self.project.get_text_length(0, gaupol.DOCUMENT.MAIN)
        assert length == 10

    def test_get_text_signal(self):

        signal = self.project.get_text_signal(gaupol.DOCUMENT.MAIN)
        assert signal == "main-texts-changed"
        signal = self.project.get_text_signal(gaupol.DOCUMENT.TRAN)
        assert signal == "translation-texts-changed"
