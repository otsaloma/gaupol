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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Dialog for editing preferences."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import Gtk
from gi.repository import Pango

class EditorPage(aeidon.Delegate, gaupol.BuilderDialog):

    """Editor preferences page."""

    _widgets = [
        "editor_custom_font_check",
        "editor_font_button",
        "editor_length_cell_check",
        "editor_length_combo",
        "editor_length_edit_check",
        "editor_length_hbox",
        "editor_spell_check_check",
    ]

    def __init__(self, master, application):
        """Initialize an :class:`EditorPage` instance."""
        aeidon.Delegate.__init__(self, master)
        self._set_attributes(self._widgets, "editor_")
        self.application = application
        self._init_length_combo()
        self._init_values()

    def _get_custom_font(self):
        """Return custom font as string."""
        context = Gtk.Label().get_pango_context()
        font_desc = context.get_font_description()
        font = gaupol.conf.editor.custom_font
        custom_font_desc = Pango.FontDescription(font)
        font_desc.merge(custom_font_desc, True)
        return font_desc.to_string()

    def _init_length_combo(self):
        """Initialize the line length combo box."""
        store = Gtk.ListStore(str)
        for label in (x.label for x in gaupol.length_units):
            store.append((label,))
        self._length_combo.set_model(store)
        renderer = Gtk.CellRendererText()
        self._length_combo.pack_start(renderer, expand=True)
        self._length_combo.add_attribute(renderer, "text", 0)

    def _init_values(self):
        """Initialize default values for widgets."""
        use_custom = gaupol.conf.editor.use_custom_font
        self._custom_font_check.set_active(use_custom)
        self._font_button.set_sensitive(use_custom)
        self._font_button.set_font(self._get_custom_font())
        show_cell = gaupol.conf.editor.show_lengths_cell
        show_edit = gaupol.conf.editor.show_lengths_edit
        self._length_hbox.set_sensitive(show_cell or show_edit)
        self._length_cell_check.set_active(show_cell)
        self._length_edit_check.set_active(show_edit)
        self._length_combo.set_active(gaupol.conf.editor.length_unit)
        if gaupol.SpellChecker.available():
            inline = gaupol.conf.spell_check.inline
            self._spell_check_check.set_active(inline)
            self._spell_check_check.set_sensitive(True)
        else: # not available
            self._spell_check_check.set_active(False)
            self._spell_check_check.set_sensitive(False)

    def _on_custom_font_check_toggled(self, check_button):
        """Save custom font usage."""
        use_custom = check_button.get_active()
        gaupol.conf.editor.use_custom_font = use_custom
        self._font_button.set_sensitive(use_custom)

    def _on_font_button_font_set(self, font_button):
        """Save custom font."""
        gaupol.conf.editor.custom_font = font_button.get_font()

    def _on_length_cell_check_toggled(self, check_button):
        """Save line length display on cells."""
        gaupol.conf.editor.show_lengths_cell = check_button.get_active()
        show_cell = gaupol.conf.editor.show_lengths_cell
        show_edit = gaupol.conf.editor.show_lengths_edit
        self._length_hbox.set_sensitive(show_cell or show_edit)

    def _on_length_combo_changed(self, combo_box):
        """Save line length unit."""
        index = combo_box.get_active()
        gaupol.conf.editor.length_unit = gaupol.length_units[index]

    def _on_length_edit_check_toggled(self, check_button):
        """Save line length display on text views."""
        gaupol.conf.editor.show_lengths_edit = check_button.get_active()
        show_cell = gaupol.conf.editor.show_lengths_cell
        show_edit = gaupol.conf.editor.show_lengths_edit
        self._length_hbox.set_sensitive(show_cell or show_edit)

    def _on_spell_check_check_toggled(self, check_button):
        """Save inline spell-check use on text views."""
        gaupol.conf.spell_check.inline = check_button.get_active()

