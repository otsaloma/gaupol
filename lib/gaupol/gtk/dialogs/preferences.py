# Copyright (C) 2005 Osmo Salomaa
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


"""Dialog for editing preferences."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk
import pango

from gaupol.base.util            import enclib
from gaupol.gtk.cons import *
from gaupol.gtk.dialogs.encoding import EncodingDialog
from gaupol.gtk.util             import config, gtklib


class PreferencesDialog(gobject.GObject):

    """
    Dialog for changing settings.

    This class is implemented as a GObject. All setting-changing events will
    send signals upstream, where they can be instant-applied.
    """

    __gsignals__ = {
        'destroyed': (
            gobject.SIGNAL_RUN_LAST,
            None,
            ()
        ),
        'limit-undo-toggled': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (gobject.TYPE_BOOLEAN,)
        ),
        'undo-levels-changed': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (gobject.TYPE_INT,)
        ),
        'use-default-font-toggled': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (gobject.TYPE_BOOLEAN,)
        ),
        'font-set': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (gobject.TYPE_STRING,)
        )
    }

    def __init__(self, parent):

        gobject.GObject.__init__(self)

        glade_xml = gtklib.get_glade_xml('preferences-dialog')
        get = glade_xml.get_widget

        self._close_button             = get('close_button')
        self._dialog                   = get('dialog')
        self._encoding_add_button      = get('encoding_add_button')
        self._encoding_down_button     = get('encoding_move_down_button')
        self._encoding_locale_check    = get('encoding_locale_check_button')
        self._encoding_remove_button   = get('encoding_remove_button')
        self._encoding_up_button       = get('encoding_move_up_button')
        self._encoding_view            = get('encoding_tree_view')
        self._font_button              = get('font_button')
        self._font_custom_label        = get('font_custom_label')
        self._font_default_check       = get('font_default_check_button')
        self._preview_command_entry    = get('preview_command_entry')
        self._preview_command_legend   = get('preview_command_legend_table')
        self._preview_command_radio    = get('preview_command_radio_button')
        self._preview_edit_button      = get('preview_edit_button')
        self._preview_offset_spin      = get('preview_offset_spin_button')
        self._preview_select_combo     = get('preview_select_combo_box')
        self._preview_select_radio     = get('preview_select_radio_button')
        self._undo_levels_spin         = get('undo_levels_spin_button')
        self._undo_limit_radio         = get('undo_limit_radio_button')
        self._undo_unlimited_radio     = get('undo_unlimited_radio_button')

        self._init_encoding_view()
        self._init_data()
        self._init_signals()

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _init_data(self):
        """Initialize data."""

        self._init_file_data()
        self._init_editor_data()
        self._init_preview_data()

    def _init_editor_signals(self):
        """Initialize editor tab signals."""

        method = self._on_undo_limit_radio_toggled
        self._undo_limit_radio.connect('toggled', method)

        method = self._on_undo_levels_spin_value_changed
        self._undo_levels_spin.connect('value-changed', method)

        method = self._on_font_default_check_toggled
        self._font_default_check.connect('toggled', method)

        method = self._on_font_button_font_set
        self._font_button.connect('font-set', method)

    def _init_editor_data(self):
        """Initialize editor tab data."""

        limit = config.Editor.limit_undo
        self._undo_limit_radio.set_active(limit)
        self._undo_unlimited_radio.set_active(not limit)
        self._undo_levels_spin.set_sensitive(limit)
        self._undo_levels_spin.set_value(config.Editor.undo_levels)

        use_default = config.Editor.use_default_font
        self._font_default_check.set_active(use_default)
        self._font_custom_label.set_sensitive(not use_default)
        self._font_button.set_sensitive(not use_default)
        self._font_button.set_font_name(self._get_custom_font())

    def _init_encoding_view(self):
        """Initialize encoding view."""

        view = self._encoding_view
        view.columns_autosize()
        selection = view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.unselect_all()
        store = gtk.ListStore(gobject.TYPE_STRING)
        view.set_model(store)
        cell_renderer = gtk.CellRendererText()
        tree_view_column = gtk.TreeViewColumn('', cell_renderer, text=0)
        view.append_column(tree_view_column)

    def _init_file_signals(self):
        """Initialize file tab signals."""

        method = self._on_encoding_locale_check_toggled
        self._encoding_locale_check.connect('toggled', method)

        method = self._on_encoding_up_button_clicked
        self._encoding_up_button.connect('clicked', method)
        method = self._on_encoding_down_button_clicked
        self._encoding_down_button.connect('clicked', method)
        method = self._on_encoding_remove_button_clicked
        self._encoding_remove_button.connect('clicked', method)
        method = self._on_encoding_add_button_clicked
        self._encoding_add_button.connect('clicked', method)

    def _init_file_data(self):
        """Initialize file tab data."""

        try_locale = config.Encoding.try_locale
        self._encoding_locale_check.set_active(try_locale)
        self._reload_encoding_view()

    def _init_preview_signals(self):
        """Initialize preview tab signals."""

        method = self._on_preview_offset_spin_value_changed
        self._preview_offset_spin.connect('value-changed', method)

        method = self._on_preview_select_radio_toggled
        self._preview_select_radio.connect('toggled', method)

        method = self._on_preview_select_combo_changed
        self._preview_select_combo.connect('changed', method)

        method = self._on_preview_edit_button_clicked
        self._preview_edit_button.connect('clicked', method)

        method = self._on_preview_command_entry_changed
        self._preview_command_entry.connect('changed', method)

    def _init_preview_data(self):
        """Initialize preview tab data."""

        self._preview_offset_spin.set_value(float(config.Preview.offset))

        use_predefined = config.Preview.use_predefined
        self._preview_select_radio.set_active(use_predefined)
        self._preview_command_radio.set_active(not use_predefined)
        self._set_preview_radio_sensitivities()

        for i, name in enumerate(VideoPlayer.display_names):
            self._preview_select_combo.insert_text(i, name)
        self._preview_select_combo.set_active(config.Preview.video_player)

        command = config.Preview.command
        self._preview_command_entry.set_text(command or '')

    def _init_signals(self):
        """Initialize signals."""

        self._init_editor_signals()
        self._init_file_signals()
        self._init_preview_signals()

        selection =  self._encoding_view.get_selection()
        method = self._on_encoding_view_selection_changed
        selection.connect('changed', method)

        self._close_button.connect('clicked', self._destroy)
        self._dialog.connect('delete-event', self._destroy)

    def _destroy(self, *args):
        """Destroy the dialog."""

        self._dialog.destroy()
        self.emit('destroyed')

    def _get_custom_font(self):
        """
        Get custom font.

        Merge the custom font setting with the default font taken from a
        random widget to create to complete font description string.
        Return font description as a string.
        """
        context = self._font_custom_label.get_pango_context()
        font_description = context.get_font_description()

        custom_font_description = pango.FontDescription(config.Editor.font)
        font_description.merge(custom_font_description, True)

        return font_description.to_string()

    def _get_selected_encoding_row(self):
        """Get the selected fallback encoding view row."""

        selection = self._encoding_view.get_selection()
        store, itr = selection.get_selected()
        if itr is None:
            return None

        row = store.get_path(itr)
        try:
            return row[0]
        except TypeError:
            return row

    def _on_encoding_add_button_clicked(self, *args):
        """Add a new fallback encoding."""

        dialog = EncodingDialog(self._dialog)
        response = dialog.run()
        encoding = dialog.get_encoding()
        dialog.destroy()

        if response != gtk.RESPONSE_OK:
            return
        if encoding is None:
            return

        config.Encoding.fallback.append(encoding)
        self._reload_encoding_view()

    def _on_encoding_down_button_clicked(self, *args):
        """Move the selected encoding down in the list."""

        source_row = self._get_selected_encoding_row()
        encodings = config.Encoding.fallback
        encodings.insert(source_row + 1, encodings.pop(source_row))
        self._reload_encoding_view()

        self._encoding_view.grab_focus()
        selection = self._encoding_view.get_selection()
        selection.select_path(source_row + 1)

    def _on_encoding_locale_check_toggled(self, check_button):
        """Save use locale encoding setting."""

        config.Encoding.try_locale = check_button.get_active()

    def _on_encoding_remove_button_clicked(self, *args):
        """Remove the selected encoding."""

        row = self._get_selected_encoding_row()
        config.Encoding.fallback.pop(row)
        self._reload_encoding_view()

    def _on_encoding_up_button_clicked(self, *args):
        """Move the selected encoding up in the list."""

        source_row = self._get_selected_encoding_row()
        encodings = config.Encoding.fallback
        encodings.insert(source_row - 1, encodings.pop(source_row))
        self._reload_encoding_view()

        self._encoding_view.grab_focus()
        selection = self._encoding_view.get_selection()
        selection.select_path(source_row - 1)

    def _on_encoding_view_selection_changed(self, *args):
        """Set sensitivities based on current selection."""

        self._set_encoding_button_sensitivities()

    def _on_font_button_font_set(self, font_button):
        """Save custom font setting and emit signal."""

        font = font_button.get_font_name()
        config.Editor.font = font
        self.emit('font-set', font)

    def _on_font_default_check_toggled(self, check_button):
        """Save use default font setting and emit signal."""

        use_default = check_button.get_active()
        self._font_custom_label.set_sensitive(not use_default)
        self._font_button.set_sensitive(not use_default)

        config.Editor.use_default_font = use_default
        self.emit('use-default-font-toggled', use_default)

    def _on_preview_command_entry_changed(self, entry):
        """Save custom preview command."""

        config.Preview.command = entry.get_text() or None

    def _on_preview_edit_button_clicked(self, button):
        """Edit command."""

        video_player = self._preview_select_combo.get_active()
        command = VideoPlayer.commands[video_player]

        self._preview_command_entry.set_text(command)
        self._preview_command_radio.set_active(True)

    def _on_preview_offset_spin_value_changed(self, spin_button):
        """Save preview offset setting."""

        spin_button.update()
        value = '%.1f' % spin_button.get_value()
        config.Preview.offset = value

    def _on_preview_select_combo_changed(self, combo_box):
        """Save selected video player setting."""

        config.Preview.video_player = combo_box.get_active()

    def _on_preview_select_radio_toggled(self, radio_button):
        """Save video player setting."""

        use_predefined = not self._preview_command_radio.get_active()
        config.Preview.use_predefined = use_predefined
        self._set_preview_radio_sensitivities()

        if use_custom:
            self._preview_command_entry.grab_focus()
        else:
            self._preview_select_combo.grab_focus()

    def _on_undo_levels_spin_value_changed(self, spin_button):
        """Save undo level setting and emit signal."""

        spin_button.update()
        levels = spin_button.get_value_as_int()
        config.Editor.undo_levels = levels
        self.emit('undo-levels-changed', levels)

    def _on_undo_limit_radio_toggled(self, radio_button):
        """Save limit undo setting and emit signal."""

        limit = self._undo_limit_radio.get_active()
        self._undo_levels_spin.set_sensitive(limit)
        config.Editor.limit_undo = limit
        self.emit('limit-undo-toggled', limit)

    def _reload_encoding_view(self):
        """Reload the list of fallback encodings."""

        store = self._encoding_view.get_model()
        store.clear()
        for encoding in config.Encoding.fallback:
            name = enclib.get_long_name(encoding)
            store.append([name])

        self._set_encoding_button_sensitivities()

    def _set_encoding_button_sensitivities(self):
        """Set sensitivities of the fallback encoding view buttons."""

        store = self._encoding_view.get_model()

        if len(store) == 0:
            self._encoding_up_button.set_sensitive(False)
            self._encoding_down_button.set_sensitive(False)
            self._encoding_remove_button.set_sensitive(False)
            return

        row = self._get_selected_encoding_row()
        last_row = len(store) - 1

        self._encoding_up_button.set_sensitive(not row == 0)
        self._encoding_down_button.set_sensitive(not row == last_row)
        self._encoding_remove_button.set_sensitive(not row is None)

    def _set_preview_radio_sensitivities(self):
        """Set sensitivities depending on preview radio buttons."""

        use_predefined = config.Preview.use_predefined
        self._preview_select_combo.set_sensitive(use_predefined)
        self._preview_edit_button.set_sensitive(use_predefined)
        self._preview_command_entry.set_sensitive(not use_predefined)
        self._preview_command_legend.set_sensitive(not use_predefined)

    def show(self):
        """Show the dialog."""

        self._dialog.show()


if __name__ == '__main__':

    from gaupol.test import Test

    class TestPreferencesDialog(Test):

        def __init__(self):

            Test.__init__(self)
            self.dialog = PreferencesDialog(gtk.Window())
            self.dialog.show()

        def destroy(self):

            self.dialog._close_button.emit('clicked')

        def test_get_custom_font(self):

            font = self.dialog._get_custom_font()
            assert isinstance(font, basestring)

        def test_get_selected_encoding(self):

            selection = self.dialog._encoding_view.get_selection()
            selection.unselect_all()
            assert self.dialog._get_selected_encoding_row() is None
            selection.select_path(0)
            assert self.dialog._get_selected_encoding_row() == 0

        def test_editor_signals(self):

            self.dialog._undo_limit_radio.emit('toggled')
            self.dialog._undo_levels_spin.emit('value-changed')
            self.dialog._font_default_check.emit('toggled')
            self.dialog._font_button.emit('font-set')

        def test_file_signals(self):

            self.dialog._encoding_locale_check.emit('toggled')
            self.dialog._encoding_add_button.emit('clicked')

            selection =  self.dialog._encoding_view.get_selection()
            selection.unselect_all()
            selection.select_path(1)
            self.dialog._encoding_up_button.emit('clicked')

            selection.unselect_all()
            selection.select_path(0)
            self.dialog._encoding_down_button.emit('clicked')
            self.dialog._encoding_remove_button.emit('clicked')

        def test_preview_signals(self):

            self.dialog._preview_offset_spin.emit('value-changed')
            self.dialog._preview_select_radio.emit('toggled')
            self.dialog._preview_select_combo.emit('changed')
            self.dialog._preview_edit_button.emit('clicked')
            self.dialog._preview_command_entry.emit('changed')

    TestPreferencesDialog().run()
