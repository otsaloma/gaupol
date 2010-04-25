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

"""Dialog for editing preferences."""

import aeidon
import gaupol
import gtk
import pango
_ = aeidon.i18n._

__all__ = ("PreferencesDialog",)


class EditorPage(aeidon.Delegate, gaupol.BuilderDialog):

    """Editor preferences page."""

    _widgets = ("editor_default_font_check",
                "editor_font_button",
                "editor_font_hbox",
                "editor_length_cell_check",
                "editor_length_combo",
                "editor_length_edit_check",
                "editor_length_hbox")

    def __init__(self, master, application):
        """Initialize an :class:`EditorPage` object."""
        aeidon.Delegate.__init__(self, master)
        self._set_attributes(self._widgets, "editor_")
        self.application = application
        self._init_length_combo()
        self._init_values()

    def _get_custom_font(self):
        """Return custom font as string."""
        context = gtk.Label().get_pango_context()
        font_desc = context.get_font_description()
        font = gaupol.conf.editor.custom_font
        custom_font_desc = pango.FontDescription(font)
        font_desc.merge(custom_font_desc, True)
        return font_desc.to_string()

    def _init_length_combo(self):
        """Initialize the line length combo box."""
        store = gtk.ListStore(str)
        for label in (x.label for x in gaupol.length_units):
            store.append((label,))
        self._length_combo.set_model(store)
        renderer = gtk.CellRendererText()
        self._length_combo.pack_start(renderer, True)
        self._length_combo.add_attribute(renderer, "text", 0)

    def _init_values(self):
        """Initialize default values for widgets."""
        use_custom = gaupol.conf.editor.use_custom_font
        self._default_font_check.set_active(not use_custom)
        self._font_hbox.set_sensitive(use_custom)
        self._font_button.set_font_name(self._get_custom_font())
        show_cell = gaupol.conf.editor.show_lengths_cell
        show_edit = gaupol.conf.editor.show_lengths_edit
        self._length_hbox.set_sensitive(show_cell or show_edit)
        self._length_cell_check.set_active(show_cell)
        self._length_edit_check.set_active(show_edit)
        self._length_combo.set_active(gaupol.conf.editor.length_unit)

    def _on_default_font_check_toggled(self, check_button):
        """Save default font usage."""
        use_custom = not check_button.get_active()
        gaupol.conf.editor.use_custom_font = use_custom
        self._font_hbox.set_sensitive(use_custom)

    def _on_font_button_font_set(self, font_button):
        """Save custom font."""
        gaupol.conf.editor.custom_font = font_button.get_font_name()

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


