# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009 Osmo Salomaa
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

import aeidon


class TestUtilityAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()
        self.delegate = self.project.get_changed.__self__

    def test_get_all_indices(self):
        indices = self.project.get_all_indices()
        assert indices == list(range(len(self.project.subtitles)))

    def test_get_changed__main(self):
        changed = self.project.get_changed(aeidon.documents.MAIN)
        assert changed == self.project.main_changed

    def test_get_changed__translation(self):
        changed = self.project.get_changed(aeidon.documents.TRAN)
        assert changed == self.project.tran_changed

    def test_get_changed__value_error(self):
        self.assert_raises(ValueError, self.project.get_changed, None)

    def test_get_file__main(self):
        file = self.project.get_file(aeidon.documents.MAIN)
        assert file is self.project.main_file

    def test_get_file__translation(self):
        file = self.project.get_file(aeidon.documents.TRAN)
        assert file is self.project.tran_file

    def test_get_file__value_error(self):
        self.assert_raises(ValueError, self.project.get_file, None)

    def test_get_format__main(self):
        format = self.project.get_format(aeidon.documents.MAIN)
        assert format == self.project.main_file.format

    def test_get_format__main_is_none(self):
        self.project.main_file = None
        format = self.project.get_format(aeidon.documents.MAIN)
        assert format is None

    def test_get_format__translation(self):
        format = self.project.get_format(aeidon.documents.TRAN)
        assert format == self.project.tran_file.format

    def test_get_format__translation_is_none(self):
        self.project.tran_file = None
        format = self.project.get_format(aeidon.documents.TRAN)
        assert format == self.project.main_file.format

    def test_get_format__value_error(self):
        self.assert_raises(ValueError, self.project.get_format, None)

    def test_get_liner(self):
        doc = aeidon.documents.MAIN
        liner = self.project.get_liner(doc)
        assert liner.re_tag == self.project.get_markup_tag_regex(doc)

    def test_get_markup__main(self):
        markup = self.project.get_markup(aeidon.documents.MAIN)
        format = self.project.main_file.format
        assert markup == aeidon.tags.new(format)

    def test_get_markup__translation(self):
        markup = self.project.get_markup(aeidon.documents.TRAN)
        format = self.project.tran_file.format
        assert markup == aeidon.tags.new(format)

    def test_get_markup_clean_func(self):
        doc = aeidon.documents.MAIN
        clean_func = self.project.get_markup_clean_func(doc)
        assert clean_func("") == ""

    def test_get_markup_tag_regex(self):
        re_tag = self.project.get_markup_tag_regex(aeidon.documents.MAIN)
        assert re_tag is not None

    def test_get_markup_tag_regex__none(self):
        self.project.main_file = None
        re_tag = self.project.get_markup_tag_regex(aeidon.documents.MAIN)
        assert re_tag is None

    def test_get_mode__default(self):
        self.project.main_file = None
        mode = self.project.get_mode()
        assert mode == aeidon.modes.TIME

    def test_get_mode__frame(self):
        self.project.open_main(self.new_microdvd_file(), "ascii")
        mode = self.project.get_mode()
        assert mode == aeidon.modes.FRAME

    def test_get_mode__time(self):
        self.project.open_main(self.new_subrip_file(), "ascii")
        mode = self.project.get_mode()
        assert mode == aeidon.modes.TIME

    def test_get_parser(self):
        doc = aeidon.documents.MAIN
        parser = self.project.get_parser(doc)
        assert parser.re_tag == self.project.get_markup_tag_regex(doc)

    def test_get_text_length(self):
        self.project.subtitles[0].main_text = "<i>test\ntest.</i>"
        length = self.project.get_text_length(0, aeidon.documents.MAIN)
        assert length == 10

    def test_get_text_signal__main(self):
        signal = self.project.get_text_signal(aeidon.documents.MAIN)
        assert signal == "main-texts-changed"

    def test_get_text_signal__translation(self):
        signal = self.project.get_text_signal(aeidon.documents.TRAN)
        assert signal == "translation-texts-changed"

    def test_get_text_signal__value_error(self):
        self.assert_raises(ValueError, self.project.get_text_signal, None)

    def test_new_revertable_action(self):
        register = aeidon.registers.DO
        action = self.project.new_revertable_action(register)
        assert action.register == register

    def test_new_subtitle(self):
        subtitle = self.project.new_subtitle()
        assert subtitle.mode == self.project.main_file.mode
        assert subtitle.framerate == self.project.framerate

    def test_new_temp_file__main(self):
        self.project.new_temp_file(aeidon.documents.MAIN)
        self.project.new_temp_file(aeidon.documents.MAIN, "ascii")

    def test_new_temp_file__translation(self):
        self.project.new_temp_file(aeidon.documents.TRAN)
        self.project.new_temp_file(aeidon.documents.TRAN, "ascii")
