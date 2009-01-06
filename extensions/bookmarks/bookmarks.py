# Copyright (C) 2008 Osmo Salomaa
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

"""Marking subtitles for easy navigation."""

import gaupol.gtk
import gtk
import os
import pango
_ = gaupol.i18n._


class AddBookmarkDialog(gaupol.Delegate):

    """Dialog for editing the metadata for a bookmark to be added."""

    def __init__(self, parent, page):
        """Initialize an AddBookmarkDialog object."""

        directory = os.path.dirname(__file__)
        glade_file = os.path.join(directory, "add-bookmark-dialog.glade")
        glade_xml = gtk.glade.XML(glade_file)
        dialog = glade_xml.get_widget("dialog")
        gaupol.Delegate.__init__(self, dialog)
        self._dialog = dialog
        self._description_entry = glade_xml.get_widget("description_entry")
        self._subtitle_spin = glade_xml.get_widget("subtitle_spin")
        self._init_values(page)
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_values(self, page):
        """Initialize default values for widgets."""

        self._subtitle_spin.set_range(1, len(page.project.subtitles))
        row = page.view.get_selected_rows()[0]
        self._subtitle_spin.set_value(row + 1)
        description = page.project.subtitles[row].main_text
        description = description.replace("\n", " ")
        description = gaupol.re_any_tag.sub("", description)
        self._description_entry.set_text(description)
        self._description_entry.set_width_chars(30)

    def get_description(self):
        """Return description of the bookmarked subtitle."""

        return self._description_entry.get_text()

    def get_row(self):
        """Return the index of the bookmarked subtitle."""

        return self._subtitle_spin.get_value_as_int() - 1

    def run(self):
        """Show the dialog, run it and return response."""

        self._description_entry.grab_focus()
        self._dialog.show()
        return self._dialog.run()


