# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010,2012 Osmo Salomaa
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
import inspect
import sys
import traceback
import webbrowser

from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import Pango


def char_to_px(nchar, font=None):
    """Convert characters to pixels."""
    if nchar < 0: return nchar
    label = Gtk.Label(label="etaoin shrdlu")
    if font is not None:
        set_widget_font(label, font)
    width = label.get_layout().get_pixel_size()[0]
    return int(round(nchar * (width / 13)))

def delay_add(delay, function, *args, **kwargs):
    """
    Call `function` with `args` and `kwargs` once after `delay` (ms).

    Return integer ID of the event source from :func:`GLib.timeout_add`.
    """
    def call_function(*args, **kwargs):
        function(*args, **kwargs)
        return False
    return GLib.timeout_add(delay, call_function, *args, **kwargs)

def document_to_text_field(doc):
    """Return :attr:`gaupol.fields` item corresponding to `doc`."""
    if doc == aeidon.documents.MAIN:
        return gaupol.fields.MAIN_TEXT
    if doc == aeidon.documents.TRAN:
        return gaupol.fields.TRAN_TEXT
    raise ValueError("Invalid document: {}"
                     .format(repr(doc)))

def flash_dialog(dialog):
    """
    Run `dialog`, destroy it and return response.

    :func:`flash_dialog` or :func:`run_dialog` should be used always when a
    :class:`Gtk.Dialog` is run so that unit tests can monkey patch this
    function with one that returns a specified response without waiting for
    user input.
    """
    response = dialog.run()
    dialog.destroy()
    return response

def get_content_size(widget):
    """Return the width and height desired by `widget`."""
    if isinstance(widget, Gtk.TextView):
        return get_text_view_size(widget)
    if isinstance(widget, Gtk.TreeView):
        return get_tree_view_size(widget)
    raise ValueError("Unsupported container type: {}"
                     .format(repr(type(widget))))

def get_font():
    """Return custom font or blank string."""
    return (gaupol.conf.editor.custom_font if
            (gaupol.conf.editor.use_custom_font and
             gaupol.conf.editor.custom_font) else "")


def get_gst_version_ensure(value):
    if value is not None:
        assert isinstance(value, str)

@aeidon.deco.contractual
def get_gst_version():
    """Return :mod:`Gst` version number as string or ``None``."""
    try:
        from gi.repository import Gst
        return ".".join(map(str, Gst.version()))
    except Exception:
        return None

def get_gtkspellcheck_version_ensure(value):
    if value is not None:
        assert isinstance(value, str)

@aeidon.deco.contractual
def get_gtkspellcheck_version():
    """Return :mod:`gtkspellcheck` version number as string or ``None``."""
    try:
        import gtkspellcheck
        return gtkspellcheck.__version__
    except Exception:
        return None

def get_preview_command():
    """Return command to use for lauching video player."""
    if gaupol.conf.preview.use_custom_command:
        return gaupol.conf.preview.custom_command
    if gaupol.conf.preview.force_utf_8:
        return gaupol.conf.preview.player.command_utf_8
    return gaupol.conf.preview.player.command

def get_text_view_size(text_view, font=None):
    """Return the width and height desired by `text_view`."""
    text_buffer = text_view.get_buffer()
    start, end = text_buffer.get_bounds()
    text = text_buffer.get_text(start, end, False)
    label = Gtk.Label(label=text)
    if font is not None:
        set_widget_font(label, font)
    label.show()
    return (label.get_preferred_width()[1]
            + text_view.props.left_margin
            + text_view.props.right_margin,
            label.get_preferred_height()[1])

def get_tree_view_size(tree_view):
    """Return the width and height desired by `tree_view`."""
    scroller = tree_view.get_parent()
    policy = scroller.get_policy()
    scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
    width = scroller.get_preferred_width()[1]
    height = scroller.get_preferred_height()[1]
    scroller.set_policy(*policy)
    return width, height

