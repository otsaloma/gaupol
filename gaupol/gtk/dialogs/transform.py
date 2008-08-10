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

"""Dialogs for applying linear tranfromations to positions."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._

__all__ = ("FrameTransformDialog", "TimeTransformDialog")


class _PositionTransformDialog(gaupol.gtk.GladeDialog):

    """Base class for dialogs for transforming positions."""

    def __init__(self, parent, application):

        gaupol.gtk.GladeDialog.__init__(self, "transform.glade")
        get_widget = self._glade_xml.get_widget
        self._correction_hbox_1 = get_widget("correction_hbox_1")
        self._correction_hbox_2 = get_widget("correction_hbox_2")
        self._correction_label_1 = get_widget("correction_label_1")
        self._correction_label_2 = get_widget("correction_label_2")
        self._current_radio = get_widget("current_radio")
        self._input_label_1 = get_widget("input_label_1")
        self._input_label_2 = get_widget("input_label_2")
        self._preview_button_1 = get_widget("preview_button_1")
        self._preview_button_2 = get_widget("preview_button_2")
        self._selected_radio = get_widget("selected_radio")
        self._subtitle_spin_1 = get_widget("subtitle_spin_1")
        self._subtitle_spin_2 = get_widget("subtitle_spin_2")
        self._text_label_1 = get_widget("text_label_1")
        self._text_label_2 = get_widget("text_label_2")
        self.application = application
        self.conf = gaupol.gtk.conf.position_transform

        self._init_sensitivities()
        self._init_signal_handlers()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _get_target(self):
        """Return the selected target."""

        if self._selected_radio.get_active():
            return gaupol.gtk.targets.SELECTED
        if self._current_radio.get_active():
            return gaupol.gtk.targets.CURRENT
        raise ValueError

    def _init_sensitivities(self):
        """Initialize the sensitivities of widgets."""

        page = self.application.get_current_page()
        rows = page.view.get_selected_rows()
        targets = gaupol.gtk.targets
        if (not rows) and (self.conf.target == targets.SELECTED):
            self._current_radio.set_active(True)
        self._selected_radio.set_sensitive(bool(rows))
        if page.project.video_path is None:
            self._preview_button_1.set_sensitive(False)
            self._preview_button_2.set_sensitive(False)
        if page.project.main_file is None:
            self._preview_button_1.set_sensitive(False)
            self._preview_button_2.set_sensitive(False)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, "_preview_button_1", "clicked")
        gaupol.util.connect(self, "_preview_button_2", "clicked")
        gaupol.util.connect(self, "_subtitle_spin_1", "value-changed")
        gaupol.util.connect(self, "_subtitle_spin_2", "value-changed")
        gaupol.util.connect(self, self, "response")

    def _init_sizes(self):
        """Initialize widget sizes."""

        width = gtk.Label("m" * 24).size_request()[0]
        self._text_label_1.set_size_request(width, -1)
        self._text_label_2.set_size_request(width, -1)

    def _init_values(self):
        """Intialize default values for widgets."""

        page = self.application.get_current_page()
        self._subtitle_spin_1.set_value(1)
        self._subtitle_spin_1.emit("value-changed")
        self._subtitle_spin_2.set_value(len(page.project.subtitles))
        self._subtitle_spin_2.emit("value-changed")
        targets = gaupol.gtk.targets
        self._selected_radio.set_active(self.conf.target == targets.SELECTED)
        self._current_radio.set_active(self.conf.target == targets.CURRENT)

    def _init_widgets(self):
        """Initialize the properties of widgets."""

        page = self.application.get_current_page()
        last_subtitle = len(page.project.subtitles)
        self._subtitle_spin_1.set_range(1, last_subtitle)
        self._subtitle_spin_2.set_range(1, last_subtitle)

    def _on_preview_button_1_clicked(self, *args):
        """Preview changes at the first point."""

        page = self.application.get_current_page()
        row = self._subtitle_spin_1.get_value_as_int() - 1
        doc = gaupol.documents.MAIN
        method = page.project.transform_positions
        target = self._get_target()
        rows = self.application.get_target_rows(target)
        point_1 = self._get_first_point()
        point_2 = self._get_second_point()
        args = (rows, point_1, point_2)
        self.application.preview_changes(page, row, doc, method, args)

    def _on_preview_button_2_clicked(self, *args):
        """Preview changes at the second point."""

        page = self.application.get_current_page()
        row = self._subtitle_spin_2.get_value_as_int() - 1
        doc = gaupol.documents.MAIN
        method = page.project.transform_positions
        target = self._get_target()
        rows = self.application.get_target_rows(target)
        point_1 = self._get_first_point()
        point_2 = self._get_second_point()
        args = (rows, point_1, point_2)
        self.application.preview_changes(page, row, doc, method, args)

    def _on_response(self, dialog, response):
        """Save settings and adjust positions."""

        self.conf.target = self._get_target()
        if response == gtk.RESPONSE_OK:
            self._transform_positions()

    def _transform_positions(self):
        """Transform positions in subtitles."""

        page = self.application.get_current_page()
        target = self._get_target()
        rows = self.application.get_target_rows(target)
        point_1 = self._get_first_point()
        point_2 = self._get_second_point()
        page.project.transform_positions(rows, point_1, point_2)


class FrameTransformDialog(_PositionTransformDialog):

    """Dialog for applying linear tranfromations to frames."""

    __metaclass__ = gaupol.Contractual

    def __init__(self, parent, application):

        _PositionTransformDialog.__init__(self, parent, application)
        self._output_spin_1 = gtk.SpinButton()
        self._output_spin_2 = gtk.SpinButton()

        self._init_widgets()
        self._init_values()

    def _get_first_point_ensure(self, value):
        assert isinstance(value[1], int)

    def _get_first_point(self):
        """Return row, output frame of the first sync point."""

        row = self._subtitle_spin_1.get_value_as_int() - 1
        frame = self._output_spin_1.get_value_as_int()
        return row, frame

    def _get_second_point_ensure(self, value):
        assert isinstance(value[1], int)

    def _get_second_point(self):
        """Return row, output frame of the second sync point."""

        row = self._subtitle_spin_2.get_value_as_int() - 1
        frame = self._output_spin_2.get_value_as_int()
        return row, frame

    def _init_widgets(self):
        """Initialize the properties of widgets."""

        _PositionTransformDialog._init_widgets(self)
        self._input_label_1.set_width_chars(6)
        self._input_label_2.set_width_chars(6)
        self._output_spin_1.set_digits(0)
        self._output_spin_1.set_increments(1, 10)
        self._output_spin_1.set_range(0, 999999)
        self._output_spin_2.set_digits(0)
        self._output_spin_2.set_increments(1, 10)
        self._output_spin_2.set_range(0, 999999)
        self._correction_hbox_1.pack_start(self._output_spin_1)
        self._correction_hbox_2.pack_start(self._output_spin_2)
        self._correction_hbox_1.show_all()
        self._correction_hbox_2.show_all()
        self._correction_label_1.set_mnemonic_widget(self._output_spin_1)
        self._correction_label_2.set_mnemonic_widget(self._output_spin_2)

    def _on_subtitle_spin_1_value_changed(self, spin_button):
        """Update subtitle data in widgets."""

        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        subtitle = page.project.subtitles[row]
        self._input_label_1.set_text(str(subtitle.start_frame))
        self._output_spin_1.set_value(subtitle.start_frame)
        text = subtitle.main_text.replace("\n", " ")
        text = gaupol.re_any_tag.sub("", text)
        self._text_label_1.set_text(text)
        self._text_label_1.set_tooltip_text(subtitle.main_text)
        self._subtitle_spin_2.props.adjustment.props.lower = row + 2

    def _on_subtitle_spin_2_value_changed(self, spin_button):
        """Update subtitle data in widgets."""

        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        subtitle = page.project.subtitles[row]
        self._input_label_2.set_text(str(subtitle.start_frame))
        self._output_spin_2.set_value(subtitle.start_frame)
        text = subtitle.main_text.replace("\n", " ")
        text = gaupol.re_any_tag.sub("", text)
        self._text_label_2.set_text(text)
        self._text_label_2.set_tooltip_text(subtitle.main_text)
        self._subtitle_spin_1.props.adjustment.props.upper = row


class TimeTransformDialog(_PositionTransformDialog):

    """Dialog for applying linear tranfromations to times."""

    __metaclass__ = gaupol.Contractual

    def __init__(self, parent, application):

        _PositionTransformDialog.__init__(self, parent, application)
        self._output_entry_1 = gaupol.gtk.TimeEntry()
        self._output_entry_2 = gaupol.gtk.TimeEntry()

        self._init_widgets()
        self._init_values()

    def _get_first_point_ensure(self, value):
        assert isinstance(value[1], basestring)

    def _get_first_point(self):
        """Return row, output time of the first sync point."""

        row = self._subtitle_spin_1.get_value_as_int() - 1
        time = self._output_entry_1.get_text()
        return row, time

    def _get_second_point_ensure(self, value):
        assert isinstance(value[1], basestring)

    def _get_second_point(self):
        """Return row, output time of the second sync point."""

        row = self._subtitle_spin_2.get_value_as_int() - 1
        time = self._output_entry_2.get_text()
        return row, time

    def _init_widgets(self):
        """Initialize the properties of widgets."""

        _PositionTransformDialog._init_widgets(self)
        self._input_label_1.set_width_chars(13)
        self._input_label_2.set_width_chars(13)
        self._correction_hbox_1.pack_start(self._output_entry_1)
        self._correction_hbox_2.pack_start(self._output_entry_2)
        self._correction_hbox_1.show_all()
        self._correction_hbox_2.show_all()
        self._correction_label_1.set_mnemonic_widget(self._output_entry_1)
        self._correction_label_2.set_mnemonic_widget(self._output_entry_2)

    def _on_subtitle_spin_1_value_changed(self, spin_button):
        """Update subtitle data in widgets."""

        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        subtitle = page.project.subtitles[row]
        self._input_label_1.set_text(subtitle.start_time)
        self._output_entry_1.set_text(subtitle.start_time)
        text = subtitle.main_text.replace("\n", " ")
        text = gaupol.re_any_tag.sub("", text)
        self._text_label_1.set_text(text)
        self._text_label_1.set_tooltip_text(subtitle.main_text)
        self._subtitle_spin_2.props.adjustment.props.lower = row + 2
        # Allow the slow TimeEntry to update.
        gaupol.gtk.util.iterate_main()

    def _on_subtitle_spin_2_value_changed(self, spin_button):
        """Update subtitle data in widgets."""

        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        subtitle = page.project.subtitles[row]
        self._input_label_2.set_text(subtitle.start_time)
        self._output_entry_2.set_text(subtitle.start_time)
        text = subtitle.main_text.replace("\n", " ")
        text = gaupol.re_any_tag.sub("", text)
        self._text_label_2.set_text(text)
        self._text_label_2.set_tooltip_text(subtitle.main_text)
        self._subtitle_spin_1.props.adjustment.props.upper = row
        # Allow the slow TimeEntry to update.
        gaupol.gtk.util.iterate_main()
