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
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""User interface container and controller for :class:`aeidon.Project`."""

import aeidon
import gaupol
import os
import sys

from aeidon.i18n   import _
from gi.repository import Gtk
from gi.repository import Pango

__all__ = ("Page",)


class Page(aeidon.Observable):

    """
    User interface container and controller for :class:`aeidon.Project`.

    :ivar edit_mode: :attr:`aeidon.modes` item corresponding to editing mode
    :ivar project: The associated :class:`aeidon.Project` instance
    :ivar tab_label: :class:`Gtk.Label` contained in :attr:`tab_widget`
    :ivar tab_widget: Widget that can be placed in a notebook tab
    :ivar untitle: Title used if :attr:`project.main_file` is unsaved
    :ivar view: The associated :class:`gaupol.View` instance

    Signals and their arguments for callback functions:
     * ``close-request``: page
     * ``view-created``: page, view

    This class represents one page in a notebook of user interfaces for
    projects. The view is updated automatically when project data changes.
    """
    signals = ("close-request", "view-created")

    def __init__(self, count=0):
        """Initialize a :class:`Page` instance."""
        aeidon.Observable.__init__(self)
        self.edit_mode = gaupol.conf.editor.mode
        self.project = None
        self.tab_label = None
        self.tab_widget = None
        self.untitle = _("Untitled {:d}").format(count)
        self.view = gaupol.View(self.edit_mode)
        self._init_project()
        self._init_widgets()
        self._init_signal_handlers()
        self.update_tab_label()
        self.emit("view-created", self.view)

    def document_to_text_column(self, doc):
        """Translate document enumeration to view's column enumeration."""
        if doc == aeidon.documents.MAIN:
            return self.view.columns.MAIN_TEXT
        if doc == aeidon.documents.TRAN:
            return self.view.columns.TRAN_TEXT
        raise ValueError("Invalid document: {!r}"
                         .format(doc))

    def get_basename(self, doc):
        """Return basename of `doc`."""
        if doc == aeidon.documents.MAIN:
            return self.get_main_basename()
        if doc == aeidon.documents.TRAN:
            return self.get_translation_basename()
        raise ValueError("Invalid document: {!r}"
                         .format(doc))

    def get_main_basename(self):
        """Return basename of the main document."""
        if self.project.main_file is not None:
            return os.path.basename(self.project.main_file.path)
        return self.untitle

    def _get_subtitle_value(self, row, field):
        """Return value of subtitle data for `row` and `field`."""
        mode = self.edit_mode
        subtitle = self.project.subtitles[row]
        if field == gaupol.fields.START:
            return subtitle.get_start(mode)
        if field == gaupol.fields.END:
            return subtitle.get_end(mode)
        if field == gaupol.fields.DURATION:
            if mode == aeidon.modes.TIME:
                return subtitle.duration_seconds
            if mode == aeidon.modes.FRAME:
                return subtitle.duration_frame
            raise ValueError("Invalid mode: {!r}"
                             .format(mode))

        if field == gaupol.fields.MAIN_TEXT:
            return subtitle.main_text
        if field == gaupol.fields.TRAN_TEXT:
            return subtitle.tran_text
        raise ValueError("Invalid field: {!r}"
                         .format(field))

    def _get_tab_close_button(self):
        """Initialize and return a tab close button."""
        button = Gtk.Button()
        style = button.get_style_context()
        style.add_class("gaupol-tab-close-button")
        image = gaupol.util.get_icon_image("window-close-symbolic",
                                           "window-close",
                                           Gtk.IconSize.MENU)

        button.add(image)
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.set_focus_on_click(False)
        width = image.get_preferred_width()[1]
        height = image.get_preferred_height()[1]
        padding = 6 if sys.platform == "win32" else 2
        button.set_size_request(width + padding, height + padding)
        request_close = lambda x, self: self.emit("close-request")
        button.connect("clicked", request_close, self)
        button.set_tooltip_text(_("Close project"))
        return button

    def get_translation_basename(self):
        """Return basename of the translation document."""
        if self.project.tran_file is not None:
            return os.path.basename(self.project.tran_file.path)
        basename = self.get_main_basename()
        if self.project.main_file is not None:
            extension = self.project.main_file.format.extension
            if basename.endswith(extension):
                basename = basename[:-len(extension)]
        return _("{} translation").format(basename)

    def _init_project(self):
        """Initialize :class:`aeidon.Project` with proper properties."""
        framerate = gaupol.conf.editor.framerate
        self.project = aeidon.Project(framerate)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""
        self._init_signal_handlers_for_data()
        self._init_signal_handlers_for_tab_label()

    def _init_signal_handlers_for_data(self):
        """Initialize signal handlers for project data updates."""
        aeidon.util.connect(self, "project", "main-file-opened")
        aeidon.util.connect(self, "project", "main-texts-changed")
        aeidon.util.connect(self, "project", "positions-changed")
        aeidon.util.connect(self, "project", "subtitles-changed")
        aeidon.util.connect(self, "project", "subtitles-inserted")
        aeidon.util.connect(self, "project", "subtitles-removed")
        aeidon.util.connect(self, "project", "translation-file-opened")
        aeidon.util.connect(self, "project", "translation-texts-changed")

    def _init_signal_handlers_for_tab_label(self):
        """Initialize signal handlers for tab label updates."""
        aeidon.util.connect(self, "tab_label", "query-tooltip")
        update_label = lambda *args: args[-1].update_tab_label()
        self.project.connect("main-file-opened", update_label, self)
        self.project.connect("main-file-saved", update_label, self)
        self.project.connect("notify::main_changed", update_label, self)
        self.project.connect("notify::tran_changed", update_label, self)

    def _init_widgets(self):
        """Initialize widgets to use in a notebook tab."""
        self.tab_label = Gtk.Label()
        self.tab_label.set_halign(Gtk.Align.CENTER)
        self.tab_label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        # Set minimum width for tab label. The actual width taken
        # depends on window size, amount of tabs and notebook
        # child properties 'tab-expand' and 'tab-fill'.
        width = gaupol.util.char_to_px(24)
        self.tab_label.set_size_request(width, -1)
        self.tab_label.set_tooltip_text(self.untitle)
        button = self._get_tab_close_button()
        box = gaupol.util.new_hbox(spacing=4)
        gaupol.util.pack_start_expand(box, self.tab_label)
        gaupol.util.pack_start(box, button)
        box.gaupol_button = button
        self.tab_widget = Gtk.EventBox()
        self.tab_widget.add(box)
        self.tab_widget.set_visible_window(False)
        self.tab_widget.show_all()

    def _on_project_main_file_opened(self, *args):
        """Reload the entire view."""
        self.reload_view_all()
        gaupol.util.iterate_main()

    def _on_project_main_texts_changed(self, project, rows):
        """Reload and select main texts in rows."""
        if not rows: return
        fields = (gaupol.fields.MAIN_TEXT,)
        self.reload_view(rows, fields)
        if not self.view.get_focus()[0] in rows:
            col = self.view.columns.MAIN_TEXT
            self.view.set_focus(rows[0], col)
        self.view.select_rows(rows)
        gaupol.util.iterate_main()

    def _on_project_positions_changed(self, project, rows):
        """Reload and select positions in rows."""
        if not rows: return
        enum = gaupol.fields
        fields = (enum.START, enum.END, enum.DURATION)
        self.reload_view(rows, fields)
        if not self.view.get_focus()[0] in rows:
            self.view.set_focus(rows[0])
        self.view.select_rows(rows)
        gaupol.util.iterate_main()

    def _on_project_subtitles_changed(self, project, rows):
        """Reload and select subtitles in rows."""
        if not rows: return
        fields = [x for x in gaupol.fields]
        fields.remove(gaupol.fields.NUMBER)
        self.reload_view(rows, fields)
        if not self.view.get_focus()[0] in rows:
            self.view.set_focus(rows[0])
        self.view.select_rows(rows)
        gaupol.util.iterate_main()

    def _on_project_subtitles_inserted(self, project, rows):
        """Insert rows to the view and select them."""
        if not rows: return
        mode = self.edit_mode
        store = self.view.get_model()
        for row in sorted(rows):
            subtitle = self.project.subtitles[row]
            store.insert(row)
            store[row][0] = row + 1
            store[row][1] = subtitle.get_start(mode)
            store[row][2] = subtitle.get_end(mode)
            if mode == aeidon.modes.TIME:
                store[row][3] = subtitle.duration_seconds
            if mode == aeidon.modes.FRAME:
                store[row][3] = subtitle.duration_frame
            store[row][4] = subtitle.main_text
            store[row][5] = subtitle.tran_text
        self.view.set_focus(rows[0])
        self.view.select_rows(rows)
        gaupol.util.iterate_main()

    def _on_project_subtitles_removed(self, project, rows):
        """Remove rows from the view."""
        if not rows: return
        store = self.view.get_model()
        if len(rows) > 50:
            # Unset and later reset the model if removing a large amount
            # of rows, because a large batch of separate live updates
            # directly made to the view are slow.
            self.view.set_model(None)
        for row in reversed(sorted(rows)):
            path = gaupol.util.tree_row_to_path(row)
            store.remove(store.get_iter(path))
        if len(rows) > 50:
            self.view.set_model(store)
        if self.project.subtitles:
            row = min(rows[0], len(self.project.subtitles)-1)
            col = self.view.get_focus()[1]
            self.view.set_focus(row, col)
        gaupol.util.iterate_main()

    def _on_project_translation_file_opened(self, *args):
        """Reload the entire view."""
        self.reload_view_all()
        gaupol.util.iterate_main()

    def _on_project_translation_texts_changed(self, project, rows):
        """Reload and select translation texts in rows."""
        if not rows: return
        fields = (gaupol.fields.TRAN_TEXT,)
        self.reload_view(rows, fields)
        if not self.view.get_focus()[0] in rows:
            col = self.view.columns.TRAN_TEXT
            self.view.set_focus(rows[0], col)
        self.view.select_rows(rows)
        gaupol.util.iterate_main()

    def _on_tab_label_query_tooltip(self, label, x, y, keyboard, tooltip):
        """Update the text in the tab tooltip."""
        if self.project.main_file is None: return
        path = self.project.main_file.path
        format = self.project.main_file.format
        encoding = self.project.main_file.encoding
        encoding = aeidon.encodings.code_to_long_name(encoding)
        newline = self.project.main_file.newline
        tooltip.set_markup("{}\n{}\n{}\n{}".format(
            "<b>{}</b> {}".format(_("Path:"), path),
            "<b>{}</b> {}".format(_("Format:"), format.label),
            "<b>{}</b> {}".format(_("Encoding:"), encoding),
            "<b>{}</b> {}".format(_("Newlines:"), newline.label)))

        return True # to show the tooltip.

    def reload_view(self, rows, fields):
        """Reload the view in `rows` and `fields`."""
        store = self.view.get_model()
        for row, field in ((x, y) for x in rows for y in fields):
            value = self._get_subtitle_value(row, field)
            store[row][field] = value

    def reload_view_all(self):
        """Clear and repopulate the entire view."""
        store = self.view.get_model()
        self.view.set_model(None)
        store.clear()
        mode = self.edit_mode
        for i, subtitle in enumerate(self.project.subtitles):
            store.insert(i)
            store[i][0] = i + 1
            store[i][1] = subtitle.get_start(mode)
            store[i][2] = subtitle.get_end(mode)
            if mode == aeidon.modes.TIME:
                store[i][3] = subtitle.duration_seconds
            if mode == aeidon.modes.FRAME:
                store[i][3] = subtitle.duration_frame
            store[i][4] = subtitle.main_text
            store[i][5] = subtitle.tran_text
        self.view.set_model(store)

    def text_column_to_document(self, col):
        """Translate view's column enumeration to document enumeration."""
        if col == self.view.columns.MAIN_TEXT:
            return aeidon.documents.MAIN
        if col == self.view.columns.TRAN_TEXT:
            return aeidon.documents.TRAN
        raise ValueError("Invalid column: {!r}"
                         .format(col))

    def update_tab_label(self):
        """Update the notebook tab label and return title."""
        title = self.get_main_basename()
        if self.project.main_changed or self.project.tran_changed:
            title = "*{}".format(title)
        # Adwaita theme uses bold notebook tab labels since 3.12.
        self.tab_label.set_markup("<b>{}</b>".format(title))
        return title
