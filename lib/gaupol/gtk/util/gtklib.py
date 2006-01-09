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


import gc
import logging
import os
import sys

import gobject
import gtk
import gtk.glade

from gaupol.gtk.paths import GLADE_DIR


# When setting dialog sizes based on their content, we get the size request of
# the scrolled window component and add the surroundings to that. For this to
# work neatly we should add some extra to adapt to different widget and font
# sizes in different themes. Let this constant vaguely account for that extra.
EXTRA = 36


logger = logging.getLogger()

normal_cursor = gtk.gdk.Cursor(gtk.gdk.LEFT_PTR)
busy_cursor   = gtk.gdk.Cursor(gtk.gdk.WATCH)

screen_width  = gtk.gdk.screen_width()
screen_height = gtk.gdk.screen_height()


def destroy_gobject(gobj):
    """Destroy gobject completely from memory."""

    # NOTE:
    # This is needed while PyGTK bug #320428 is unsolved.
    # http://bugzilla.gnome.org/show_bug.cgi?id=320428
    # http://bugzilla.gnome.org/attachment.cgi?id=18069

    try:
        gobj.destroy()
    except AttributeError:
        pass

    del gobj
    gc.collect()

def get_glade_xml(basename):
    """
    Get gtk.glade.XML object from basename in Glade directory.

    Raise RuntimeError if unable to load Glade XML file.
    """
    path = os.path.join(GLADE_DIR, basename)

    try:
        return gtk.glade.XML(path)
    except RuntimeError:
        logger.error('Failed to load Glade XML file "%s".' % path)
        raise

def get_event_box(widget):
    """Get EventBox if it is a parent of widget."""

    event_box = widget.get_parent()
    while not isinstance(event_box, gtk.EventBox):
        event_box = event_box.get_parent()

    return event_box

def get_parent_widget(child, parent_type):
    """Get parent of widget that is of given type."""

    parent = child.get_parent()
    while not isinstance(parent, parent_type):
        parent = parent.get_parent()

    return parent

def get_text_view_size(text_view):
    """
    Get size desired by text view.

    Return width, height.
    """
    text_buffer = text_view.get_buffer()
    start, end = text_buffer.get_bounds()
    text = text_buffer.get_text(start, end, True)
    label = gtk.Label(text)
    return label.size_request()

def get_tree_view_size(tree_view):
    """
    Get size desired by tree view.

    Return width, height.
    """
    scrolled_window = tree_view.get_parent()
    orig_policy = scrolled_window.get_policy()
    scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_NEVER)
    width, height = scrolled_window.size_request()
    scrolled_window.set_policy(*orig_policy)
    return width, height

def idlemethod(function):
    """
    Decorator for doing a GUI operation while idle.

    This is a decorator that threads doing GUI operations should use, so that
    GUI operations get done in the main loop.

    Usage:
    @gtklib.idlemethod
    def threaded_method(...):
        widget.do_something()
    """
    # This decorator is required for Windows compatible threading.
    # http://www.async.com.br/faq/pygtk/index.py?req=show&file=faq21.003.htp
    # http://www.mail-archive.com/pygtk@daa.com.au/msg10338.html

    def do_idle(args, kwargs):
        function(*args, **kwargs)
        return False

    def wrapper(*args, **kwargs):
        gobject.idle_add(do_idle, args, kwargs)

    return wrapper

def resize_dialog(dialog, width, height, max_width=0.65, max_height=0.65):
    """
    Resize dialog in a smart manner.

    width and height are desired sizes in pixels. max_width and max_height are
    between 0 and 1 representing maximum screen space taken.
    """
    # Dialog should not take more screen space than defined.
    max_width  = int(max_width  * screen_width )
    max_height = int(max_height * screen_height)
    width  = min(width , max_width )
    height = min(height, max_height)

    # Dialog must be able fit its contents.
    current_width, current_height = dialog.size_request()
    width  = max(current_width , width )
    height = max(current_height, height)

    dialog.set_size_request(width, height)

def resize_message_dialog(dialog, width, height, max_width=0.55,
                          max_height=0.55):
    """
    Resize message dialog in a smart manner.

    width and height are desired sizes in pixels. max_width and max_height are
    between 0 and 1 representing maximum screen space taken.
    """
    resize_dialog(dialog, width, height, max_width, max_height)

def set_cursor_busy(window):
    """
    Set cursor busy when above window.

    window: gtk.Window
    """
    window.window.set_cursor(busy_cursor)
    while gtk.events_pending():
        gtk.main_iteration()

def set_cursor_normal(window):
    """
    Set cursor normal when above window.

    window: gtk.Window
    """
    window.window.set_cursor(normal_cursor)
    while gtk.events_pending():
        gtk.main_iteration()
