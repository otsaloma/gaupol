# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Time and frame editing actions."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._


class AdjustDurationsAction(gaupol.gtk.Action):

    """Lengthen or shorten durations."""

    def __init__(self):
        """Initialize an AdjustDurationsAction object."""

        gaupol.gtk.Action.__init__(self, "adjust_durations")
        self.props.label = _("Adjust _Durations\342\200\246")
        self.props.tooltip = _("Lengthen or shorten durations")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class ConvertFramerateAction(gaupol.gtk.Action):

    """Convert framerate."""

    def __init__(self):
        """Initialize a ConvertFramerateAction object."""

        gaupol.gtk.Action.__init__(self, "convert_framerate")
        self.props.label = _("Convert _Framerate\342\200\246")
        self.props.tooltip = _("Change positions for a different framerate")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.main_file is not None)


class PreviewAction(gaupol.gtk.Action):

    """Preview from selected position with a video player."""

    def __init__(self):
        """Initialize a PreviewAction object."""

        gaupol.gtk.Action.__init__(self, "preview")
        self.props.label = _("_Preview")
        self.props.stock_id = gtk.STOCK_MEDIA_PLAY
        tooltip = _("Preview from selected position with a video player")
        self.props.tooltip = tooltip
        self.accelerator = "P"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.project.video_path is not None)
        if gaupol.gtk.conf.preview.use_custom:
            gaupol.util.affirm(gaupol.gtk.conf.preview.custom_command)
        col = page.view.get_focus()[1]
        if col == page.view.columns.TRAN_TEXT:
            gaupol.util.affirm(page.project.tran_file is not None)
        else: # Any other column previews the main file.
            gaupol.util.affirm(page.project.main_file is not None)


class ShiftPositionsAction(gaupol.gtk.Action):

    """Make subtitles appear earlier or later."""

    def __init__(self):
        """Initialize a ShiftPositionsAction object."""

        gaupol.gtk.Action.__init__(self, "shift_positions")
        self.props.label = _("_Shift Positions\342\200\246")
        self.props.tooltip = _("Make subtitles appear earlier or later")
        self.accelerator = "H"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class TransformPositionsAction(gaupol.gtk.Action):

    """Change positions by linear two-point correction."""

    def __init__(self):
        """Initialize a TransformPositionsAction object."""

        gaupol.gtk.Action.__init__(self, "transform_positions")
        self.props.label = _("_Transform Positions\342\200\246")
        tooltip = _("Change positions by linear two-point correction")
        self.props.tooltip = tooltip
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(len(page.project.subtitles) > 1)


__all__ = gaupol.util.get_all(dir(), r"Action$")
