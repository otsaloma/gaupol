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


"""Widely useful functions for GTK GUI components."""


import os
import sys

import gtk


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
    # not the default browser. Add other OSs/DEs start commands, if such
    # exist.
    
    if sys.platform == 'win32':
        os.startfile(WEBSITE)
    elif os.path.isfile('/usr/bin/gnome-open'):
        os.system('/usr/bin/gnome-open "%s"' % url)
    else:
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
