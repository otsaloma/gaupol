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


class JumpToSubtitleDialog(object):

    """Dialog to choose a subtitle number to jump to."""
    
    def __init__(self, parent, maximum):

        glade_xml = gui.get_glade_xml('jumpto-dialog.glade')
                            
        self._dialog      = glade_xml.get_widget('dialog'     )
        self._spin_button = glade_xml.get_widget('spin_button')

        label = glade_xml.get_widget('label')
        label.set_mnemonic_widget(self._spin_button)

        self._spin_button.set_activates_default(True)
        self._spin_button.set_range(1, maximum)

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)
    
    def destroy(self):
        """Destroy dialog."""
        
        self._dialog.destroy()
        
    def get_subtitle(self):
        """Get selected subtitle number."""
        
        self._spin_button.update()

        return self._spin_button.get_value_as_int()

    def run(self):
        """Show and run dialog."""
        
        self._spin_button.select_region(0, -1)
        self._dialog.show()
        
        return self._dialog.run()