class FilePage(aeidon.Delegate, gaupol.BuilderDialog):

    """File preferences page."""

    _widgets = [
        "file_add_button",
        "file_auto_check",
        "file_down_button",
        "file_encoding_list",
        "file_encoding_scroller",
        "file_locale_check",
        "file_remove_button",
        "file_up_button",
    ]

    def __init__(self, master, application):
        """Initialize a :class:`FilePage` instance."""
        aeidon.Delegate.__init__(self, master)
        self._set_attributes(self._widgets, "file_")
        self.application = application
        max_height = gaupol.util.lines_to_px(15)
        self._encoding_scroller.set_max_content_height(max_height)
        self._init_values()

    def _get_selected_row(self):
        """Return the index of the selected row or ``None``."""
        row = self._encoding_list.get_selected_row()
        return row.get_index() if row else None

    def _init_values(self):
        """Initialize default values for widgets."""
        self._auto_check.set_active(gaupol.conf.encoding.try_auto)
        self._auto_check.set_sensitive(aeidon.util.chardet_available())
        self._locale_check.set_active(gaupol.conf.encoding.try_locale)
        self._reload_encoding_list()

    def _on_add_button_clicked(self, *args):
        """Add a new fallback encoding."""
        dialog = gaupol.EncodingDialog(self._dialog)
        response = gaupol.util.run_dialog(dialog)
        encoding = dialog.get_encoding()
        dialog.destroy()
        if response != Gtk.ResponseType.OK: return
        if encoding is None: return
        if encoding in gaupol.conf.encoding.fallback: return
        gaupol.conf.encoding.fallback.append(encoding)
        self._reload_encoding_list()
        self._select_row(len(gaupol.conf.encoding.fallback) - 1)

    def _on_auto_check_toggled(self, check_button):
        """Save encoding auto-detection usage."""
        gaupol.conf.encoding.try_auto = check_button.get_active()

    def _on_down_button_clicked(self, *args):
        """Move the selected fallback encoding down."""
        row = self._get_selected_row()
        encodings = gaupol.conf.encoding.fallback
        encodings.insert(row + 1, encodings.pop(row))
        self._reload_encoding_list()
        self._select_row(row + 1)

    def _on_encoding_list_row_selected(self, list_box, row):
        """Set the fallback list button sensitivities."""
        self._set_sensitivities()

    def _on_locale_check_toggled(self, check_button):
        """Save locale encoding usage."""
        gaupol.conf.encoding.try_locale = check_button.get_active()

    def _on_remove_button_clicked(self, *args):
        """Remove the selected fallback encoding."""
        row = self._get_selected_row()
        gaupol.conf.encoding.fallback.pop(row)
        self._reload_encoding_list()
        if not gaupol.conf.encoding.fallback: return
        self._select_row(max(row - 1, 0))

    def _on_up_button_clicked(self, *args):
        """Move the selected fallback encoding up."""
        row = self._get_selected_row()
        encodings = gaupol.conf.encoding.fallback
        encodings.insert(row - 1, encodings.pop(row))
        self._reload_encoding_list()
        self._select_row(row - 1)

    def _reload_encoding_list(self):
        """Reload the fallback encoding list."""
        self._encoding_list.remove_all()
        for encoding in gaupol.conf.encoding.fallback:
            box = gaupol.util.new_hbox(spacing=12)
            label = Gtk.Label(
                label=aeidon.encodings.code_to_description(encoding))
            label.add_css_class("dim-label")
            box.append(label)
            box.append(Gtk.Label(
                label=aeidon.encodings.code_to_name(encoding)))
            self._encoding_list.append(box)
        self._set_sensitivities()

    def _select_row(self, index):
        """Select and focus the fallback encoding row at `index`."""
        row = self._encoding_list.get_row_at_index(index)
        self._encoding_list.select_row(row)
        row.grab_focus()

    def _set_sensitivities(self):
        """Set the fallback list button sensitivities."""
        row = self._get_selected_row()
        row = -1 if row is None else row
        count = len(gaupol.conf.encoding.fallback)
        self._remove_button.set_sensitive(row >= 0)
        self._up_button.set_sensitive(row > 0)
        self._down_button.set_sensitive(0 <= row < count - 1)

