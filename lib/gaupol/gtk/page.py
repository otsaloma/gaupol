# Copyright (C) 2005-2006 Osmo Salomaa
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


"""User interface for a single project."""


from gettext import gettext as _
import os

import gobject
import gtk
import pango

from gaupol.base.project     import Project
from gaupol.gtk              import cons
from gaupol.gtk.icons        import *
from gaupol.gtk.util         import conf, gtklib
from gaupol.gtk.view         import View


class Page(gobject.GObject):

    """
    User interface for a single project.

    Instance variables:

        edit_mode:      Mode constant
        project:        Project
        tab_label:      gtk.Label on tab
        tab_menu_label: gtk.Label in tab menu
        tooltips:       gtk.Tooltips
        untitle:        Name for unsaved document
        view:           View

    """

    __gsignals__ = {
        'closed': (
            gobject.SIGNAL_RUN_LAST,
            None,
            ()
        ),
    }

    def __init__(self, counter=0):

        gobject.GObject.__init__(self)

        undo_limit = None
        if conf.editor.limit_undo:
            undo_limit = conf.editor.undo_levels

        self.edit_mode      = conf.editor.mode
        self.project        = Project(conf.editor.framerate, undo_limit)
        self.tab_label      = None
        self.tab_menu_label = None
        self.tooltips       = gtk.Tooltips()
        self.untitle        = _('Untitled %d') % counter
        self.view           = View(conf.editor.mode)

    def _on_close_button_clicked(self, *args):
        """Emit closed signal."""

        self.emit('closed')

    def _get_positions(self):
        """Return project.times or project.frames depending on edit mode."""

        if self.edit_mode == cons.Mode.TIME:
            return self.project.times
        elif self.edit_mode == cons.Mode.FRAME:
            return self.project.frames

    def assert_store(self):
        """Assert that store's data matches project's."""

        store = self.view.get_model()
        positions = self._get_positions()

        for row in range(len(store)):
            assert store[row][0] == row + 1
            assert store[row][1] == positions[row][0]
            assert store[row][2] == positions[row][1]
            assert store[row][3] == positions[row][2]
            assert store[row][4] == self.project.main_texts[row]
            assert store[row][5] == self.project.tran_texts[row]

    def document_to_text_column(self, document):
        """Translate document constant to text column constant."""

        if document == MAIN:
            return MTXT
        if document == TRAN:
            return TTXT

    def get_main_basename(self):
        """Get basename of main document."""

        try:
            return os.path.basename(self.project.main_file.path)
        except AttributeError:
            return self.untitle

    def get_main_corename(self):
        """Get basename of main document without extension."""

        try:
            basename = os.path.basename(self.project.main_file.path)
            format = self.project.main_file.format
        except AttributeError:
            return self.untitle

        extension = cons.Format.extensions[format]
        if basename.endswith(extension):
            return basename[0:-len(extension)]
        else:
            return basename

    def get_main_filename(self):
        """Get filename of main document."""

        try:
            return self.project.main_file.path
        except AttributeError:
            return self.untitle

    def get_translation_basename(self):
        """Get basename of translation document."""

        if self.project.tran_file is not None:
            return os.path.basename(self.project.tran_file.path)
        elif self.project.main_file is not None:
            basename = self.get_main_corename()
        else:
            basename = self.untitle

        # Translators: Suggested translation file basename,
        # "MAIN BASENAME translation".
        return _('%s translation') % basename

    def get_translation_corename(self):
        """Get basename of translation document without extension."""

        try:
            basename = os.path.basename(self.project.tran_file.path)
            format = self.project.tran_file.format
        except AttributeError:
            return self.get_translation_basename()

        extension = cons.Format.extensions[format]
        if basename.endswith(extension):
            return basename[0:-len(extension)]
        else:
            return basename

    def init_tab_widget(self):
        """Initialize and return notebook tab widget."""

        title = self.get_main_basename()
        self.tab_label = gtk.Label(title)
        self.tab_label.props.xalign = 0
        self.tab_label.set_ellipsize(pango.ELLIPSIZE_MIDDLE)
        self.tab_label.set_max_width_chars(24)
        event_box = gtk.EventBox()
        event_box.add(self.tab_label)
        self.tooltips.set_tip(event_box, self.get_main_filename())

        self.tab_menu_label = gtk.Label(title)
        self.tab_menu_label.props.xalign = 0

        image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        width, height = image.size_request()
        button = gtk.Button()
        button.add(image)
        button.set_relief(gtk.RELIEF_NONE)
        button.set_size_request(width + 2, height + 2)
        button.connect('clicked', self._on_close_button_clicked)

        tab_widget = gtk.HBox(False, 4)
        tab_widget.pack_start(event_box, True , True , 0)
        tab_widget.pack_start(button   , False, False, 0)
        tab_widget.show_all()

        return tab_widget

    def reload_after(self, row):
        """Reload view after row."""

        store      = self.view.get_model()
        positions  = self._get_positions()
        main_texts = self.project.main_texts
        tran_texts = self.project.tran_texts

        # Selection must be cleared before removing rows to avoid selection
        # constantly changing and emitting the "changed" signal if the row
        # being removed was selected.
        selected_rows = self.view.get_selected_rows()
        self.view.select_rows([])

        while len(store) > row:
            store.remove(store.get_iter(row))
        for i in range(row, len(self.project.times)):
            store.append(
                [i + 1] + positions[i] + [main_texts[i], tran_texts[i]])

        for i in reversed(range(len(selected_rows))):
            if selected_rows[i] >= len(self.project.times):
                selected_rows.pop(i)
        self.view.select_rows(selected_rows)

    def reload_all(self):
        """
        Reload entire view.

        Selection, focus and scroll position are lost.
        """
        store = self.view.get_model()
        self.view.set_model(None)
        store.clear()
        positions  = self._get_positions()
        main_texts = self.project.main_texts
        tran_texts = self.project.tran_texts

        for i in range(len(self.project.times)):
            store.append(
                [i + 1] + positions[i] + [main_texts[i], tran_texts[i]])

        self.view.set_model(store)

    def reload_columns(self, cols, rows=None):
        """Reload view column by column."""

        store = self.view.get_model()
        rows = rows or range(len(store))

        for col in cols:
            if col == NUMB:
                for row in rows:
                    store[row][col] = row + 1
            elif col in (SHOW, HIDE, DURN):
                positions = self._get_positions()
                base_col = col - 1
                for row in rows:
                    store[row][col] = positions[row][base_col]
            elif col == MTXT:
                main_texts = self.project.main_texts
                for row in rows:
                    store[row][col] = main_texts[row]
            elif col == TTXT:
                tran_texts = self.project.tran_texts
                for row in rows:
                    store[row][col] = tran_texts[row]

    def reload_rows(self, rows):
        """Reload view by full rows."""

        store      = self.view.get_model()
        positions  = self._get_positions()
        main_texts = self.project.main_texts
        tran_texts = self.project.tran_texts

        for row in rows:
            store[row] = [row + 1] + positions[row] + \
                         [main_texts[row], tran_texts[row]]

    def text_column_to_document(self, col):
        """Translate text column constant to document constant."""

        if col == MTXT:
            return MAIN
        if col == TTXT:
            return TRAN

    def update_tab_labels(self):
        """
        Update text in notebook tab labels.

        Return tab label title.
        """
        title = self.get_main_basename()
        if self.project.main_changed:
            title = '*' + title
        elif self.project.tran_active and self.project.tran_changed:
            title = '*' + title

        self.tab_label.set_text(title)
        self.tab_menu_label.set_text(title)
        event_box = gtklib.get_event_box(self.tab_label)
        self.tooltips.set_tip(event_box, self.get_main_filename())

        return title
