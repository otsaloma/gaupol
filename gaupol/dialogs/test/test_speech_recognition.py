# -*- coding: utf-8-unix -*-

# Copyright (C) 2011 Osmo Salomaa
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
import gaupol
from gi.repository import Gtk


class TestSpeechRecognitionDialog(gaupol.TestCase):

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        conf = gaupol.conf.speech_recognition
        conf.acoustic_model = aeidon.temp.create_directory()
        conf.phonetic_dict = aeidon.temp.create()
        conf.lang_model = aeidon.temp.create()
        self.application = self.new_application()
        self.dialog = gaupol.SpeechRecognitionDialog(self.application.window,
                                                     self.application)

        self.dialog.show()

    def test__on_advance_spin_value_changed(self):
        self.dialog._advance_spin.set_value(100)
        self.dialog._advance_spin.set_value(200)
        self.dialog._advance_spin.set_value(300)

    def test__on_default_model_check_toggled(self):
        self.dialog._default_model_check.set_active(True)
        self.dialog._default_model_check.set_active(False)
        self.dialog._default_model_check.set_active(True)

    def test__on_noise_spin_value_changed(self):
        self.dialog._noise_spin.set_value(100)
        self.dialog._noise_spin.set_value(200)
        self.dialog._noise_spin.set_value(300)

    def test__on_response__close(self):
        self.dialog.response(Gtk.ResponseType.CLOSE)

    def test__on_response__help(self):
        self.dialog.response(Gtk.ResponseType.HELP)

    def test__on_revert_button_clicked__advance(self):
        self.dialog._advance_spin.set_value(100)
        advance = self.dialog._advance_spin.get_value_as_int()
        assert advance == 100
        self.dialog._revert_button.clicked()
        advance = self.dialog._advance_spin.get_value_as_int()
        default = gaupol.conf.query_default("speech_recognition",
                                            "advance_length")

        assert advance == default

    def test__on_revert_button_clicked__noise(self):
        self.dialog._noise_spin.set_value(100)
        noise = self.dialog._noise_spin.get_value_as_int()
        assert noise == 100
        self.dialog._revert_button.clicked()
        noise = self.dialog._noise_spin.get_value_as_int()
        default = gaupol.conf.query_default("speech_recognition",
                                            "noise_level")

        assert noise == default

    def test__on_revert_button_clicked__silence(self):
        self.dialog._silence_spin.set_value(100)
        silence = self.dialog._silence_spin.get_value_as_int()
        assert silence == 100
        self.dialog._revert_button.clicked()
        silence = self.dialog._silence_spin.get_value_as_int()
        default = gaupol.conf.query_default("speech_recognition",
                                            "silence_length")

        assert silence == default

    def test__on_silence_spin_value_changed(self):
        self.dialog._silence_spin.set_value(100)
        self.dialog._silence_spin.set_value(200)
        self.dialog._silence_spin.set_value(300)
