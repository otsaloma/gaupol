# -*- coding: utf-8 -*-

# Copyright (C) 2012 Osmo Salomaa
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


class VideoPlayer(object):

    """
    GStreamer video player.

    :ivar _bus: The :class:`Gtk.Bus` used to receive messages
    :ivar _pipeline: The :class:`Gst.Pipeline` used
    :ivar _playbin: The GStreamer playbin element
    :ivar _xid: `widget`'s X resource (window)
    :ivar calc: The instance of :class:`aeidon.Calculator` used
    :ivar widget: :class:`Gtk.DrawingArea` used to render video
    """

    def __init__(self):
        """Initialize a :class:`VideoPlayer` object."""
        self._bus = None
        self._pipeline = None
        self._playbin = None
        self._xid = None
        self.calc = aeidon.Calculator()
        self.widget = None
        self._init_pipeline()
        self._init_bus()
        self._init_widget()

    def _init_bus(self):
        """Initialize the GStreamer message bus."""
        self._bus = self._pipeline.get_bus()
        self._bus.enable_sync_message_emission()
        self._bus.connect("sync-message::element", self._on_bus_sync_message)
        self._bus.add_signal_watch()
        self._bus.connect("message::eos", self._on_bus_message_eos)
        self._bus.connect("message::error", self._on_bus_message_error)

    def _init_pipeline(self):
        """Initialize the GStreamer playback pipeline."""
        self._pipeline = Gst.Pipeline()
        self._playbin = Gst.ElementFactory.make("playbin", name=None)
        self._pipeline.add(self._playbin)

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
        title = _("Video playback failed")
        dialog = gaupol.ErrorDialog(self, title, message.parse_error())
        dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _on_bus_sync_message(self, bus, message):
        """Handle sync messages from the bus."""
        struct = message.get_structure()
        if struct.get_name() == "prepare-window-handle":
            message.src.set_window_handle(self._xid)

    def get_duration(self, mode):
        """Return duration of video stream."""
        success, duration = self._pipeline.query_duration(Gst.Format.TIME)
        if not success: return duration
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
        """Return current position in video stream."""
        success, pos = self._pipeline.query_position(Gst.Format.TIME)
        if not success: return pos
        pos = pos / Gst.SECOND
        if mode == aeidon.modes.TIME:
            return self.calc.to_time(pos)
        if mode == aeidon.modes.FRAME:
            return self.calc.to_frame(pos)
        if mode == aeidon.modes.SECONDS:
            return self.calc.to_seconds(pos)
        raise ValueError("Invalid mode: {}"
                         .format(repr(mode)))

    def pause(self):
        """Pause."""
        self._pipeline.set_state(Gst.State.PAUSED)

    def play(self):
        """Play."""
        self._xid = self.widget.get_property("window").get_xid()
        self._pipeline.set_state(Gst.State.PLAYING)

    def play_segment(self, start, end):
        """Play from `start` to `end` (either time, frame or seconds."""
        seek_flags = Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT
        start = self.calc.to_seconds(start) * Gst.SECOND
        end = self.calc.to_seconds(end) * Gst.SECOND
        self._pipeline.seek(rate=1.0,
                            format=Gst.Format.TIME,
                            flags=seek_flags,
                            start_type=Gst.SeekType.SET,
                            start=start,
                            stop_type=Gst.SeekType.SET,
                            stop=end)

        self.play()

    def seek(self, pos):
        """Seek to position (either time, frame or seconds)."""
        seek_flags = Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT
        pos = self.calc.to_seconds(pos) * Gst.SECOND
        self._pipeline.seek_simple(Gst.Format.TIME, seek_flags, pos)

    def seek_relative(self, offset):
        """
        Seek to `offset` relative to current position.

        `offset` can be either time, frame or seconds.
        """
        success, pos = self._pipeline.query_position(Gst.Format.TIME)
        if not success: return
        pos = pos + (self.calc.to_seconds(offset) * Gst.SECOND)
        success, duration = self._pipeline.query_duration(Gst.Format.TIME)
        if not success: return
        pos = max(0, min(pos, duration))
        seek_flags = Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT
        self._pipeline.seek_simple(Gst.Format.TIME, seek_flags, pos)

    def set_path(self, path):
        """Set the path of the file to play."""
        self.set_uri(aeidon.util.path_to_uri(path))

    def set_uri(self, uri):
        """Set the URI of the file to play."""
        self._playbin.set_property("uri", uri)
        # Find out the exact framerate to be able
        # to convert between position types.
        discoverer = GstPbutils.Discoverer()
        info = discoverer.discover_uri(uri)
        stream = info.get_video_streams()[0]
        num = float(stream.get_framerate_num())
        denom = float(stream.get_framerate_denom())
        self.calc = aeidon.Calculator(num/denom)

    def stop(self):
        """Stop."""
        self._pipeline.set_state(Gst.State.NULL)
