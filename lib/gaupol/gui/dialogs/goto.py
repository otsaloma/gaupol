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


"""Dialog to choose a subtitle number to go to."""


import os
import sys

try:
    from psyco.classes import *
except ImportError:
    pass

import gtk
import gtk.glade

from gaupol.paths import GLADE_DIR


GLADE_XML_PATH = os.path.join(GLADE_DIR, 'goto-dialog.glade')


class GoToDialog(object):

    """Dialog to choose a subtitle number to go to."""
    
    def __init__(self, parent, maximum):

        try:
            glade_xml = gtk.glade.XML(GLADE_XML_PATH)
        except RuntimeError:
            logger.critical('Failed to import glade XML file "%s".' \
                            % GLADE_XML_PATH)
            sys.exit()
                            
        self._dialog      = glade_xml.get_widget('dialog'     )
        self._spin_button = glade_xml.get_widget('spin_button')

        label = glade_xml.get_widget('label')
        label.set_mnemonic_widget(self._spin_button)

        self._spin_button.set_activates_default(True)
        self._spin_button.set_range(1, maximum)

        # Set Go button label.
        button = glade_xml.get_widget('go_button')
        alignment = button.get_children()[0]
        hbox = alignment.get_children()[0]
        go_label = hbox.get_children()[1]
        go_label.set_text(_('_Go'))
        go_label.set_use_underline(True)

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)
    
    def destroy(self):
        """Destroy the dialog."""
        
        self._dialog.destroy()
        
    def get_subtitle(self):
        """Get selected subtitle number."""
        
        self._spin_button.update()
        return self._spin_button.get_value_as_int()

    def run(self):
        """Show and run the dialog."""
        
        self._dialog.show()
        self._spin_button.select_region(0, -1)
        
        return self._dialog.run()        
