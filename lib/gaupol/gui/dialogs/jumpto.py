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


"""Dialog for choose a subtitle number to jump to."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.gui.util import gui


class JumpToSubtitleDialog(gobject.GObject):

    """Dialog to choose a subtitle number to jump to."""

    STAGE = gobject.SIGNAL_RUN_LAST
    BOOL  = gobject.TYPE_BOOLEAN
    INT   = gobject.TYPE_INT

    __gsignals__ = {
        'jump-to-button-clicked' : (STAGE, None, (INT, )),
        'keep-open-value-changed': (STAGE, None, (BOOL,)),
    }
    
    def __init__(self, parent, maximum, keep_open):

        gobject.GObject.__init__(self)

        glade_xml = gui.get_glade_xml('jumpto-dialog.glade')
                            
        self._dialog         = glade_xml.get_widget('dialog'        )
        self._spin_button    = glade_xml.get_widget('spin_button'   )
        self._check_button   = glade_xml.get_widget('check_button'  )
        self._cancel_button  = glade_xml.get_widget('cancel_button' )
        self._jump_to_button = glade_xml.get_widget('jump_to_button')
        
        # Set mnemonics.
        label = glade_xml.get_widget('label')
        label.set_mnemonic_widget(self._spin_button)

        # Configure SpinButton.
        self._spin_button.set_activates_default(True)
        self._spin_button.set_range(1, maximum)

        self._check_button.set_active(keep_open)

        # Connect signals.
        self._check_button.connect('toggled' , self._on_check_button_toggled )
        self._cancel_button.connect('clicked', self._on_cancel_button_clicked)
        self._dialog.connect('delete-event'  , self._on_dialog_delete_event  )
        
        method = self._on_jump_to_button_clicked
        self._jump_to_button.connect('clicked', method)
        
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _on_cancel_button_clicked(self, *args):
        """Destroy the dialog"""

        self._dialog.destroy()
        self.destroy()

    def _on_check_button_toggled(self, *args):
        """Emit signal that the "keep open" value has changed."""
        
        keep_open = self._check_button.get_active()
        self.emit('keep-open-value-changed', keep_open)
        
    def _on_dialog_delete_event(self, *args):
        """Destroy the dialog"""

        self._dialog.destroy()
        self.destroy()

    def _on_jump_to_button_clicked(self, *args):
        """Emit signal that the "jump to" button has been clicked."""
        
        self._spin_button.update()
        subtitle = self._spin_button.get_value_as_int()
        self.emit('jump-to-button-clicked', subtitle)

    def show(self):
        """Show the dialog."""
        
        self._spin_button.select_region(0, -1)
        self._dialog.show()


gobject.type_register(JumpToSubtitleDialog)
