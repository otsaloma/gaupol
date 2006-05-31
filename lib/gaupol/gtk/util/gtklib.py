# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Functions for GTK widgets."""


import gc
import os

import gobject
import gtk
import gtk.glade
import pango

from gaupol.gtk.paths import GLADE_DIR


# When setting dialog sizes based on their content, we get the size request of
# the scrolled window component and add the surroundings to that. For this to
# work neatly we should add some extra to adapt to different widget and font
# sizes in different themes. Let this constant vaguely account for that extra.
EXTRA = 36

cursor_busy   = gtk.gdk.Cursor(gtk.gdk.WATCH)
cursor_normal = gtk.gdk.Cursor(gtk.gdk.LEFT_PTR)
screen_height = gtk.gdk.screen_height()
screen_width  = gtk.gdk.screen_width()


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

def get_glade_xml(name):
    """
    Get gtk.glade.XML object from file in Glade directory.

    name is Glade XML file's basename without extension.
    Raise RuntimeError if unable to load Glade XML file.
    """
    path = os.path.join(GLADE_DIR, name + '.glade')
    try:
        return gtk.glade.XML(path)
    except RuntimeError:
        print 'Failed to load Glade XML file "%s".' % path
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
    text = text_buffer.get_text(start, end)
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
    Decorator for functions to be run in main loop while idle.

    Threads doing GUI operations should use this decorator so that all GUI
    operations get done in the main loop keeping the threading
    Windows-compatible.
    """
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
    # Set maximum based on percentage of screen space.
    width  = min(width , int(max_width  * screen_width ))
    height = min(height, int(max_height * screen_height))

    # Set minimum based on dialog content.
    size = dialog.size_request()
    width  = max(size[0], width )
    height = max(size[1], height)

    dialog.set_size_request(width, height)

def resize_message_dialog(
    dialog, width, height, max_width=0.55, max_height=0.55):
    """
    Resize message dialog in a smart manner.

    width and height are desired sizes in pixels. max_width and max_height are
    between 0 and 1 representing maximum screen space taken.
    """
    resize_dialog(dialog, width, height, max_width, max_height)

def set_cursor_busy(window):
    """Set cursor busy when above window."""

    window.window.set_cursor(cursor_busy)
    while gtk.events_pending():
        gtk.main_iteration()

def set_cursor_normal(window):
    """Set cursor normal when above window."""

    window.window.set_cursor(cursor_normal)
    while gtk.events_pending():
        gtk.main_iteration()

def set_label_font(label, font):
    """
    Set label font.

    font is a string, e.g. "Sans 9".
    """
    context = label.get_pango_context()
    font_desc = context.get_font_description()
    custom_font_desc = pango.FontDescription(font)
    font_desc.merge(custom_font_desc, True)

    attr = pango.AttrFontDesc(font_desc, 0, -1)
    attr_list = pango.AttrList()
    attr_list.insert(attr)
    label.set_attributes(attr_list)

def set_widget_font(widget, font):
    """
    Set widget font.

    font is a string, e.g. "Sans 9".
    """
    context = widget.get_pango_context()
    font_desc = context.get_font_description()
    custom_font_desc = pango.FontDescription(font)
    font_desc.merge(custom_font_desc, True)
    widget.modify_font(font_desc)
