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

from gi.repository import Gtk


class VideoAgent(aeidon.Delegate):

    """Loading a video file and interacting with its content."""

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
        self.update_gui()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.player = gaupol.VideoPlayer()
        self.player.set_path(path)
        vbox.pack_start(self.player.widget,
                        expand=True,
                        fill=True,
                        padding=0)

        self.seekbar = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        self.seekbar.props.draw_value = False
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
        self.player.play()
