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

"""Dialog for editing preferences."""

import gaupol.gtk
import gtk
import pango
_ = gaupol.i18n._

__all__ = ("PreferencesDialog",)


class _EditorPage(gaupol.Delegate):

    """Editor preferences page."""

    def __init__(self, master):

        gaupol.Delegate.__init__(self, master)
        get_widget = self._glade_xml.get_widget
        self._default_font_check = get_widget("editor_default_font_check")
        self._font_button = get_widget("editor_font_button")
        self._font_hbox = get_widget("editor_font_hbox")
        self._length_cell_check = get_widget("editor_length_cell_check")
        self._length_combo = get_widget("editor_length_combo")
        self._length_edit_check = get_widget("editor_length_edit_check")
        self._length_hbox = get_widget("editor_length_hbox")
        self.conf = gaupol.gtk.conf.editor

        self._init_length_combo()
        self._init_values()
        self._init_signal_handlers()

    def _get_custom_font(self):
        """Return custom font as string."""

        context = gtk.Label().get_pango_context()
        font_desc = context.get_font_description()
        font = self.conf.custom_font
        custom_font_desc = pango.FontDescription(font)
        font_desc.merge(custom_font_desc, True)
        return font_desc.to_string()

    def _init_length_combo(self):
        """Initialize the line length combo box."""

        store = self._length_combo.get_model()
        for label in (x.label for x in gaupol.gtk.length_units):
            store.append((label,))

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, "_default_font_check", "toggled")
        gaupol.util.connect(self, "_font_button", "font-set")
        gaupol.util.connect(self, "_length_cell_check", "toggled")
        gaupol.util.connect(self, "_length_combo", "changed")
        gaupol.util.connect(self, "_length_edit_check", "toggled")

    def _init_values(self):
        """Initialize default values for widgets."""

        use_custom = self.conf.use_custom_font
        self._default_font_check.set_active(not use_custom)
        self._font_hbox.set_sensitive(use_custom)
        self._font_button.set_font_name(self._get_custom_font())

        cell = self.conf.show_lengths_cell
        edit = self.conf.show_lengths_edit
        self._length_hbox.set_sensitive(cell or edit)
        self._length_cell_check.set_active(cell)
        self._length_edit_check.set_active(edit)
        self._length_combo.set_active(self.conf.length_unit)

    def _on_default_font_check_toggled(self, check_button):
        """Save the default font usage."""

        use_custom = not check_button.get_active()
        self.conf.use_custom_font = use_custom
        self._font_hbox.set_sensitive(use_custom)

    def _on_font_button_font_set(self, font_button):
        """Save the custom font."""

        self.conf.custom_font = font_button.get_font_name()

    def _on_length_cell_check_toggled(self, check_button):
        """Save the line length showage on cells."""

        self.conf.show_lengths_cell = check_button.get_active()
        cell = self.conf.show_lengths_cell
        edit = self.conf.show_lengths_edit
        self._length_hbox.set_sensitive(cell or edit)

    def _on_length_combo_changed(self, combo_box):
        """Save the line length unit."""

        index = combo_box.get_active()
        self.conf.length_unit = gaupol.gtk.length_units[index]

    def _on_length_edit_check_toggled(self, check_button):
        """Save the line length showage on text views."""

        self.conf.show_lengths_edit = check_button.get_active()
        cell = self.conf.show_lengths_cell
        edit = self.conf.show_lengths_edit
        self._length_hbox.set_sensitive(cell or edit)


