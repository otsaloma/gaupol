# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Dialog for editing preferences."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk
import pango

from gaupol.base.util            import encodinglib
from gaupol.gtk.dialogs.encoding import EncodingDialog
from gaupol.gtk.util             import config, gui


class PreferencesDialog(gobject.GObject):

    """
    Dialog for changing settings.

    This class is implemented as a GObject. All setting-changing events will
    send signals upstream, where they can be instant-applied.
    """

    STAGE = gobject.SIGNAL_RUN_LAST
    BOOL  = gobject.TYPE_BOOLEAN
    INT   = gobject.TYPE_INT
    STR   = gobject.TYPE_STRING

    __gsignals__ = {
        'destroyed'               : (STAGE, None, (     )),
        'limit-undo-toggled'      : (STAGE, None, (BOOL,)),
        'undo-levels-changed'     : (STAGE, None, (INT ,)),
        'use-default-font-toggled': (STAGE, None, (BOOL,)),
        'font-set'                : (STAGE, None, (STR ,)),
    }

    def __init__(self, parent):

        gobject.GObject.__init__(self)

        glade_xml = gui.get_glade_xml('preferences-dialog.glade')
        get = glade_xml.get_widget

        # Widgets
        self._dialog                  = get('dialog')
        self._encoding_locale_check   = get('encoding_locale_check_button')
        self._encoding_view           = get('encoding_tree_view')
        self._encoding_up_button      = get('encoding_move_up_button')
        self._encoding_down_button    = get('encoding_move_down_button')
        self._encoding_remove_button  = get('encoding_remove_button')
        self._encoding_add_button     = get('encoding_add_button')
        self._undo_limit_radio        = get('undo_limit_radio_button')
        self._undo_levels_spin_button = get('undo_levels_spin_button')
        self._undo_unlimited_radio    = get('undo_unlimited_radio_button')
        self._font_default_check      = get('font_default_check_button')
        self._font_custom_label       = get('font_custom_label')
        self._font_button             = get('font_button')
        self._close_button            = get('close_button')

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)
        self._dialog.connect('delete-event', self._destroy)

        self._init_encoding_view()
        self._set_mnemonics(glade_xml)
        self._connect_signals()
        self._set_from_config()

    def _init_encoding_view(self):
        """Init the list of encodings."""

        view = self._encoding_view
        view.columns_autosize()

        selection = view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.unselect_all()
        selection.connect('changed', self._on_encoding_view_selection_changed)

        store = gtk.ListStore(gobject.TYPE_STRING)
        view.set_model(store)

        cell_renderer = gtk.CellRendererText()
        tree_view_column = gtk.TreeViewColumn('', cell_renderer, text=0)
        view.append_column(tree_view_column)

    def _connect_editor_signals(self):
        """Connect signals of the editor tab's widgets."""

        # Ensure that undo limiting radio buttons have the same group.
        # ValueError is raised if button already is in group.
        group = self._undo_limit_radio.get_group()[0]
        try:
            self._undo_unlimited_radio.set_group(group)
        except ValueError:
            pass

        # Undo limit radio button
        method = self._on_undo_limit_radio_toggled
        self._undo_limit_radio.connect('toggled', method)

        # Undo levels spin button
        method = self._on_undo_levels_spin_button_value_changed
        self._undo_levels_spin_button.connect('value-changed', method)

        # Font default check button
        method = self._on_font_default_check_toggled
        self._font_default_check.connect('toggled', method)

        # Font button
        method = self._on_font_button_font_set
        self._font_button.connect('font-set', method)

    def _connect_file_signals(self):
        """Connect signals of the file tab's widgets."""

        # Locale encoding check button
        method = self._on_encoding_locale_check_toggled
        self._encoding_locale_check.connect('toggled', method)

        # Encoding move buttons
        method = self._on_encoding_up_button_clicked
        self._encoding_up_button.connect('clicked', method)
        method = self._on_encoding_down_button_clicked
        self._encoding_down_button.connect('clicked', method)

        # Encoding add and remove buttons
        method = self._on_encoding_remove_button_clicked
        self._encoding_remove_button.connect('clicked', method)
        method = self._on_encoding_add_button_clicked
        self._encoding_add_button.connect('clicked', method)

    def _connect_signals(self):
        """Connect signals to widgets."""

        self._connect_editor_signals()
        self._connect_file_signals()

        # Close button
        self._close_button.connect('clicked', self._destroy)

    def _destroy(self, *args):
        """Destroy the dialog."""

        self._dialog.destroy()
        self.emit('destroyed')

    def _get_custom_font(self):
        """
        Get custom font.

        This method merges the custom font setting with the default font
        taken from a random widget to create to complete font description
        string.
        Return font description as a string.
        """
        # Get the default font description from a random widget.
        context = self._font_custom_label.get_pango_context()
        font_description = context.get_font_description()

        # Create custom font description and merge that with the default.
        custom_font_description = pango.FontDescription(config.editor.font)
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

        config.file.fallback_encodings.append(encoding)
        self._reload_encoding_view()

    def _on_encoding_down_button_clicked(self, *args):
        """Move the selected encoding down in the list."""

        source_row = self._get_selected_encoding_row()
        encodings = config.file.fallback_encodings
        encodings.insert(source_row + 1, encodings.pop(source_row))
        self._reload_encoding_view()

        self._encoding_view.grab_focus()
        selection = self._encoding_view.get_selection()
        selection.select_path(source_row + 1)

    def _on_encoding_locale_check_toggled(self, check_button):
        """Set use/don't use locale encoding."""

        config.file.try_locale_encoding = check_button.get_active()

    def _on_encoding_remove_button_clicked(self, *args):
        """Remove the selected encoding."""

        row = self._get_selected_encoding_row()
        config.file.fallback_encodings.pop(row)
        self._reload_encoding_view()

    def _on_encoding_up_button_clicked(self, *args):
        """Move the selected encoding up in the list."""

        source_row = self._get_selected_encoding_row()
        encodings = config.file.fallback_encodings
        encodings.insert(source_row - 1, encodings.pop(source_row))
        self._reload_encoding_view()

        self._encoding_view.grab_focus()
        selection = self._encoding_view.get_selection()
        selection.select_path(source_row - 1)

    def _on_encoding_view_selection_changed(self, *args):
        """Set sensitivities based on current selection."""

        self._set_encoding_button_sensitivities()

    def _on_font_button_font_set(self, font_button):
        """Set custom font and emit signal."""

        font = font_button.get_font_name()
        config.editor.font = font
        self.emit('font-set', font)

    def _on_font_default_check_toggled(self, check_button):
        """Set default/custom font and send signal."""

        use_default = check_button.get_active()
        self._font_custom_label.set_sensitive(not use_default)
        self._font_button.set_sensitive(not use_default)

        config.editor.use_default_font = use_default
        self.emit('use-default-font-toggled', use_default)

    def _on_undo_levels_spin_button_value_changed(self, spin_button):
        """Set the amount of undo levels and send signal."""

        spin_button.update()
        levels = spin_button.get_value_as_int()

        config.editor.undo_levels = levels
        self.emit('undo-levels-changed', levels)

    def _on_undo_limit_radio_toggled(self, radio_button):
        """Limit/unlimit undo and send signal."""

        limit = self._undo_limit_radio.get_active()
        self._undo_levels_spin_button.set_sensitive(limit)

        config.editor.limit_undo = limit
        self.emit('limit-undo-toggled', limit)

    def _reload_encoding_view(self):
        """Reload the list of fallback encodings."""

        store = self._encoding_view.get_model()
        store.clear()
        for encoding in config.file.fallback_encodings:
            name = encodinglib.get_descriptive_name(encoding)
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

    def _set_from_config(self):
        """Set values from config."""

        # Locale encoding
        try_locale = config.file.try_locale_encoding
        self._encoding_locale_check.set_active(try_locale)

        # Fallback encodings
        self._reload_encoding_view()

        # Limit undo
        limit = config.editor.limit_undo
        self._undo_limit_radio.set_active(limit)
        self._undo_unlimited_radio.set_active(not limit)

        # Undo levels
        self._undo_levels_spin_button.set_value(config.editor.undo_levels)

        # Use default/custom font
        use_default = config.editor.use_default_font
        self._font_default_check.set_active(use_default)

        # Font
        self._font_button.set_font_name(self._get_custom_font())

    def _set_mnemonics(self, glade_xml):
        """Set mnemonics for widgets."""

        # Encoding view
        label = glade_xml.get_widget('encoding_label')
        label.set_mnemonic_widget(self._encoding_view)

        # Undo levels spin button
        label = glade_xml.get_widget('undo_levels_label')
        label.set_mnemonic_widget(self._undo_levels_spin_button)

        # Font button
        self._font_custom_label.set_mnemonic_widget(self._font_button)

    def show(self):
        """Show the dialog."""

        self._dialog.show()
