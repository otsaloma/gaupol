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
    
    This class is implemented as a GObject. All settings are applied
    instantly. These events will send signals to the Application class,
    which will apply the changed settings.
    """

    STAGE = gobject.SIGNAL_RUN_LAST
    BOOL  = gobject.TYPE_BOOLEAN
    INT   = gobject.TYPE_INT
    STR   = gobject.TYPE_STRING

    __gsignals__ = {
        'limit-undo-toggled'      : (STAGE, None, (BOOL,)),
        'undo-levels-changed'     : (STAGE, None, (INT ,)),
        'use-default-font-toggled': (STAGE, None, (BOOL,)),
        'font-set'                : (STAGE, None, (STR ,)),
    }

    def __init__(self, parent):

        gobject.GObject.__init__(self)

        glade_xml = gui.get_glade_xml('prefs-dialog.glade')
        get = glade_xml.get_widget

        # Widgets
        self._dialog                      = get('dialog')
        self._undo_limit_radio_button     = get('undo_limit_radio_button')
        self._undo_levels_spin_button     = get('undo_levels_spin_button')
        self._undo_unlimited_radio_button = get('undo_unlimited_radio_button')
        self._font_default_check_button   = get('font_default_check_button')
        self._font_custom_label           = get('font_custom_label')
        self._font_button                 = get('font_button')
        self._close_button                = get('close_button')

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)
        self._dialog.connect('delete-event', self._destroy)

        self._set_mnemonics(glade_xml)
        self._connect_signals()

    def _connect_signals(self):
        """Connect signals to widgets."""
        
        # Set a group for undo RadioButtons. ValueError is raised if button
        # already is in group.
        group = self._undo_limit_radio_button.get_group()[0]
        try:
            self._undo_unlimited_radio_button.set_group(group)
        except ValueError:
            pass

        # Undo limit RadioButton (It is enough to connect only one of the two
        # RadioButtons.)
        method = self._on_undo_limit_radio_button_toggled
        self._undo_limit_radio_button.connect('toggled', method)

        # Undo levels SpinButton
        method = self._on_undo_levels_spin_button_value_changed
        self._undo_levels_spin_button.connect('value-changed', method)

        # Font default CheckButton
        method = self._on_font_default_check_button_toggled
        self._font_default_check_button.connect('toggled', method)

        # FontButton
        method = self._on_font_button_font_set
        self._font_button.connect('font-set', method)

        # Close button
        self._close_button.connect('clicked', self._destroy)

    def _destroy(self, *args):
        """Destroy the dialog."""
        
        self._dialog.destroy()
    
    def _on_font_button_font_set(self, font_button):
        """Emit signal that the custom font has been set."""
        
        font = font_button.get_font_name()
        self.emit('font-set', font)
    
    def _on_font_default_check_button_toggled(self, check_button):
        """Emit signal that use default/custom font has changed."""
        
        use_default = check_button.get_active()
        self._font_custom_label.set_sensitive(not use_default)
        self._font_button.set_sensitive(not use_default)
        self.emit('use-default-font-toggled', use_default)
    
    def _on_undo_levels_spin_button_value_changed(self, spin_button):
        """Emit signal that the amount of undo levels has changed."""

        spin_button.update()
        levels = spin_button.get_value_as_int()
        self.emit('undo-levels-changed', levels)
    
    def _on_undo_limit_radio_button_toggled(self, radio_button):
        """Emit signal that undo limit/unlimit has changed."""
        
        limit = self._undo_limit_radio_button.get_active()
        self._undo_levels_spin_button.set_sensitive(limit)
        self.emit('limit-undo-toggled', limit)

    def set_font(self, font):
        """Set custom font in FontButton."""
        
        self._font_button.set_font_name(font)
    
    def set_limit_undo(self, limit):
        """Set value of undo limiting/unlimiting."""

        self._undo_limit_radio_button.set_active(limit)
        self._undo_unlimited_radio_button.set_active(not limit)

    def _set_mnemonics(self, glade_xml):
        """Set mnemonics for widgets."""

        undo_levels_label = glade_xml.get_widget('undo_levels_label')
        undo_levels_label.set_mnemonic_widget(self._undo_levels_spin_button)

        self._font_custom_label.set_mnemonic_widget(self._font_button)
    
    def set_undo_levels(self, levels):
        """Set value of undo levels."""
        
        self._undo_levels_spin_button.set_value(levels)
    
    def set_use_default_font(self, default):
        """Set value of use default/custom font."""

        self._font_default_check_button.set_active(default)

    def show(self):
        """Show the dialog."""
        
        self._dialog.show()


gobject.type_register(PreferencesDialog)
