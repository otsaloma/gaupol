# Copyright (C) 2005-2008 Osmo Salomaa
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


class TestUtilityAgent(gaupol.TestCase):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = self.project.get_changed.im_self

    def test__get_format(self):

        get_format = self.delegate._get_format
        format = get_format(gaupol.documents.MAIN)
        assert format == self.project.main_file.format
        format = get_format(gaupol.documents.TRAN)
        assert format == self.project.tran_file.format
        self.project.tran_file = None
        format = get_format(gaupol.documents.TRAN)
        assert format == self.project.main_file.format
        self.raises(ValueError, get_format, None)

    def test_get_changed(self):

        get_changed = self.project.get_changed
        changed = get_changed(gaupol.documents.MAIN)
        assert changed == self.project.main_changed
        changed = get_changed(gaupol.documents.TRAN)
        assert changed == self.project.tran_changed
        self.raises(ValueError, get_changed, None)

    def test_get_file(self):

        get_file = self.project.get_file
        file = get_file(gaupol.documents.MAIN)
        assert file == self.project.main_file
        file = get_file(gaupol.documents.TRAN)
        assert file == self.project.tran_file
        self.raises(ValueError, get_file, None)

    def test_get_liner(self):

        doc = gaupol.documents.MAIN
        liner = self.project.get_liner(doc)
        assert liner.re_tag == self.project.get_markup_tag_regex(doc)

    def test_get_markup(self):

        markup = self.project.get_markup(gaupol.documents.MAIN)
        format = self.project.main_file.format
        assert markup == gaupol.tags.new(format)
        markup = self.project.get_markup(gaupol.documents.TRAN)
        format = self.project.tran_file.format
        assert markup == gaupol.tags.new(format)

    def test_get_markup_clean_func(self):

        doc = gaupol.documents.MAIN
        clean_func = self.project.get_markup_clean_func(doc)
        assert clean_func("") == ""

    def test_get_markup_tag_regex(self):

        get_regex = self.project.get_markup_tag_regex
        re_tag = get_regex(gaupol.documents.MAIN)
        assert re_tag is not None
        self.project.main_file = None
        re_tag = get_regex(gaupol.documents.MAIN)
        assert re_tag is None

    def test_get_mode(self):

        self.project.open_main(self.get_subrip_path(), "ascii")
        assert self.project.get_mode() == gaupol.modes.TIME
        self.project.open_main(self.get_microdvd_path(), "ascii")
        assert self.project.get_mode() == gaupol.modes.FRAME
        self.project.main_file = None
        assert self.project.get_mode() == gaupol.modes.TIME

    def test_get_parser(self):

        doc = gaupol.documents.MAIN
        parser = self.project.get_parser(doc)
        assert parser.re_tag == self.project.get_markup_tag_regex(doc)

    def test_get_revertable_action(self):

        register = gaupol.registers.DO
        action = self.project.get_revertable_action(register)
        assert action.register == register

    def test_get_subtitle(self):

        subtitle = self.project.get_subtitle()
        assert subtitle.mode == self.project.main_file.mode
        assert subtitle.framerate == self.project.framerate

    def test_get_text_length(self):

        self.project.subtitles[0].main_text = "<i>test\ntest.</i>"
        length = self.project.get_text_length(0, gaupol.documents.MAIN)
        assert length == 10

    def test_get_text_signal(self):

        get_text_signal = self.project.get_text_signal
        signal = get_text_signal(gaupol.documents.MAIN)
        assert signal == "main-texts-changed"
        signal = get_text_signal(gaupol.documents.TRAN)
        assert signal == "translation-texts-changed"
        self.raises(ValueError, get_text_signal, None)
