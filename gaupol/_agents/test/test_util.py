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


from gaupol import const, tags
from gaupol.unittest import TestCase


class TestUtilityAgent(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()

    def test_get_changed(self):

        changed = self.project.get_changed(const.DOCUMENT.MAIN)
        assert changed == self.project.main_changed
        changed = self.project.get_changed(const.DOCUMENT.TRAN)
        assert changed == self.project.tran_changed

    def test_get_file(self):

        file = self.project.get_file(const.DOCUMENT.MAIN)
        assert file == self.project.main_file
        file = self.project.get_file(const.DOCUMENT.TRAN)
        assert file == self.project.tran_file

    def test_get_file_class(self):

        cls = self.project.get_file_class(const.DOCUMENT.MAIN)
        assert cls == self.project.main_file.__class__
        cls = self.project.get_file_class(const.DOCUMENT.TRAN)
        assert cls == self.project.tran_file.__class__

    def test_get_line_lengths(self):

        self.project.subtitles[0].main_text = "<i>test\ntest.</i>"
        lengths = self.project.get_line_lengths(0, const.DOCUMENT.MAIN)
        assert lengths == [4, 5]

    def test_get_mode(self):

        self.project.open_main(self.get_subrip_path(), "ascii")
        assert self.project.get_mode() == const.MODE.TIME
        self.project.open_main(self.get_microdvd_path(), "ascii")
        assert self.project.get_mode() == const.MODE.FRAME

    def test_get_parser(self):

        doc = const.DOCUMENT.MAIN
        parser = self.project.get_parser(doc)
        assert parser.re_tag == self.project.get_tag_regex(doc)

    def test_get_revertable_action(self):

        register = const.REGISTER.DO
        action = self.project.get_revertable_action(register)
        assert action.register == register

    def test_get_subtitle(self):

        subtitle = self.project.get_subtitle()
        assert subtitle.mode == self.project.main_file.mode
        assert subtitle.framerate == self.project.framerate

    def test_get_tag_library(self):

        taglib = self.project.get_tag_library(const.DOCUMENT.MAIN)
        class_name = self.project.main_file.__class__.__name__
        assert taglib == getattr(tags, class_name)()
        taglib = self.project.get_tag_library(const.DOCUMENT.TRAN)
        class_name = self.project.tran_file.__class__.__name__
        assert taglib == getattr(tags, class_name)()

    def test_get_tag_regex(self):

        re_tag = self.project.get_tag_regex(const.DOCUMENT.MAIN)
        assert re_tag is not None
        self.project.main_file = None
        re_tag = self.project.get_tag_regex(const.DOCUMENT.MAIN)
        assert re_tag is None

    def test_get_text_length(self):

        self.project.subtitles[0].main_text = "<i>test\ntest.</i>"
        length = self.project.get_text_length(0, const.DOCUMENT.MAIN)
        assert length == 10

    def test_get_text_signal(self):

        signal = self.project.get_text_signal(const.DOCUMENT.MAIN)
        assert signal == "main-texts-changed"
        signal = self.project.get_text_signal(const.DOCUMENT.TRAN)
        assert signal == "translation-texts-changed"