class _ExtensionPage(gaupol.Delegate):

    """Extension activation and preferences page."""

    def __init__(self, master, application):

        gaupol.Delegate.__init__(self, master)
        get_widget = self._glade_xml.get_widget
        self._about_button = get_widget("extensions_about_button")
        self._help_button = get_widget("extensions_help_button")
        self._preferences_button = get_widget("extensions_preferences_button")
        self._tree_view = get_widget("extensions_tree_view")
        self.application = application
        self.conf = gaupol.gtk.conf.extensions
        self.manager = self.application.extension_manager

        self._init_tree_view()
        self._init_values()
        self._init_sensitivities()
        self._init_signal_handlers()

    def _get_selected_module(self):
        """Return the selected module in the tree view or None."""

        selection = self._tree_view.get_selection()
        store, itr = selection.get_selected()
        if itr is None: return None
        return store.get_value(itr, 0)

    def _init_sensitivities(self):
        """Initialize button sensitivities."""

        self._about_button.set_sensitive(False)
        self._help_button.set_sensitive(False)
        self._preferences_button.set_sensitive(False)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, "_about_button", "clicked")
        gaupol.util.connect(self, "_help_button", "clicked")
        gaupol.util.connect(self, "_preferences_button", "clicked")

    def _init_tree_view(self):
        """Initialize the tree view."""

        store = gtk.ListStore(str, bool, str)
        self._tree_view.set_model(store)
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        callback = self._on_tree_view_selection_changed
        selection.connect("changed", callback)

        renderer = gtk.CellRendererToggle()
        renderer.props.activatable = True
        renderer.props.xpad = 6
        callback = self._on_tree_view_cell_toggled
        renderer.connect("toggled", callback)
        column = gtk.TreeViewColumn("", renderer, active=1)
        self._tree_view.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.props.ellipsize = pango.ELLIPSIZE_END
        column = gtk.TreeViewColumn("", renderer, markup=2)
        self._tree_view.append_column(column)

    def _init_values(self):
        """Initialize default values for widgets."""

        store = self._tree_view.get_model()
        extensions = []
        for module in self.manager.get_modules():
            metadata = self.manager.get_metadata(module)
            if metadata.get_field_boolean("Hidden", False): continue
            name = metadata.get_name()
            description = metadata.get_description()
            markup = "<b>%s</b>\n%s" % (name, description)
            extensions.append((module, markup))
        extensions.sort(key=lambda x: x[1])
        for module, markup in extensions:
            active = module in self.conf.active
            store.append((module, active, markup))

    def _on_about_button_clicked(self, *args):
        """Show an automatically constructed about dialog."""

        module = self._get_selected_module()
        metadata = self.manager.get_metadata(module)
        dialog = gtk.AboutDialog()
        dialog.set_transient_for(self._dialog)
        gtk.about_dialog_set_url_hook(self._on_about_dialog_url_clicked)
        dialog.set_program_name(metadata.get_name())
        dialog.set_comments(metadata.get_description())
        dialog.set_logo_icon_name("gaupol")
        if metadata.has_field("Version"):
            dialog.set_version(metadata.get_field("Version"))
        if metadata.has_field("Copyright"):
            dialog.set_copyright(metadata.get_field("Copyright"))
        if metadata.has_field("Website"):
            dialog.set_website(metadata.get_field("Website"))
            label = _("%s Extension Website") %  metadata.get_name()
            dialog.set_website_label(label)
        if metadata.has_field("Authors"):
            dialog.set_authors(metadata.get_field_list("Authors"))
        self.flash_dialog(dialog)

    def _on_about_dialog_url_clicked(self, dialog, url):
        """Open website in a web browser."""

        gaupol.util.browse_url(url)

    def _on_help_button_clicked(self, *args):
        """Show whatever form documentation the extension has."""

        module = self._get_selected_module()
        self.manager.show_help(module)

    def _on_preferences_button_clicked(self, *args):
        """Show the extension's preferences dialog."""

        module = self._get_selected_module()
        self.manager.show_preferences_dialog(module, self._dialog)

    def _on_tree_view_cell_toggled(self, renderer, path):
        """Toggle the check button value."""

        store = self._tree_view.get_model()
        module = store[path][0]
        active = store[path][1]
        if active:
            self.manager.teardown_extension(module)
            self.conf.active.remove(module)
        else:
            self.manager.setup_extension(module)
            self.conf.active.append(module)
        store[path][1] = not active
        selection = self._tree_view.get_selection()
        selection.emit("changed")

    def _on_tree_view_selection_changed(self, *args):
        """Set the sensitivities of the buttons."""

        module = self._get_selected_module()
        have_selection = self._get_selected_module() is not None
        self._about_button.set_sensitive(have_selection)
        sensitive = have_selection and (module in self.conf.active)
        if module in self.conf.active:
            sensitive = self.manager.has_help(module)
            self._help_button.set_sensitive(sensitive)
            sensitive = self.manager.has_preferences_dialog(module)
            self._preferences_button.set_sensitive(sensitive)
        else: # Cannot query unimported extensions.
            self._help_button.set_sensitive(False)
            self._preferences_button.set_sensitive(False)


