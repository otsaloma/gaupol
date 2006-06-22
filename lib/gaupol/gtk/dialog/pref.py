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


"""Dialog for editing preferences."""


from gettext import gettext as _

import gobject
import gtk
import pango

from gaupol.base.util            import enclib
from gaupol.gtk                  import cons
from gaupol.gtk.dialog.encoding  import EncodingDialog
from gaupol.gtk.util             import conf, gtklib

try:
    import chardet
    _CHARDET_AVAILABLE = True
except ImportError:
    _CHARDET_AVAILABLE = False


class _Editor(object):

    """Editor preferences."""

    def __init__(self, master, parent, glade_xml):

        self._master = master

        get_widget = glade_xml.get_widget
        self._default_font_check = get_widget('editor_default_font_check')
        self._font_button        = get_widget('editor_font_button')
        self._font_hbox          = get_widget('editor_font_hbox')
        self._parent             = parent
        self._undo_limit_hbox    = get_widget('editor_undo_limit_hbox')
        self._undo_limit_spin    = get_widget('editor_undo_limit_spin')
        self._unlimit_undo_check = get_widget('editor_unlimit_undo_check')

        self._init_data()
        self._init_signals()

    def _get_custom_font(self):
        """Get custom font as string."""

        context = gtk.Label().get_pango_context()
        font_desc = context.get_font_description()
        custom_font_desc = pango.FontDescription(conf.editor.font)
        font_desc.merge(custom_font_desc, True)
        return font_desc.to_string()

    def _init_data(self):
        """Initialize default values."""

        use_default = conf.editor.use_default_font
        self._default_font_check.set_active(use_default)
        self._font_hbox.set_sensitive(not use_default)
        self._font_button.set_font_name(self._get_custom_font())

        limit = conf.editor.limit_undo
        self._unlimit_undo_check.set_active(not limit)
        self._undo_limit_hbox.set_sensitive(limit)
        self._undo_limit_spin.set_value(conf.editor.undo_levels)

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, '_default_font_check', 'toggled'      )
        gtklib.connect(self, '_font_button'       , 'font-set'     )
        gtklib.connect(self, '_undo_limit_spin'   , 'value-changed')
        gtklib.connect(self, '_unlimit_undo_check', 'toggled'      )

    def _on_default_font_check_toggled(self, check_button):
        """Save default font usage and emit signal."""

        use_default = check_button.get_active()
        conf.editor.use_default_font = use_default
        self._master.emit('use-default-font-toggled', use_default)
        self._font_hbox.set_sensitive(not use_default)

    def _on_font_button_font_set(self, font_button):
        """Save custom font and emit signal."""

        font = font_button.get_font_name()
        conf.editor.font = font
        self._master.emit('font-set', font)

    def _on_undo_limit_spin_value_changed(self, spin_button):
        """Save undo limit and emit signal."""

        levels = spin_button.get_value_as_int()
        conf.editor.undo_levels = levels
        self._master.emit('undo-levels-changed', levels)

    def _on_unlimit_undo_check_toggled(self, check_button):
        """Save undo limiting and emit signal."""

        limit = not check_button.get_active()
        conf.editor.limit_undo = limit
        self._master.emit('limit-undo-toggled', limit)
        self._undo_limit_hbox.set_sensitive(limit)