class ExtensionPage(aeidon.Delegate, gaupol.BuilderDialog):

    """Extension activation and preferences page."""

    _widgets = ("extensions_about_button",
                "extensions_help_button",
                "extensions_preferences_button",
                "extensions_tree_view")

    def __init__(self, master, application):
        """Initialize an :class:`ExtensionPage` object."""
        aeidon.Delegate.__init__(self, master)
        self._set_attributes(self._widgets, "extensions_")
        self.application = application
        self.manager = self.application.extension_manager
        self._init_tree_view()
        self._init_values()
        self._init_sensitivities()

    def _get_selected_module(self):
        """Return the selected module in the tree view or ``None``."""
        selection = self._tree_view.get_selection()
        store, itr = selection.get_selected()
        if itr is None: return None
        return store.get_value(itr, 0)

    def _init_sensitivities(self):
        """Initialize button sensitivities."""
        self._about_button.set_sensitive(False)
        self._help_button.set_sensitive(False)
        self._preferences_button.set_sensitive(False)

    def _init_tree_view(self):
        """Initialize the tree view."""
        store = gtk.ListStore(str, bool, str)
        self._tree_view.set_model(store)
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.connect("changed", self._on_tree_view_selection_changed)
        renderer = gtk.CellRendererToggle()
        renderer.props.activatable = True
        renderer.props.xpad = 6
        renderer.connect("toggled", self._on_tree_view_cell_toggled)
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
            markup = "<b>%s</b>\n%s" % (metadata.get_name(),
                                        metadata.get_description())

            extensions.append((module, markup))
        extensions.sort(key=lambda x: x[1])
        for module, markup in extensions:
            active = module in gaupol.conf.extensions.active
            store.append((module, active, markup))

    def _on_about_button_clicked(self, *args):
        """Construct and show a :class:`gtk.AboutDialog` for extension."""
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
            copyright = "\n".join(metadata.get_field_list("Copyright"))
            dialog.set_copyright(copyright)
        if metadata.has_field("Website"):
            dialog.set_website(metadata.get_field("Website"))
            label = _("%s Extension Website") %  metadata.get_name()
            dialog.set_website_label(label)
        if metadata.has_field("Authors"):
            dialog.set_authors(metadata.get_field_list("Authors"))
        gaupol.util.flash_dialog(dialog)

    def _on_about_dialog_url_clicked(self, dialog, url):
        """Open website in a web browser."""
        gaupol.util.show_uri(url)

    def _on_help_button_clicked(self, *args):
        """Show extension's own documentation."""
        module = self._get_selected_module()
        self.manager.show_help(module)

    def _on_preferences_button_clicked(self, *args):
        """Show extension's preferences dialog."""
        module = self._get_selected_module()
        self.manager.show_preferences_dialog(module, self._dialog)

    def _on_tree_view_cell_toggled(self, renderer, path):
        """Activate or deactivate toggled extension."""
        store = self._tree_view.get_model()
        module = store[path][0]
        active = store[path][1]
        if active: # Deactivating extension.
            try: self.manager.teardown_extension(module)
            except gaupol.DependencyError:
                title = _("Cannot deactivate extension")
                message = _('Extension "%s" is required by other extensions.')
                message = message % store[path][2]
                dialog = gaupol.ErrorDialog(self._dialog, title, message)
                dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
                gaupol.util.flash_dialog(dialog)
            else: # Deactivation successful.
                gaupol.conf.extensions.active.remove(module)
        else: # Activating extension.
            self.manager.setup_extension(module)
            gaupol.conf.extensions.active.append(module)
        for row in store:
            row[1] = self.manager.is_active(row[0])
        selection = self._tree_view.get_selection()
        selection.emit("changed")

    def _on_tree_view_selection_changed(self, *args):
        """Set sensitivities of buttons."""
        module = self._get_selected_module()
        have_selection = self._get_selected_module() is not None
        self._about_button.set_sensitive(have_selection)
        if module in gaupol.conf.extensions.active:
            has_help = self.manager.has_help(module)
            self._help_button.set_sensitive(has_help)
            has_preferences = self.manager.has_preferences_dialog(module)
            self._preferences_button.set_sensitive(has_preferences)
        else: # Cannot query unimported extensions.
            self._help_button.set_sensitive(False)
            self._preferences_button.set_sensitive(False)