@aeidon.deco.once
def get_zebra_color(tree_view):
    """Return background color to use for tree view zebra-stripes."""
    # Gtk.TreeView.set_rules_hint does not actually always produce
    # zebra-stripes since some GTK+ theme authors have chosen to not allow
    # them. To, at least provide the option to, clarify multiline text,
    # we can calculate the colors theme-independently as a weighted mean of
    # normal background and foreground colors and set those using
    # Gtk.TreeViewColumn.set_cell_data_func.
    style = tree_view.get_style_context()
    fg = style.get_color(Gtk.StateFlags.NORMAL)
    bg = style.get_background_color(Gtk.StateFlags.NORMAL)
    color = Gdk.RGBA()
    color.red =   0.9 * bg.red   + 0.1 * fg.red
    color.green = 0.9 * bg.green + 0.1 * fg.green
    color.blue =  0.9 * bg.blue  + 0.1 * fg.blue
    return(color)

@aeidon.deco.once
def gst_available():
    """Return ``True`` if :mod:`Gst` module is available."""
    try:
        from gi.repository import Gst
        return True
    except Exception:
        return False

@aeidon.deco.once
def gtkspellcheck_available():
    """Return ``True`` if :mod:`gtkspellcheck` module is available."""
    try:
        import gtkspellcheck
        return True
    except Exception:
        return False

def install_module(name, obj):
    """
    Install `obj`'s module into the :mod:`gaupol` namespace.

    Typical call is of form::

        gaupol.util.install_module("foo", lambda: None)
    """
    gaupol.__dict__[name] = inspect.getmodule(obj)

def iterate_main():
    """Iterate the GTK+ main loop while events are pending."""
    while Gtk.events_pending():
        Gtk.main_iteration()

def lines_to_px(nlines, font=None):
    """Convert lines to pixels."""
    if nlines < 0: return nlines
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    label = Gtk.Label(label=text)
    if font is not None:
        set_widget_font(label, font)
    height = label.get_layout().get_pixel_size()[1]
    return int(round(nlines * height))

@aeidon.deco.once
def pocketsphinx_available():
    """Return ``True`` if `pocketsphinx` GStreamer plugin is available."""
    # XXX: Return False for now while waiting for pocketsphinx to be ported to
    # GStreamer 1.0. Speech recognition code is technically already ported,
    # but lacking pocketsphinx, it's completely untested.
    # https://sourceforge.net/projects/cmusphinx/forums/forum/5471/topic/5497616
    return False
    try:
        from gi.repository import Gst
        return Gst.Plugin.load_by_name("pocketsphinx") is not None
    except Exception:
        return False

def prepare_text_view(text_view):
    """Set spell-check, line-length margin and font properties."""
    if (gaupol.util.gtkspellcheck_available() and
        gaupol.conf.spell_check.inline):
        import gtkspellcheck
        language = gaupol.conf.spell_check.language
        try: checker = gtkspellcheck.SpellChecker(text_view, language)
        except Exception: pass
    connect = gaupol.conf.editor.connect
    def update_margin(section, value, text_view):
        if gaupol.conf.editor.show_lengths_edit:
            return gaupol.ruler.connect_text_view(text_view)
        return gaupol.ruler.disconnect_text_view(text_view)
    connect("notify::show_lengths_edit", update_margin, text_view)
    update_margin(None, None, text_view)
    def update_font(section, value, text_view):
        set_widget_font(text_view, get_font())
    connect("notify::use_custom_font", update_font, text_view)
    connect("notify::custom_font", update_font, text_view)
    update_font(None, None, text_view)
    def update_spacing(section, value, text_view):
        if gaupol.conf.editor.show_lengths_cell:
            return text_view.set_pixels_above_lines(2)
        return text_view.set_pixels_above_lines(0)
    connect("notify::show_lengths_cell", update_spacing, text_view)
    update_spacing(None, None, text_view)

def raise_default(expression):
    """Raise :exc:`gaupol.Default` if expression evaluates to ``True``."""
    if expression:
        raise gaupol.Default

def run_dialog(dialog):
    """
    Run `dialog` and return response.

    :func:`run_dialog` or :func:`flash_dialog` should be used always when a
    :class:`Gtk.Dialog` is run so that unit tests can monkey patch this
    function with one that returns a specified response without waiting for
    user input.
    """
    return dialog.run()