class _File(object):

    """File preferences."""

    def __init__(self, master, parent, glade_xml):

        self._master = master

        get_widget = glade_xml.get_widget
        self._add_button    = get_widget('file_add_button')
        self._auto_check    = get_widget('file_auto_check')
        self._down_button   = get_widget('file_down_button')
        self._tree_view     = get_widget('file_tree_view')
        self._locale_check  = get_widget('file_locale_check')
        self._parent        = parent
        self._remove_button = get_widget('file_remove_button')
        self._up_button     = get_widget('file_up_button')

        self._init_widgets()
        self._init_data()
        self._init_signals()

    def _get_selected_row(self):
        """Return selected fallback encoding or None."""

        selection = self._tree_view.get_selection()
        try:
            return selection.get_selected_rows()[1][0][0]
        except IndexError:
            return None

    def _init_data(self):
        """Initialize default values."""

        self._auto_check.set_active(conf.encoding.try_auto)
        self._auto_check.set_sensitive(_CHARDET_AVAILABLE)
        self._locale_check.set_active(conf.encoding.try_locale)
        self._reload_tree_view()

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, '_add_button'   , 'clicked')
        gtklib.connect(self, '_auto_check'   , 'toggled')
        gtklib.connect(self, '_down_button'  , 'clicked')
        gtklib.connect(self, '_locale_check' , 'toggled')
        gtklib.connect(self, '_remove_button', 'clicked')
        gtklib.connect(self, '_up_button'    , 'clicked')

        selection = self._tree_view.get_selection()
        selection.connect('changed', self._on_selection_changed)

    def _init_widgets(self):
        """Initialize widgets."""

        self._tree_view.columns_autosize()
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.unselect_all()
        store = gtk.ListStore(gobject.TYPE_STRING)
        self._tree_view.set_model(store)
        column = gtk.TreeViewColumn('', gtk.CellRendererText(), text=0)
        self._tree_view.append_column(column)

    def _on_add_button_clicked(self, *args):
        """Add new fallback encoding."""

        dialog = EncodingDialog(self._parent)
        response = dialog.run()
        encoding = dialog.get_encoding()
        dialog.destroy()
        if response != gtk.RESPONSE_OK or encoding is None:
            return
        if encoding not in conf.encoding.fallbacks:
            conf.encoding.fallbacks.append(encoding)

        self._reload_tree_view()
        self._tree_view.grab_focus()
        store = self._tree_view.get_model()
        self._tree_view.set_cursor(len(store) - 1)

    def _on_auto_check_toggled(self, check_button):
        """Save auto-detect encoding usage."""

        conf.encoding.try_auto = check_button.get_active()

    def _on_down_button_clicked(self, *args):
        """Move selected encoding down."""

        row = self._get_selected_row()
        encodings = conf.encoding.fallbacks
        encodings.insert(row + 1, encodings.pop(row))

        self._reload_tree_view()
        self._tree_view.grab_focus()
        self._tree_view.set_cursor(row + 1)

    def _on_locale_check_toggled(self, check_button):
        """Save locale encoding usage."""

        conf.encoding.try_locale = check_button.get_active()

    def _on_remove_button_clicked(self, *args):
        """Remove selected encoding."""

        row = self._get_selected_row()
        conf.encoding.fallbacks.pop(row)

        self._reload_tree_view()
        self._tree_view.grab_focus()
        store = self._tree_view.get_model()
        if len(store) > 0:
            self._tree_view.set_cursor(max(row - 1, 0))

    def _on_selection_changed(self, *args):
        """Set fallback tree view button sensitivities."""

        self._set_sensitivities()

    def _on_up_button_clicked(self, *args):
        """Move selected encoding up."""

        row = self._get_selected_row()
        encodings = conf.encoding.fallbacks
        encodings.insert(row - 1, encodings.pop(row))

        self._reload_tree_view()
        self._tree_view.grab_focus()
        self._tree_view.set_cursor(row - 1)

    def _reload_tree_view(self):
        """Reload fallback tree view data."""

        store = self._tree_view.get_model()
        store.clear()
        for encoding in conf.encoding.fallbacks:
            store.append([enclib.get_long_name(encoding)])

        self._set_sensitivities()

    def _set_sensitivities(self):
        """Set fallback tree view button sensitivities."""

        def set_sensitive(remove, up, down):
            self._remove_button.set_sensitive(remove)
            self._up_button.set_sensitive(up)
            self._down_button.set_sensitive(down)

        try:
            row = int(self._get_selected_row())
            store = self._tree_view.get_model()
            set_sensitive(True, row > 0, row < len(store) - 1)
        except (IndexError, TypeError):
            set_sensitive(False, False, False)