class FilePage(aeidon.Delegate, gaupol.BuilderDialog):

    """File preferences page."""

    __metaclass__ = aeidon.Contractual

    _widgets = ("file_add_button",
                "file_auto_check",
                "file_down_button",
                "file_tree_view",
                "file_locale_check",
                "file_remove_button",
                "file_up_button")

    def __init__(self, master, application):
        """Initialize a :class:`FilePage` object."""
        aeidon.Delegate.__init__(self, master)
        self._set_attributes(self._widgets, "file_")
        self.application = application
        self._init_tree_view()
        self._init_values()

    def _get_selected_row(self):
        """Return the selected row in the tree view or ``None``."""
        selection = self._tree_view.get_selection()
        store, itr = selection.get_selected()
        if itr is None: return None
        return store.get_path(itr)[0]

    def _init_tree_view(self):
        """Initialize the fallback encoding tree view."""
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        update = lambda x, self: self._set_sensitivities()
        selection.connect("changed", update, self)
        store = gtk.ListStore(str)
        self._tree_view.set_model(store)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("", renderer, text=0)
        self._tree_view.append_column(column)

    def _init_values(self):
        """Initialize default values for widgets."""
        self._auto_check.set_active(gaupol.conf.encoding.try_auto)
        self._auto_check.set_sensitive(aeidon.util.chardet_available())
        self._locale_check.set_active(gaupol.conf.encoding.try_locale)
        self._reload_tree_view()

    def _on_add_button_clicked(self, *args):
        """Add a new fallback encoding."""
        dialog = gaupol.EncodingDialog(self._dialog)
        response = gaupol.util.run_dialog(dialog)
        encoding = dialog.get_encoding()
        dialog.destroy()
        if response != gtk.RESPONSE_OK: return
        if encoding is None: return
        if encoding in gaupol.conf.encoding.fallback: return
        gaupol.conf.encoding.fallback.append(encoding)
        self._reload_tree_view()
        self._tree_view.grab_focus()
        store = self._tree_view.get_model()
        self._tree_view.set_cursor(len(store) - 1)

    def _on_auto_check_toggled_require(self, check_button):
        assert aeidon.util.chardet_available()

    def _on_auto_check_toggled(self, check_button):
        """Save encoding auto-detection usage."""
        gaupol.conf.encoding.try_auto = check_button.get_active()

    def _on_down_button_clicked_require(self, *args):
        row = self._get_selected_row()
        store = self._tree_view.get_model()
        assert row < len(store) - 1

    def _on_down_button_clicked(self, *args):
        """Move the selected fallback encoding down."""
        row = self._get_selected_row()
        encodings = gaupol.conf.encoding.fallback
        encodings.insert(row + 1, encodings.pop(row))
        self._reload_tree_view()
        self._tree_view.grab_focus()
        self._tree_view.set_cursor(row + 1)

    def _on_locale_check_toggled(self, check_button):
        """Save locale encoding usage."""
        gaupol.conf.encoding.try_locale = check_button.get_active()

    def _on_remove_button_clicked_require(self, *args):
        self._get_selected_row() is not None

    def _on_remove_button_clicked(self, *args):
        """Remove the selected fallback encoding."""
        row = self._get_selected_row()
        gaupol.conf.encoding.fallback.pop(row)
        self._reload_tree_view()
        self._tree_view.grab_focus()
        store = self._tree_view.get_model()
        if len(store) <= 0: return
        self._tree_view.set_cursor(max(row - 1, 0))

    def _on_up_button_clicked_require(self, *args):
        self._get_selected_row() > 0

    def _on_up_button_clicked(self, *args):
        """Move the selected fallback encoding up."""
        row = self._get_selected_row()
        encodings = gaupol.conf.encoding.fallback
        encodings.insert(row - 1, encodings.pop(row))
        self._reload_tree_view()
        self._tree_view.grab_focus()
        self._tree_view.set_cursor(row - 1)

    def _reload_tree_view(self):
        """Reload the fallback encoding tree view."""
        store = self._tree_view.get_model()
        store.clear()
        for encoding in gaupol.conf.encoding.fallback:
            store.append((aeidon.encodings.code_to_long_name(encoding),))
        self._set_sensitivities()

    def _set_sensitivities(self):
        """Set the fallback tree view button sensitivities."""
        store = self._tree_view.get_model()
        row = self._get_selected_row()
        self._remove_button.set_sensitive(row >= 0)
        self._up_button.set_sensitive(row > 0)
        self._down_button.set_sensitive(0 <= row < len(store) - 1)


class PreviewPage(aeidon.Delegate, gaupol.BuilderDialog):

    """Preview preferences page."""

    _widgets = ("preview_app_combo",
                "preview_command_entry",
                "preview_force_utf_8_check",
                "preview_offset_spin")

    def __init__(self, master, application):
        """Initialize a :class:`PreviewPage` object."""
        aeidon.Delegate.__init__(self, master)
        self._set_attributes(self._widgets, "preview_")
        self.application = application
        self._init_app_combo()
        self._init_values()

    def _init_app_combo(self):
        """Initialize the application combo box."""
        store = gtk.ListStore(str)
        self._app_combo.set_model(store)
        for label in (x.label for x in aeidon.players):
            store.append((label,))
        store.append((gaupol.COMBO_SEPARATOR,))
        store.append((_("Custom"),))
        renderer = gtk.CellRendererText()
        self._app_combo.pack_start(renderer, True)
        self._app_combo.add_attribute(renderer, "text", 0)
        self._app_combo.set_row_separator_func(gaupol.util.separate_combo)

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


class PreferencesDialog(gaupol.BuilderDialog):

    """Dialog for editing preferences."""

    def __init__(self, parent, application):
        """Initialize a :class:`PreferencesDialog` object."""
        gaupol.BuilderDialog.__init__(self,
                                      "preferences-dialog.ui",
                                      connect_signals=False)

        self._editor_page = EditorPage(self, application)
        self._extension_page = ExtensionPage(self, application)
        self._file_page = FilePage(self, application)
        self._preview_page = PreviewPage(self, application)
        self._builder.connect_signals(self._get_callbacks())
        self.set_transient_for(parent)
        self.set_default_response(gtk.RESPONSE_CLOSE)


    def _get_callbacks(self):
        """Return a dictionary mapping names to callback methods."""
        callbacks = {}
        for page in (self._editor_page,
                     self._extension_page,
                     self._file_page,
                     self._preview_page):

            for name in filter(lambda x: x.startswith("_on_"), dir(page)):
                callbacks[name] = getattr(page, name)
        return callbacks
