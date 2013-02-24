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

"""Video actions for :class:`gaupol.Application`."""

import aeidon
import gaupol
_ = aeidon.i18n._

from gi.repository import Gtk


class LoadVideoAction(gaupol.Action):

    """Load a video file."""

    def __init__(self):
        """Initialize a :class:`LoadVideoAction` object."""
        gaupol.Action.__init__(self, "load_video")
        self.props.label = _("_Load Video…")
        self.props.tooltip = _("Load a video file")
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(gaupol.util.gst_available())
        aeidon.util.affirm(page is not None)


class PlayPauseAction(gaupol.Action):

    """Play or pause video."""

    def __init__(self):
        """Initialize a :class:`PlayPauseAction` object."""
        gaupol.Action.__init__(self, "play_pause")
        self.props.label = _("_Play/Pause")
        self.props.stock_id = Gtk.STOCK_MEDIA_PLAY
        self.props.tooltip = _("Play or pause video")
        self.accelerator = "P"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)


__all__ = tuple(x for x in dir() if x.endswith("Action"))
