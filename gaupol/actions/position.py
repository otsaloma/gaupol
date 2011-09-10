# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

"""Time and frame editing actions for :class:`gaupol.Application`."""

import aeidon
import gaupol
from gi.repository import Gtk
_ = aeidon.i18n._


class AdjustDurationsAction(gaupol.Action):

    """Lengthen or shorten durations."""

    def __init__(self):
        """Initialize an :class:`AdjustDurationsAction` object."""
        gaupol.Action.__init__(self, "adjust_durations")
        self.props.label = _("Adjust _Durations\342\200\246")
        self.props.tooltip = _("Lengthen or shorten durations")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class ConvertFramerateAction(gaupol.Action):

    """Change positions for a different framerate."""

    def __init__(self):
        """Initialize a :class:`ConvertFramerateAction` object."""
        gaupol.Action.__init__(self, "convert_framerate")
        self.props.label = _("Convert _Framerate\342\200\246")
        self.props.tooltip = _("Change positions for a different framerate")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class PreviewAction(gaupol.Action):

    """Preview from selected position with a video player."""

    def __init__(self):
        """Initialize a :class:`PreviewAction` object."""
        gaupol.Action.__init__(self, "preview")
        self.props.label = _("_Preview")
        self.props.stock_id = Gtk.STOCK_MEDIA_PLAY
        self.props.tooltip = _("Preview from selected position "
                               "with a video player")

        self.accelerator = "P"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.video_path is not None)
        if gaupol.conf.preview.use_custom_command:
            aeidon.util.affirm(gaupol.conf.preview.custom_command)
        col = page.view.get_focus()[1]
        if col == page.view.columns.TRAN_TEXT:
            aeidon.util.affirm(page.project.tran_file is not None)
        else: # Any other column previews the main file.
            aeidon.util.affirm(page.project.main_file is not None)


class ShiftPositionsAction(gaupol.Action):

    """Make subtitles appear earlier or later."""

    def __init__(self):
        """Initialize a :class:`ShiftPositionsAction` object."""
        gaupol.Action.__init__(self, "shift_positions")
        self.props.label = _("_Shift Positions\342\200\246")
        self.props.tooltip = _("Make subtitles appear earlier or later")
        self.accelerator = "H"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class SpeechRecognitionAction(gaupol.Action):

    """Generate subtitles by voice and speech recognition."""

    def __init__(self):
        """Initialize a :class:`SpeechRecognitionAction` object."""
        gaupol.Action.__init__(self, "speech_recognition")
        self.props.label = _("Sp_eech Recognition\342\200\246")
        self.props.tooltip = _("Generate subtitles by voice "
                               "and speech recognition")

        self.action_group = "main-safe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(gaupol.util.gst_available())
        aeidon.util.affirm(gaupol.util.pocketsphinx_available())


class TransformPositionsAction(gaupol.Action):

    """Change positions by linear two-point correction."""

    def __init__(self):
        """Initialize a :class:`TransformPositionsAction` object."""
        gaupol.Action.__init__(self, "transform_positions")
        self.props.label = _("_Transform Positions\342\200\246")
        self.props.tooltip = _("Change positions by linear "
                               "two-point correction")

        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(len(page.project.subtitles) > 1)


__all__ = tuple([x for x in dir() if x.endswith("Action")])
