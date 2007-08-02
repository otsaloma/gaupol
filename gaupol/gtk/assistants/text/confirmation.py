# Copyright (C) 2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Page to confirm changes made after performing all tasks."""

import gaupol.gtk
import gobject
import gtk
import pango
_ = gaupol.i18n._

from .page import TextAssistantPage


class ConfirmationPage(TextAssistantPage):

    """Page to confirm changes made after performing all tasks."""

    def __init__(self):

        TextAssistantPage.__init__(self)
        self.application = None
        self.doc = None
        self.page_title = _("Confirm Changes")
        self.page_type = gtk.ASSISTANT_PAGE_CONFIRM

        name = "text-assistant-confirmation-page"
        self._glade_xml = gaupol.gtk.util.get_glade_xml(name)
        get_widget = self._glade_xml.get_widget
        self._mark_all_button = get_widget("mark_all_button")
        self._preview_button = get_widget("preview_button")
        self._remove_check = get_widget("remove_check")
        self._tree_view = get_widget("tree_view")
        self._unmark_all_button = get_widget("unmark_all_button")
        get_widget("vbox").reparent(self)

        self._init_tree_view()
        self._init_signal_handlers()
        self._init_values()

    def _add_text_column(self, index, title):
        """Add a multiline text column to the tree view."""

        renderer = gaupol.gtk.MultilineCellRenderer()
        renderer.set_show_lengths(False)
        renderer.props.editable = (index == 4)
        renderer.props.ellipsize = pango.ELLIPSIZE_END
        renderer.props.font = gaupol.gtk.util.get_font()
        renderer.props.yalign = 0
        column = gtk.TreeViewColumn(title, renderer, text=index)
        column.set_resizable(True)
        column.props.expand = True
        self._tree_view.append_column(column)

    @gaupol.gtk.util.asserted_return
    def _get_preview_sensitivity(self):
        """Return True if preview is possible."""

        row = self._get_selected_row()
        page = self._tree_view.get_model()[row][0]
        assert page is not None
        assert page.project.video_path is not None
        assert page.project.main_file is not None
        return True

    @gaupol.gtk.util.asserted_return
    def _get_selected_row(self):
        """Get the selected row in the tree view or None."""

        selection = self._tree_view.get_selection()
        store, itr = selection.get_selected()
        assert itr is not None
        return store.get_path(itr)[0]

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.gtk.util.connect(self, "_mark_all_button", "clicked")
        gaupol.gtk.util.connect(self, "_preview_button", "clicked")
        gaupol.gtk.util.connect(self, "_remove_check", "toggled")
        gaupol.gtk.util.connect(self, "_unmark_all_button", "clicked")

        selection = self._tree_view.get_selection()
        callback = self._on_tree_view_selection_changed
        selection.connect("changed", callback)

    def _init_tree_view(self):
        """Initialize the tree view."""

        cols = (object, gobject.TYPE_INT, gobject.TYPE_BOOLEAN)
        cols += (gobject.TYPE_STRING, gobject.TYPE_STRING)
        store = gtk.ListStore(*cols)
        self._tree_view.set_model(store)
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)

        renderer = gtk.CellRendererToggle()
        renderer.props.activatable = True
        renderer.props.xpad = 6
        callback = self._on_tree_view_cell_toggled
        renderer.connect("toggled", callback)
        column = gtk.TreeViewColumn(_("Accept"), renderer, active=2)
        column.set_resizable(True)
        self._tree_view.append_column(column)

        self._add_text_column(3, _("Original Text"))
        self._add_text_column(4, _("Corrected Text"))
        column = self._tree_view.get_column(2)
        renderer = column.get_cell_renderers()[0]
        callback = self._on_tree_view_cell_edited
        renderer.connect("edited", callback)

    def _init_values(self):
        """Initialize default values for widgets."""

        domain = gaupol.gtk.conf.text_assistant
        self._remove_check.set_active(domain.remove_blank)
        self._preview_button.set_sensitive(False)

    def _on_mark_all_button_clicked(self, *args):
        """Set all 'Accept' column values to True."""

        store = self._tree_view.get_model()
        for i in range(len(store)):
            store[i][2] = True

    def _on_preview_button_clicked(self, *args):
        """Preview the original text in a video player."""

        row = self._get_selected_row()
        page = self._tree_view.get_model()[row][0]
        index = self._tree_view.get_model()[row][1]
        time = page.project.subtitles[index].start_time
        self.application.preview(page, time, self.doc)

    def _on_remove_check_toggled(self, check_button):
        """Save the remove check button value."""

        domain = gaupol.gtk.conf.text_assistant
        domain.remove_blank = check_button.get_active()

    def _on_tree_view_cell_edited(self, renderer, row, text):
        """Edit the text in the 'Correct Text' column."""

        store = self._tree_view.get_model()
        store[row][4] = unicode(text)

    def _on_tree_view_cell_toggled(self, renderer, row):
        """Toggle the 'Accept' column value."""

        store = self._tree_view.get_model()
        store[row][2] = not store[row][2]

    def _on_tree_view_selection_changed(self, *args):
        """Update the preview button sensitivity."""

        sensitive = bool(self._get_preview_sensitivity())
        self._preview_button.set_sensitive(sensitive)

    def _on_unmark_all_button_clicked(self, *args):
        """Set all 'Accept' column values to False."""

        store = self._tree_view.get_model()
        for i in range(len(store)):
            store[i][2] = False

    def get_confirmed_changes(self):
        """Get a list of changes marked as accepted."""

        changes = []
        store = self._tree_view.get_model()
        for i in (x for x in range(len(store)) if store[x][2]):
            items = list(store[i])
            items.pop(2)
            changes.append(tuple(items))
        return changes

    def populate_tree_view(self, changes):
        """Populate the list of changes to texts."""

        self._tree_view.get_model().clear()
        store = self._tree_view.get_model()
        for (page, index, old, new) in changes:
            store.append([page, index, True, old, new])
        self._tree_view.get_selection().unselect_all()
