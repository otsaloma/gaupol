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

"""Loading a video file and interacting with its content."""

import aeidon
import gaupol
import os
_ = aeidon.i18n._

from gi.repository import GLib
from gi.repository import Gtk


class VideoAgent(aeidon.Delegate):

    """Loading a video file and interacting with its content."""

    def __init__(self, master):
        """Initialize an :class:`VideoAgent` object."""
        aeidon.Delegate.__init__(self, master)
        # Maintain an up-to-date cache of subtitle positions in seconds and
        # subtitle texts in order to allow fast polled updates in video player.
        # This cache must be updated when page or subtitle data changes.
        self._cache = []

    def _clear_subtitle_cache(self):
        """Clear subtitle position and text cache."""
        self._cache = []

    def _init_cache_updates(self):
        """Initialize cache updates on application signals."""
        self.connect("page-added",    self._update_subtitle_cache)
        self.connect("page-changed",  self._update_subtitle_cache)
        self.connect("page-closed",   self._update_subtitle_cache)
        self.connect("page-switched", self._update_subtitle_cache)

    def _init_player_widgets(self):
        """Initialize the video player and related widgets."""
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.player = gaupol.VideoPlayer()
        vbox.pack_start(self.player.widget,
                        expand=True,
                        fill=True,
                        padding=0)

        adjustment = Gtk.Adjustment(value=0,
                                    lower=0,
                                    upper=1,
                                    step_increment=0.01,
                                    page_increment=0.05,
                                    page_size=0.05)

        self.seekbar = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,
                                 adjustment=adjustment)

        self.seekbar.props.draw_value = False
        self.seekbar.connect("change-value", self._on_seekbar_change_value)
        vbox.pack_start(self.seekbar,
                        expand=False,
                        fill=True,
                        padding=0)

        self.player_toolbar = self.uim.get_widget("/ui/player_toolbar")
        self.player_toolbar.set_style(Gtk.ToolbarStyle.ICONS)
        vbox.pack_start(self.player_toolbar,
                        expand=False,
                        fill=True,
                        padding=0)

        self.player_box.pack_start(vbox,
                                   expand=True,
                                   fill=True,
                                   padding=0)

        self.player_box.show_all()
        self.paned.add1(self.player_box)
        orientation = self.paned.props.orientation
        if orientation == Gtk.Orientation.HORIZONTAL:
            size = self.notebook.props.window.get_width()
        if orientation == Gtk.Orientation.VERTICAL:
            size = self.notebook.props.window.get_height()
        self.paned.set_position(int(size/2))

    def _init_polled_updates(self, data=None):
        """Initialize seekbar and subtitle overlay updates."""
        if not self.player.is_playing():
            return True # to be called again.
        GLib.timeout_add(1000, self._on_player_update_seekbar)
        GLib.timeout_add(20, self._on_player_update_subtitle)
        return False # to not be called again.

    @aeidon.deco.export
    def _on_load_video_activate(self, *args):
        """Load a video file."""
        gaupol.util.set_cursor_busy(self.window)
        page = self.get_current_page()
        path = page.project.video_path
        dialog = gaupol.VideoDialog(self.window,
                                    title=_("Load Video"),
                                    button_label=_("_Load"))

        if page.project.main_file is not None:
            directory = os.path.dirname(page.project.main_file.path)
            dialog.set_current_folder(directory)
        if page.project.video_path is not None:
            dialog.set_filename(page.project.video_path)
        gaupol.util.set_cursor_normal(self.window)
        response = gaupol.util.run_dialog(dialog)
        path = dialog.get_filename()
        dialog.destroy()
        if response != Gtk.ResponseType.OK: return
        page.project.video_path = path
        if self.player is None:
            self._init_player_widgets()
            self._init_cache_updates()
            self._update_subtitle_cache()
        action = self.get_action("toggle_player")
        action.set_active = True
        self.player.set_path(path)
        self.update_gui()

    @aeidon.deco.export
    def _on_play_pause_activate(self, *args):
        """Play or pause video."""
        if self.player.is_playing():
            self.player.pause()
            action = self.get_action("play_pause")
            action.props.stock_id = Gtk.STOCK_MEDIA_PLAY
        else: # Not playing.
            self.player.play()
            action = self.get_action("play_pause")
            action.props.stock_id = Gtk.STOCK_MEDIA_PAUSE
            # Even though we have called self.player.play, the state of the
            # player changes to 'playing' with a slight delay. Hence, let's
            # initialize polled updates of the seekbar and the subtitle overlay
            # as soon as that state change has happened.
            GLib.timeout_add(20, self._init_polled_updates)

    def _on_player_update_seekbar_require(self, data=None):
        assert self.player is not None
        assert self.player.is_playing()

    def _on_player_update_seekbar(self, data=None):
        """Update seekbar from video position."""
        duration = self.player.get_duration(aeidon.modes.SECONDS)
        position = self.player.get_position(aeidon.modes.SECONDS)
        adjustment = self.seekbar.get_adjustment()
        adjustment.set_value(position/duration)
        # Continue repeated calls until paused.
        return self.player.is_playing()

    def _on_player_update_subtitle(self, data=None):
        """Update subtitle overlay from video position."""
        position = self.player.get_position(aeidon.modes.SECONDS)
        subtitle = list(filter(lambda x: x[0] <= position <= x[1],
                               self._cache))

        if subtitle:
            text = aeidon.RE_ANY_TAG.sub("", subtitle[0][2])
            if text != self.player.get_subtitle_text():
                self.player.set_subtitle_text(text)
        else:
            if self.player.get_subtitle_text():
                self.player.set_subtitle_text("")
        # Continue repeated calls until paused.
        return self.player.is_playing()

    def _on_seekbar_change_value(self, seekbar, scroll, value, data=None):
        """Seek to specified position in video."""
        self.player.set_subtitle_text("")
        duration = self.player.get_duration(aeidon.modes.SECONDS)
        self.player.seek(value * duration)

    def _update_subtitle_cache(self, *args, **kwargs):
        """Update subtitle position and text cache."""
        page = self.get_current_page()
        if self.player is None or page is None:
            return self._clear_subtitle_cache()
        self._cache = [(x.start_seconds, x.end_seconds, x.main_text)
                       for x in page.project.subtitles]
