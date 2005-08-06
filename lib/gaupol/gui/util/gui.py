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


"""Common functions for GTK GUI components."""


import os
import sys

import gtk
import gtk.glade

from gaupol.paths import GLADE_DIR


def get_glade_xml(basename):
    """
    Get gtk.glade.XML object from basename in Glade directory.
    
    Exit if unable to import Glade XML file.
    """
    # TODO:
    # Is sys.exit() too harsh?
    
    path = os.path.join(GLADE_DIR, basename)

    try:
        return gtk.glade.XML(path)
    except RuntimeError:
        logger.critical('Failed to import Glade XML file "%s".' % path)
        sys.exit()

def get_event_box(widget):
    """Get EventBox, if it is a parent of widget."""
    
    event_box = widget
    while not isinstance(event_box, gtk.EventBox):
        event_box = event_box.get_parent()

    return event_box

def open_url(url):
    """Open url in web-browser."""

    # TODO:
    # webbrowser module is not very good. It will open some browser, but
    # not the default browser. Add detection and start commands for other
    # OSs and DEs if such exist.
    
    # Windows
    if sys.platform == 'win32':
        os.startfile(WEBSITE)
        return

    # Gnome
    if os.getenv('GNOME_DESKTOP_SESSION_ID') is not None:
        return_value = os.system('gnome-open "%s"' % url)
        if return_value == 0:
            return

    import webbrowser
    webbrowser.open(url)

def set_cursor_busy(window):
    """
    Set cursor busy when above window.
    
    window: gtk.Window
    """
    window.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

    while gtk.events_pending():
        gtk.main_iteration()
    
def set_cursor_normal(window):
    """
    Set cursor normal when above window.
    
    window: gtk.Window
    """
    window.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

    while gtk.events_pending():
        gtk.main_iteration()
