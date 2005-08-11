# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.gui.util import gui


class PreferencesDialog(gobject.GObject):

    __gsignals__ = {
        'font-changed': (gobject.SIGNAL_RUN_LAST, None, ()),
        'recent-files-cleared': (gobject.SIGNAL_RUN_LAST, None, ()),
    }

    def __init__(self, parent):
        """
        Initialize a Project object.
        
        counter: an integer that gives this project a unique ID
        """
        gobject.GObject.__init__(self)

        glade_xml = gui.get_glade_xml('goto-dialog.glade')

        # Widgets
        self._rc_spin_button = glade_xml.get_widget('maximum_recent_files_spin_button')
        rc_label = glade_xml.get_widget('maximum_recent_files_label')
        rc_label.set_mnemonic_widget(self._rc_spin_button)

        self._rc_button = glade_xml.get_widget('recent_files_clear_button')

        self._undo_limit_radio_button = glade_xml.get_widget('limit_undo_radio_button')
        self._unlimited_undo_radio_button = glade_xml.get_widget('unlimited_undo_radio_button')
        
        self._undo_spin_button = glade_xml.get_widget('undo_levels_spin_button')
        undo_actions_label = glade_xml.get_widget('undo_actions_label')
        undo_actions_label.set_mnemonic_widget(self._undo_spin_button)

        self._default_font_toggle_button = glade_xml.get_widget('use_default_font_check_button')
        self._font_button = glade_xml.get_widget('font_button')
        self._font_label = glade_xml.get_widget('font_selection_label')
        self._font_label.set_mnemonic_widget(self._font_button)

        self._dialog = glade_xml.get_widget('dialog')

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def destroy
    def run
    def set_max_recent_files
    def get_max_recent_files
    def on_clear_button_clicked
    def on_limit_undo_toggled
    def get_limit_undo
    def set_limit_undo
    def get_undo_levels
    def set_undo_levels
    def get_use_default_font
    def set_use_default_font
    def on_use_default_font_toggled
    def get_font
    def set_font
    def on_font_changed
    
        
        


gobject.type_register(PreferencesDialog)
