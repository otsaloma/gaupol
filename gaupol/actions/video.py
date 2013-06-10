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
        self.accelerator = "<Control>L"
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


class PlaySelectionAction(gaupol.Action):

    """Play the selected subtitles."""

    def __init__(self):
        """Initialize a :class:`PlaySelectionAction`."""
        gaupol.Action.__init__(self, "play_selection")
        self.props.label = _("Play _Selection")
        self.props.tooltip = _("Play the selected subtitles")
        self.accelerator = "O"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)
        aeidon.util.affirm(selected_rows)


class SeekBackwardAction(gaupol.Action):

    """Seek backward."""

    def __init__(self):
        """Initialize a :class:`SeekBackwardAction` object."""
        gaupol.Action.__init__(self, "seek_backward")
        self.props.label = _("Seek _Backward")
        self.props.stock_id = Gtk.STOCK_MEDIA_REWIND
        self.props.tooltip = _("Seek backward")
        self.accelerator = "<Shift><Ctrl>Left"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)


class SeekForwardAction(gaupol.Action):

    """Seek forward."""

    def __init__(self):
        """Initialize a :class:`SeekForwardAction` object."""
        gaupol.Action.__init__(self, "seek_forward")
        self.props.label = _("Seek _Forward")
        self.props.stock_id = Gtk.STOCK_MEDIA_FORWARD
        self.props.tooltip = _("Seek forward")
        self.accelerator = "<Shift><Ctrl>Right"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)


class SeekNextAction(gaupol.Action):

    """Seek to the start of the next subtitle."""

    def __init__(self):
        """Initialize a :class:`SeekNextAction` object."""
        gaupol.Action.__init__(self, "seek_next")
        self.props.label = _("Seek _Next")
        self.props.stock_id = Gtk.STOCK_MEDIA_NEXT
        self.props.tooltip = _("Seek to the start of the next subtitle")
        self.accelerator = "<Ctrl>Right"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)


class SeekPreviousAction(gaupol.Action):

    """Seek to the start of the previous subtitle."""

    def __init__(self):
        """Initialize a :class:`SeekPreviousAction` object."""
        gaupol.Action.__init__(self, "seek_previous")
        self.props.label = _("Seek _Previous")
        self.props.stock_id = Gtk.STOCK_MEDIA_PREVIOUS
        self.props.tooltip = _("Seek to the start of the previous subtitle")
        self.accelerator = "<Ctrl>Left"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)


class SeekSelectionEndAction(gaupol.Action):

    """Seek the end of selection."""

    def __init__(self):
        """Initialize a :class:`SeekSelectionEnd` object."""
        gaupol.Action.__init__(self, "seek_selection_end")
        self.props.label = _("See_k Selection End")
        self.props.tooltip = _("Seek the end of selection")
        self.accelerator = "<Ctrl>Down"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)
        aeidon.util.affirm(selected_rows)


class SeekSelectionStartAction(gaupol.Action):

    """Seek the start of selection."""

    def __init__(self):
        """Initialize a :class:`SeekSelectionStart` object."""
        gaupol.Action.__init__(self, "seek_selection_start")
        self.props.label = _("S_eek Selection Start")
        self.props.tooltip = _("Seek the start of selection")
        self.accelerator = "<Ctrl>Up"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)
        aeidon.util.affirm(selected_rows)


__all__ = tuple(x for x in dir() if x.endswith("Action"))
