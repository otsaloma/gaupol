# -*- coding: utf-8 -*-

# Copyright (C) 2011 Osmo Salomaa
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

"""Allow use of non-standard framerates."""

import aeidon
import gaupol
import os

from aeidon.i18n   import _
from gi.repository import Gtk


class AddFramerateDialog(gaupol.BuilderDialog):

    """Dialog for entering a custom framerate value."""

    _widgets = ["spin_button"]

    def __init__(self, parent):
        """Initialize an :class:`AddFramerateDialog` instance."""
        directory = os.path.abspath(os.path.dirname(__file__))
        ui_file_path = os.path.join(directory, "add-framerate-dialog.ui")
        gaupol.BuilderDialog.__init__(self, ui_file_path)
        self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("_Add"), Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_transient_for(parent)
        self.set_modal(True)

    def _on_response(self, *args):
        """Update spin button before dispatching response."""
        self._spin_button.update()

    def get_framerate(self):
        """Return framerate entered in the spin button."""
        return float(self._spin_button.get_value())


class PreferencesDialog(gaupol.BuilderDialog):

    """Dialog for editing a list of custom framerates."""

    _widgets = ["add_button", "remove_button", "toolbar", "tree_view"]

    def __init__(self, framerates, parent):
        """Initialize a :class:`PreferencesDialog` instance."""
        directory = os.path.abspath(os.path.dirname(__file__))
        ui_file_path = os.path.join(directory, "preferences-dialog.ui")
        gaupol.BuilderDialog.__init__(self, ui_file_path)
        self.set_default_response(Gtk.ResponseType.CLOSE)
        self.set_transient_for(parent)
        self.set_modal(True)
        self._init_toolbar()
        self._init_tree_view(framerates)
        self._remove_button.set_sensitive(False)
        gaupol.util.scale_to_content(self._tree_view,
                                     min_nchar=30,
                                     max_nchar=60,
                                     min_nlines=8,
                                     max_nlines=16)

    def get_framerates(self):
        """Return the defined custom framerates."""
        framerates = []
        store = self._tree_view.get_model()
        for i in range(len(store)):
            framerates.append(store[i][0])
        return sorted(framerates)

    def _get_selected_rows(self):
        """Return a sequence of the selected rows."""
        selection = self._tree_view.get_selection()
        paths = selection.get_selected_rows()[1]
        return list(map(gaupol.util.tree_path_to_row, paths))

    def _init_toolbar(self):
        """Initialize the tree view inline toolbar."""
        self._toolbar.set_icon_size(Gtk.IconSize.MENU)
        style = self._toolbar.get_style_context()
        style.add_class(Gtk.STYLE_CLASS_INLINE_TOOLBAR)
        theme = Gtk.IconTheme.get_default()
        # Tool buttons in the UI file are specified as symbolic icons
        # by name, found in adwaita-icon-theme, if missing in another
        # theme fall back to non-symbolic icons.
        if not all((theme.has_icon(self._add_button.get_icon_name()),
                    theme.has_icon(self._remove_button.get_icon_name()))):
            self._add_button.set_icon_name("list-add")
            self._remove_button.set_icon_name("list-remove")

    def _init_tree_view(self, framerates):
        """Initialize the tree view."""
        selection = self._tree_view.get_selection()
        selection.set_mode(Gtk.SelectionMode.MULTIPLE)
        selection.connect("changed", self._on_tree_view_selection_changed)
        store = Gtk.ListStore(float)
        for framerate in framerates:
            store.append((framerate,))
        store.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        self._tree_view.set_model(store)
        renderer = Gtk.CellRendererText()
        renderer.props.xalign = 1
        column = Gtk.TreeViewColumn("", renderer, text=0)
        column.set_sort_column_id(0)
        def format_framerate(column, renderer, store, itr, data):
            renderer.props.text = "{:.6f}".format(store.get_value(itr, 0))
        column.set_cell_data_func(renderer, format_framerate)
        self._tree_view.append_column(column)

    def _on_add_button_clicked(self, *args):
        """Add a new framerate."""
        dialog = AddFramerateDialog(self._dialog)
        response = gaupol.util.run_dialog(dialog)
        framerate = dialog.get_framerate()
        dialog.destroy()
        if response != Gtk.ResponseType.OK: return
        store = self._tree_view.get_model()
        store.append((framerate,))

    def _on_remove_button_clicked(self, *args):
        """Remove the selected framerate."""
        rows = self._get_selected_rows()
        store = self._tree_view.get_model()
        for row in reversed(sorted(rows)):
            path = gaupol.util.tree_row_to_path(row)
            store.remove(store.get_iter(path))
        if len(store) <= 0: return
        self._tree_view.set_cursor(max(row-1, 0))

    def _on_tree_view_selection_changed(self, *args):
        """Set the remove button sensitivity."""
        selection = self._tree_view.get_selection()
        n = selection.count_selected_rows()
        self._remove_button.set_sensitive(n > 0)


class CustomFrameratesExtension(gaupol.Extension):

    """Allow use of non-standard framerates."""

    def __init__(self):
        """Initialize a :class:`CustomFrameratesExtension` instance."""
        self.application = None
        self.conf = None
        self.framerates = []

    def _add_framerates(self):
        """Add custom framerates and corresponding UI elements."""
        self.framerates = []
        menu = self.application.get_menubar_section(
            "custom-framerates-placeholder")
        for value in sorted(self.conf.framerates):
            name = "FPS_{:.3f}".format(value).replace(".", "_")
            if hasattr(aeidon.framerates, name): continue
            setattr(aeidon.framerates, name, aeidon.EnumerationItem())
            framerate = getattr(aeidon.framerates, name)
            framerate.label = _("{:.3f} fps").format(value)
            framerate.value = float(value)
            self.framerates.append(framerate)
            with aeidon.util.silent(AttributeError):
                # Menubar not available when running unit tests.
                action = "win.set-framerate::{}".format(name)
                menu.append(framerate.label, action)

    def _remove_framerates(self):
        """Remove custom framerates and corresponding UI elements."""
        fallback = aeidon.framerates.FPS_23_976
        if gaupol.conf.editor.framerate in self.framerates:
            gaupol.conf.editor.framerate = fallback
        # Go through all application's pages and reset those set
        # to a custom framerate back to the default framerate.
        orig_page = self.application.get_current_page()
        for page in self.application.pages:
            if not page.project.framerate in self.framerates: continue
            self.application.set_current_page(page)
            action = self.application.get_action("set-framerate")
            action.activate(str(fallback))
        self.application.set_current_page(orig_page)
        for framerate in self.framerates:
            delattr(aeidon.framerates, str(framerate))
        with aeidon.util.silent(AttributeError):
            # Menubar not available when running unit tests.
            self.application.get_menubar_section(
                "custom-framerates-placeholder").remove_all()

    def setup(self, application):
        """Setup extension for use with `application`."""
        options = dict(framerates=[48.0])
        gaupol.conf.register_extension("custom_framerates", options)
        self.conf = gaupol.conf.extensions.custom_framerates
        self.application = application
        self.framerates = []
        self._add_framerates()

    def show_preferences_dialog(self, parent):
        """Show a dialog to edit list of custom framerates."""
        dialog = PreferencesDialog(self.conf.framerates, parent)
        gaupol.util.run_dialog(dialog)
        self.conf.framerates = list(dialog.get_framerates())
        dialog.destroy()
        self._remove_framerates()
        self._add_framerates()

    def teardown(self, application):
        """End use of extension with `application`."""
        self._remove_framerates()
        self.application = None
        self.conf = None
        self.framerates = []