class _Preview(object):

    """Preview preferences."""

    def __init__(self, master, parent, glade_xml):

        self._master = master

        get_widget = glade_xml.get_widget
        self._app_combo     = get_widget('preview_app_combo')
        self._command_entry = get_widget('preview_command_entry')
        self._offset_spin   = get_widget('preview_offset_spin')
        self._parent        = parent

        self._init_widgets()
        self._init_data()
        self._init_signals()

    def _init_data(self):
        """Initialize default values."""

        if conf.preview.use_predefined:
            self._app_combo.set_active(conf.preview.video_player)
            command = cons.VideoPlayer.commands[conf.preview.video_player]
            self._command_entry.set_text(command)
            self._command_entry.set_editable(False)
        else:
            store = self._app_combo.get_model()
            self._app_combo.set_active(len(store) - 1)
            self._command_entry.set_text(conf.preview.custom_command)
            self._command_entry.set_editable(True)

        self._offset_spin.set_value(conf.preview.offset)

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, '_app_combo'    , 'changed'      )
        gtklib.connect(self, '_command_entry', 'changed'      )
        gtklib.connect(self, '_offset_spin'  , 'value-changed')

    def _init_widgets(self):
        """Initialize application combo box."""

        store = gtk.ListStore(gobject.TYPE_STRING)
        renderer = gtk.CellRendererText()
        self._app_combo.pack_start(renderer, True)
        self._app_combo.add_attribute(renderer, 'text', 0)
        self._app_combo.set_model(store)
        for name in cons.VideoPlayer.display_names:
            store.append([name])
        store.append([gtklib.COMBO_SEP])
        store.append([_('Custom')])
        self._app_combo.set_row_separator_func(gtklib.separate)

    def _on_app_combo_changed(self, combo_box):
        """Save video player and show command."""

        index = combo_box.get_active()
        if index in range(len(cons.VideoPlayer.display_names)):
            conf.preview.use_predefined = True
            conf.preview.video_player = index
            self._command_entry.set_text(cons.VideoPlayer.commands[index])
            self._command_entry.set_editable(False)
        else:
            conf.preview.use_predefined = False
            self._command_entry.set_text(conf.preview.custom_command)
            self._command_entry.set_editable(True)

        self._master.emit('video-player-set')

    def _on_command_entry_changed(self, entry):
        """Save custom command."""

        if not conf.preview.use_predefined:
            conf.preview.custom_command = entry.get_text()

    def _on_offset_spin_value_changed(self, spin_button):
        """Save offset."""

        conf.preview.offset = spin_button.get_value()


class PreferencesDialog(gobject.GObject):

    """Dialog for changing preferences."""

    __gsignals__ = {
        'destroyed': (
            gobject.SIGNAL_RUN_LAST,
            None,
            ()
        ),
        'font-set': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (gobject.TYPE_STRING,)
        ),
        'limit-undo-toggled': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (gobject.TYPE_BOOLEAN,)
        ),
        'undo-levels-changed': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (gobject.TYPE_INT,)
        ),
        'use-default-font-toggled': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (gobject.TYPE_BOOLEAN,)
        ),
        'video-player-set': (
            gobject.SIGNAL_RUN_LAST,
            None,
            ()
        ),
    }

    def __init__(self):

        gobject.GObject.__init__(self)

        glade_xml = gtklib.get_glade_xml('pref-dialog')
        self._dialog = glade_xml.get_widget('dialog')

        self._editor  = _Editor(self, self._dialog, glade_xml)
        self._file    = _File(self, self._dialog, glade_xml)
        self._preview = _Preview(self, self._dialog, glade_xml)

        gtklib.connect(self, '_dialog', 'response')
        self._dialog.set_transient_for(None)
        self._dialog.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_NORMAL)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _on_dialog_response(self, dialog, response):
        """Emit destroyed signal."""

        self._dialog.destroy()
        self.emit('destroyed')

    def present(self):
        """Present dialog."""

        self._dialog.present()

    def show(self):
        """Show dialog."""

        self._dialog.show()
