# Copyright (C) 2005-2008 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Miscellaneous functions and decorators."""

import aeidon
import gaupol
import gobject
import gtk.glade
import inspect
import os
import pango


def delay_add(delay, function, *args):
    """Call function with arguments once after delay milliseconds.

    Return integer ID of the event source from 'gobject.timeout_add'.
    """
    def call_function(*args):
        function(*args)
        return False
    return gobject.timeout_add(delay, call_function, *args)

def document_to_text_field(doc):
    """Return text field enumeration corresponding to document enumeration."""

    if doc == aeidon.documents.MAIN:
        return gaupol.fields.MAIN_TEXT
    if doc == aeidon.documents.TRAN:
        return gaupol.fields.TRAN_TEXT
    raise ValueError("Invalid document: %s" % repr(doc))

def get_font():
    """Return custom font or blank string."""

    if not gaupol.conf.editor.use_custom_font: return ""
    return gaupol.conf.editor.custom_font

def get_glade_xml_require(*parts):
    path = os.path.join(aeidon.DATA_DIR, "glade", *parts)
    assert os.path.isfile(path)

@aeidon.deco.contractual
def get_glade_xml(*parts):
    """Return gtk.glade.XML object from Glade file path.

    parts are pathname components under aeidon.DATA_DIR/glade, i.e. optionally
    directories and, as the last item, the basename of the glade XML file.
    Raise RuntimeError if unable to load Glade XML file.
    """
    path = os.path.join(aeidon.DATA_DIR, "glade", *parts)
    return gtk.glade.XML(path)

def get_preview_command():
    """Return command to use for lauching video player for preview."""

    if gaupol.conf.preview.use_custom:
        return gaupol.conf.preview.custom_command
    player = gaupol.conf.preview.video_player
    if gaupol.conf.preview.force_utf_8:
        return player.command_utf_8
    return player.command

def get_text_view_size(text_view, font=""):
    """Return the width and height desired by text view."""

    text_buffer = text_view.get_buffer()
    bounds = text_buffer.get_bounds()
    text = text_buffer.get_text(*bounds)
    label = gtk.Label(text)
    set_label_font(label, font)
    return label.size_request()

def get_tree_view_size(tree_view):
    """Return the width and height desired by tree view."""

    scroller = tree_view.get_parent()
    policy = scroller.get_policy()
    scroller.set_policy(gtk.POLICY_NEVER, gtk.POLICY_NEVER)
    width, height = scroller.size_request()
    scroller.set_policy(*policy)
    return width, height

def install_module(name, obj):
    """Install object's module into the gaupol's namespace.

    Typical call is of form install_module("foo", lambda: None).
    """
    gaupol.__dict__[name] = inspect.getmodule(obj)

def iterate_main():
    """Iterate the GTK main loop while events are pending."""

    while gtk.events_pending():
        gtk.main_iteration()

def prepare_text_view(text_view):
    """Connect text view to font and length margin updates."""

    def update_margin(section, value, text_view):
        if gaupol.conf.editor.show_lengths_edit:
            return gaupol.ruler.connect_text_view(text_view)
        return gaupol.ruler.disconnect_text_view(text_view)
    connect = gaupol.conf.editor.connect
    connect("notify::show_lengths_edit", update_margin, text_view)
    update_margin(None, None, text_view)

    def update_font(section, value, text_view):
        set_widget_font(text_view, get_font())
    connect = gaupol.conf.editor.connect
    connect("notify::use_custom_font", update_font, text_view)
    connect("notify::custom_font", update_font, text_view)
    update_font(None, None, text_view)

def raise_default(expression):
    """Raise Default if expression evaluates to True."""

    if expression:
        raise gaupol.Default

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

    return store.get_value(itr, 0) == gaupol.COMBO_SEPARATOR

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

@aeidon.deco.contractual
def set_cursor_busy(window):
    """Set cursor busy when above window."""

    window.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
    iterate_main()

def set_cursor_normal_require(window):
    assert hasattr(window, "window")

@aeidon.deco.contractual
def set_cursor_normal(window):
    """Set cursor normal when above window."""

    window.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
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

def text_field_to_document(field):
    """Return document enumeration corresponding to text field enumeration."""

    if field == gaupol.fields.MAIN_TEXT:
        return aeidon.documents.MAIN
    if field == gaupol.fields.TRAN_TEXT:
        return aeidon.documents.TRAN
    raise ValueError("Invalid field: %s" % repr(field))