class _FilePage(gaupol.Delegate):

    """File preferences page."""

    __metaclass__ = gaupol.Contractual

    def __init__(self, master):

        gaupol.Delegate.__init__(self, master)
        get_widget = self._glade_xml.get_widget
        self._add_button = get_widget("file_add_button")
        self._auto_check = get_widget("file_auto_check")
        self._down_button = get_widget("file_down_button")
        self._tree_view = get_widget("file_tree_view")
        self._locale_check = get_widget("file_locale_check")
        self._remove_button = get_widget("file_remove_button")
        self._up_button = get_widget("file_up_button")
        self.conf = gaupol.gtk.conf.encoding

        self._init_tree_view()
        self._init_values()
        self._init_signal_handlers()

    def _get_selected_row(self):
        """Return the selected row in the tree view or None."""

        selection = self._tree_view.get_selection()
        store, itr = selection.get_selected()
        if itr is None: return None
        return store.get_path(itr)[0]

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, "_add_button", "clicked")
        gaupol.util.connect(self, "_auto_check", "toggled")
        gaupol.util.connect(self, "_down_button", "clicked")
        gaupol.util.connect(self, "_locale_check", "toggled")
        gaupol.util.connect(self, "_remove_button", "clicked")
        gaupol.util.connect(self, "_up_button", "clicked")

        update = lambda x, self: self._set_sensitivities()
        selection = self._tree_view.get_selection()
        selection.connect("changed", update, self)

    def _init_tree_view(self):
        """Initialize the tree view."""

        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        store = gtk.ListStore(str)
        self._tree_view.set_model(store)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("", renderer, text=0)
        self._tree_view.append_column(column)

    def _init_values(self):
        """Initialize default values for widgets."""

        self._auto_check.set_active(self.conf.try_auto)
        self._auto_check.set_sensitive(gaupol.util.chardet_available())
        self._locale_check.set_active(self.conf.try_locale)
        self._reload_tree_view()

    def _on_add_button_clicked(self, *args):
        """Add a new fallback encoding."""

        dialog = gaupol.gtk.EncodingDialog(self._dialog)
        response = self.run_dialog(dialog)
        encoding = dialog.get_encoding()
        dialog.destroy()
        if response != gtk.RESPONSE_OK: return
        if encoding is None: return
        if encoding in self.conf.fallbacks: return
        self.conf.fallbacks.append(encoding)
        self._reload_tree_view()
        self._tree_view.grab_focus()
        store = self._tree_view.get_model()
        self._tree_view.set_cursor(len(store) - 1)

    def _on_auto_check_toggled_require(self, check_button):
        assert gaupol.util.chardet_available()

    def _on_auto_check_toggled(self, check_button):
        """Save the encoding auto-detection usage."""

        self.conf.try_auto = check_button.get_active()

    def _on_down_button_clicked_require(self, *args):
        row = self._get_selected_row()
        store = self._tree_view.get_model()
        assert row < len(store) - 1

    def _on_down_button_clicked(self, *args):
        """Move the selected fallback encoding down."""

        row = self._get_selected_row()
        encodings = self.conf.fallbacks
        encodings.insert(row + 1, encodings.pop(row))
        self._reload_tree_view()
        self._tree_view.grab_focus()
        self._tree_view.set_cursor(row + 1)

    def _on_locale_check_toggled(self, check_button):
        """Save the locale encoding usage."""

        self.conf.try_locale = check_button.get_active()

    def _on_remove_button_clicked_require(self, *args):
        self._get_selected_row() is not None

    def _on_remove_button_clicked(self, *args):
        """Remove the selected encoding."""

        row = self._get_selected_row()
        self.conf.fallbacks.pop(row)
        self._reload_tree_view()
        self._tree_view.grab_focus()
        store = self._tree_view.get_model()
        if len(store) <= 0: return
        self._tree_view.set_cursor(max(row - 1, 0))

    def _on_up_button_clicked_require(self, *args):
        self._get_selected_row() > 0

    def _on_up_button_clicked(self, *args):
        """Move the selected encoding up."""

        row = self._get_selected_row()
        encodings = self.conf.fallbacks
        encodings.insert(row - 1, encodings.pop(row))
        self._reload_tree_view()
        self._tree_view.grab_focus()
        self._tree_view.set_cursor(row - 1)

    def _reload_tree_view(self):
        """Reload the tree view."""

        store = self._tree_view.get_model()
        store.clear()
        for encoding in self.conf.fallbacks:
            store.append((gaupol.encodings.code_to_long_name(encoding),))
        self._set_sensitivities()

    def _set_sensitivities(self):
        """Set the tree view button sensitivities."""

        store = self._tree_view.get_model()
        row = self._get_selected_row()
        self._remove_button.set_sensitive(row >= 0)
        self._up_button.set_sensitive(row > 0)
        self._down_button.set_sensitive(0 <= row < len(store) - 1)


