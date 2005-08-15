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


"""Functions for GTK widgets."""


import os
import sys

import gtk
import gtk.glade

from gaupol.paths import GLADE_DIR


def get_glade_xml(basename):
    """
    Get gtk.glade.XML object from basename in Glade directory.
    
    Raise RuntimeError if unable to load Glade XML file.
    """
    path = os.path.join(GLADE_DIR, basename)

    try:
        return gtk.glade.XML(path)
    except RuntimeError:
        logger.critical('Failed to load Glade XML file "%s".' % path)
        raise

def get_event_box(widget):
    """Get EventBox, if it is a parent of widget."""
    
    event_box = widget
    while not isinstance(event_box, gtk.EventBox):
        event_box = event_box.get_parent()

    return event_box

def get_parent_widget(child, parent_type):
    """Get parent of widget that is type parent."""
    
    parent = child
    while not isinstance(parent, parent_type):
        parent = parent.get_parent()

    return parent

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
