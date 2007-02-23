# Copyright (C) 2005-2007 Osmo Salomaa
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


"""Miscellaneous functions for GTK widgets.

Module variables:

    COMBO_SEP:     String rendered as a separator in combo boxes
    EXTRA:         Extra width to add to size calculations
    BUSY_CURSOR:   gtk.gdk.Cursor
    HAND_CURSOR:   gtk.gdk.Cursor
    INSERT_CURSOR: gtk.gdk.Cursor
    NORMAL_CURSOR: gtk.gdk.Cursor

When setting dialog sizes based on their content, we get the size request of
the scrolled window component and add the surroundings to that. For this to
work neatly we should add some extra to adapt to different widget sizes in
different themes. Let the EXTRA constant very vaguely account for that.
"""


import functools
import os

import gobject
import gtk
import gtk.glade
import pango

from gaupol.gtk import paths
from gaupol.util import *
from . import conf, lengthlib


COMBO_SEP = "<separator/>"
EXTRA = 36

BUSY_CURSOR   = gtk.gdk.Cursor(gtk.gdk.WATCH)
HAND_CURSOR   = gtk.gdk.Cursor(gtk.gdk.HAND2)
INSERT_CURSOR = gtk.gdk.Cursor(gtk.gdk.XTERM)
NORMAL_CURSOR = gtk.gdk.Cursor(gtk.gdk.LEFT_PTR)


def get_glade_xml(name, root=None, directory=None):
    """Get gtk.glade.XML object from Glade file path.

    name should be Glade XML file's basename without extension.
    directory can be None for the default global directory.
    Raise RuntimeError if unable to load Glade XML file.
    """
    if directory is None:
        directory = os.path.join(paths.DATA_DIR, "glade")
    path = os.path.join(directory, "%s.glade" % name)
    try:
        return gtk.glade.XML(path, root)
    except RuntimeError:
        print "Failed to load Glade XML file '%s'." % path
        raise

def get_event_box(widget):
    """Get an event box if it is a parent of widget."""

    return get_parent(widget, gtk.EventBox)

def get_parent(child, parent_type):
    """Get the first parent of widget that is of given type."""

    parent = child.get_parent()
    while not isinstance(parent, parent_type):
        parent = parent.get_parent()
    return parent

def get_text_view_size(text_view):
    """Get the size desired by text view.

    Return width, height.
    """
    text_buffer = text_view.get_buffer()
    start, end = text_buffer.get_bounds()
    text = text_buffer.get_text(start, end)
    label = gtk.Label(text)
    return label.size_request()

def get_tree_view_size(tree_view):
    """Get the size desired by tree view.

    Return width, height.
    """
    scroller = tree_view.get_parent()
    policy = scroller.get_policy()
    scroller.set_policy(gtk.POLICY_NEVER, gtk.POLICY_NEVER)
    width, height = scroller.size_request()
    scroller.set_policy(*policy)
    return width, height

def idle_method(function):
    """Decorator for functions to be run in main loop while idle.

    Threads doing GUI operations should use this decorator so that all GUI
    operations get done in the main loop.
    """
    def do_idle(args, kwargs):
        function(*args, **kwargs)
        return False

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        gobject.idle_add(do_idle, args, kwargs)

    return wrapper

def prepare_text_view(text_view):
    """Connect text view to font and length margin updates."""

    # pylint: disable-msg=E0102
    def update(*args):
        if conf.editor.show_lengths_edit:
            return lengthlib.connect_text_view(text_view)
        return lengthlib.disconnect_text_view(text_view)
    conf.editor.connect("notify::show_lengths_edit", update)
    update()

    def update(*args):
        font = ("" if conf.editor.use_default_font else conf.editor.font)
        set_widget_font(text_view, font)
    conf.editor.connect("notify::use_default_font", update)
    conf.editor.connect("notify::font", update)
    update()

def resize_dialog(dialog, width, height, max_width=0.6, max_height=0.6):
    """Resize dialog in a smart manner.

    width and height should be desired sizes in pixels.
    max_width and max_height should be between 0 and 1.
    """
    # Set maximum based on percentage of screen space.
    width = min(width, int(max_width * gtk.gdk.screen_width()))
    height = min(height, int(max_height * gtk.gdk.screen_height()))

    # Set minimum based on dialog content.
    size = dialog.size_request()
    width = max(size[0], width)
    height = max(size[1], height)

    dialog.set_default_size(width, height)

def resize_message_dialog(
    dialog, width, height, max_width=0.5, max_height=0.5):
    """Resize message dialog in a smart manner.

    width and height should be desired sizes in pixels.
    max_width and max_height should be between 0 and 1.
    """
    resize_dialog(dialog, width, height, max_width, max_height)

def separate_combo(store, itr):
    """Separator function for combo box models."""

    return store.get_value(itr, 0) == COMBO_SEP

def set_button(button, text, stock=None):
    """Set the label and the image on button."""

    if stock is not None:
        image = gtk.Button(stock=stock).get_image()
        button.set_image(image)
    alignment = button.get_children()[0]
    hbox = alignment.get_children()[0]
    image = hbox.get_children()[0]
    if stock is None:
        hbox.remove(image)
    button.set_label(text)
    button.set_use_underline(True)

def set_cursor_busy(window):
    """Set cursor busy when above window."""

    while gtk.events_pending():
        gtk.main_iteration()
    window.window.set_cursor(BUSY_CURSOR)
    while gtk.events_pending():
        gtk.main_iteration()

def set_cursor_normal(window):
    """Set cursor normal when above window."""

    while gtk.events_pending():
        gtk.main_iteration()
    window.window.set_cursor(NORMAL_CURSOR)
    while gtk.events_pending():
        gtk.main_iteration()

def set_label_font(label, font):
    """Set label font."""

    context = label.get_pango_context()
    font_desc = context.get_font_description()
    custom_font_desc = pango.FontDescription(font)
    font_desc.merge(custom_font_desc, True)

    attr = pango.AttrFontDesc(font_desc, 0, -1)
    attr_list = pango.AttrList()
    attr_list.insert(attr)
    label.set_attributes(attr_list)

def set_widget_font(widget, font):
    """Set widget font."""

    context = widget.get_pango_context()
    font_desc = context.get_font_description()
    custom_font_desc = pango.FontDescription(font)
    font_desc.merge(custom_font_desc, True)
    widget.modify_font(font_desc)
