# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Time and frame editing actions."""


import gaupol.gtk
import gtk
_ = gaupol.i18n._

from .action import Action


class AdjustDurationsAction(Action):

    """Lengthen or shorten durations."""

    def __init__(self):

        Action.__init__(self, "adjust_durations")
        self.props.label = _("Adjust _Durations\342\200\246")
        self.props.tooltip = _("Lengthen or shorten durations")

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None


class ConvertFramerateAction(Action):

    """Convert framerate."""

    def __init__(self):

        Action.__init__(self, "convert_framerate")
        self.props.label = _("Convert _Framerate\342\200\246")
        self.props.tooltip = _("Change positions for a different framerate")

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.project.main_file is not None


class PreviewAction(Action):

    """Preview from selected position with a video player."""

    def __init__(self):

        Action.__init__(self, "preview")
        self.props.label = _("_Preview")
        self.props.stock_id = gtk.STOCK_MEDIA_PLAY
        tooltip = _("Preview from selected position with a video player")
        self.props.tooltip = tooltip
        self.accelerator = "P"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.project.video_path is not None
        if gaupol.gtk.conf.preview.use_custom:
            assert gaupol.gtk.conf.preview.custom_command
        col = page.view.get_focus()[1]
        main_file = page.project.main_file
        tran_file = page.project.tran_file
        TRAN_TEXT = gaupol.gtk.COLUMN.TRAN_TEXT
        file = (tran_file if col == TRAN_TEXT else main_file)
        assert file is not None


class ShiftPositionsAction(Action):

    """Make subtitles appear earlier or later."""

    def __init__(self):

        Action.__init__(self, "shift_positions")
        self.props.label = _("_Shift Positions\342\200\246")
        self.props.tooltip = _("Make subtitles appear earlier or later")
        self.accelerator = "H"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None


class TransformPositionsAction(Action):

    """Change positions by linear two-point correction."""

    def __init__(self):

        Action.__init__(self, "transform_positions")
        self.props.label = _("_Transform Positions\342\200\246")
        tooltip = _("Change positions by linear two-point correction")
        self.props.tooltip = tooltip

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert len(page.project.subtitles) > 1
