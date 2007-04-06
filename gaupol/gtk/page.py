# Copyright (C) 2005-2007 Osmo Salomaa
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


"""User interface for a single project.

Module variables:

    _TOOLTIPS: Template for tooltips to show on tab widgets
"""


import gtk
import os
import pango
import string

from gaupol import enclib
from gaupol.base import Observable
from gaupol.gtk import conf, const, util
from gaupol.gtk.i18n import _
from gaupol.gtk.index import *
from gaupol.project import Project
from .view import View


_TOOLTIP = \
"""<b>Path:</b> $path

<b>Format:</b> $format
<b>Encoding:</b> $encoding
<b>Newlines:</b> $newline"""


class Page(Observable):

    """User interface for a single project.

    Instance variables:

        edit_mode:  MODE constant, currently used in the view
        project:    The associated Project
        tab_label:  gtk.Label used in the tab_widget
        tab_widget: Widget to use in a notebook tab
        tooltips:   Markup-enabled gtk.Tooltips
        untitle:    Title used if the main document is unsaved
        view:       The associated View

    Signals:

        close-request (page)
    """

    _signals = ["close-request"]

    def __init__(self, counter=0):

        Observable.__init__(self)

        limit = conf.editor.limit_undo
        levels = conf.editor.undo_levels
        undo_levels = (levels if limit else None)

        self.edit_mode  = conf.editor.mode
        self.project    = Project(conf.editor.framerate, undo_levels)
        self.tab_label  = None
        self.tab_widget = None
        self.tooltips   = None
        self.untitle    = _("Untitled %d") % counter
        self.view       = View(conf.editor.mode)

        self._init_tooltips()
        self._init_widgets()
        self._init_signal_handlers()
        self.update_tab_label()

    def _get_positions(self):
        """Return times or frames depending on edit mode."""

        if self.edit_mode == const.MODE.TIME:
            return self.project.times
        if self.edit_mode == const.MODE.FRAME:
            return self.project.frames
        raise ValueError

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, "project", "main-file-opened")
        util.connect(self, "project", "main-texts-changed")
        util.connect(self, "project", "positions-changed")
        util.connect(self, "project", "subtitles-changed")
        util.connect(self, "project", "subtitles-inserted")
        util.connect(self, "project", "subtitles-removed")
        util.connect(self, "project", "translation-file-opened")
        util.connect(self, "project", "translation-texts-changed")

        def update_label(*args):
            self.update_tab_label()
        self.project.connect("main-file-opened", update_label)
        self.project.connect("main-file-saved", update_label)
        self.project.connect("notify::main_changed", update_label)
        self.project.connect("notify::tran_active", update_label)
        self.project.connect("notify::tran_changed", update_label)

        def update_levels(*args):
            limit = conf.editor.limit_undo
            limit = (conf.editor.undo_levels if limit else None)
            self.project.undo_levels = limit
        conf.editor.connect("notify::limit_undo", update_levels)
        conf.editor.connect("notify::undo_levels", update_levels)

    def _init_tooltips(self):
        """Initialize the markup-enabled tooltips."""

        def revert(label, *args):
            label.set_use_markup(True)
        self.tooltips = gtk.Tooltips()
        self.tooltips.force_window()
        label = self.tooltips.tip_label
        if label is not None:
            # pylint: disable-msg=E1101
            label.set_use_markup(True)
            label.connect("notify::use-markup", revert)

    def _init_widgets(self):
        """Initialize the widgets to use in a notebook tab."""

        self.tab_label = gtk.Label()
        self.tab_label.props.xalign = 0
        self.tab_label.set_ellipsize(pango.ELLIPSIZE_END)
        self.tab_label.set_max_width_chars(24)
        event_box = gtk.EventBox()
        event_box.add(self.tab_label)
        self.tooltips.set_tip(event_box, self.untitle)
        method = self._on_tab_event_box_enter_notify_event
        event_box.connect("enter-notify-event", method)

        def request_close(*args):
            self.emit("close-request")
        image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        width, height = image.size_request()
        button = gtk.Button()
        button.add(image)
        button.set_relief(gtk.RELIEF_NONE)
        button.set_focus_on_click(False)
        button.set_name("gaupol-tab-close-button")
        button.set_size_request(width + 2, height + 2)
        button.connect("clicked", request_close)
        self.tooltips.set_tip(button, _("Close project"))

        self.tab_widget = gtk.HBox(False, 4)
        self.tab_widget.pack_start(event_box, True, True, 0)
        self.tab_widget.pack_start(button, False, False, 0)
        self.tab_widget.set_data("button", button)
        self.tab_widget.set_data("event_box", event_box)
        self.tab_widget.show_all()

    def _on_project_main_file_opened(self, project, main_file):
        """Reload the entire view."""

        self.reload_view_all()

    @util.silent(AssertionError)
    def _on_project_main_texts_changed(self, project, rows):
        """Reload main texts in rows."""

        assert rows
        self.reload_view(rows, [MTXT])
        self.view.select_rows(rows)

    @util.silent(AssertionError)
    def _on_project_positions_changed(self, project, rows):
        """Reload positions in rows."""

        assert rows
        self.reload_view(rows, [SHOW, HIDE, DURN])
        self.view.select_rows(rows)

    @util.silent(AssertionError)
    def _on_project_subtitles_changed(self, project, rows):
        """Reload subtitles in rows."""

        assert rows
        self.reload_view(rows, [SHOW, HIDE, DURN, MTXT, TTXT])
        self.view.select_rows(rows)

    @util.silent(AssertionError)
    def _on_project_subtitles_inserted(self, project, rows):
        """Insert rows to the list store."""

        assert rows
        store = self.view.get_model()
        positions = self._get_positions()
        mains = self.project.main_texts
        trans = self.project.tran_texts
        for row in sorted(rows):
            item = [row + 1] + positions[row] + [mains[row], trans[row]]
            store.insert(row, item)
        # FIX: REMOVE WHEN THIS WORKS.
        self.assert_store()
        self.view.set_focus(rows[0])
        self.view.select_rows(rows)

    @util.silent(AssertionError)
    def _on_project_subtitles_removed(self, project, rows):
        """Remove rows from the list store."""

        assert rows
        store = self.view.get_model()
        for row in reversed(sorted(rows)):
            store.remove(store.get_iter(row))
        # FIX: REMOVE WHEN THIS WORKS.
        self.assert_store()
        if self.project.times:
            row = min(rows[0], len(self.project.times) - 1)
            col = self.view.get_focus()[1]
            self.view.set_focus(row, col)

    def _on_project_translation_file_opened(self, project, tran_file):
        """Reload the entire view."""

        self.reload_view_all()

    @util.silent(AssertionError)
    def _on_project_translation_texts_changed(self, project, rows):
        """Reload translation texts in rows."""

        assert rows
        self.reload_view(rows, [TTXT])
        self.view.select_rows(rows)

    @util.silent(AssertionError)
    def _on_tab_event_box_enter_notify_event(self, *args):
        """Update the text in the tooltip."""

        main_file = self.project.main_file
        assert main_file is not None
        event_box = self.tab_widget.get_data("event_box")
        tooltip = string.Template(_TOOLTIP).substitute(
            path=main_file.path,
            format=main_file.format.display_name,
            encoding=enclib.get_long_name(main_file.encoding),
            newline=main_file.newline.display_name,)
        self.tooltips.set_tip(event_box, tooltip)

    def assert_store(self):
        """Assert that store's data matches project's."""

        store = self.view.get_model()
        positions = self._get_positions()
        mains = self.project.main_texts
        trans = self.project.tran_texts
        for i in range(len(store)):
            assert store[i][1] == positions[i][0]
            assert store[i][2] == positions[i][1]
            assert store[i][3] == positions[i][2]
            assert store[i][4] == mains[i]
            assert store[i][5] == trans[i]

    def document_to_text_column(self, document):
        """Translate document index to text column index."""

        if document == const.DOCUMENT.MAIN:
            return MTXT
        if document == const.DOCUMENT.TRAN:
            return TTXT
        raise ValueError

    def get_main_basename(self):
        """Get the basename of the main document."""

        if self.project.main_file is not None:
            # pylint: disable-msg=E1101
            return os.path.basename(self.project.main_file.path)
        return self.untitle

    def get_main_corename(self):
        """Get the basename of the main document without extension."""

        # pylint: disable-msg=E1101
        if self.project.main_file is None:
            return self.untitle
        basename = os.path.basename(self.project.main_file.path)
        extension = self.project.main_file.format.extension
        if basename.endswith(extension):
            basename = basename[0:-len(extension)]
        return basename

    def get_translation_basename(self):
        """Get the basename of the translation document."""

        if self.project.tran_file is not None:
            # pylint: disable-msg=E1101
            return os.path.basename(self.project.tran_file.path)
        basename = self.get_main_corename()
        return _("%s translation") % basename

    def get_translation_corename(self):
        """Get basename of translation document without extension."""

        # pylint: disable-msg=E1101
        if self.project.tran_file is None:
            return self.get_translation_basename()
        basename = os.path.basename(self.project.tran_file.path)
        extension = self.project.tran_file.format.extension
        if basename.endswith(extension):
            basename = basename[0:-len(extension)]
        return basename

    def reload_view(self, rows, cols):
        """Reload the view in columns and rows."""

        store = self.view.get_model()
        for col in cols:
            if col in (SHOW, HIDE, DURN):
                positions = self._get_positions()
                get_data = lambda row: positions[row][col - 1]
            elif col == MTXT:
                texts = self.project.main_texts
                get_data = lambda row: texts[row]
            elif col == TTXT:
                texts = self.project.tran_texts
                get_data = lambda row: texts[row]
            for row in rows:
                store[row][col] = get_data(row)
        # FIX: REMOVE WHEN THIS WORKS.
        self.assert_store()

    def reload_view_all(self):
        """Clear and repopulate the entire view."""

        store = self.view.get_model()
        self.view.set_model(None)
        store.clear()
        positions = self._get_positions()
        mains = self.project.main_texts
        trans = self.project.tran_texts
        for row in range(len(self.project.times)):
            item = [row + 1] + positions[row] + [mains[row], trans[row]]
            store.append(item)
        self.view.set_model(store)
        # FIX: REMOVE WHEN THIS WORKS.
        self.assert_store()

    def text_column_to_document(self, col):
        """Translate text column constant to document constant."""

        if col == MTXT:
            return const.DOCUMENT.MAIN
        if col == TTXT:
            return const.DOCUMENT.TRAN
        if col is None:
            return None
        raise ValueError

    def update_tab_label(self):
        """Update the notebook tab label and return the title."""

        title = self.get_main_basename()
        if self.project.main_changed:
            title = "*%s" % title
        elif self.project.tran_active and self.project.tran_changed:
            title = "*%s" % title
        self.tab_label.set_text(title)
        return title