def scale_to_content(widget,
                     min_nchar=0,
                     max_nchar=2**16,
                     min_nlines=0,
                     max_nlines=2**16,
                     font=None):

    """Set `widget's` size by content, but limited by `min` and `max`."""
    width, height = get_content_size(widget)
    width = max(width, char_to_px(min_nchar, font))
    width = min(width, char_to_px(max_nchar, font))
    height = max(height, lines_to_px(min_nlines, font))
    height = min(height, lines_to_px(max_nlines, font))
    if isinstance(widget.get_parent(), Gtk.ScrolledWindow):
        # It seems that for tree views and text views
        # we need to set the size request of the scrolled window.
        # Vaguely account for possible scrollbars.
        widget = widget.get_parent()
        width, height = width + 24, height + 24
    widget.set_size_request(width, height)

def scale_to_size(widget, nchar, nlines, font=None):
    """Set `widget`'s size to `nchar` and `nlines`."""
    width = char_to_px(nchar, font)
    height = lines_to_px(nlines, font)
    if isinstance(widget.get_parent(), Gtk.ScrolledWindow):
        # It seems that for tree views and text views
        # we need to set the size request of the scrolled window.
        # Vaguely account for possible scrollbars.
        widget = widget.get_parent()
        width, height = width + 24, height + 24
    widget.set_size_request(width, height)

def separate_combo(store, itr, data=None):
    """Separator function for combo box models."""
    return store.get_value(itr, 0) == gaupol.COMBO_SEPARATOR

def set_cursor_busy(window):
    """Set mouse pointer busy when above window."""
    cursor = Gdk.Cursor(cursor_type=Gdk.CursorType.WATCH)
    window.get_window().set_cursor(cursor)
    iterate_main()

def set_cursor_normal(window):
    """Set mouse pointer normal when above window."""
    cursor = Gdk.Cursor(cursor_type=Gdk.CursorType.LEFT_PTR)
    window.get_window().set_cursor(cursor)
    iterate_main()

def set_widget_font(widget, font):
    """Use `font` for `widget`."""
    context = widget.get_pango_context()
    font_desc = context.get_font_description()
    custom_font_desc = Pango.FontDescription(font)
    font_desc.merge(custom_font_desc, True)
    widget.override_font(font_desc)

def show_exception(exctype, value, tb):
    """
    Show exception traceback in :class:`gaupol.DebugDialog`.

    This function can be set as a :func:`sys.excepthook`.
    """
    traceback.print_exception(exctype, value, tb)
    if not isinstance(value, Exception): return
    try: # to avoid recursion.
        dialog = gaupol.DebugDialog()
        dialog.set_text(exctype, value, tb)
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.NO:
            raise SystemExit(1)
    except Exception:
        traceback.print_exc()

def show_uri(uri):
    """Open `uri` in default application."""
    if sys.platform == "win32" and uri.startswith(("http://", "https://")):
        # Gtk.show_uri (GTK+ 2.20) fails on Windows.
        # GError: No application is registered as handling this file
        return webbrowser.open(uri)
    return Gtk.show_uri(None, uri, Gdk.CURRENT_TIME)

def text_field_to_document(field):
    """Return :attr:`aeidon.documents` item corresponding to `field`."""
    if field == gaupol.fields.MAIN_TEXT:
        return aeidon.documents.MAIN
    if field == gaupol.fields.TRAN_TEXT:
        return aeidon.documents.TRAN
    raise ValueError("Invalid field: {}"
                     .format(repr(field)))

def tree_path_to_row(path):
    """
    Convert `path` to a list row integer.

    `path` can be either a :class:`Gtk.Treepath` instance or a string
    representation of it (as commonly used by various callbacks).
    """
    if path is None: return None
    if isinstance(path, Gtk.TreePath):
        return(path.get_indices()[0])
    if isinstance(path, str):
        return(int(path))
    raise TypeError("Bad type {} for path {}"
                    .format(repr(type(path)), repr(path)))

def tree_row_to_path(row):
    """Convert list row integer to a :class:`Gtk.TreePath`."""
    if row is None: return None
    return Gtk.TreePath.new_from_string(str(row))