class _PreviewPage(gaupol.Delegate):

    """Preview preferences page."""

    def __init__(self, master):

        gaupol.Delegate.__init__(self, master)
        get_widget = self._glade_xml.get_widget
        self._app_combo = get_widget("preview_app_combo")
        self._command_entry = get_widget("preview_command_entry")
        self._force_utf_8_check = get_widget("preview_force_utf_8_check")
        self._offset_spin = get_widget("preview_offset_spin")
        self.conf = gaupol.gtk.conf.preview

        self._init_app_combo()
        self._init_values()
        self._init_signal_handlers()

    def _init_app_combo(self):
        """Initialize the application combo box."""

        store = self._app_combo.get_model()
        for label in (x.label for x in gaupol.players):
            store.append((label,))
        store.append((gaupol.gtk.COMBO_SEPARATOR,))
        store.append((_("Custom"),))
        function = gaupol.gtk.util.separate_combo
        self._app_combo.set_row_separator_func(function)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, "_app_combo", "changed")
        gaupol.util.connect(self, "_command_entry", "changed")
        gaupol.util.connect(self, "_force_utf_8_check", "toggled")
        gaupol.util.connect(self, "_offset_spin", "value-changed")

    def _init_values(self):
        """Initialize default values for widgets."""

        if not self.conf.use_custom:
            player = self.conf.video_player
            self._app_combo.set_active(player)
        else: # Use custom command.
            store = self._app_combo.get_model()
            self._app_combo.set_active(len(store) - 1)
        command = gaupol.gtk.util.get_preview_command()
        self._command_entry.set_text(command)
        self._command_entry.set_editable(self.conf.use_custom)
        self._force_utf_8_check.set_active(self.conf.force_utf_8)
        self._offset_spin.set_value(self.conf.offset)

    def _on_app_combo_changed(self, combo_box):
        """Save the video player and show it's command."""

        index = combo_box.get_active()
        self.conf.use_custom = not (index in gaupol.players)
        if index in gaupol.players:
            player = gaupol.players[index]
            self.conf.video_player = player
        command = gaupol.gtk.util.get_preview_command()
        self._command_entry.set_text(command)
        self._command_entry.set_editable(self.conf.use_custom)

    def _on_command_entry_changed(self, entry):
        """Save the custom command."""

        if not self.conf.use_custom: return
        self.conf.custom_command = entry.get_text()

    def _on_force_utf_8_check_toggled(self, check_button):
        """Save forced UTF-8 preview setting."""

        self.conf.force_utf_8 = check_button.get_active()
        command = gaupol.gtk.util.get_preview_command()
        self._command_entry.set_text(command)

    def _on_offset_spin_value_changed(self, spin_button):
        """Save the start position offset."""

        self.conf.offset = spin_button.get_value()


class PreferencesDialog(gaupol.gtk.GladeDialog):

    """Dialog for editing preferences."""

    def __init__(self, parent, application):

        gaupol.gtk.GladeDialog.__init__(self, "preferences.glade")
        self._editor_page = _EditorPage(self)
        self._extension_page = _ExtensionPage(self, application)
        self._file_page = _FilePage(self)
        self._preview_page = _PreviewPage(self)

        self.set_transient_for(parent)
        self.set_default_response(gtk.RESPONSE_CLOSE)
