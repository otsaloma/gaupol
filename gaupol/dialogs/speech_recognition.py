# -*- coding: utf-8 -*-

# Copyright (C) 2011-2012 Osmo Salomaa
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

"""Dialog for generating subtitles by voice and speech recognition."""

import aeidon
import gaupol
import itertools
import os
_ = aeidon.i18n._

from gi.repository import Gtk

try:
    from gi.repository import Gst
except Exception:
    pass

__all__ = ("SpeechRecognitionDialog",)


class SpeechRecognitionDialog(gaupol.BuilderDialog):

    """Dialog for generating subtitles by voice and speech recognition."""

    _widgets = ("acoustic_button",
                "advance_spin",
                "default_model_check",
                "dialog",
                "dict_button",
                "lang_button",
                "model_grid",
                "noise_spin",
                "options_vbox",
                "progressbar",
                "revert_button",
                "silence_spin",
                "video_button",
                )

    def __init__(self, parent, application):
        """Initialize a :class:`SpeechRecognitionDialog` instance."""
        gaupol.BuilderDialog.__init__(self, "speech-recognition-dialog.ui")
        self.application = application
        self._page = None
        self._pipeline = None
        self._starts = []
        self._stops = []
        self._text = None
        self._texts = []
        self._init_values()
        self._init_sensitivities()
        width = gaupol.util.char_to_px(42)
        self._video_button.set_size_request(width, -1)
        self._update_response_sensitivities()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(Gtk.ResponseType.CLOSE)

    def _clear_attributes(self):
        """Clear values of result attributes."""
        self._pipeline = None
        self._starts = []
        self._stops = []
        self._text = None
        self._texts = []

    def _get_filesrc_definition(self):
        """Return ``filesrc`` definition for :func:`Gst.parse_launch`."""
        path = self._video_button.get_filename()
        return 'filesrc location="{}" '.format(path)

    def _get_pipeline_definition(self):
        """Return pipeline definition for :func:`Gst.parse_launch`."""
        return (self._get_filesrc_definition()
                + "! decodebin "
                + "! audioconvert "
                + "! audioresample "
                + self._get_vader_definition()
                + self._get_pocketsphinx_definition()
                + "! fakesink"
                )

    def _get_pocketsphinx_definition(self):
        """Return ``pocketsphinx`` definition for :func:`Gst.parse_launch`."""
        definition = "! pocketsphinx name=pocketsphinx "
        if self._default_model_check.get_active():
            return definition
        return definition + 'hmm="{}" dict="{}" lm="{}" '.format(
            self._acoustic_button.get_current_folder(),
            self._dict_button.get_filename(),
            self._lang_button.get_filename())

    def _get_vader_definition(self):
        """Return ``vader`` definition for :func:`Gst.parse_launch`."""
        # Convert noise level from spin button range [0,32768] to GStreamer
        # element's range [0,1]. Likewise, convert silence from spin button's
        # milliseconds to GStreamer element's nanoseconds.
        noise = self._noise_spin.get_value_as_int() / 32768
        silence = self._silence_spin.get_value_as_int() * 1000000
        return ("! vader "
                + "name=vader "
                + "auto-threshold=false "
                + "threshold={:.9f} ".format(noise)
                + "run-length={:d} ".format(silence)
                )

    def _init_sensitivities(self):
        """Initialize widget sensitivities."""
        self.set_response_sensitive(Gtk.ResponseType.HELP, True)
        self.set_response_sensitive(Gtk.ResponseType.CANCEL, False)
        self.set_response_sensitive(Gtk.ResponseType.OK, False)
        self.set_response_sensitive(Gtk.ResponseType.CLOSE, True)

    def _init_values(self):
        """Initialize default values for widgets."""
        conf = gaupol.conf.speech_recognition
        self._noise_spin.set_value(conf.noise_level)
        self._silence_spin.set_value(conf.silence_length)
        self._advance_spin.set_value(conf.advance_length)
        self._default_model_check.set_active(not conf.use_custom_models)
        self._model_grid.set_sensitive(conf.use_custom_models)
        if os.path.isdir(conf.acoustic_model):
            self._acoustic_button.set_current_folder(conf.acoustic_model)
        if os.path.isfile(conf.phonetic_dict):
            self._dict_button.set_filename(conf.phonetic_dict)
        if os.path.isfile(conf.lang_model):
            self._lang_button.set_filename(conf.lang_model)

    def _append_subtitle(self, index):
        """Create subtitle from `index` and append to page."""
        if index < 0:
            index += len(self._starts)
        advance = gaupol.conf.speech_recognition.advance_length
        advance = aeidon.as_seconds(advance/1000) # ms to s
        subtitle = aeidon.Subtitle(mode=aeidon.modes.TIME)
        start = self._starts[index] - advance
        start = max(start, self._stops[index-1] if index > 0 else 0.0)
        subtitle.start = aeidon.as_seconds(start)
        subtitle.end = aeidon.as_seconds(self._stops[index])
        subtitle.main_text = self._texts[index] or ("[{:d}]".format(index+1))
        indices = (len(self._page.project.subtitles),)
        self._page.project.insert_subtitles(indices,
                                            (subtitle,),
                                            register=None)

    def _on_acoustic_button_current_folder_changed(self, file_button):
        """Save the acoustic model directory setting."""
        value = file_button.get_current_folder()
        if value is None: return
        gaupol.conf.speech_recognition.acoustic_model = value
        self._update_response_sensitivities()

    def _on_advance_spin_value_changed(self, spin_button):
        """Save advance length setting."""
        value = spin_button.get_value_as_int()
        gaupol.conf.speech_recognition.advance_length = value

    def _on_bus_message_application(self, bus, message):
        """Process application messages from the bus."""
        struct = message.get_structure()
        if struct.get_name() == "start":
            pos = message.get_value("pos")
            self._starts.append(pos)
            if self._text is not None:
                # Store previous text.
                self._texts[-1] = self._text
                self._text = None
            self._stops.append(None)
            self._texts.append(None)
            duration = self._pipeline.query_duration(Gst.Format.TIME)[1]
            duration = duration/1000000000 # ns to s
            fraction = pos/duration
            self._progressbar.set_fraction(fraction)
            if len(self._starts) > 1:
                # Append previous subtitle to page.
                self._append_subtitle(-2)
        if struct.get_name() == "stop":
            pos = message.get_value("pos")
            self._stops[-1] = pos
        if struct.get_name() == "text":
            text = message.get_value("text")
            if not isinstance(text, str):
                text = str(text, errors="replace")
            self._text = text

    def _on_bus_message_eos(self, bus, message):
        """Flush remaining subtitles to page."""
        if self._text is not None:
            # Store previous text.
            self._texts[-1] = self._text
            self._text = None
        self._progressbar.set_fraction(1)
        if self._starts and self._stops[-1] is not None:
            self._append_subtitle(-1)
        self._stop_speech_recognition()

    def _on_bus_message_error(self, bus, message):
        """Show an error dialog and abort speech recognition."""
        self._show_bus_message_error_dialog(message.parse_error())
        self._stop_speech_recognition()

    def _on_default_model_check_toggled(self, toggle_button):
        """Save default model usage setting."""
        value = toggle_button.get_active()
        gaupol.conf.speech_recognition.use_custom_models = not value
        self._model_grid.set_sensitive(not value)
        self._update_response_sensitivities()

    def _on_dict_button_file_set(self, file_button):
        """Save the phonetic dictionary file setting."""
        value = file_button.get_filename()
        if value is None: return
        gaupol.conf.speech_recognition.phonetic_dict = value
        self._update_response_sensitivities()

    def _on_lang_button_file_set(self, file_button):
        """Save the language model file setting."""
        value = file_button.get_filename()
        if value is None: return
        gaupol.conf.speech_recognition.lang_model = value
        self._update_response_sensitivities()

    def _on_noise_spin_value_changed(self, spin_button):
        """Save noise level setting."""
        value = spin_button.get_value_as_int()
        gaupol.conf.speech_recognition.noise_level = value

    def _on_pocketsphinx_result(self, sphinx, text, uttid):
        """Send recognized text as a message on the bus."""
        struct = Gst.Structure.new_empty("text")
        struct.set_value("text", text)
        struct.set_value("uttid", uttid)
        message = Gst.Message.new_application(sphinx, struct)
        sphinx.post_message(message)

    def _on_response(self, dialog, response):
        """Handle responses without destroying dialog."""
        if response == Gtk.ResponseType.HELP:
            gaupol.util.show_uri(gaupol.SPEECH_RECOGNITION_HELP_URL)
            self.stop_emission("response")
        if response == Gtk.ResponseType.CANCEL:
            self._stop_speech_recognition()
            self.stop_emission("response")
        if response == Gtk.ResponseType.OK:
            self._recognize_speech()
            self.stop_emission("response")

    def _on_revert_button_clicked(self, *args):
        """Revert voice recognition parameters to their defaults."""
        query = lambda x: gaupol.conf.query_default("speech_recognition", x)
        self._noise_spin.set_value(query("noise_level"))
        self._silence_spin.set_value(query("silence_length"))
        self._advance_spin.set_value(query("advance_length"))

    def _on_silence_spin_value_changed(self, spin_button):
        """Save silence length setting."""
        value = spin_button.get_value_as_int()
        gaupol.conf.speech_recognition.silence_length = value

    def _on_vader_start(self, vader, pos):
        """Send start position as a message on the bus."""
        struct = Gst.Structure.new_empty("start")
        pos = pos/1000000000 # ns to s
        struct.set_value("pos", pos)
        message = Gst.Message.new_application(vader, struct)
        vader.post_message(message)

    def _on_vader_stop(self, vader, pos):
        """Send stop position as a message on the bus."""
        struct = Gst.Structure.new_empty("stop")
        pos = pos/1000000000 # ns to s
        struct.set_value("pos", pos)
        message = Gst.Message.new_application(vader, struct)
        vader.post_message(message)

    def _on_video_button_file_set(self, file_button):
        """Update response sensitivities."""
        self._update_response_sensitivities()

    def _prepare_page(self):
        """Prepare page properties for speech recognition."""
        if self._page is None:
            self._page = gaupol.Page(next(self.application.counter))
            self.application.add_page(self._page)
        video_path = self._video_button.get_filename()
        self._page.project.video_path = video_path
        # Set project's main_file attribute to a SubRip file so that
        # previewing is possible wihtout a need to save the file. Set
        # the path to VIDEO.#.srt, so that the file can be easily saved
        # to the same directory, but without risk of overwriting anything.
        base = video_path[:video_path.rfind(".")]
        for i in itertools.count(1):
            path = "{}.{:d}.srt".format(base, i)
            if not os.path.isfile(path): break
        file = aeidon.files.new(aeidon.formats.SUBRIP, path, "utf_8")
        self._page.project.main_file = file
        self._page.project.main_changed = 1
        if self._page.project.subtitles:
            indices = list(range(len(self._page.project.subtitles)))
            self._page.project.remove_subtitles(indices, register=None)

    def _recognize_speech(self):
        """Generate subtitles from video or audio file."""
        self._set_sensitivities_start()
        self._progressbar.set_fraction(0)
        self._clear_attributes()
        self._pipeline = Gst.parse_launch(self._get_pipeline_definition())
        vader = self._pipeline.get_by_name("vader")
        vader.connect("vader-start", self._on_vader_start)
        vader.connect("vader-stop", self._on_vader_stop)
        sphinx = self._pipeline.get_by_name("pocketsphinx")
        sphinx.connect("result", self._on_pocketsphinx_result)
        sphinx.set_property("configured", True)
        bus = self._pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message::application", self._on_bus_message_application)
        bus.connect("message::eos", self._on_bus_message_eos)
        bus.connect("message::error", self._on_bus_message_error)
        self._prepare_page()
        self._pipeline.set_state(Gst.State.PLAYING)

    def _set_sensitivities_start(self):
        """Set widget sensitivies for speech recognition start."""
        self._options_vbox.set_sensitive(False)
        self.set_response_sensitive(Gtk.ResponseType.HELP, False)
        self.set_response_sensitive(Gtk.ResponseType.CANCEL, True)
        self.set_response_sensitive(Gtk.ResponseType.OK, False)
        self.set_response_sensitive(Gtk.ResponseType.CLOSE, False)

    def _set_sensitivities_stop(self):
        """Set widget sensitivies for speech recognition start."""
        self._options_vbox.set_sensitive(True)
        self.set_response_sensitive(Gtk.ResponseType.HELP, True)
        self.set_response_sensitive(Gtk.ResponseType.CANCEL, False)
        self.set_response_sensitive(Gtk.ResponseType.OK, True)
        self.set_response_sensitive(Gtk.ResponseType.CLOSE, True)

    def _show_bus_message_error_dialog(self, message):
        """Show an error dialog after failing to decode file."""
        title = _("Something went wrong")
        dialog = gaupol.ErrorDialog(self, title, message)
        dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _stop_speech_recognition(self):
        """Stop generating subtitles from video or audio file."""
        self._pipeline.set_state(Gst.State.NULL)
        self._set_sensitivities_stop()

    def _update_response_sensitivities(self):
        """Update dialog response sensitivities."""
        sensitive = self._video_button.get_filename() is not None
        if not self._default_model_check.get_active():
            sensitive = (sensitive and
                         self._acoustic_button.get_current_folder() is not None
                         and self._dict_button.get_filename() is not None
                         and self._lang_button.get_filename() is not None)

        self.set_response_sensitive(Gtk.ResponseType.OK, sensitive)
