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

"""Loading and interacting with video."""

import aeidon
import gaupol
import os
import sys

from aeidon.i18n   import _
from gi.repository import GLib
from gi.repository import Gtk

with aeidon.util.silent(Exception):
    from gi.repository import Gst
    from gi.repository import GstTag



class VideoAgent(aeidon.Delegate):

    """Loading and interacting with video."""

    def __init__(self, master):
        """Initialize an :class:`VideoAgent` instance."""
        aeidon.Delegate.__init__(self, master)
        # Maintain an up-to-date cache of subtitle positions in seconds and
        # subtitle texts in order to allow fast polled updates in video player.
        # This cache must be updated when page or subtitle data changes.
        self._cache = []
        self._update_handlers = []

    def _clear_subtitle_cache(self):
        """Clear subtitle position and text cache."""
        self._cache = []

    def _init_cache_updates(self):
        """Initialize cache updates on application signals."""
        self.connect("page-added",    self._update_subtitle_cache)
        self.connect("page-changed",  self._update_subtitle_cache)
        self.connect("page-closed",   self._update_subtitle_cache)
        self.connect("page-switched", self._update_subtitle_cache)

    def _init_player_toolbar(self):
        """Initialize the video player toolbar."""
        self.player_toolbar = Gtk.Toolbar()
        self.player_toolbar.set_style(Gtk.ToolbarStyle.ICONS)
        if sys.platform == "win32":
            self.player_toolbar.set_icon_size(Gtk.IconSize.MENU)
        # win.play-pause
        button = Gtk.ToolButton(
            label=_("_Play/Pause"), icon_name="media-playback-start")
        button.set_action_name("win.play-pause")
        button.set_tooltip_text(_("Play or pause video"))
        self.player_toolbar.insert(button, -1)
        self.player_toolbar.insert(Gtk.SeparatorToolItem(), -1)
        self.play_button = button
        # win.seek-previous
        button = Gtk.ToolButton(
            label=_("Seek _Previous"), icon_name="media-skip-backward")
        button.set_action_name("win.seek-previous")
        button.set_tooltip_text(_("Seek to the start of the previous subtitle"))
        self.player_toolbar.insert(button, -1)
        # win.seek-next
        button = Gtk.ToolButton(
            label=_("Seek _Next"), icon_name="media-skip-forward")
        button.set_action_name("win.seek-next")
        button.set_tooltip_text(_("Seek to the start of the next subtitle"))
        self.player_toolbar.insert(button, -1)
        self.player_toolbar.insert(Gtk.SeparatorToolItem(), -1)
        # win.seek-backward
        button = Gtk.ToolButton(
            label=_("Seek _Backward"), icon_name="media-seek-backward")
        button.set_action_name("win.seek-backward")
        button.set_tooltip_text(_("Seek backward"))
        self.player_toolbar.insert(button, -1)
        # win.seek-forward
        button = Gtk.ToolButton(
            label=_("Seek _Forward"), icon_name="media-seek-forward")
        button.set_action_name("win.seek-forward")
        button.set_tooltip_text(_("Seek forward"))
        self.player_toolbar.insert(button, -1)
        self.player_toolbar.insert(Gtk.SeparatorToolItem(), -1)
        # Volume button
        self.volume_button = Gtk.VolumeButton()
        self.volume_button.props.use_symbolic = False
        adjustment = self.volume_button.get_adjustment()
        adjustment.set_lower(0)
        adjustment.set_upper(1)
        adjustment.set_value(self.player.volume)
        aeidon.util.connect(self, "volume_button", "value-changed")
        item = Gtk.ToolItem()
        item.add(self.volume_button)
        item.set_tooltip_text(_("Volume"))
        self.player_toolbar.insert(item, -1)
        # Seekbar
        self.seekbar = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL,
            adjustment=Gtk.Adjustment(value=0,
                                      lower=0,
                                      upper=1,
                                      step_increment=0.01,
                                      page_increment=0.05,
                                      page_size=0.05))

        self.seekbar.set_draw_value(False)
        self.seekbar.connect("change-value", self._on_seekbar_change_value)
        item = Gtk.ToolItem()
        item.set_expand(True)
        item.add(self.seekbar)
        self.player_toolbar.insert(item, -1)

    def _init_player_widgets(self):
        """Initialize the video player and related widgets."""
        vbox = gaupol.util.new_vbox(spacing=0)
        self.player = gaupol.VideoPlayer()
        aeidon.util.connect(self, "player", "state-changed")
        gaupol.util.pack_start_expand(vbox, self.player.widget)
        self._init_player_toolbar()
        gaupol.util.pack_start_fill(vbox, self.player_toolbar)
        gaupol.util.pack_start_expand(self.player_box, vbox)
        self.player_box.show_all()
        self.paned.add1(self.player_box)
        orientation = self.paned.get_orientation()
        size = (
            self.notebook.get_window().get_width()
            if orientation == Gtk.Orientation.HORIZONTAL
            else self.notebook.get_window().get_height())
        self.paned.set_position(int(size / 2))
        self.get_action("toggle-player").set_state(True)

    def _init_update_handlers(self):
        """Initialize timed updates of widgets."""
        while self._update_handlers:
            GLib.source_remove(self._update_handlers.pop())
        self._update_handlers = [
            GLib.timeout_add( 10, self._on_player_update_subtitle),
            GLib.timeout_add( 50, self._on_player_update_seekbar),
            GLib.timeout_add(100, self._on_player_update_volume),
        ]

    @aeidon.deco.export
    def load_video(self, path):
        """Load a video file."""
        page = self.get_current_page()
        page.project.video_path = path
        if self.player is None:
            self._init_player_widgets()
            self._init_cache_updates()
            self._init_update_handlers()
            self._update_subtitle_cache()
        else: # Player exists
            if self.player.is_playing():
                self.get_action("play-pause").activate()
            adjustment = self.seekbar.get_adjustment()
            adjustment.set_value(0)
            self.player.stop()
        self.player.set_path(path)
        # Playback initialization can fail, e.g. due to missing codecs,
        # in which case the player itself has shown an error dialog.
        if not self.player.ready: return
        self._update_languages_menu()
        self.update_gui()
        self.player.play()
        if not gaupol.conf.video_player.autoplay:
            self.player.pause()

    @aeidon.deco.export
    def _on_load_video_activate(self, *args):
        """Load a video file."""
        gaupol.util.set_cursor_busy(self.window)
        page = self.get_current_page()
        dialog = gaupol.VideoDialog(
            self.window, title=_("Load Video"), button_label=_("_Load"))
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
        self.load_video(path)

    @aeidon.deco.export
    def _on_play_pause_activate(self, *args):
        """Play or pause video."""
        if self.player.is_playing():
            self.player.pause()
        else: # Not playing.
            self.player.play()

    @aeidon.deco.export
    def _on_play_selection_activate(self, *args):
        """Play the selected subtitles."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        offset = gaupol.conf.video_player.context_length
        start = page.project.subtitles[rows[0]].start_seconds - offset
        end = page.project.subtitles[rows[-1]].end_seconds + offset
        self.player.play_segment(start, end)

    def _on_player_state_changed(self, player, state):
        """Update UI to match `state` of `player`."""
        self.play_button.set_icon_name(
            "media-playback-pause"
            if state == Gst.State.PLAYING
            else "media-playback-start")

    def _on_player_update_seekbar(self, data=None):
        """Update seekbar from video position."""
        if not self.player.ready:
            return True # to be called again.
        duration = self.player.get_duration(mode=None)
        position = self.player.get_position(mode=None)
        if duration is not None and position is not None:
            adjustment = self.seekbar.get_adjustment()
            adjustment.set_value(position/duration)
        return True # to be called again.

    def _on_player_update_subtitle(self, data=None):
        """Update subtitle overlay from video position."""
        if not self.player.ready:
            return True # to be called again.
        pos = self.player.get_position(aeidon.modes.SECONDS)
        if pos is None:
            return True # to be called again.
        subtitles = list(filter(lambda x: x[0] <= pos <= x[1], self._cache))
        if subtitles:
            text = subtitles[-1][2]
            if text != self.player.subtitle_text_raw:
                self.player.subtitle_text = text
        else:
            if self.player.subtitle_text:
                self.player.subtitle_text = ""
        return True # to be called again.

    def _on_player_update_volume(self, data=None):
        """Update volume from player."""
        if not self.player.ready:
            return True # to be called again.
        self.volume_button.set_value(self.player.volume)
        return True # to be called again.

    @aeidon.deco.export
    def _on_seek_backward_activate(self, *args):
        """Seek backward."""
        pos = self.player.get_position(aeidon.modes.SECONDS)
        if pos is None: return
        pos = pos - gaupol.conf.video_player.seek_length
        pos = max(pos, 0)
        self.player.seek(pos)

    @aeidon.deco.export
    def _on_seek_forward_activate(self, *args):
        """Seek forward."""
        position = self.player.get_position(aeidon.modes.SECONDS)
        duration = self.player.get_duration(aeidon.modes.SECONDS)
        if position is None: return
        if duration is None: return
        position = position + gaupol.conf.video_player.seek_length
        position = min(position, duration)
        self.player.seek(position)

    @aeidon.deco.export
    def _on_seek_next_activate(self, *args):
        """Seek to the start of the next subtitle."""
        pos = self.player.get_position(aeidon.modes.SECONDS)
        if pos is None: return
        subtitles = list(filter(lambda x: x[0] > pos + 0.001, self._cache))
        if not subtitles: return
        self.player.seek(subtitles[0][0])

    @aeidon.deco.export
    def _on_seek_previous_activate(self, *args):
        """Seek to the start of the previous subtitle."""
        pos = self.player.get_position(aeidon.modes.SECONDS)
        if pos is None: return
        subtitles = list(filter(lambda x: x[1] < pos - 0.001, self._cache))
        if not subtitles: return
        self.player.seek(subtitles[-1][0])

    @aeidon.deco.export
    def _on_seek_selection_end_activate(self, *args):
        """Seek to the end of selection."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        pos = page.project.subtitles[rows[-1]].end_seconds
        offset = gaupol.conf.video_player.context_length
        self.player.seek(max(pos - offset, 0))

    @aeidon.deco.export
    def _on_seek_selection_start_activate(self, *args):
        """Seek to the start of selection."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        pos = page.project.subtitles[rows[0]].start_seconds
        offset = gaupol.conf.video_player.context_length
        self.player.seek(max(pos - offset, 0))

    def _on_seekbar_change_value(self, seekbar, scroll, value, data=None):
        """Seek to specified position in video."""
        self.player.subtitle_text = ""
        duration = self.player.get_duration(aeidon.modes.SECONDS)
        if duration is None: return
        self.player.seek(value * duration)

    @aeidon.deco.export
    def _on_set_audio_language_activate(self, action, parameter):
        """Set the audio language to use."""
        # Avoid freeze by pausing prior and playing after.
        # https://github.com/otsaloma/gaupol/issues/58
        self.player.pause()
        index = int(parameter.get_string())
        self.player.audio_track = index
        self._update_languages_menu()
        self.player.play()

    def _on_volume_button_value_changed(self, button, value):
        """Update video player volume."""
        self.player.volume = value
        self.update_gui()

    @aeidon.deco.export
    def _on_volume_down_activate(self, *args):
        """Decrease volume."""
        self.player.volume = self.player.volume - 0.05
        self.volume_button.set_value(self.player.volume)
        self.update_gui()

    @aeidon.deco.export
    def _on_volume_up_activate(self, *args):
        """Increase volume."""
        self.player.volume = self.player.volume + 0.05
        self.volume_button.set_value(self.player.volume)
        self.update_gui()

    def _update_languages_menu(self):
        """Update the audio language selection menu."""
        menu = self.get_menubar_section("audio-languages-placeholder")
        menu.remove_all()
        tracks = self.player.get_audio_infos()
        for i, track in enumerate(tracks):
            title = track.title or _("Track {:d}").format(i + 1)
            lang = None
            if track.language_code is not None:
                lang = GstTag.tag_get_language_name(track.language_code)
            if lang is None:
                lang = track.language_name
            name = title if lang is None else "{} - [{}]".format(title, lang.title())
            action = "win.set-audio-language::{:d}".format(i)
            menu.append(name, action)
            if i == self.player.audio_track:
                action = self.get_action("set-audio-language")
                action.set_state(str(i))

    def _update_subtitle_cache(self, *args, **kwargs):
        """Update subtitle position and text cache."""
        page = self.get_current_page()
        if self.player is None or page is None:
            return self._clear_subtitle_cache()
        self._cache = [(x.start_seconds, x.end_seconds, x.main_text)
                       for x in page.project.subtitles]