class PreviewPage(aeidon.Delegate, gaupol.BuilderDialog):

    """Preview preferences page."""

    _widgets = [
        "preview_app_combo",
        "preview_command_entry",
        "preview_force_utf_8_check",
        "preview_offset_spin",
    ]

    def __init__(self, master, application):
        """Initialize a :class:`PreviewPage` instance."""
        aeidon.Delegate.__init__(self, master)
        self._set_attributes(self._widgets, "preview_")
        self.application = application
        self._init_app_combo()
        self._init_values()

    def _init_app_combo(self):
        """Initialize the application combo box."""
        store = Gtk.ListStore(str)
        self._app_combo.set_model(store)
        for label in (x.label for x in aeidon.players):
            store.append((label,))
        store.append((gaupol.COMBO_SEPARATOR,))
        store.append((_("Custom"),))
        renderer = Gtk.CellRendererText()
        self._app_combo.pack_start(renderer, expand=True)
        self._app_combo.add_attribute(renderer, "text", 0)
        func = gaupol.util.separate_combo
        self._app_combo.set_row_separator_func(func, None)

    def _init_values(self):
        """Initialize default values for widgets."""
        store = self._app_combo.get_model()
        self._app_combo.set_active((len(store) - 1 if
                                    gaupol.conf.preview.use_custom_command else
                                    gaupol.conf.preview.player))

        self._command_entry.set_text(gaupol.util.get_preview_command())
        editable = gaupol.conf.preview.use_custom_command
        self._command_entry.set_editable(editable)
        self._force_utf_8_check.set_active(gaupol.conf.preview.force_utf_8)
        self._offset_spin.set_value(gaupol.conf.preview.offset)

    def _on_app_combo_changed(self, combo_box):
        """Save video player and show it's command."""
        index = combo_box.get_active()
        use_custom = not index in aeidon.players
        gaupol.conf.preview.use_custom_command = use_custom
        if not use_custom:
            gaupol.conf.preview.player = aeidon.players[index]
        self._command_entry.set_text(gaupol.util.get_preview_command())
        editable = gaupol.conf.preview.use_custom_command
        self._command_entry.set_editable(editable)

    def _on_command_entry_changed(self, entry):
        """Save custom command."""
        if not gaupol.conf.preview.use_custom_command: return
        gaupol.conf.preview.custom_command = entry.get_text()

    def _on_force_utf_8_check_toggled(self, check_button):
        """Save forced UTF-8 preview setting."""
        gaupol.conf.preview.force_utf_8 = check_button.get_active()
        self._command_entry.set_text(gaupol.util.get_preview_command())

    def _on_offset_spin_value_changed(self, spin_button):
        """Save start position offset."""
        gaupol.conf.preview.offset = spin_button.get_value()