class BookmarksExtension(gaupol.gtk.Extension):

    """Marking subtitles for easy navigation."""

    def __init__(self):
        """Initialize a BookmarksExtension object."""

        self._action_group = None
        self._bookmarks = {}
        self._conf = None
        self._search_entry = gtk.Entry()
        self._side_container = gtk.Alignment(0, 0, 1, 1)
        self._side_vbox = gtk.VBox(False, 6)
        self._tree_view = gtk.TreeView()
        self._uim_id = None
        self.application = None
        self._init_tree_view()
        self._init_signal_handlers()
        self._init_side_pane_widget()

    def _add_bookmark_column(self, page):
        """Add the bookmark column to the subtitle tree view."""

        def set_pixbuf(column, renderer, store, tree_iter):
            pixbuf = None
            if page in self._bookmarks:
                row = store.get_path(tree_iter)[0]
                if row in self._bookmarks[page]:
                    pixbuf = column.get_data("pixbuf")
            renderer.props.pixbuf = pixbuf
        renderer = gtk.CellRendererPixbuf()
        directory = os.path.dirname(__file__)
        pixbuf_path = os.path.join(directory, "bookmark.png")
        pixbuf = gtk.gdk.pixbuf_new_from_file(pixbuf_path)
        column = gtk.TreeViewColumn(_("Bm."), renderer)
        column.set_clickable(True)
        column.set_resizable(False)
        column.set_reorderable(True)
        column.set_visible(self._conf.show_column)
        label = page.view.get_header_label(_("Bm."))
        column.set_widget(label)
        column.set_data("pixbuf", pixbuf)
        column.set_data("identifier", "bookmark")
        column.set_cell_data_func(renderer, set_pixbuf)
        page.view.insert_column(column, 0)

    def _connect_page(self, page):
        """Connect to signals emitted by page."""

        page.connect("view-created", self._on_page_view_created)

    def _init_side_pane_widget(self):
        """Initialize the side pane widget."""

        self._side_vbox.set_border_width(2)
        hbox = gtk.HBox(False, 6)
        label = gtk.Label(_("Search:"))
        hbox.pack_start(label, False, False)
        hbox.pack_start(self._search_entry, True, True)
        self._side_vbox.pack_start(hbox, False, False)
        scroller = gtk.ScrolledWindow()
        scroller.set_policy(*((gtk.POLICY_AUTOMATIC,) * 2))
        scroller.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scroller.add(self._tree_view)
        self._side_vbox.pack_start(scroller, True, True)
        self._side_container.set_padding(0, 6, 2, 0)
        self._side_container.add(self._side_vbox)
        self._side_container.show_all()

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, "_search_entry", "changed")
        gaupol.util.connect(self, "_tree_view", "key-press-event")

    def _init_tree_view(self):
        """Initialize the side pane tree view."""

        store = gtk.ListStore(bool, int, str)
        store_filter = store.filter_new()
        store_filter.set_visible_column(0)
        self._tree_view.set_model(store_filter)
        self._tree_view.set_headers_visible(False)
        self._tree_view.set_rules_hint(True)
        self._tree_view.set_enable_search(False)
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.connect("changed", self._on_tree_view_selection_changed)
        renderer = gtk.CellRendererText()
        renderer.props.xalign = 1
        column = gtk.TreeViewColumn("", renderer, text=1)
        self._tree_view.append_column(column)
        renderer = gtk.CellRendererText()
        renderer.props.xalign = 0
        renderer.props.editable = True
        renderer.props.ellipsize = pango.ELLIPSIZE_END
        renderer.connect("edited", self._on_tree_view_cell_edited)
        column = gtk.TreeViewColumn("", renderer, text=2)
        self._tree_view.append_column(column)

    def _on_add_bookmark_activate(self, *args):
        """Add a bookmark for the current subtitle."""

        page = self.application.get_current_page()
        if not page in self._bookmarks:
            self._bookmarks[page] = {}
        dialog = AddBookmarkDialog(self.application.window, page)
        response = dialog.run()
        row = dialog.get_row()
        description = dialog.get_description()
        dialog.destroy()
        if response != gtk.RESPONSE_OK: return
        self._bookmarks[page][row] = description
        self._update_tree_view()

    def _on_application_page_added(self, application, page):
        """Connect to signals in added page."""

        self._connect_page(page)
        self._add_bookmark_column(page)

    def _on_application_page_closed(self, application, page):
        """Remove all data stored for closed page."""

        if page in self._bookmarks:
            del self._bookmarks[page]

    def _on_edit_bookmarks_activate(self, *args):
        """Show the bookmarks side pane."""

        pass

    def _on_next_bookmark_activate(self, *args):
        """Go to the next bookmarked subtitle."""

        page = self.application.get_current_page()
        row = page.view.get_selected_rows()[0]
        bookmarks = sorted(self._bookmarks[page].keys())
        bookmarks.append(bookmarks[0])
        for bookmark in bookmarks:
            if bookmark > row: break
        col = page.view.get_focus()[1]
        page.view.set_focus(bookmark, col)
        page.view.scroll_to_row(bookmark)

    def _on_page_view_created(self, page, view):
        """Add the bookmark column to the subtitle tree view."""

        self._add_bookmark_column(page)

    def _on_previous_bookmark_activate(self, *args):
        """Go to the previous bookmarked subtitle."""

        page = self.application.get_current_page()
        row = page.view.get_selected_rows()[0]
        bookmarks = sorted(self._bookmarks[page].keys())
        bookmarks.insert(0, bookmarks[-1])
        for bookmark in reversed(bookmarks):
            if bookmark < row: break
        col = page.view.get_focus()[1]
        page.view.set_focus(bookmark, col)
        page.view.scroll_to_row(bookmark)

    def _on_search_entry_changed(self, entry):
        """Check which bookmark descriptions match the new search string."""

        store_filter = self._tree_view.get_model()
        store = store_filter.get_model()
        pattern = entry.get_text().lower()
        for i, (visible, number, description) in enumerate(store):
            store[i][0] = (description.lower().find(pattern) >= 0)

    def _on_toggle_bookmark_column_toggled(self, action, *args):
        """Show or hide the bookmark column."""

        page = self.application.get_current_page()
        col = page.view.columns.BOOKMARK
        page.view.get_column(col).set_visible(action.get_active())
        self._conf.show_column = action.get_active()

    def _on_tree_view_cell_edited(self, renderer, path, new_text):
        """Update the description in the list store model of the tree view."""

        store = self._tree_view.get_model().get_model()
        store[path][2] = unicode(new_text)

    def _on_tree_view_key_press_event(self, tree_view, event):
        """Remove selected bookmark if Delete key pressed."""

        if event.keyval != gtk.keysyms.Delete: return
        selection = self._tree_view.get_selection()
        store, tree_iter = selection.get_selected()
        if tree_iter is None: return
        path = store.get_path(tree_iter)
        row = store[path][1] - 1
        del store[path]
        page = self.application.get_current_page()
        del self._bookmarks[page][row]

    def _on_tree_view_selection_changed(self, selection):
        """Jump to the subtitle of the selected bookmark."""

        store, tree_iter = selection.get_selected()
        if tree_iter is None: return
        path = store.get_path(tree_iter)
        row = store[path][1] - 1
        page = self.application.get_current_page()
        col = page.view.get_focus()[1]
        page.view.set_focus(row, col)
        page.view.scroll_to_row(row)

    def _update_tree_view(self):
        """Update the tree view to display bookmarks for the current page."""

        store_filter = self._tree_view.get_model()
        store = store_filter.get_model()
        store.clear()
        page = self.application.get_current_page()
        pattern = self._search_entry.get_text().lower()
        for row in sorted(self._bookmarks[page].keys()):
            description = self._bookmarks[page][row]
            visible = (description.lower().find(pattern) >= 0)
            store.append((visible, row + 1, description))

    def setup(self, application):
        """Setup extension for use with application."""

        self.application = application
        directory = os.path.dirname(__file__)
        spec_file = os.path.join(directory, "bookmarks.conf.spec")
        self.read_config(spec_file)
        self._conf = gaupol.gtk.conf.extensions.bookmarks
        self._action_group = gtk.ActionGroup("bookmarks")
        self._action_group.add_actions((
            ("show_bookmarks_menu", None, _("_Bookmarks")),
            ("add_bookmark", gtk.STOCK_ADD, _("_Add\342\200\246"),
             "<Control>D", _("Add a bookmark for the current subtitle"),
             self._on_add_bookmark_activate),
            ("edit_bookmarks", None, _("_Edit Bookmarks"),
             "<Control>B", "Show the bookmarks side pane",
             self._on_edit_bookmarks_activate),
            ("next_bookmark", None, _("_Next"),
             None, _("Go to the next bookmarked subtitle"),
             self._on_next_bookmark_activate),
            ("previous_bookmark", None, _("_Previous"),
             None, _("Go to the previous bookmarked subtitle"),
             self._on_previous_bookmark_activate),))
        self._action_group.add_toggle_actions((
            ("toggle_bookmark_column", None, _("_Bookmark"),
             None, _("Show or hide the bookmark column"),
             self._on_toggle_bookmark_column_toggled,
             self._conf.show_column),))
        application.uim.insert_action_group(self._action_group, -1)
        ui_file = os.path.join(directory, "bookmarks.ui.xml")
        self._uim_id = application.uim.add_ui_from_file(ui_file)
        application.uim.ensure_update()
        application.set_menu_notify_events("bookmarks")
        for page in application.pages:
            self._connect_page(page)
        gaupol.util.connect(self, "application", "page-added")
        gaupol.util.connect(self, "application", "page-closed")
        args = (self._side_container, "bookmarks", _("Bookmarks"))
        application.side_pane.add_page(*args)

    def teardown(self, application):
        """End use of extension with application."""

        self.application.uim.remove_ui(self._uim_id)
        self.application.uim.remove_action_group(self._action_group)
        self.application.uim.ensure_update()

    def update(self, application, page):
        """Update state of extension for application and active page."""

        action = self._action_group.get_action("add_bookmark")
        try: action.set_sensitive(len(page.view.get_selected_rows()) == 1)
        except AttributeError: action.set_sensitive(False)
        action = self._action_group.get_action("edit_bookmarks")
        action.set_sensitive(page is not None)
        action = self._action_group.get_action("next_bookmark")
        try: action.set_sensitive(bool(self._bookmarks[page]))
        except KeyError: action.set_sensitive(False)
        action = self._action_group.get_action("previous_bookmark")
        try: action.set_sensitive(bool(self._bookmarks[page]))
        except KeyError: action.set_sensitive(False)
