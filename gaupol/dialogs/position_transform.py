# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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

"""Dialogs for applying linear transformations to positions."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import Gtk
from gi.repository import Pango

__all__ = ("FrameTransformDialog", "TimeTransformDialog")


class PositionTransformDialog(gaupol.BuilderDialog):

    """Base class for dialogs for transforming positions."""

    _widgets = [
        "correction_hbox_1",
        "correction_hbox_2",
        "correction_label_1",
        "correction_label_2",
        "current_radio",
        "input_entry_1",
        "input_entry_2",
        "preview_button_1",
        "preview_button_2",
        "selected_radio",
        "subtitle_spin_1",
        "subtitle_spin_2",
        "text_label_1",
        "text_label_2",
    ]

    def __init__(self, parent, application):
        """Initialize a :class:`PositionTransformDialog` instance."""
        gaupol.BuilderDialog.__init__(self, "position-transform-dialog.ui")
        self.application = application
        self._init_dialog(parent)
        self._init_sensitivities()
        self._init_sizes()

    def _get_target(self):
        """Return the selected target."""
        if self._selected_radio.get_active():
            return gaupol.targets.SELECTED
        if self._current_radio.get_active():
            return gaupol.targets.CURRENT
        raise ValueError("Invalid target radio state")

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("_Transform"), Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_transient_for(parent)
        self.set_modal(True)

    def _init_sensitivities(self):
        """Initialize sensitivities of widgets."""
        page = self.application.get_current_page()
        if page.project.video_path is None:
            self._preview_button_1.set_sensitive(False)
            self._preview_button_2.set_sensitive(False)
        if page.project.main_file is None:
            self._preview_button_1.set_sensitive(False)
            self._preview_button_2.set_sensitive(False)

    def _init_sizes(self):
        """Initialize widget sizes."""
        self._text_label_1.set_ellipsize(Pango.EllipsizeMode.END)
        self._text_label_2.set_ellipsize(Pango.EllipsizeMode.END)
        width = gaupol.util.char_to_px(50)
        self._text_label_1.set_size_request(width, -1)
        self._text_label_2.set_size_request(width, -1)

    def _init_values(self):
        """Intialize default values for widgets."""
        page = self.application.get_current_page()
        self._subtitle_spin_1.set_value(1)
        self._subtitle_spin_2.set_value(len(page.project.subtitles))
        self._subtitle_spin_1.emit("value-changed")
        self._subtitle_spin_2.emit("value-changed")
        target = gaupol.conf.position_transform.target
        self._selected_radio.set_active(target == gaupol.targets.SELECTED)
        self._current_radio.set_active(target == gaupol.targets.CURRENT)
        rows = page.view.get_selected_rows()
        if not rows and target == gaupol.targets.SELECTED:
            self._current_radio.set_active(True)
        self._selected_radio.set_sensitive(bool(rows))
        self._selected_radio.emit("toggled")

    def _init_widgets(self):
        """Initialize properties of widgets."""
        page = self.application.get_current_page()
        last_subtitle = len(page.project.subtitles)
        self._subtitle_spin_1.set_range(1, last_subtitle)
        self._subtitle_spin_2.set_range(1, last_subtitle)
        with aeidon.util.silent(AttributeError):
            self._text_label_1.props.xalign = 0
            self._text_label_2.props.xalign = 0

    def _on_preview_button_1_clicked(self, *args):
        """Preview changes from the first point."""
        page = self.application.get_current_page()
        row = self._subtitle_spin_1.get_value_as_int() - 1
        doc = aeidon.documents.MAIN
        method = page.project.transform_positions
        target = self._get_target()
        rows = self.application.get_target_rows(target)
        point_1 = self._get_first_point()
        point_2 = self._get_second_point()
        args = (rows, point_1, point_2)
        self.application.preview_changes(page, row, doc, method, args)

    def _on_preview_button_2_clicked(self, *args):
        """Preview changes from the second point."""
        page = self.application.get_current_page()
        row = self._subtitle_spin_2.get_value_as_int() - 1
        doc = aeidon.documents.MAIN
        method = page.project.transform_positions
        target = self._get_target()
        rows = self.application.get_target_rows(target)
        point_1 = self._get_first_point()
        point_2 = self._get_second_point()
        args = (rows, point_1, point_2)
        self.application.preview_changes(page, row, doc, method, args)

    def _on_response(self, dialog, response):
        """Save target and transform positions."""
        gaupol.conf.position_transform.target = self._get_target()
        if response == Gtk.ResponseType.OK:
            self._transform_positions()

    def _on_selected_radio_toggled(self, *args):
        """Set subtitle values from selection."""
        page = self.application.get_current_page()
        rows = page.view.get_selected_rows()
        ranges = aeidon.util.get_ranges(rows)
        if (self._selected_radio.get_active()
            and len(rows) > 1
            and len(ranges) == 1
            and not self._output_edited()):
            self._subtitle_spin_1.set_value(rows[0] + 1)
            self._subtitle_spin_2.set_value(rows[-1] + 1)
        elif not self._output_edited():
            self._subtitle_spin_1.set_value(1)
            self._subtitle_spin_2.set_value(len(page.project.subtitles))

    def _transform_positions(self):
        """Transform positions in subtitles."""
        page = self.application.get_current_page()
        target = self._get_target()
        rows = self.application.get_target_rows(target)
        point_1 = self._get_first_point()
        point_2 = self._get_second_point()
        page.project.transform_positions(rows, point_1, point_2)


class FrameTransformDialog(PositionTransformDialog):

    """Dialog for applying a linear tranfromation to frames."""

    def __init__(self, parent, application):
        """Initialize a :class:`FrameTransformDialog` instance."""
        PositionTransformDialog.__init__(self, parent, application)
        self._output_spin_1 = Gtk.SpinButton()
        self._output_spin_2 = Gtk.SpinButton()
        self._init_widgets()
        self._init_values()

    def _get_first_point(self):
        """Return row, output frame of the first sync point."""
        return (self._subtitle_spin_1.get_value_as_int() - 1,
                aeidon.as_frame(self._output_spin_1.get_value_as_int()))

    def _get_second_point(self):
        """Return row, output frame of the second sync point."""
        return (self._subtitle_spin_2.get_value_as_int() - 1,
                aeidon.as_frame(self._output_spin_2.get_value_as_int()))

    def _init_widgets(self):
        """Initialize properties of widgets."""
        PositionTransformDialog._init_widgets(self)
        self._input_entry_1.set_width_chars(6)
        self._input_entry_2.set_width_chars(6)
        self._output_spin_1.set_digits(0)
        self._output_spin_2.set_digits(0)
        self._output_spin_1.set_increments(1, 10)
        self._output_spin_2.set_increments(1, 10)
        self._output_spin_1.set_range(0, 999999)
        self._output_spin_2.set_range(0, 999999)
        gaupol.util.pack_start_expand(self._correction_hbox_1, self._output_spin_1)
        gaupol.util.pack_start_expand(self._correction_hbox_2, self._output_spin_2)
        self._correction_hbox_1.show_all()
        self._correction_hbox_2.show_all()
        self._correction_label_1.set_mnemonic_widget(self._output_spin_1)
        self._correction_label_2.set_mnemonic_widget(self._output_spin_2)

    def _on_subtitle_spin_1_value_changed(self, spin_button):
        """Update subtitle data in widgets."""
        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        subtitle = page.project.subtitles[row]
        self._input_entry_1.set_text(str(subtitle.start_frame))
        self._output_spin_1.set_value(int(subtitle.start_frame))
        text = subtitle.main_text.replace("\n", " ")
        text = aeidon.RE_ANY_TAG.sub("", text)
        self._text_label_1.set_text(text)
        self._text_label_1.set_tooltip_text(subtitle.main_text)
        self._subtitle_spin_2.get_adjustment().set_lower(row + 2)

    def _on_subtitle_spin_2_value_changed(self, spin_button):
        """Update subtitle data in widgets."""
        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        subtitle = page.project.subtitles[row]
        self._input_entry_2.set_text(str(subtitle.start_frame))
        self._output_spin_2.set_value(int(subtitle.start_frame))
        text = subtitle.main_text.replace("\n", " ")
        text = aeidon.RE_ANY_TAG.sub("", text)
        self._text_label_2.set_text(text)
        self._text_label_2.set_tooltip_text(subtitle.main_text)
        self._subtitle_spin_1.get_adjustment().set_upper(row)

    def _output_edited(self):
        """Return ``True`` if output of either point has been edited."""
        in_1  = aeidon.as_frame(self._input_entry_1.get_text())
        in_2  = aeidon.as_frame(self._input_entry_2.get_text())
        out_1 = aeidon.as_frame(self._output_spin_1.get_value_as_int())
        out_2 = aeidon.as_frame(self._output_spin_2.get_value_as_int())
        return (out_1 != in_1 or out_2 != in_2)


class TimeTransformDialog(PositionTransformDialog):

    """Dialog for applying a linear tranfromation to times."""

    def __init__(self, parent, application):
        """Initialize a :class:`TimeTransformDialog` instance."""
        PositionTransformDialog.__init__(self, parent, application)
        self._output_entry_1 = gaupol.TimeEntry()
        self._output_entry_2 = gaupol.TimeEntry()
        self._init_widgets()
        self._init_values()

    def _get_first_point(self):
        """Return row, output time of the first sync point."""
        return (self._subtitle_spin_1.get_value_as_int() - 1,
                aeidon.as_time(self._output_entry_1.get_text()))

    def _get_second_point(self):
        """Return row, output time of the second sync point."""
        return (self._subtitle_spin_2.get_value_as_int() - 1,
                aeidon.as_time(self._output_entry_2.get_text()))

    def _init_widgets(self):
        """Initialize properties of widgets."""
        PositionTransformDialog._init_widgets(self)
        self._input_entry_1.set_width_chars(13)
        self._input_entry_2.set_width_chars(13)
        gaupol.util.pack_start_expand(self._correction_hbox_1, self._output_entry_1)
        gaupol.util.pack_start_expand(self._correction_hbox_2, self._output_entry_2)
        self._correction_hbox_1.show_all()
        self._correction_hbox_2.show_all()
        self._correction_label_1.set_mnemonic_widget(self._output_entry_1)
        self._correction_label_2.set_mnemonic_widget(self._output_entry_2)

    def _on_subtitle_spin_1_value_changed(self, spin_button):
        """Update subtitle data in widgets."""
        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        subtitle = page.project.subtitles[row]
        self._input_entry_1.set_text(str(subtitle.start_time))
        self._output_entry_1.set_text(str(subtitle.start_time))
        text = subtitle.main_text.replace("\n", " ")
        text = aeidon.RE_ANY_TAG.sub("", text)
        self._text_label_1.set_text(text)
        self._text_label_1.set_tooltip_text(subtitle.main_text)
        self._subtitle_spin_2.get_adjustment().set_lower(row + 2)
        # Allow the GLib.idle_add-using TimeEntry to update.
        gaupol.util.iterate_main()

    def _on_subtitle_spin_2_value_changed(self, spin_button):
        """Update subtitle data in widgets."""
        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        subtitle = page.project.subtitles[row]
        self._input_entry_2.set_text(str(subtitle.start_time))
        self._output_entry_2.set_text(str(subtitle.start_time))
        text = subtitle.main_text.replace("\n", " ")
        text = aeidon.RE_ANY_TAG.sub("", text)
        self._text_label_2.set_text(text)
        self._text_label_2.set_tooltip_text(subtitle.main_text)
        self._subtitle_spin_1.get_adjustment().set_upper(row)
        # Allow the GLib.idle_add-using TimeEntry to update.
        gaupol.util.iterate_main()

    def _output_edited(self):
        """Return ``True`` if output of either point has been edited."""
        in_1  = aeidon.as_time(self._input_entry_1.get_text())
        in_2  = aeidon.as_time(self._input_entry_2.get_text())
        out_1 = aeidon.as_time(self._output_entry_1.get_text())
        out_2 = aeidon.as_time(self._output_entry_2.get_text())
        return (out_1 != in_1 or out_2 != in_2)
