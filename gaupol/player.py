# -*- coding: utf-8 -*-

# Copyright (C) 2012 Osmo Salomaa
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

"""GStreamer video player."""

import aeidon
import gaupol
import time

from collections import namedtuple
from aeidon.i18n   import _
from gi.repository import GLib
from gi.repository import Gtk

with aeidon.util.silent(Exception):
    from gi.repository import Gst

__all__ = ("VideoPlayer",)


class VideoPlayer(aeidon.Observable):

    """
    GStreamer video player.

    :ivar audio_track: Current audio track as integer
    :ivar calc: The instance of :class:`aeidon.Calculator` used
    :ivar _in_default_segment: ``True`` if in the default playback segment
    :ivar _info: :class:`Gst.DiscovererInfo` from current URI
    :ivar _playbin: GStreamer "playbin" element
    :ivar _prev_state: Previous state of `_playbin`
    :ivar ready: ``True`` if a file is loaded and ready to play
    :ivar subtitle_text: Current text shown in the subtitle overlay
    :ivar subtitle_text_raw: `subtitle_text` before removal of tags
    :ivar _text_overlay: GStreamer "textoverlay" element
    :ivar _time_overlay: GStreamer "timeoverlay" element
    :ivar volume: Current audio stream volume
    :ivar widget: :class:`Gtk.DrawingArea` used to render video

    Signals and their arguments for callback functions:
     * ``state-changed``: player new state
    """

    signals = ("state-changed",)

    TrackInfo = namedtuple("TrackInfo", ["title", "language_code", "language_name"])

    def __init__(self):
        """Initialize a :class:`VideoPlayer` instance."""
        aeidon.Observable.__init__(self)
        self.calc = aeidon.Calculator()
        self._in_default_segment = True
        self._info = None
        self._playbin = None
        self._prev_state = None
        self.ready = False
        self.subtitle_text_raw = ""
        self._text_overlay = None
        self._time_overlay = None
        self.widget = None
        self._init_widget()
        self._init_text_overlay()
        self._init_time_overlay()
        self._init_pipeline()
        self._init_bus()

    @property
    def audio_track(self):
        """Return number of the current audio track."""
        track = self._playbin.props.current_audio
        # If at the default value, the first track is used,
        # which is (probably?) zero.
        return 0 if track == -1 else track

    @audio_track.setter
    def audio_track(self, track):
        """Set the current audio track."""
        self._playbin.props.current_audio = track

    def _ensure_default_segment(self):
        """
        Reset playback start and stop positions.

        When using `play_segment`, the playback limits are set to those
        (instead of the default 0 and -1). To be able to do useful things,
        we often need to reset those segment limits to their defaults.
        Any methods that need to rely on the whole duration being
        accessible, should as first thing call this method.
        """
        if self._in_default_segment: return
        # XXX: There's got to be a simpler way to do this.
        seek_flags = Gst.SeekFlags.FLUSH | Gst.SeekFlags.ACCURATE
        pos = self.get_position(aeidon.modes.SECONDS) * Gst.SECOND
        end = self.get_duration(aeidon.modes.SECONDS) * Gst.SECOND
        if pos is None: return
        if end is None: return
        self._playbin.seek(rate=1.0,
                           format=Gst.Format.TIME,
                           flags=seek_flags,
                           start_type=Gst.SeekType.SET,
                           start=0,
                           stop_type=Gst.SeekType.SET,
                           stop=end)

        self._playbin.seek_simple(Gst.Format.TIME, seek_flags, pos)
        self._in_default_segment = True

    def get_audio_infos(self):
        """Return a sequence of audio track infos."""
        return tuple(
            self._make_track_infos(self._playbin.emit("get-audio-tags", i))
            for i in range(self._playbin.props.n_audio)
        )

    def _make_track_infos(self, tags):
        return self.TrackInfo(
            tags.get_string("title")[1],
            tags.get_string("language-code")[1],
            tags.get_string("language-name")[1]
        )

    def get_duration(self, mode=None):
        """Return duration of video stream or ``None``."""
        q = self._playbin.query_duration
        for i in range(100):
            # Querying duration sometimes fails very unreproducibly,
            # likely due to a particular pipeline state or state change.
            # Try repeated times, hoping to pass the bad state.
            success, duration = q(Gst.Format.TIME)
            if success: break
            time.sleep(1/100)
        if not success: return None
        if mode is None: return duration
        duration = duration / Gst.SECOND
        if mode == aeidon.modes.SECONDS:
            return duration
        if mode == aeidon.modes.TIME:
            return self.calc.to_time(duration)
        if mode == aeidon.modes.FRAME:
            return self.calc.to_frame(duration)
        raise ValueError("Invalid mode: {!r}".format(mode))

    def get_position(self, mode=None):
        """Return current position in video stream or ``None``."""
        q = self._playbin.query_position
        for i in range(100):
            # Querying position sometimes fails very unreproducibly,
            # likely due to a particular pipeline state or state change.
            # Try repeated times, hoping to pass the bad state.
            success, pos = q(Gst.Format.TIME)
            if success: break
            time.sleep(1/100)
        if not success: return None
        if mode is None: return pos
        pos = pos / Gst.SECOND
        if mode == aeidon.modes.SECONDS:
            return pos
        if mode == aeidon.modes.TIME:
            return self.calc.to_time(pos)
        if mode == aeidon.modes.FRAME:
            return self.calc.to_frame(pos)
        raise ValueError("Invalid mode: {!r}".format(mode))

    def _init_bus(self):
        """Initialize the GStreamer message bus."""
        bus = self._playbin.get_bus()
        bus.add_signal_watch()
        bus.connect("message::eos", self._on_bus_message_eos)
        bus.connect("message::error", self._on_bus_message_error)
        bus.connect("message::state-changed", self._on_bus_message_state_changed)

    def _init_pipeline(self):
        """Initialize the GStreamer playback pipeline."""
        self._playbin = Gst.ElementFactory.make("playbin", None)
        if gaupol.conf.video_player.volume is not None:
            self.volume = gaupol.conf.video_player.volume
        sink = Gst.ElementFactory.make("gtksink", None)
        self.widget.pack_start(sink.props.widget, True, True, 0)
        bin = Gst.Bin()
        bin.add(self._time_overlay)
        bin.add(self._text_overlay)
        pad = self._time_overlay.get_static_pad("video_sink")
        bin.add_pad(Gst.GhostPad.new("sink", pad))
        bin.add(sink)
        self._time_overlay.link(self._text_overlay)
        self._text_overlay.link(sink)
        self._playbin.props.video_sink = bin
        # We need to disable playbin's own subtitle rendering, since we don't
        # want embedded subtitles to be displayed, but rather what we
        # explicitly set to our own overlays. Since Gst.PlayFlags is not
        # available via introspection, we need to use Gst.util_set_object_arg.
        # Playbin's default values can be found via 'gst-inspect-1.0 playbin'.
        Gst.util_set_object_arg(self._playbin,
                                "flags",
                                "+".join(("soft-colorbalance",
                                          "deinterlace",
                                          "soft-volume",
                                          "audio",
                                          "video")))

    def _init_text_overlay(self):
        """Initialize the text overlay element."""
        self._text_overlay = Gst.ElementFactory.make("textoverlay", None)
        conf = gaupol.conf.video_player
        callback = self._on_conf_notify_subtitle_property
        conf.connect("notify::subtitle_font", callback)
        conf.connect("notify::subtitle_color", callback)
        conf.connect("notify::subtitle_alpha", callback)
        conf.connect("notify::subtitle_background", callback)
        self._on_conf_notify_subtitle_property()

    def _init_time_overlay(self):
        """Initialize the time overlay element."""
        self._time_overlay = Gst.ElementFactory.make("timeoverlay", None)
        conf = gaupol.conf.video_player
        callback = self._on_conf_notify_time_property
        conf.connect("notify::time_font", callback)
        conf.connect("notify::time_color", callback)
        conf.connect("notify::time_alpha", callback)
        conf.connect("notify::time_background", callback)
        self._on_conf_notify_time_property()

    def _init_widget(self):
        """Initialize the rendering widget."""
        self.widget = Gtk.Box()
        style = self.widget.get_style_context()
        style.add_class("gaupol-video-background")
        gaupol.style.load_css(self.widget)

    def is_playing(self):
        """Return ``True`` if playing video."""
        # GStreamer's state information is far too detailed for our purposes.
        # Let's consider the state to be playing also if undergoing a state
        # change and/or having a pending playing state.
        success, current, pending = self._playbin.get_state(timeout=1)
        return (success == Gst.StateChangeReturn.ASYNC or
                current == Gst.State.PLAYING or
                pending == Gst.State.PLAYING)

    def _on_bus_message_eos(self, bus, message):
        """Handle EOS message from the bus."""
        self._ensure_default_segment()
        self.pause()

    def _on_bus_message_error(self, bus, message):
        """Handle error message from the bus."""
        title, message = message.parse_error()
        dialog = gaupol.ErrorDialog(None, title, message)
        dialog.add_button(_("_OK"), Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _on_bus_message_state_changed(self, bus, message):
        """Emit signal if state changed in a relevant manner."""
        old, new, pending = message.parse_state_changed()
        states = (Gst.State.NULL, Gst.State.PAUSED, Gst.State.PLAYING)
        if not new in states: return
        if new == self._prev_state: return
        self.emit("state-changed", new)
        self._prev_state = new

    def _on_conf_notify_subtitle_property(self, *args):
        """Update subtitle text overlay properties."""
        conf = gaupol.conf.video_player
        self._text_overlay.props.font_desc = conf.subtitle_font
        self._text_overlay.props.halignment = "center"
        self._text_overlay.props.valignment = "bottom"
        self._text_overlay.props.line_alignment = conf.line_alignment
        self._text_overlay.props.shaded_background = conf.subtitle_background
        alpha = "{:02x}".format(int(conf.subtitle_alpha * 255))
        color = conf.subtitle_color.replace("#", "")
        color = int(float.fromhex("".join((alpha, color))))
        self._text_overlay.props.color = color

    def _on_conf_notify_time_property(self, *args):
        """Update time overlay properties."""
        conf = gaupol.conf.video_player
        self._time_overlay.props.font_desc = conf.time_font
        self._time_overlay.props.halignment = "right"
        self._time_overlay.props.valignment = "top"
        self._time_overlay.props.shaded_background = conf.time_background
        alpha = "{:02x}".format(int(conf.time_alpha * 255))
        color = conf.time_color.replace("#", "")
        color = int(float.fromhex("".join((alpha, color))))
        self._time_overlay.props.color = color

    def pause(self):
        """Pause."""
        self._playbin.set_state(Gst.State.PAUSED)

    def play(self):
        """Play."""
        self._playbin.set_state(Gst.State.PLAYING)

    def play_segment(self, start, end):
        """Play from `start` to `end`."""
        self._in_default_segment = False
        seek_flags = Gst.SeekFlags.FLUSH | Gst.SeekFlags.ACCURATE
        start = max(0, self.calc.to_seconds(start)) * Gst.SECOND
        duration = self.get_duration(aeidon.modes.SECONDS)
        if duration is None: return
        end = min(duration, self.calc.to_seconds(end)) * Gst.SECOND
        self._playbin.seek(rate=1.0,
                           format=Gst.Format.TIME,
                           flags=seek_flags,
                           start_type=Gst.SeekType.SET,
                           start=start,
                           stop_type=Gst.SeekType.SET,
                           stop=end)

        self.play()

    def seek(self, pos):
        """Seek to `pos`."""
        self._ensure_default_segment()
        seek_flags = Gst.SeekFlags.FLUSH | Gst.SeekFlags.ACCURATE
        pos = self.calc.to_seconds(pos) * Gst.SECOND
        self._playbin.seek_simple(Gst.Format.TIME, seek_flags, pos)

    def seek_relative(self, offset):
        """Seek to `offset` relative to current position."""
        self._ensure_default_segment()
        pos = self.get_position(aeidon.modes.SECONDS)
        duration = self.get_duration(aeidon.modes.SECONDS)
        if pos is None or duration is None: return
        pos = pos + self.calc.to_seconds(offset)
        pos = max(0, min(pos, duration))
        pos = pos * Gst.SECOND
        seek_flags = Gst.SeekFlags.FLUSH | Gst.SeekFlags.ACCURATE
        self._playbin.seek_simple(Gst.Format.TIME, seek_flags, pos)

    def set_path(self, path):
        """Set the path of the file to play."""
        self.set_uri(aeidon.util.path_to_uri(path))

    def set_uri(self, uri):
        """Set the URI of the file to play."""
        self.ready = False
        self._playbin.props.uri = uri
        self.subtitle_text = ""
        try:
            # Find out the exact framerate to be able
            # to convert between position types.
            from gi.repository import GstPbutils
            discoverer = GstPbutils.Discoverer()
            self._info = discoverer.discover_uri(uri)
            streams = self._info.get_stream_list()
            stream_types = [x.get_stream_type_nick() for x in streams]
            if "video" not in stream_types:
                raise Exception(_("No video streams found"))
            stream = self._info.get_video_streams()[0]
            num = float(stream.get_framerate_num())
            denom = float(stream.get_framerate_denom())
            self.calc = aeidon.Calculator(num/denom)
            self.ready = True
        except Exception as error:
            title = _("Failed to initialize playback")
            dialog = gaupol.ErrorDialog(None, title, str(error))
            dialog.add_button(_("_OK"), Gtk.ResponseType.OK)
            dialog.set_default_response(Gtk.ResponseType.OK)
            gaupol.util.flash_dialog(dialog)
        else:
            # Make stream tags available from _playbin
            self._playbin.set_state(Gst.State.PAUSED)
            self._playbin.get_state(Gst.CLOCK_TIME_NONE)

    def stop(self):
        """Stop."""
        self._playbin.set_state(Gst.State.NULL)
        self.subtitle_text = ""

    @property
    def subtitle_text(self):
        """Return text shown in the subtitle overlay."""
        return self._text_overlay.props.text

    @subtitle_text.setter
    def subtitle_text(self, text):
        """Set `text` to the subtitle overlay."""
        self.subtitle_text_raw = text
        text = aeidon.RE_ANY_TAG.sub("", text)
        text = GLib.markup_escape_text(text)
        self._text_overlay.props.text = text

    @property
    def volume(self):
        """Return the current volume, in range [0,1]."""
        return self._playbin.props.volume

    @volume.setter
    def volume(self, volume):
        """Set the volume to use, in range [0,1]."""
        volume = round(max(0, min(1, volume)), 2)
        if abs(volume - self.volume) < 0.001: return
        self._playbin.props.volume = volume
        gaupol.conf.video_player.volume = volume
