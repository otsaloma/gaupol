# -*- coding: utf-8 -*-

# Copyright (C) 2012-2013 Osmo Salomaa
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

"""GStreamer video player."""

import aeidon
import gaupol
_ = aeidon.i18n._

from gi.repository import Gdk
from gi.repository import GdkX11
from gi.repository import Gtk

try:
    from gi.repository import Gst
    from gi.repository import GstPbutils
    from gi.repository import GstVideo
except Exception:
    pass

__all__ = ("VideoPlayer",)


class VideoPlayer(aeidon.Observable):

    """
    GStreamer video player.

    :ivar _info: :class:`Gst.DiscovererInfo` from current uri
    :ivar _playbin: GStreamer "playbin" element
    :ivar _prev_state: Previous state of `_playbin`
    :ivar _text_overlay: GStreamer "textoverlay" element
    :ivar _time_overlay: GStreamer "timeoverlay" element
    :ivar _xid: `widget`'s X resource (window)
    :ivar audio_track: Current audio track as integer
    :ivar calc: The instance of :class:`aeidon.Calculator` used
    :ivar subtitle_text: Current text shown in the subtitle overlay
    :ivar volume: Current audio stream volume
    :ivar widget: :class:`Gtk.DrawingArea` used to render video

    Signals and their arguments for callback functions:
     * ``state-changed``: player new state
     * ``volume-changed``: player, volume
    """

    signals = ("state-changed", "volume-changed")

    def __init__(self):
        """Initialize a :class:`VideoPlayer` object."""
        aeidon.Observable.__init__(self)
        self._info = None
        self._playbin = None
        self._prev_state = None
        self._text_overlay = None
        self._time_overlay = None
        self._xid = None
        self.calc = aeidon.Calculator()
        self.widget = None
        self._init_text_overlay()
        self._init_time_overlay()
        self._init_pipeline()
        self._init_bus()
        self._init_widget()

    def _init_bus(self):
        """Initialize the GStreamer message bus."""
        bus = self._playbin.get_bus()
        bus.enable_sync_message_emission()
        bus.connect("sync-message::element", self._on_bus_sync_message)
        bus.add_signal_watch()
        bus.connect("message::eos", self._on_bus_message_eos)
        bus.connect("message::error", self._on_bus_message_error)
        bus.connect("message::state-changed",
                    self._on_bus_message_state_changed)

    def _init_pipeline(self):
        """Initialize the GStreamer playback pipeline."""
        self._playbin = Gst.ElementFactory.make("playbin", name=None)
        self._playbin.props.volume = gaupol.conf.video_player.volume
        sink = Gst.ElementFactory.make("autovideosink", name=None)
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
        # Playbin's default values can be found via 'gst-inspect playbin'.
        Gst.util_set_object_arg(self._playbin,
                                "flags",
                                "+".join(("soft-colorbalance",
                                          "deinterlace",
                                          "soft-volume",
                                          "audio",
                                          "video")))

    def _init_text_overlay(self):
        """Initialize the text overlay element."""
        conf = gaupol.conf.video_player
        text = Gst.ElementFactory.make("textoverlay", name=None)
        text.props.font_desc = conf.subtitle_font
        text.props.halignment = "center"
        text.props.valignment = "bottom"
        text.props.line_alignment = "left"
        text.props.shaded_background = conf.subtitle_background
        alpha = "{:02x}".format(int(conf.subtitle_alpha * 255))
        color = conf.subtitle_color.replace("#", "")
        text.props.color = eval("0x{}{}".format(alpha, color))
        self._text_overlay = text

    def _init_time_overlay(self):
        """Initialize the time overlay element."""
        conf = gaupol.conf.video_player
        time = Gst.ElementFactory.make("timeoverlay", name=None)
        time.props.font_desc = conf.time_font
        time.props.halignment = "right"
        time.props.valignment = "top"
        time.props.shaded_background = conf.time_background
        alpha = "{:02x}".format(int(conf.time_alpha * 255))
        color = conf.time_color.replace("#", "")
        time.props.color = eval("0x{}{}".format(alpha, color))
        self._time_overlay = time

    def _init_widget(self):
        """Initialize the rendering widget."""
        self.widget = Gtk.DrawingArea()
        color = Gdk.RGBA()
        success = color.parse("black")
        if not success: return
        state = Gtk.StateFlags.NORMAL
        self.widget.override_background_color(state, color)

    def _on_bus_message_eos(self, bus, message):
        """Handle EOS message from the bus."""
        self.pause()

    def _on_bus_message_error(self, bus, message):
        """Handle error message from the bus."""
        title, message = message.parse_error()
        dialog = gaupol.ErrorDialog(None, title, message)
        dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _on_bus_message_state_changed(self, bus, message):
        """Emit signal if state changed in a relevant manner."""
        old, new, pending = message.parse_state_changed()
        states = (Gst.State.NULL, Gst.State.PAUSED, Gst.State.PLAYING)
        if not new in states: return
        if new == self._prev_state: return
        self.emit("state-changed", new)
        self._prev_state = new

    def _on_bus_sync_message(self, bus, message):
        """Handle sync messages from the bus."""
        struct = message.get_structure()
        if struct.get_name() == "prepare-window-handle":
            message.src.set_window_handle(self._xid)

    @property
    def audio_track(self):
        """Return number of the current audio track."""
        track = self._playbin.props.current_audio
        # If at the default value, the first track is used,
        # which is (probably?) zero.
        track = (0 if track == -1 else track)
        return track

    @audio_track.setter
    def audio_track(self, track):
        """Set the current audio track."""
        self._playbin.props.current_audio = track

    def get_audio_languages(self):
        """Return a sequence of audio languages or ``None``."""
        if self._info is None: return None
        # TODO: Maybe we should try to parse these language codes to human
        # readable form, but the codes probably vary a lot by container.
        return tuple(x.get_language() for x in
                     self._info.get_audio_streams())

    def get_duration(self, mode):
        """Return duration of video stream or ``None``."""
        success, duration = self._playbin.query_duration(Gst.Format.TIME)
        if not success: return None
        duration = duration / Gst.SECOND
        if mode == aeidon.modes.TIME:
            return self.calc.to_time(duration)
        if mode == aeidon.modes.FRAME:
            return self.calc.to_frame(duration)
        if mode == aeidon.modes.SECONDS:
            return self.calc.to_seconds(duration)
        raise ValueError("Invalid mode: {}"
                         .format(repr(mode)))

    def get_position(self, mode):
        """Return current position in video stream or ``None``."""
        success, pos = self._playbin.query_position(Gst.Format.TIME)
        if not success: return None
        pos = pos / Gst.SECOND
        if mode == aeidon.modes.TIME:
            return self.calc.to_time(pos)
        if mode == aeidon.modes.FRAME:
            return self.calc.to_frame(pos)
        if mode == aeidon.modes.SECONDS:
            return self.calc.to_seconds(pos)
        raise ValueError("Invalid mode: {}"
                         .format(repr(mode)))

    def is_playing(self):
        """Return ``True`` if playing video."""
        # GStreamer's state information is far too detailed for our purposes.
        # Let's consider the state to be playing also if undergoing a state
        # change and/or having a pending playing state.
        success, current, pending = self._playbin.get_state(timeout=1)
        return (success == Gst.StateChangeReturn.ASYNC or
                current == Gst.State.PLAYING or
                pending == Gst.State.PLAYING)

    def pause(self):
        """Pause."""
        self._playbin.set_state(Gst.State.PAUSED)

    def play(self):
        """Play."""
        self._playbin.set_state(Gst.State.PLAYING)

    def play_segment(self, start, end):
        """
        Play from `start` to `end`.

        `start` and `end` can be either time, frame or seconds.
        """
        seek_flags = Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT
        start = self.calc.to_seconds(start) * Gst.SECOND
        end = self.calc.to_seconds(end) * Gst.SECOND
        self._playbin.seek(rate=1.0,
                           format=Gst.Format.TIME,
                           flags=seek_flags,
                           start_type=Gst.SeekType.SET,
                           start=start,
                           stop_type=Gst.SeekType.SET,
                           stop=end)

        self.play()

    def seek(self, pos):
        """
        Seek to `pos`.

        `pos` can be either time, frame or seconds.
        """
        seek_flags = Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT
        pos = self.calc.to_seconds(pos) * Gst.SECOND
        self._playbin.seek_simple(Gst.Format.TIME, seek_flags, pos)

    def seek_relative(self, offset):
        """
        Seek to `offset` relative to current position.

        `offset` can be either time, frame or seconds.
        """
        pos = self.get_position(aeidon.modes.SECONDS)
        duration = self.get_duration(aeidon.modes.SECONDS)
        if pos is None or duration is None: return
        pos = pos + self.calc.to_seconds(offset)
        pos = max(0, min(pos, duration))
        pos = pos * Gst.SECOND
        seek_flags = Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT
        self._playbin.seek_simple(Gst.Format.TIME, seek_flags, pos)

    def set_path(self, path):
        """Set the path of the file to play."""
        self.set_uri(aeidon.util.path_to_uri(path))

    def set_uri(self, uri):
        """Set the URI of the file to play."""
        self._playbin.props.uri = uri
        self._xid = self.widget.props.window.get_xid()
        self.subtitle_text= ""
        try:
            # Find out the exact framerate to be able
            # to convert between position types.
            discoverer = GstPbutils.Discoverer()
            self._info = discoverer.discover_uri(uri)
            stream = self._info.get_video_streams()[0]
            num = float(stream.get_framerate_num())
            denom = float(stream.get_framerate_denom())
            self.calc = aeidon.Calculator(num/denom)
        except Exception:
            # If any of this fails, playback probably fails
            # as well and we'll show an error dialog then.
            pass

    def stop(self):
        """Stop."""
        self._playbin.set_state(Gst.State.NULL)
        self.subtitle_text= ""

    @property
    def subtitle_text(self):
        """Return text shown in the subtitle overlay."""
        return self._text_overlay.props.text

    @subtitle_text.setter
    def subtitle_text(self, text):
        """Set `text` to the subtitle overlay."""
        self._text_overlay.props.text = text

    @property
    def volume(self):
        """Return the current volume, in range [0,1]."""
        return self._playbin.props.volume

    @volume.setter
    def volume(self, volume):
        """Set the volume to use, in range [0,1]."""
        volume = max(0, min(1, volume))
        if abs(volume - self.volume) < 0.001: return
        self._playbin.props.volume = volume
        gaupol.conf.video_player.volume = volume
        self.emit("volume-changed", volume)