class VideoPage(aeidon.Delegate, gaupol.BuilderDialog):

    """Video preferences page."""

    _widgets = [
        "video_seek_spin",
        "video_subtitle_bg_toggle",
        "video_subtitle_color_button",
        "video_subtitle_font_button",
        "video_time_bg_toggle",
        "video_time_color_button",
        "video_time_font_button",
    ]

    def __init__(self, master, application):
        """Initialize a :class:`PreviewPage` instance."""
        aeidon.Delegate.__init__(self, master)
        self._set_attributes(self._widgets, "video_")
        self.application = application
        self.conf = gaupol.conf.video_player
        self._init_values()

    def _get_custom_font(self, font):
        """Return custom font as string."""
        context = Gtk.Label().get_pango_context()
        font_desc = context.get_font_description()
        custom_font_desc = Pango.FontDescription(font)
        font_desc.merge(custom_font_desc, True)
        return font_desc.to_string()

    def _init_values(self):
        """Initialize default values for widgets."""
        font = self._get_custom_font(self.conf.subtitle_font)
        self._subtitle_font_button.set_font(font)
        font = self._get_custom_font(self.conf.time_font)
        self._time_font_button.set_font(font)
        self._subtitle_bg_toggle.set_active(self.conf.subtitle_background)
        color = gaupol.util.hex_to_rgba(self.conf.subtitle_color)
        color.alpha = self.conf.subtitle_alpha
        self._subtitle_color_button.set_rgba(color)
        self._time_bg_toggle.set_active(self.conf.time_background)
        color = gaupol.util.hex_to_rgba(self.conf.time_color)
        color.alpha = self.conf.time_alpha
        self._time_color_button.set_rgba(color)
        self._seek_spin.set_value(self.conf.seek_length)

    def _on_seek_spin_value_changed(self, spin_button):
        """Save seek length."""
        self.conf.seek_length = spin_button.get_value()

    def _on_subtitle_bg_toggle_toggled(self, toggle_button):
        """Save subtitle background use."""
        self.conf.subtitle_background = toggle_button.get_active()

    def _on_subtitle_color_button_color_set(self, color_button):
        """Save subtitle color."""
        color = color_button.get_rgba()
        self.conf.subtitle_color = gaupol.util.rgba_to_hex(color)
        self.conf.subtitle_alpha = color.alpha

    def _on_subtitle_font_button_font_set(self, font_button):
        """Save subtitle font."""
        self.conf.subtitle_font = font_button.get_font()

    def _on_time_bg_toggle_toggled(self, toggle_button):
        """Save time background use."""
        self.conf.time_background = toggle_button.get_active()

    def _on_time_color_button_color_set(self, color_button):
        """Save time color."""
        color = color_button.get_rgba()
        self.conf.time_color = gaupol.util.rgba_to_hex(color)
        self.conf.time_alpha = color.alpha

    def _on_time_font_button_font_set(self, font_button):
        """Save time font."""
        self.conf.time_font = font_button.get_font()

class PreferencesDialog(gaupol.BuilderDialog):

    """Dialog for editing preferences."""

    def __init__(self, parent, application):
        """Initialize a :class:`PreferencesDialog` instance."""
        # The signal handlers, which live on the page instances created
        # below, are resolved against self already when the UI definition
        # file is parsed. __getattr__ resolves them to placeholders that
        # look up the actual handler from _callbacks only when called.
        self._callbacks = {}
        gaupol.BuilderDialog.__init__(self, "preferences-dialog.ui")
        self._editor_page = EditorPage(self, application)
        self._file_page = FilePage(self, application)
        self._preview_page = PreviewPage(self, application)
        self._video_page = VideoPage(self, application)
        self._callbacks.update(self._get_callbacks())
        self._init_dialog(parent)

    def __getattr__(self, name):
        """Return signal handler placeholder or attribute from dialog."""
        if name.startswith("_on_"):
            # Setting initial widget values in the page constructors emits
            # signals before _callbacks is populated. Those just echo values
            # already in the configuration, so they can be safely dropped.
            def placeholder(*args):
                if name in self._callbacks:
                    return self._callbacks[name](*args)
            return placeholder
        return super().__getattr__(name)

    def _get_callbacks(self):
        """Return a dictionary mapping names to callback methods."""
        callbacks = {}
        for page in (self._editor_page,
                     self._file_page,
                     self._preview_page,
                     self._video_page):

            for name in (x for x in dir(page) if x.startswith("_on_")):
                callbacks[name] = getattr(page, name)
        return callbacks

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.set_default_response(Gtk.ResponseType.CLOSE)
        self.set_transient_for(parent)
        self.set_modal(True)
