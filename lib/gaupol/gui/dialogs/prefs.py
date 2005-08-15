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


"""Dialog for changing settings."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk

from gaupol.gui.util import gui


class PreferencesDialog(gobject.GObject):

    """
    Dialog for changing settings.
    
    This class is implemented as a gObject. All settings are applied
    instantly. These events will send signals to the Application class,
    which will apply the changed settings.

    Settings not instant-applied can be gotten with the get-methods and
    applied after closing this dialog.
    """

    STAGE = gobject.SIGNAL_RUN_LAST
    BOOL  = gobject.TYPE_BOOLEAN
    INT   = gobject.TYPE_INT
    STR   = gobject.TYPE_STRING

    __gsignals__ = {
        'recent-files-amount-changed': (STAGE, None, (INT ,)),
        'recent-files-cleared'       : (STAGE, None, ()     ),
        'undo-limit-toggled'         : (STAGE, None, (BOOL,)),
        'undo-levels-changed'        : (STAGE, None, (INT ,)),
        'font-use-theme-toggled'     : (STAGE, None, (BOOL,)),
        'font-set'                   : (STAGE, None, (STR ,)),
    }

    def __init__(self, parent):

        gobject.GObject.__init__(self)

        glade_xml = gui.get_glade_xml('prefs-dialog.glade')
        get = glade_xml.get_widget

        # Widgets
        self._dialog                      = get('dialog')
        self._recent_spin_button          = get('recent_spin_button')
        self._recent_clear_button         = get('recent_clear_button')
        self._undo_limit_radio_button     = get('undo_limit_radio_button')
        self._undo_levels_spin_button     = get('undo_levels_spin_button')
        self._undo_unlimited_radio_button = get('undo_unlimited_radio_button')
        self._font_theme_radio_button     = get('font_theme_radio_button')
        self._font_custom_radio_button    = get('font_custom_radio_button')
        self._font_button                 = get('font_button')

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def connect_signals(self):pass
    
    def on_font_button_font_set(self): pass
    
    def on_font_theme_radio_button_toggled(self): pass
    
    def on_recent_clear_button_clicked(self): pass
    
    def on_recent_spin_button_value_changed(self):pass
    
    def on_undo_levels_spin_button_value_changed(self): pass
    
    def on_undo_limit_radio_button_toggled(self): pass
    
    def prepare_mnemonics(self): pass
    
    def set_font(self): pass
    
    def set_limit_undo(self): pass
    
    def set_maximum_recent_files(self): pass
    
    def set_undo_levels(self): pass
    
    def set_use_default_font(self): pass

    def show(self):
        """Show the dialog."""
        
        self._dialog.show()


gobject.type_register(PreferencesDialog)
