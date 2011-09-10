# Copyright (C) 2008-2010 Osmo Salomaa
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

"""Marking subtitles for easy navigation."""

import aeidon
import gaupol
import gtk
import os
import pango
_ = aeidon.i18n._


class AddBookmarkDialog(gaupol.BuilderDialog):

    """Dialog for editing metadata for a bookmark to be added."""

    _widgets = ("description_entry", "subtitle_spin")

    def __init__(self, parent, page):
        """Initialize an :class:`AddBookmarkDialog` object."""
        directory = os.path.abspath(os.path.dirname(__file__))
        ui_file_path = os.path.join(directory, "add-bookmark-dialog.ui")
        gaupol.BuilderDialog.__init__(self, ui_file_path)
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
        description = aeidon.re_any_tag.sub("", description)
        self._description_entry.set_text(description)
        self._description_entry.set_width_chars(30)

    def get_description(self):
        """Return description of the bookmarked subtitle."""
        return self._description_entry.get_text()

    def get_row(self):
        """Return index of the bookmarked subtitle."""
        return self._subtitle_spin.get_value_as_int() - 1

    def run(self):
        """Show the dialog, run it and return response."""
        self._description_entry.grab_focus()
        return gaupol.BuilderDialog.run(self)


class BookmarksExtension(gaupol.Extension):

    """Marking subtitles for easy navigation."""

    def __init__(self):
        """Initialize a :class:`BookmarksExtension` object."""
        self._action_group = None
        self._bookmarks = None
        self._conf = None
        self._search_entry = None
        self._side_container = None
        self._side_vbox = None
        self._tree_view = None
        self._uim_id = None
        self.application = None

    def _add_bookmark(self):
        """Add a bookmark for the selected subtitle in the current page."""
        page = self.application.get_current_page()
        if not page in self._bookmarks:
            self._bookmarks[page] = {}
        dialog = AddBookmarkDialog(self.application.window, page)
        response = gaupol.util.run_dialog(dialog)
        row = dialog.get_row()
        description = dialog.get_description()
        dialog.destroy()
        if response != gtk.RESPONSE_OK: return
        self._bookmarks[page][row] = description
        self._update_tree_view()
        self.update(self.application, page)

    def _add_bookmark_column(self, page):
        """Add a bookmark column to the subtitle tree view of page."""
        renderer = gtk.CellRendererPixbuf()
        directory = os.path.abspath(os.path.dirname(__file__))
        pixbuf_path = os.path.join(directory, "bookmark.png")
        pixbuf = gtk.gdk.pixbuf_new_from_file(pixbuf_path)
        # Translators: 'Bm.' is short for 'Bookmark'. It is used in the header
        # of a tree view column that contains 16 pixels wide pixbufs.
        column = gtk.TreeViewColumn(_("Bm."), renderer)
        column.set_clickable(True)
        column.set_resizable(False)
        column.set_reorderable(True)
        column.set_visible(self._conf.show_column)
        label = page.view.get_header_label(_("Bm."))
        label.set_tooltip_text(_("Bookmark"))
        column.set_widget(label)
        column.set_data("pixbuf", pixbuf)
        column.set_data("identifier", "bookmark")
        column.set_cell_data_func(renderer, self._set_cell_pixbuf, page)
        page.view.insert_column(column, 0)
        def toggle_bookmark(view, path, column, bookmark_column):
            if column is not bookmark_column: return
            self._toggle_bookmark(int(path[0]))
        page.view.connect("row-activated", toggle_bookmark, column)

    def _clear_attributes(self):
        """Set values of attributes to ``None``."""
        self._action_group = None
        self._bookmarks = None
        self._conf = None
        self._search_entry = None
        self._side_container = None
        self._side_vbox = None
        self._tree_view = None
        self._uim_id = None
        self.application = None

    def _connect_page(self, page):
        """Connect to signals emitted by `page`."""
        page.connect("view-created", self._on_page_view_created)
        callback = self._on_project_subtitles_inserted
        page.project.connect("subtitles-inserted", callback, page)
        callback = self._on_project_subtitles_removed
        page.project.connect("subtitles-removed", callback, page)
        callback = self._on_project_main_file_opened
        page.project.connect("main-file-opened", callback, page)
        callback = self._on_project_main_file_saved
        page.project.connect("main-file-saved", callback, page)

    def _disconnect_application(self, application):
        """Disconnect from signals emitted by ``application``."""
        callback = self._on_application_page_added
        self.application.disconnect("page-added", callback)
        callback = self._on_application_page_closed
        self.application.disconnect("page-closed", callback)
        callback = self._on_application_page_switched
        self.application.disconnect("page-switched", callback)

    def _disconnect_page(self, page):
        """Disconnect from signals emitted by ``page``."""
        callback = self._on_page_view_created
        page.disconnect("view-created", callback)
        callback = self._on_project_subtitles_inserted
        page.project.disconnect("subtitles-inserted", callback)
        callback = self._on_project_subtitles_removed
        page.project.disconnect("subtitles-removed", callback)
        callback = self._on_project_main_file_opened
        page.project.disconnect("main-file-opened", callback)
        callback = self._on_project_main_file_saved
        page.project.disconnect("main-file-saved", callback)

    def _get_bookmark_file_path(self, page):
        """Return the path to ``.gaupol-bookmarks`` file or ``None``."""
        main_file = page.project.main_file
        if main_file is None: return None
        path = main_file.path
        if path.endswith(main_file.format.extension):
            path = path[:-len(main_file.format.extension)]
        return "%s.gaupol-bookmarks" % path

    def _init_actions(self):
        """Initialize UI manager actions."""
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

        self.application.uim.insert_action_group(self._action_group, -1)
        directory = os.path.abspath(os.path.dirname(__file__))
        ui_file_path = os.path.join(directory, "bookmarks.ui.xml")
        self._uim_id = self.application.uim.add_ui_from_file(ui_file_path)
        self.application.uim.ensure_update()
        self.application.set_menu_notify_events("bookmarks")

    def _init_attributes(self, application):
        """Initialize default values for attributes."""
        self._action_group = gtk.ActionGroup("bookmarks")
        self._bookmarks = {}
        self._conf = gaupol.conf.extensions.bookmarks
        self._search_entry = gtk.Entry()
        self._side_container = gtk.Alignment(0, 0, 1, 1)
        self._side_vbox = gtk.VBox(False, 6)
        self._tree_view = gtk.TreeView()
        self._uim_id = None
        self.application = application

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
        aeidon.util.connect(self, "_search_entry", "changed")
        aeidon.util.connect(self, "_tree_view", "key-press-event")
        aeidon.util.connect(self, "application", "page-added")
        aeidon.util.connect(self, "application", "page-closed")
        aeidon.util.connect(self, "application", "page-switched")

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
        """Add a bookmark for the selected subtitle in the current page."""
        self._add_bookmark()

    def _on_application_page_added(self, application, page):
        """Connect to signals in `page` and read bookmarks."""
        self._prepare_page(page)

    def _on_application_page_closed(self, application, page):
        """Remove all data stored for `page`."""
        if page in self._bookmarks:
            del self._bookmarks[page]

    def _on_application_page_switched(self, application, page):
        """Update the side pane to show `page`'s bookmarks."""
        self._update_tree_view()

    def _on_edit_bookmarks_activate(self, *args):
        """Show the bookmarks page in the side pane."""
        action = self.application.get_action("toggle_side_pane")
        action.set_active(True)
        self.application.side_pane.set_current_page(self._side_container)
        self._search_entry.grab_focus()

    def _on_next_bookmark_activate(self, *args):
        """Go to the next bookmarked subtitle."""
        # pylint: disable=W0631
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
        """Add a bookmark column to `view`."""
        self._add_bookmark_column(page)

    def _on_project_main_file_opened(self, project, main_file, page):
        """Read bookmarks from ``.gaupol-bookmarks`` file."""
        self._read_bookmarks(page)

    def _on_project_main_file_saved(self, project, main_file, page):
        """Write bookmarks to a ``.gaupol-bookmarks`` file."""
        self._write_bookmarks(page)

    def _on_project_subtitles_inserted(self, project, rows, page):
        """Update rows of bookmarks with `rows` inserted before them."""
        if not page in self._bookmarks: return
        store_filter = self._tree_view.get_model()
        store = store_filter.get_model()
        for irow in rows:
            for crow in sorted(list(self._bookmarks[page].keys()), reverse=True):
                if crow < irow: continue
                description = self._bookmarks[page][crow]
                del self._bookmarks[page][crow]
                self._bookmarks[page][crow + 1] = description
        self._update_tree_view()

    def _on_project_subtitles_removed(self, project, rows, page):
        """Remove bookmarks and update rows of those remaining."""
        if not page in self._bookmarks: return
        store_filter = self._tree_view.get_model()
        store = store_filter.get_model()
        for crow in list(self._bookmarks[page].keys()):
            if crow in rows: del self._bookmarks[page][crow]
        for crow in sorted(self._bookmarks[page].keys()):
            count = sum(1 for x in rows if x < crow)
            if count == 0: continue
            description = self._bookmarks[page][crow]
            del self._bookmarks[page][crow]
            self._bookmarks[page][crow - count] = description
        self._update_tree_view()

    def _on_previous_bookmark_activate(self, *args):
        """Go to the previous bookmarked subtitle."""
        # pylint: disable=W0631
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
        """Check which bookmark descriptions match with new search string."""
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
        """Update description in the list store model of the tree view."""
        store = self._tree_view.get_model().get_model()
        store[path][2] = str(new_text)
        page = self.application.get_current_page()

    def _on_tree_view_key_press_event(self, tree_view, event):
        """Remove selected bookmark if ``Delete`` key pressed."""
        if event.keyval != gtk.keysyms.Delete: return
        selection = self._tree_view.get_selection()
        store, tree_iter = selection.get_selected()
        if tree_iter is None: return
        path = store.get_path(tree_iter)
        self._remove_bookmark(store[path][1] - 1)

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

    def _prepare_page(self, page):
        """Prepare data structures and signal handlers for `page`."""
        if not page in self._bookmarks:
            self._bookmarks[page] = {}
        self._connect_page(page)
        self._add_bookmark_column(page)
        self._read_bookmarks(page)

    def _read_bookmarks(self, page):
        """Read bookmarks for `page` from ``.gaupol-bookmarks`` file."""
        if not page in self._bookmarks:
            self._bookmarks[page] = {}
        self._bookmarks[page].clear()
        path = self._get_bookmark_file_path(page)
        if path is None: return
        if not os.path.isfile(path): return
        encoding = page.project.main_file.encoding
        for line in aeidon.util.readlines(path, encoding):
            row, description = line.split(" ", 1)
            self._bookmarks[page][int(row) - 1] = description
        self._update_tree_view()

    def _remove_bookmark(self, row):
        """Remove existing bookmark in `row` of the current page."""
        store = self._tree_view.get_model()
        path = None
        for i in range(len(store)):
            if store[i][1] - 1 == row:
                path = i
        if path is not None:
            del store[path]
        page = self.application.get_current_page()
        if row in self._bookmarks[page]:
            del self._bookmarks[page][row]
        # Update the pixbuf column immediately.
        page_store = page.view.get_model()
        page_store.row_changed(row, page_store.get_iter(row))
        self.update(self.application, page)

    def _set_cell_pixbuf(self, column, renderer, store, tree_iter, page):
        """Set the pixbuf property of `renderer`."""
        pixbuf = None
        if page in self._bookmarks:
            row = store.get_path(tree_iter)[0]
            if row in self._bookmarks[page]:
                pixbuf = column.get_data("pixbuf")
        renderer.props.pixbuf = pixbuf

    def _toggle_bookmark(self, row):
        """Remove existing bookmark or add new bookmark to the current page."""
        page = self.application.get_current_page()
        if row in self._bookmarks[page]:
            return self._remove_bookmark(row)
        return self._add_bookmark()

    def _update_tree_view(self):
        """Update tree view to display bookmarks for the current page."""
        store_filter = self._tree_view.get_model()
        store = store_filter.get_model()
        store.clear()
        page = self.application.get_current_page()
        if not page in self._bookmarks: return
        pattern = self._search_entry.get_text().lower()
        for row in sorted(self._bookmarks[page].keys()):
            description = self._bookmarks[page][row]
            visible = (description.lower().find(pattern) >= 0)
            store.append((visible, row + 1, description))

    def _write_bookmarks(self, page):
        """Write bookmarks from `page` to a ``.gaupol-bookmarks`` file."""
        if not page in self._bookmarks: return
        path = self._get_bookmark_file_path(page)
        if path is None: return
        if not self._bookmarks[page]:
            # Remove bookmark file when all bookmarks are removed.
            if os.path.isfile(path): os.remove(path)
            return
        lines = []
        for row in sorted(self._bookmarks[page].keys()):
            lines.append("%d %s" % (row + 1, self._bookmarks[page][row]))
        text = os.linesep.join(lines) + os.linesep
        encoding = page.project.main_file.encoding
        aeidon.util.write(path, text, encoding)

    def setup(self, application):
        """Setup extension for use with `application`."""
        gaupol.conf.register_extension("bookmarks", {"show_column": True})
        self._init_attributes(application)
        self._init_tree_view()
        self._init_signal_handlers()
        self._init_side_pane_widget()
        self._init_actions()
        for page in application.pages:
            self._prepare_page(page)
        application.side_pane.add_page(self._side_container,
                                       "bookmarks",
                                       _("Bookmarks"))

    def teardown(self, application):
        """End use of extension with `application`."""
        application.uim.remove_ui(self._uim_id)
        application.uim.remove_action_group(self._action_group)
        application.uim.ensure_update()
        for page in application.pages:
            col = page.view.columns.BOOKMARK
            column = page.view.get_column(col)
            page.view.remove_column(column)
            self._disconnect_page(page)
        self._disconnect_application(application)
        application.side_pane.remove_page(self._side_container)
        self._clear_attributes()

    def update(self, application, page):
        """Update state of extension for `application` and active `page`."""
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
