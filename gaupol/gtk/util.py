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


"""Miscellaneous functions and decorators."""


import functools
import gaupol.gtk
import gobject
import gtk.glade
import os
import pango

from gaupol.util import *


def idle_method(function):
    """Decorator for functions to be run in main loop while idle."""

    def do_idle(args, kwargs):
        function(*args, **kwargs)
        return False
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        gobject.idle_add(do_idle, args, kwargs)

    return wrapper

def document_to_text_column(doc):
    """Translate DOCUMENT constant to COLUMN constant."""

    if doc == gaupol.gtk.DOCUMENT.MAIN:
        return gaupol.gtk.COLUMN.MAIN_TEXT
    if doc == gaupol.gtk.DOCUMENT.TRAN:
        return gaupol.gtk.COLUMN.TRAN_TEXT
    raise ValueError

def get_font():
    """Get custom font or blank string."""

    if not gaupol.gtk.conf.editor.use_default_font:
        return gaupol.gtk.conf.editor.font
    return ""

def get_glade_xml(name, root=None, directory=None):
    """Get gtk.glade.XML object from Glade file path.

    name should be Glade XML file's basename without extension.
    directory can be None for the default global directory.
    Raise RuntimeError if unable to load Glade XML file.
    """
    if directory is None:
        directory = os.path.join(gaupol.DATA_DIR, "glade")
    path = os.path.join(directory, "%s.glade" % name)
    return gtk.glade.XML(path, root)

def get_text_view_size(text_view, font=""):
    """Get the width and height desired by text view."""

    text_buffer = text_view.get_buffer()
    bounds = text_buffer.get_bounds()
    text = text_buffer.get_text(*bounds)
    label = gtk.Label(text)
    set_label_font(label, font)
    return label.size_request()

def get_tree_view_size(tree_view):
    """Get the width and height desired by tree view."""

    scroller = tree_view.get_parent()
    policy = scroller.get_policy()
    scroller.set_policy(gtk.POLICY_NEVER, gtk.POLICY_NEVER)
    width, height = scroller.size_request()
    scroller.set_policy(*policy)
    return width, height

def iterate_main():
    """Iterate the GTK main loop while events are pending."""

    while gtk.events_pending():
        gtk.main_iteration()

def prepare_text_view(text_view):
    """Connect text view to font and length margin updates."""

    def update_margin(*args):
        if gaupol.gtk.conf.editor.show_lengths_edit:
            return gaupol.gtk.ruler.connect_text_view(text_view)
        return gaupol.gtk.ruler.disconnect_text_view(text_view)
    gaupol.gtk.conf.editor.connect("notify::show_lengths_edit", update_margin)
    update_margin()

    update_font = lambda *args: set_widget_font(text_view, get_font())
    gaupol.gtk.conf.editor.connect("notify::use_default_font", update_font)
    gaupol.gtk.conf.editor.connect("notify::font", update_font)
    update_font()

def raise_default(expression):
    """Raise Default if expression evaluates to True."""

    if bool(expression):
        raise gaupol.gtk.Default

def resize_dialog(dialog, width, height, max_size=0.6):
    """Resize dialog to size required by its widgets.

    width and height should be desired sizes in pixels.
    max_size should be between 0 and 1.
    """
    width = min(width, int(max_size * gtk.gdk.screen_width()))
    height = min(height, int(max_size * gtk.gdk.screen_height()))
    width = max(dialog.size_request()[0], width)
    height = max(dialog.size_request()[1], height)
    dialog.set_default_size(width, height)

def resize_message_dialog(dialog, width, height, max_size=0.5):
    """Resize message dialog to size required by its widgets.

    width and height should be desired sizes in pixels.
    max_size should be width, height, between 0 and 1.
    """
    resize_dialog(dialog, width, height, max_size)

def separate_combo(store, itr):
    """Separator function for combo box models."""

    return store.get_value(itr, 0) == gaupol.gtk.COMBO_SEPARATOR

def set_button(button, text, stock=None):
    """Set the label and the image on button."""

    if stock is not None:
        image = gtk.Button(stock=stock).get_image()
        button.set_image(image)
    child = button.get_children()[0]
    if isinstance(child, gtk.Alignment):
        hbox = child.get_children()[0]
        image = hbox.get_children()[0]
        if stock is None:
            hbox.remove(image)
    button.set_label(text)
    button.set_use_underline(True)

def set_cursor_busy_require(window):
    assert hasattr(window, "window")

@contractual
def set_cursor_busy(window):
    """Set cursor busy when above window."""

    window.window.set_cursor(gaupol.gtk.BUSY_CURSOR)
    iterate_main()

def set_cursor_normal_require(window):
    assert hasattr(window, "window")

@contractual
def set_cursor_normal(window):
    """Set cursor normal when above window."""

    window.window.set_cursor(gaupol.gtk.NORMAL_CURSOR)
    iterate_main()

def set_label_font(label, font):
    """Set the font on label."""

    context = label.get_pango_context()
    font_desc = context.get_font_description()
    custom_font_desc = pango.FontDescription(font)
    font_desc.merge(custom_font_desc, True)
    attr = pango.AttrFontDesc(font_desc, 0, -1)
    attr_list = pango.AttrList()
    attr_list.insert(attr)
    label.set_attributes(attr_list)

def set_widget_font(widget, font):
    """Set the font on widget of any type."""

    context = widget.get_pango_context()
    font_desc = context.get_font_description()
    custom_font_desc = pango.FontDescription(font)
    font_desc.merge(custom_font_desc, True)
    widget.modify_font(font_desc)

def text_column_to_document(col):
    """Translate COLUMN constant to DOCUMENT constant."""

    if col == gaupol.gtk.COLUMN.MAIN_TEXT:
        return gaupol.gtk.DOCUMENT.MAIN
    if col == gaupol.gtk.COLUMN.TRAN_TEXT:
        return gaupol.gtk.DOCUMENT.TRAN
    raise ValueError
