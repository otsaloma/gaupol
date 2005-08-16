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

import gobject
import gtk

from gaupol.gui.util import gui


class JumpToSubtitleDialog(gobject.GObject):

    """Dialog to choose a subtitle number to jump to."""

    STAGE = gobject.SIGNAL_RUN_LAST

    __gsignals__ = {
        'jump-button-clicked': (STAGE, None, (gobject.TYPE_INT, )),
    }

    def __init__(self, parent, keep_open):

        gobject.GObject.__init__(self)

        glade_xml = gui.get_glade_xml('jumpto-dialog.glade')
                            
        self._dialog       = glade_xml.get_widget('dialog')
        self._spin_button  = glade_xml.get_widget('spin_button')
        self._check_button = glade_xml.get_widget('check_button')
        
        close_button = glade_xml.get_widget('close_button')
        jump_button  = glade_xml.get_widget('jump_button')
        label        = glade_xml.get_widget('label')
        
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)
        self._dialog.connect('delete-event', self.destroy)

        self._spin_button.set_activates_default(True)
        self._check_button.set_active(keep_open)
        
        close_button.connect('clicked', self.destroy)
        jump_button.connect('clicked', self._on_jump_button_clicked)

        label.set_mnemonic_widget(self._spin_button)

    def destroy(self, *args):
        """Destroy the dialog."""
        
        self._dialog.destroy()

    def get_keep_open(self):
        """Get value of dialog's "keep open" setting."""
        
        return self._check_button.get_active()

    def _on_jump_button_clicked(self, *args):
        """Emit signal that the "jump to" button has been clicked."""
        
        self._spin_button.update()
        subtitle = self._spin_button.get_value_as_int()
        self.emit('jump-button-clicked', subtitle)
        self._spin_button.select_region(0, -1)

    def set_subtitle_number(self, subtitle):
        """Set value for spin button."""
        
        self._spin_button.set_value(subtitle)
        self._spin_button.select_region(0, -1)

    def show(self):
        """Show the dialog."""
        
        self._spin_button.select_region(0, -1)
        self._dialog.show()


gobject.type_register(JumpToSubtitleDialog)
