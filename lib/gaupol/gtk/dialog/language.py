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


"""Dialog for configuring spell-check."""


import gobject
import gtk

from gaupol.base.util   import langlib
from gaupol.gtk         import cons
from gaupol.gtk.colcons import *
from gaupol.gtk.util    import config, gtklib

try:
    import enchant
except ImportError:
    pass
except enchant.Error:
    pass


class LanguageDialog(object):

    """Dialog for configuring spell-check."""

    def __init__(self, parent):

        self._langs = []

        glade_xml = gtklib.get_glade_xml('language-dialog')
        self._all_radio      = glade_xml.get_widget('all_radio')
        self._current_radio  = glade_xml.get_widget('current_radio')
        self._dialog         = glade_xml.get_widget('dialog')
        self._main_check     = glade_xml.get_widget('main_check')
        self._main_tree_view = glade_xml.get_widget('main_tree_view')
        self._tran_check     = glade_xml.get_widget('tran_check')
        self._tran_tree_view = glade_xml.get_widget('tran_tree_view')

        self._init_langs()
        self._init_tree_views()
        self._init_signals()
        self._init_data()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _init_data(self):
        """Initialize default values."""

        try:
            row = self._langs.index(config.spell_check.main_lang)
            self._main_tree_view.get_selection().select_path(row)
        except ValueError:
            pass
        try:
            row = self._langs.index(config.spell_check.tran_lang)
            self._tran_tree_view.get_selection().select_path(row)
        except ValueError:
            pass

        target = config.spell_check.target
        self._all_radio.set_active(target == cons.Target.ALL)
        self._current_radio.set_active(target == cons.Target.CURRENT)

        cols = config.spell_check.cols
        self._main_check.set_active(MTXT in cols)
        self._tran_check.set_active(TTXT in cols)

    def _init_langs(self):
        """Initialize list of available languages."""

        # The only sane approach to providing a list of laguages appears to be
        # to try initialize dictionaries for a predefined list of locales and
        # displaying all successful languages. The downside here being speed.
        for lang in langlib.LOCALES:
            try:
                enchant.Dict(lang)
                self._langs.append(lang)
            except enchant.Error:
                pass
        self._langs.sort()

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, '_all_radio'    , 'toggled')
        gtklib.connect(self, '_current_radio', 'toggled')
        gtklib.connect(self, '_main_check'   , 'toggled')
        gtklib.connect(self, '_tran_check'   , 'toggled')

        selection = self._main_tree_view.get_selection()
        selection.connect('changed', self._on_main_selection_changed)
        selection = self._tran_tree_view.get_selection()
        selection.connect('changed', self._on_tran_selection_changed)

    def _init_sizes(self):
        """Initialize widget sizes."""

        width, height = gtklib.get_tree_view_size(self._main_tree_view)
        width  = (width * 2) + 100 + gtklib.EXTRA
        height = height + 267 + gtklib.EXTRA
        gtklib.resize_dialog(self._dialog, width, height, 0.5, 0.5)

    def _init_tree_views(self):
        """Initialize tree views."""

        for tree_view in (self._main_tree_view, self._tran_tree_view):
            tree_view.columns_autosize()
            selection = tree_view.get_selection()
            selection.set_mode(gtk.SELECTION_SINGLE)
            selection.unselect_all()
            store = gtk.ListStore(gobject.TYPE_STRING)
            tree_view.set_model(store)
            renderer = gtk.CellRendererText()
            tree_view.append_column(gtk.TreeViewColumn('', renderer, text=0))
            for lang in self._langs:
                name = langlib.get_long_name(lang)
                store.append([name])

    def _on_all_radio_toggled(self, radio_button):
        """Save target."""

        if radio_button.get_active():
            config.spell_check.target = cons.Target.ALL
        else:
            config.spell_check.target = cons.Target.CURRENT

    def _on_current_radio_toggled(self, radio_button):
        """Save target."""

        if radio_button.get_active():
            config.spell_check.target = cons.Target.CURRENT
        else:
            config.spell_check.target = cons.Target.ALL

    def _on_main_check_toggled(self, check_button):
        """Save columns."""

        if check_button.get_active():
            if not MTXT in config.spell_check.cols:
                config.spell_check.cols.append(MTXT)
        else:
            if MTXT in config.spell_check.cols:
                config.spell_check.cols.remove(MTXT)

    def _on_main_selection_changed(self, selection):
        """Save main language."""

        try:
            row = selection.get_selected_rows()[1][0][0]
            config.spell_check.main_lang = self._langs[row]
        except IndexError:
            pass

    def _on_tran_check_toggled(self, check_button):
        """Save columns."""

        if check_button.get_active():
            if not TTXT in config.spell_check.cols:
                config.spell_check.cols.append(TTXT)
        else:
            if TTXT in config.spell_check.cols:
                config.spell_check.cols.remove(TTXT)

    def _on_tran_selection_changed(self, selection):
        """Save translation language."""

        try:
            row = selection.get_selected_rows()[1][0][0]
            config.spell_check.tran_lang = self._langs[row]
        except IndexError:
            pass

    def destroy(self):
        """Destroy dialog."""

        self._dialog.destroy()

    def run(self):
        """Run dialog."""

        self._dialog.show()
        return self._dialog.run()
